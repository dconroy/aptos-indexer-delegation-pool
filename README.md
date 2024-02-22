##  Quickstart

This repository was based off https://github.com/aptos-labs/aptos-indexer-processors
### Prerequisite
- Docker
- Postgres DB

### Basic Example

In this example, we will be demonstrating an event processor that looks at delegation contract events.  All source code is based off n `aptos-indexer-processors/python/processors/example_event_processor`.

1. Download the example:

```
# Clone the repository to get the example code:
$ git clone https://github.com/aptos-labs/aptos-indexer-processors
# Navigate to the python folder
$ cd aptos-indexer-processors/python
```

3. Prepare the `config.yaml` file.
   Make sure to update the `config.yaml` file with the correct indexer settings and database credentials.

   ```
   $ cp config.yaml.example config.yaml
   ```

4. Define the data model and create the table(s).

   - In this tutorial, we want to extract data about transaction events. In `models.py`, you can define an Events data model.
   - The example uses Postgres. For now only Postgres is supported and we use SQLAlchemy ORM to interact with the Postgres database.

5. Create a processor.

   - Extend `TransactionsProcessor`.
   - In `process_transactions()`, implement the parsing logic and insert the rows into DB.

6. Run `poetry run python -m processors.main -c config.yaml` to start indexing!



8. Query the data from database in your dApp. It's recommended to use SQLAlchemy for this part.


### Run locally in Docker

```bash
docker compose up --build --force-recreate
```
