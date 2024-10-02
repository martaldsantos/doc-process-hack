import azure.functions as func
import json
from utils import get_file_names
from process_files import generate_sas_url, get_blob_service_client, analyze_layout, save_analysis_results
from model_paystubs import model_paystubs
from model_loanforms import model_loanforms
from model_loanagreements import model_loanagreements

app = func.FunctionApp(http_auth_level=func.AuthLevel.ANONYMOUS)

@app.blob_trigger(arg_name="myblob", path="data/loanagreements/{name}",
                               connection="STORAGE_CONNECTION_STRING")
@app.cosmos_db_output(arg_name="outputDocument",
                      database_name="ContosoDB",
                      container_name="LoanAgreements",
                      connection="COSMOS_CONNECTION_STRING")
def ProcessLoanAgreements(myblob: func.InputStream, outputDocument: func.Out[func.Document]):  
    """
    Triggered when a new blob is added to the 'loanagreements' container.
    Processes the blob and saves the results to Cosmos DB if it is a JSON file.
    
    Parameters:
    myblob (func.InputStream): The input blob stream.
    outputDocument (func.Out[func.Document]): The output document for Cosmos DB.
    """
    container_name = 'data/loanagreements'
    blob_service_client = get_blob_service_client()

    # Extract file name and root from the blob name
    file_name, file_root = get_file_names(myblob.name)

    # Check if the file extension is .json
    if file_name.endswith('.json'):
        # Read the blob data
        blob_data = myblob.read()
        data = json.loads(blob_data)
        
        # Model the paystubs data
        document = model_loanagreements(data)
        
        # Save the analysis results to Cosmos DB
        outputDocument.set(func.Document.from_dict(document))
        return 
    
    # Generate SAS URL for the blob
    sas_url = generate_sas_url(blob_service_client, container_name, file_name)   

    # Analyze the layout of the file using the SAS URL
    analysis_results = analyze_layout(sas_url=sas_url)

    # Save the analysis results
    save_analysis_results(blob_service_client, container_name, file_root, analysis_results)

@app.blob_trigger(arg_name="myblob", path="data/loanform/{name}",
                               connection="STORAGE_CONNECTION_STRING") 
@app.cosmos_db_output(arg_name="outputDocument",
                      database_name="ContosoDB",
                      container_name="LoanForms",
                      connection="COSMOS_CONNECTION_STRING")
def ProcessLoanForms(myblob: func.InputStream, outputDocument: func.Out[func.Document]):
    """
    Triggered when a new blob is added to the 'loanforms' container.
    Processes the blob and saves the results to Cosmos DB if it is a JSON file.
    
    Parameters:
    myblob (func.InputStream): The input blob stream.
    outputDocument (func.Out[func.Document]): The output document for Cosmos DB.
    """
    container_name = 'data/loanforms'
    blob_service_client = get_blob_service_client()
    
    # Extract file name and root from the blob name
    file_name, file_root = get_file_names(myblob.name)

    # Check if the file extension is .json
    if file_name.endswith('.json'):
        # Read the blob data
        blob_data = myblob.read()
        data = json.loads(blob_data)
        
        # Model the paystubs data
        document = model_loanforms(data)
        
        # Save the analysis results to Cosmos DB
        outputDocument.set(func.Document.from_dict(document))
        return
    
    # Generate SAS URL for the blob
    sas_url = generate_sas_url(blob_service_client, container_name, file_name)   

    # Analyze the layout of the file using the SAS URL
    analysis_results = analyze_layout(sas_url=sas_url)

    # Save the analysis results
    save_analysis_results(blob_service_client, container_name, file_root, analysis_results)

@app.blob_trigger(arg_name="myblob", path="data/paystubs/{name}",
                               connection="STORAGE_CONNECTION_STRING")
@app.cosmos_db_output(arg_name="outputDocument",
                      database_name="ContosoDB",
                      container_name="PayStubs",
                      connection="COSMOS_CONNECTION_STRING")
def ProcessPayStubs(myblob: func.InputStream, outputDocument: func.Out[func.Document]):
    """
    Triggered when a new blob is added to the 'paystubs' container.
    Processes the blob and saves the results to Cosmos DB if it is a JSON file.
    
    Parameters:
    myblob (func.InputStream): The input blob stream.
    outputDocument (func.Out[func.Document]): The output document for Cosmos DB.
    """
    container_name = 'data/paystubs'
    blob_service_client = get_blob_service_client()
    
    # Extract file name and root from the blob name
    file_name, file_root = get_file_names(myblob.name)

    # Check if the file extension is .json
    if file_name.endswith('.json'):
        # Read the blob data
        blob_data = myblob.read()
        data = json.loads(blob_data)
        
        # Model the paystubs data
        document = model_paystubs(data)
        
        # Save the analysis results to Cosmos DB
        outputDocument.set(func.Document.from_dict(document))
        return
    
    # Generate SAS URL for the blob
    sas_url = generate_sas_url(blob_service_client, container_name, file_name)   

    # Analyze the layout of the file using the SAS URL
    analysis_results = analyze_layout(sas_url=sas_url)

    # Save the analysis results back to the blob storage
    save_analysis_results(blob_service_client, container_name, file_root, analysis_results)