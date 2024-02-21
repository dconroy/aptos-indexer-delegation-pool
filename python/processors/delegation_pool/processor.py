from aptos_protos.aptos.transaction.v1 import transaction_pb2
from processors.delegation_pool.models import AddDelegationEvent
from typing import List
from utils.transactions_processor import ProcessingResult
from utils import general_utils
from utils.transactions_processor import TransactionsProcessor
from utils.models.schema_names import DELEGATION_POOL_SCHEMA_NAME
from utils.session import Session
from utils.processor_name import ProcessorName
import json
import logging
from datetime import datetime
from time import perf_counter

MODULE_ADDRESS = general_utils.standardize_address(
    "0x9bfd93ebaa1efd65515642942a607eeca53a0188c04c21ced646d2f0b9f551e8"
)

class AddDelegationProcessor(TransactionsProcessor):
    def name(self) -> str:
        return ProcessorName.DELEGATION_POOL.value

    def schema(self) -> str:
        return DELEGATION_POOL_SCHEMA_NAME

    def process_transactions(
        self,
        transactions: list[transaction_pb2.Transaction],
        start_version: int,
        end_version: int,
    ) -> ProcessingResult:
        event_db_objs: List[AddDelegationEvent] = []
        start_time = perf_counter()
        for transaction in transactions:
            # Custom filtering
            # Here we filter out all transactions that are not of type TRANSACTION_TYPE_USER
            if transaction.type != transaction_pb2.Transaction.TRANSACTION_TYPE_USER:
                continue

            # Parse Transaction struct
            transaction_version = transaction.version
            transaction_block_height = transaction.block_height
            transaction_timestamp = general_utils.parse_pb_timestamp(
                transaction.timestamp
            )
            user_transaction = transaction.user
 

            # Parse AddDelegationEvent struct
            for event_index, event in enumerate(user_transaction.events):
                # Skip events that don't match our filter criteria
                sequence_number = event.sequence_number
                logging.info(event.type_str)
              
                try:
                    if not AddDelegationProcessor.included_event_type(event.type_str):
                        continue
                except Exception as e:
                        logging.error(f"Error Checking Event Type String: {event.data}, Error: {e}")
                        continue
               

                data = json.loads(event.data)
                parsed_call = event.type_str.split("::")
                try:
                    event_type = parsed_call[2]
                except Exception as e:
                    logging.error(f"JSON parsing failed for event data: {event.data}, Error: {e}")
                    continue
                   
                creation_number = event.key.creation_number
                sequence_number = event.sequence_number 
                delegator_address = general_utils.standardize_address(data["delegator_address"])
            
                    
                pool_address = general_utils.standardize_address(data["pool_address"])
                
                #function specific calls
                amount_added = int(data.get("amount_added", 0))
                amount_unlocked = int(data.get("amount_unlocked", 0))
                amount_reactivated = int(data.get("amount_reactivated", 0))
                amount_withdrawn = int(data.get("amount_withdrawn", 0))
                add_stake_fee = int(data.get("add_stake_fee", 0))




                # Create an instance of AddDelegationEvent
                event_db_obj = AddDelegationEvent(
                    sequence_number=sequence_number,
                    creation_number=creation_number,
                    pool_address=pool_address,
                    delegator_address=delegator_address,
                    amount_added=amount_added,
                    add_stake_fee=add_stake_fee,
                    amount_unlocked=amount_unlocked,
                    amount_reactivated=amount_reactivated,
                    amount_withdrawn=amount_withdrawn,
                    event_type=event_type,   
                    transaction_version=transaction_version,
                    transaction_timestamp=transaction_timestamp,
                    event_index=event_index,  # when multiple events of the same type are emitted in a single transaction, this is the index of the event in the transaction
                )
                
                event_db_objs.append(event_db_obj)

        processing_duration_in_secs = perf_counter() - start_time
        start_time = perf_counter()
        self.insert_to_db(event_db_objs)
        db_insertion_duration_in_secs = perf_counter() - start_time
        return ProcessingResult(
            start_version=start_version,
            end_version=end_version,
            processing_duration_in_secs=processing_duration_in_secs,
            db_insertion_duration_in_secs=db_insertion_duration_in_secs,
        )

    def insert_to_db(self, parsed_objs: List[AddDelegationEvent]) -> None:
        with Session() as session, session.begin():
            for obj in parsed_objs:
                session.merge(obj)

    @staticmethod
    def included_event_type(event_type: str) -> bool:
        parsed_tag = event_type.split("::")
        module_address = general_utils.standardize_address(parsed_tag[0])
        module_name = parsed_tag[1]
        event_type = parsed_tag[2]

        # Now we can filter out events that are not of type delegation pool
        # We can filter by the module address, module name, and event type
        # If someone deploys a different version of our contract with the same event type, we may want to index it one day.
        # So we could only check the event type instead of the full string
        # For our sake, check the full string
        return (
            module_name == "delegation_pool" and 
            (
                event_type == "AddStakeEvent" or 
                event_type == "ReactivateStakeEvent" or
                event_type == "UnlockStakeEvent" or
                event_type == "WithdrawStakeEvent" 
             
            ) 
        )

