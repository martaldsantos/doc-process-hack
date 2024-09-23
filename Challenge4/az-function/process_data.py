# process_data.py
import os
import json
from utils import get_words
from datetime import datetime, timedelta, timezone
from azure.storage.blob import BlobServiceClient, generate_blob_sas, BlobSasPermissions
from azure.core.credentials import AzureKeyCredential
from azure.ai.documentintelligence import DocumentIntelligenceClient
from azure.ai.documentintelligence.models import AnalyzeResult, AnalyzeDocumentRequest

def get_blob_service_client():
    return BlobServiceClient.from_connection_string(os.getenv('STORAGE_CONNECTION_STRING'))

def generate_sas_url(blob_service_client, container_name, blob_name, expiry_hours=1):
    """
    Generate a SAS URL for a blob in Azure Blob Storage.

    :param blob_service_client: BlobServiceClient instance
    :param container_name: Name of the container
    :param blob_name: Name of the blob
    :param expiry_hours: Expiry time in hours for the SAS token
    :return: SAS URL for the blob
    """

    start_time = datetime.now(timezone.utc)
    expiry_time = start_time + timedelta(hours=expiry_hours)

    sas_token = generate_blob_sas(
        account_name=blob_service_client.account_name,
        container_name=container_name,
        blob_name=blob_name,
        account_key=blob_service_client.credential.account_key,
        permission=BlobSasPermissions(read=True),
        expiry=expiry_time,
        start=start_time,
    )

    sas_url = f"https://{blob_service_client.account_name}.blob.core.windows.net/{container_name}/{blob_name}?{sas_token}"
    return sas_url


def analyze_layout(sas_url):

    document_intelligence_client = DocumentIntelligenceClient(
        endpoint=os.getenv("DOCUMENTINTELLIGENCE_ENDPOINT"),
        credential=AzureKeyCredential(os.getenv("DOCUMENTINTELLIGENCE_API_KEY")),
    )

    poller = document_intelligence_client.begin_analyze_document(
        "prebuilt-layout", AnalyzeDocumentRequest(url_source=sas_url)
    )

    result: AnalyzeResult = poller.result()

    analysis_result = {
        "handwritten": (
            any([style.is_handwritten for style in result.styles])
            if result.styles
            else False
        ),
        "pages": [],
        "tables": [],
    }

    for page in result.pages:
        page_info = {
            "page_number": page.page_number,
            "width": page.width,
            "height": page.height,
            "unit": page.unit,
            "lines": [],
            "selection_marks": [],
        }

        if page.lines:
            for line in page.lines:
                line_info = {
                    "text": line.content,
                    "polygon": line.polygon,
                    "words": [
                        {"content": word.content, "confidence": word.confidence}
                        for word in get_words(page, line)
                    ],
                }
                page_info["lines"].append(line_info)

        if page.selection_marks:
            for selection_mark in page.selection_marks:
                selection_mark_info = {
                    "state": selection_mark.state,
                    "polygon": selection_mark.polygon,
                    "confidence": selection_mark.confidence,
                }
                page_info["selection_marks"].append(selection_mark_info)

        analysis_result["pages"].append(page_info)

    if result.tables:
        for table in result.tables:
            table_info = {
                "row_count": table.row_count,
                "column_count": table.column_count,
                "bounding_regions": (
                    [
                        {"page_number": region.page_number, "polygon": region.polygon}
                        for region in table.bounding_regions
                    ]
                    if table.bounding_regions
                    else []
                ),
                "cells": [
                    {
                        "row_index": cell.row_index,
                        "column_index": cell.column_index,
                        "content": cell.content,
                        "bounding_regions": (
                            [
                                {
                                    "page_number": region.page_number,
                                    "polygon": region.polygon,
                                }
                                for region in cell.bounding_regions
                            ]
                            if cell.bounding_regions
                            else []
                        ),
                    }
                    for cell in table.cells
                ],
            }
            analysis_result["tables"].append(table_info)

    return analysis_result


def save_analysis_results(
    blob_service_client, container_name, blob_name, analysis_results
):
    if analysis_results is None:
        print(f"No analysis results for {blob_name}. Skipping save.")
        return

    # Define the name for the results file
    results_blob_name = f"{blob_name}_results.json"

    # Convert the analysis results to JSON
    results_json = json.dumps(analysis_results, indent=2)

    # Upload the results to the blob
    blob_client = blob_service_client.get_blob_client(
        container=container_name, blob=results_blob_name
    )
    blob_client.upload_blob(results_json, overwrite=True)

    print(f"Saved analysis results to {results_blob_name}")
