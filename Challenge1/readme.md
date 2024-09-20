
## 1. Enviornment Creation and Resources Deployment

**Expected Duration:** 30 minutes

## Introduction
Your goal in this challenge is to create the services necessary to conduct this hackathon. You will deploy the required resources in Azure, including the Azure AI services that will be used in the subsequent challenges. By completing this challenge, you will set up the foundation for the rest of the hackathon.

## Introduction to the services

<img src="https://learn.microsoft.com/en-us/training/achievements/extract-data-from-forms-use-form-recognizer.svg" alt="Description" width="25" style="vertical-align: middle;"/> <span style="font-size:14px; font-weight:bold;">Azure AI Document Intelligence

[Azure AI Document Intelligence](https://azure.microsoft.com/en-us/products/ai-services/ai-document-intelligence?msockid=3b33a8ae1caf6af23334bc5b1dc86b9e) is an AI service that applies advanced machine learning to extract text, key-value pairs, tables, and structures from documents automatically and accurately. Turn documents into usable data and shift your focus to acting on information rather than compiling it. Start with prebuilt models or create custom models tailored to your documents both on premises and in the cloud with the AI Document Intelligence studio or SDK.



<img src="https://ms-azuretools.gallerycdn.vsassets.io/extensions/ms-azuretools/vscode-azurestorage/0.16.1/1724440951047/Microsoft.VisualStudio.Services.Icons.Default" alt="Description" width="25" style="vertical-align: middle;"/> <span style="font-size:14px; font-weight:bold;">Azure Storage Account


An [Azure Storage Account](https://learn.microsoft.com/en-us/azure/storage/common/storage-account-overview) contains all of your Azure Storage data objects: blobs, files, queues, and tables. The storage account provides a unique namespace for your Azure Storage data that's accessible from anywhere in the world over HTTP or HTTPS. Data in your storage account is durable and highly available, secure, and massively scalable.



<img src="https://seeklogo.com/images/A/azure-cosmos-db-logo-128436034F-seeklogo.com.png" alt="Description" width="25" style="vertical-align: middle;"/> <span style="font-size:14px; font-weight:bold;"> Azure Cosmos DB

[Azure Cosmos DB](https://azure.microsoft.com/en-us/products/cosmos-db/#Features) is a globally distributed, multi-model database service provided by Microsoft Azure. It is designed to provide low latency, elastic scalability of throughput, well-defined semantics for data consistency, and high availability. Azure Cosmos DB supports multiple data models including key-value, documents, graphs, and columnar. It is a good choice for any serverless application that needs low order-of-millisecond response times and needs to scale rapidly and globally.

<img src="https://media.licdn.com/dms/image/D5612AQHlaIMpsaaU9Q/article-cover_image-shrink_600_2000/0/1704683403049?e=2147483647&v=beta&t=vHiU0ktWw5l6v2UlURc_wyVqh_vIujasJHm1URDDE2o" alt="Description" width="35" style="vertical-align: middle;"/> <span style="font-size:14px; font-weight:bold;">Azure Functions

[Azure Functions](https://azure.microsoft.com/en-us/products/functions/?msockid=3b33a8ae1caf6af23334bc5b1dc86b9e) is a cloud service available on-demand that provides all the continually updated infrastructure and resources needed to run your applications. You focus on the code that matters most to you, in the most productive language for you, and Functions handles the rest. Functions provides serverless compute for Azure. You can use Functions to build web APIs, respond to database changes, process IoT streams, manage message queues, and more.


## Resource Deployment Guide
Clicking on button bellow will redirect you to the Azure portal to deploy the resources using the [ARM template](iac) provided in this repository.

[![Deploy to Azure](https://aka.ms/deploytoazurebutton)](https://portal.azure.com/#create/Microsoft.Template/uri/https%3A%2F%2Fraw.githubusercontent.com%2Fmartaldsantos%2Fdoc-process-hack%2Fts%2Fiac%2Fazuredeploy.json)

Resource deployment can take up to 5 minutes. Once the deployment is complete, you will see the resources in your Azure portal.

In the meantime, you can proceed with the next step - opening pre-configured development environment in GitHub Codespaces.

GitHub Codespaces is a cloud-based development environment that allows you to code from anywhere. It provides a fully configured environment that can be launched directly from any GitHub repository, saving you from lengthy setup times. You can access Codespaces from your browser, Visual Studio Code, or the GitHub CLI, making it easy to work from virtually any device.

To open this repository in GitHub Codespaces, click on the button below:

[![Open in GitHub Codespaces](https://github.com/codespaces/badge.svg)](https://codespaces.new/martaldsantos/doc-process-hack/tree/ts)

## Verify your resources' creation

Go back to your `Azure Portal` and find your `Resource Group`that should by now contain 5 resources and look like this:

![image](https://github.com/user-attachments/assets/91215492-faaf-4696-aa5c-2b955fb2f7d5)

After deploying the resources, you will need to configure the environment variables in the `.env` file. The `.env` file is a configuration file that contains the environment variables for the application. The `.env` file is automatically created runnig following command within terminal in your Codespace:

```bash
cd Challenge1
./get-keys.sh --resource-group <resource-group-name>
```

This script will connect to Azure and fetch the necessary keys and populate the `.env` file with the required values in the root directory of the repository. If needed, script will prompt you to sign in to your Azure account.

## Verify `.env` setup

When the script is finished, review the `.env` file to ensure that all the values are correct. If you need to make any changes, you can do so manually.

The default sample has an `.env.sample` file that shows the relevant environment variables that need to be configured in this project. The script should create a `.env` file that has these same variables _but populated with the right values_ for your Azure resources.

If the file is not created, simply copy over `.env.sample` to `.env` - then populate those values manually from the respective Azure resource pages using the Azure Portal.

## Conclusion
By reaching this section you should have every resource and installed the requirements necessary to conduct the hackathon. You have deployed an Azure AI Document Intelligence service, an Azure Cosmos DB account, an Azure Storage Account and Azure OpenAI Service.

In the next challenges, you will use these services to build a strong document processing workflow.
