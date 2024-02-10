import logging
import os
import azure.functions as func
from azure.cosmos import CosmosClient, PartitionKey

app = func.FunctionApp(http_auth_level=func.AuthLevel.ANONYMOUS)


@app.function_name(name="visitorCount")
@app.route(route="visitorCount")
def main(req: func.HttpRequest) -> func.HttpResponse:
    logging.info("Python HTTP trigger function processed a request.")

    # Initialize Cosmos Client
    # create env vars by using export varname=whatever
    # i also created app settings for these
    url = os.getenv("COSMOSDB_URL")
    key = os.getenv("COSMOSDB_KEY")
    client = CosmosClient(url, credential=key)

    # Select database
    database_name = "my-database"
    database = client.get_database_client(database_name)

    # Select Container
    container_name = "CRC-visitor count"
    container = database.get_container_client(container_name)

    # Read the item ( item = id, partition key = 'visitorCount )
    item_response = container.read_item(item="3", partition_key="test")

    # Increment the counter
    item_response["count"] += 1

    # Update the item
    container.upsert_item(item_response)

    return func.HttpResponse({item_response["count"]})
