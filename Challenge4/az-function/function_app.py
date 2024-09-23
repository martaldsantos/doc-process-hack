import azure.functions as func
import logging
from datetime import datetime, timedelta
from azure.core.credentials import AzureKeyCredential
from azure.ai.documentintelligence import DocumentIntelligenceClient
from azure.ai.documentintelligence.models import AnalyzeResult, AnalyzeDocumentRequest
import os

app = func.FunctionApp(http_auth_level=func.AuthLevel.ANONYMOUS)

@app.route(route="http_trigger")
def http_trigger(req: func.HttpRequest) -> func.HttpResponse:
    logging.info('Python HTTP trigger function processed a request.')

    name = req.params.get('name')
    if not name:
        try:
            req_body = req.get_json()
        except ValueError:
            pass
        else:
            name = req_body.get('name')

    if name:
        return func.HttpResponse(f"Hello, {name}. This HTTP triggered function executed successfully.")
    else:
        return func.HttpResponse(
             "This HTTP triggered function executed successfully. Pass a name in the query string or in the request body for a personalized response.",
             status_code=200
        )


@app.blob_trigger(arg_name="myblob", path="paystubs",
                               connection="224d94_STORAGE") 
def BlobTrigger(myblob: func.InputStream):    
    # Read the contents of the blob
    blob_contents = myblob.read()

    logging.info(f"Python blob trigger function processed blob"
                f"Name: {myblob.uri}"
                f"Blob Size: {myblob.length} bytes"
                f"Blob Contents: {blob_contents}")
    
    analyze_layout(blob_contents)

def get_words(page, line):
    result = []
    for word in page.words:
        if _in_span(word, line.spans):
            result.append(word)
    return result

def _in_span(word, spans):
    for span in spans:
        if word.span.offset >= span.offset and (word.span.offset + word.span.length) <= (span.offset + span.length):
            return True
    return False

def analyze_layout(sas_url):
    logging.info(f"Endpoint: {os.getenv('DOCUMENTINTELLIGENCE_ENDPOINT')}")
    logging.info(f"Key: {os.getenv('DOCUMENTINTELLIGENCE_API_KEY')}")
    
    document_intelligence_client = DocumentIntelligenceClient(
        endpoint=os.getenv("DOCUMENTINTELLIGENCE_ENDPOINT"), credential=AzureKeyCredential(os.getenv("DOCUMENTINTELLIGENCE_API_KEY"))
    )

    poller = document_intelligence_client.begin_analyze_document(
        # "prebuilt-layout", AnalyzeDocumentRequest(url_source=sas_url)
        "prebuilt-layout", AnalyzeDocumentRequest(bytes_source=sas_url)
    )

    result: AnalyzeResult = poller.result()

    # analysis_result = {
    #     "handwritten": any([style.is_handwritten for style in result.styles]) if result.styles else False,
    #     "pages": [],
    #     "tables": []
    # }

    # for page in result.pages:
    #     page_info = {
    #         "page_number": page.page_number,
    #         "width": page.width,
    #         "height": page.height,
    #         "unit": page.unit,
    #         "lines": [],
    #         "selection_marks": []
    #     }

    #     if page.lines:
    #         for line in page.lines:
    #             line_info = {
    #                 "text": line.content,
    #                 "polygon": line.polygon,
    #                 "words": [{"content": word.content, "confidence": word.confidence} for word in get_words(page, line)]
    #             }
    #             page_info["lines"].append(line_info)

    #     if page.selection_marks:
    #         for selection_mark in page.selection_marks:
    #             selection_mark_info = {
    #                 "state": selection_mark.state,
    #                 "polygon": selection_mark.polygon,
    #                 "confidence": selection_mark.confidence
    #             }
    #             page_info["selection_marks"].append(selection_mark_info)

    #     analysis_result["pages"].append(page_info)

    # if result.tables:
    #     for table in result.tables:
    #         table_info = {
    #             "row_count": table.row_count,
    #             "column_count": table.column_count,
    #             "bounding_regions": [{"page_number": region.page_number, "polygon": region.polygon} for region in table.bounding_regions] if table.bounding_regions else [],
    #             "cells": [{"row_index": cell.row_index, "column_index": cell.column_index, "content": cell.content, "bounding_regions": [{"page_number": region.page_number, "polygon": region.polygon} for region in cell.bounding_regions] if cell.bounding_regions else []} for cell in table.cells]
    #         }
    #         analysis_result["tables"].append(table_info)

    # return analysis_result

def save_analysis_results(blob_service_client, container_name, blob_name, analysis_results):
    if analysis_results is None:
        print(f"No analysis results for {blob_name}. Skipping save.")
        return

    # Define the name for the results file
    results_blob_name = f"{blob_name}_results.json"

    # Convert the analysis results to JSON
    results_json = json.dumps(analysis_results, indent=2)

    # Upload the results to the blob
    blob_client = blob_service_client.get_blob_client(container=container_name, blob=results_blob_name)
    blob_client.upload_blob(results_json, overwrite=True)

    print(f"Saved analysis results to {results_blob_name}")