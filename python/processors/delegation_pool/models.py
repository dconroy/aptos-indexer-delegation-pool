from utils.models.annotated_types import StringType
from utils.models.annotated_types import (
    BooleanType,
    StringPrimaryKeyType,
    BigIntegerType,
    BigIntegerPrimaryKeyType,
    InsertedAtType,
    TimestampType,
    StringType,
    NumericType
)
from utils.models.general_models import Base
from utils.models.schema_names import DELEGATION_POOL_SCHEMA_NAME


class AddDelegationEvent(Base):
    __tablename__ = "delegation_pool_events"
    __table_args__ = ({"schema": DELEGATION_POOL_SCHEMA_NAME},)

    sequence_number: BigIntegerPrimaryKeyType
    creation_number: BigIntegerType
    pool_address: StringType
    delegator_address: StringType
    event_type: StringType
    amount_added: BigIntegerType
    add_stake_fee: BigIntegerType
    amount_unlocked: BigIntegerType
    amount_reactivated: BigIntegerType
    amount_withdrawn: BigIntegerType
    transaction_version: BigIntegerType
    transaction_timestamp: TimestampType
    inserted_at: InsertedAtType
    event_index: BigIntegerType
