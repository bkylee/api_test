""" import azure.functions as func
import logging

app = func.FunctionApp(http_auth_level=func.AuthLevel.FUNCTION)


@app.cosmos_db_output(
    arg_name="outputDocument",
    database_name="my-database",
    collection_name="my-container",
    connection_string_setting="CosmosDbConnectionString",
)
@app.route(route="http_trigger")
def http_trigger(req: func.HttpRequest) -> func.HttpResponse:
    logging.info("Python HTTP trigger function processed a request.")

    name = req.params.get("name")
    if not name:
        try:
            req_body = req.get_json()
        except ValueError:
            pass
        else:
            name = req_body.get("name")

    if name:
        return func.HttpResponse(
            f"Hello, {name}. This HTTP triggered function executed successfully."
        )
    else:
        return func.HttpResponse(
            "This HTTP triggered function executed successfully. Pass a name in the query string or in the request body for a personalized response.",
            status_code=200,
        )
 """

import azure.functions as func
import logging

app = func.FunctionApp()


@app.function_name(name="HttpTrigger1")
@app.route(route="hello", auth_level=func.AuthLevel.ANONYMOUS)
@app.queue_output(
    arg_name="msg", queue_name="outqueue", connection="AzureWebJobsStorage"
)
@app.cosmos_db_output(
    arg_name="outputDocument",
    database_name="my-database",
    container_name="my-container",
    connection="CosmosDbConnectionString",
)
def test_function(
    req: func.HttpRequest,
    msg: func.Out[func.QueueMessage],
    outputDocument: func.Out[func.Document],
) -> func.HttpResponse:
    logging.info("Python HTTP trigger function processed a request.")
    logging.info("Python Cosmos DB trigger function processed a request.")
    name = req.params.get("name")
    if not name:
        try:
            req_body = req.get_json()
        except ValueError:
            pass
        else:
            name = req_body.get("name")

    if name:
        outputDocument.set(func.Document.from_dict({"id": name}))
        msg.set(name)
        return func.HttpResponse(f"Hello {name}!")
    else:
        return func.HttpResponse(
            "Please pass a name on the query string or in the request body",
            status_code=400,
        )
