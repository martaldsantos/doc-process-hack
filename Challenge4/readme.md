# Challenge 04: AutoFlow: Streamlining Processes with Azure Functions

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

```bash
# Navigate to the az-function folder
cd Challenge4/az-function

pip install -r requirements.txt
func host start
```

## Resource Deployment Guide

### VS Code

### Azure CLI
