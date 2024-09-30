# Challenge 04: AutoFlow: Streamlining Processes with Azure Functions

**Expected Duration:** 90 minutes

## Introduction
Your goal in this challenge is to create and deploy an Azure Function written in Python that will automate the processing of the different data files. 
You will deploy the required resources in Azure, including the Azure Function, and set up the development environment. By completing this challenge, you will have a fully functional serverless function ready for further development.

## Introduction to Azure Functions

<img src="https://media.licdn.com/dms/image/D5612AQHlaIMpsaaU9Q/article-cover_image-shrink_600_2000/0/1704683403049?e=2147483647&v=beta&t=vHiU0ktWw5l6v2UlURc_wyVqh_vIujasJHm1URDDE2o" alt="Description" width="35" style="vertical-align: middle;"/> <span style="font-size:14px; font-weight:bold;">Azure Functions

[Azure Functions](https://azure.microsoft.com/en-us/products/functions/?msockid=3b33a8ae1caf6af23334bc5b1dc86b9e) is a cloud service available on-demand that provides all the continually updated infrastructure and resources needed to run your applications. You focus on the code that matters most to you, in the most productive language for you, and Functions handles the rest. Functions provides serverless compute for Azure. You can use Functions to build web APIs, respond to database changes, process IoT streams, manage message queues, and more.

## Configuring Environment Variables

### Create a local.settings.json file

The `local.settings.json` file is a configuration file that contains the environment variables for the application. Create a `local.settings.json` in the `az-function` folder and replace the values below with the endpoints/keys generated in Challenge 1.

```json
{
  "IsEncrypted": false,
  "Values": {
    "AzureWebJobsStorage": "",
    "FUNCTIONS_WORKER_RUNTIME": "python",
    "DOCUMENTINTELLIGENCE_ENDPOINT": "",
    "DOCUMENTINTELLIGENCE_API_KEY": "",
    "STORAGE_CONNECTION_STRING": "",
    "COSMOS_CONNECTION_STRING" : "",
    "AZURE_OPENAI_ENDPOINT" : "",
    "AZURE_OPENAI_KEY" : "",
    "AZURE_OPENAI_MODEL" : ""
  }
}
```

## Running the Azure Function Locally

To run the Azure Function locally, you need to install the Azure Functions Core Tools. The Azure Functions Core Tools provide a local development experience for creating, developing, testing, running, and debugging Azure Functions.

This should already be installed in your GitHub Codespaces.

To start the Azure Function, navigate to the `az-function` folder run the following command in the terminal:

NOTE: Azure Functions Core Tools requires Python 3.9 to 3.11. Python 3.12 is not supported.

The CodeSpaces environment should have all the required packages installed. So creating a python virtual environment is optional.

```bash
# OPTIONAL - Create a virtual environment using VS Code
# 1. Open the command palette (Ctrl + Shift + P)
# 2. Type Python: Create Virtual Environment
# 3. Select Venv
# 4. Select Python 3.9 or any version between 3.9 and 3.11
# 5. Select Challenge4/az-function/requirements.txt to install the required packages
# 6. Check if the virtual environment folder was created in the root of the repository (.venv folder)
# 7. Relaunch the terminal

# Navigate to the az-function folder
cd Challenge4/az-function

# Start the Azure Function
func host start
```

You should now see the Azure Function running locally and processing the data files as they are uploaded to the containers in the Azure Storage Account.

## Resource Deployment Guide

### VS Code

Using the Azure Functions extension in VS Code, you can deploy your Azure Function to Azure.

1. Open the command palette (Ctrl + Shift + P)
2. Type `Azure Functions: Upload Local Settings`
3. Select the Function App you created in Challenge 1.
4. Right-click on the `az-function` folder.
5. Select `Deploy to Function App`.
6. Select the Function App you created in Challenge 1.

### Azure CLI

1. Navigate to the `az-function` folder.
2. Run the following commands to deploy the Azure Function to Azure.
```bash
az login
az account set --subscription <subscription_id_where_function_exists>
func azure functionapp publish <function_app_name> --publish-local-settings
```
