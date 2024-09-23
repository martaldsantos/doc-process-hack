import azure.functions as func
import logging
from utils import get_file_names
from process_data import generate_sas_url, get_blob_service_client, analyze_layout, save_analysis_results

app = func.FunctionApp(http_auth_level=func.AuthLevel.ANONYMOUS)

@app.blob_trigger(arg_name="myblob", path="loanagreements",
                               connection="STORAGE_CONNECTION_STRING") 
def ProcessLoanAgreements(myblob: func.InputStream):  
    
    blob_service_client = get_blob_service_client()

    file_name, file_root = get_file_names(myblob.name)

    # Check if the file extension is .json
    if file_name.endswith('.json'):
        logging.info(f"Ignoring file {file_name} as it is a JSON file.")
        return    
    
    sas_url = generate_sas_url(blob_service_client, 'paystubs', file_name)   

    analysis_results = analyze_layout(sas_url=sas_url)

    # Save the analysis results
    save_analysis_results(blob_service_client, 'paystubs', file_root, analysis_results)

@app.blob_trigger(arg_name="myblob", path="loanforms",
                               connection="STORAGE_CONNECTION_STRING") 
def ProcessLoanForms(myblob: func.InputStream):  
    
    blob_service_client = get_blob_service_client()
    
    file_name, file_root = get_file_names(myblob.name)

    # Check if the file extension is .json
    if file_name.endswith('.json'):
        logging.info(f"Ignoring file {file_name} as it is a JSON file.")
        return
    
    sas_url = generate_sas_url(blob_service_client, 'paystubs', file_name)   

    analysis_results = analyze_layout(sas_url=sas_url)

    # Save the analysis results
    save_analysis_results(blob_service_client, 'paystubs', file_root, analysis_results)

@app.blob_trigger(arg_name="myblob", path="paystubs",
                               connection="STORAGE_CONNECTION_STRING") 
def ProcessPayStubs(myblob: func.InputStream):  
    
    blob_service_client = get_blob_service_client()
    
    file_name, file_root = get_file_names(myblob.name)

    # Check if the file extension is .json
    if file_name.endswith('.json'):
        logging.info(f"Ignoring file {file_name} as it is a JSON file.")
        return
    
    sas_url = generate_sas_url(blob_service_client, 'paystubs', file_name)   

    analysis_results = analyze_layout(sas_url=sas_url)

    # Save the analysis results
    save_analysis_results(blob_service_client, 'paystubs', file_root, analysis_results)