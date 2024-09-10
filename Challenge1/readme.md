
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



## 1. Resource Deployment Guide

1. Clone the repo

    ```bash
    git clone https://github.com/martaldsantos/doc-process-hack
    ```

1. Open the repo in VS Code

    ```bash
    cd doc-process-hack
    code .
    ```

1. Create a new local Python environment using **either** [anaconda](https://www.anaconda.com/products/individual) **or** [venv](https://docs.python.org/3/library/venv.html) for a managed environment.

    1. **Option 1**: Using anaconda

        ```bash
        conda create -n contoso-chat python=3.11
        conda activate contoso-chat
        pip install -r requirements.txt
        ```

    1. **Option 2:** Using venv

        ```bash
        python3 -m venv .venv
        source .venv/bin/activate
        pip install -r requirements.txt
        ```

## 2. Create Azure resources

We setup our development ennvironment in the previous step. In this step, we'll **provision Azure resources** for our project, ready to use for developing our LLM Application.


### 2.1 Authenticate with Azure

Start by connecting your Visual Studio Code environment to your Azure account:

1. Open the terminal in VS Code and use command `az login`. 
1. Complete the authentication flow. 

Verify that the console shows a message indicating a successful authentication. **Congratulations! Your VS Code session is now connected to your Azure subscription!**

### 2.2 Run Provisioning Script

The project requires a number of Azure resources to be set up, in a specified order. To simplify this, an auto-provisioning script has been provided. (NOTE: It will use the current active subscription to create the resource. If you have multiple subscriptions, use `az account set --subscription "<SUBSCRIPTION-NAME>"` first to set the desired active subscription.)

Run the provisioning script as follows:

  ```bash
  ./provision.sh
  ```

**⚠️ Warning:** This script will create a new resource group by default. If you want to use an existing RG, replace variables `resourceGroupName`and `location` on lines 4 and 5 to the parameters of your existing RG.

If you get an error of permissions, please firstly run the following code: 

  ```bash
chmod u+r+x provision.sh
  ```

 This run should take a couple of minutes. 
  
The script should **set up a dedicated resource group** with the following resources:

 - **Azure Document Intelligence workspace** resource
 - **Azure OpenAI Service**  resource
 - **Azure Cosmos DB account** resource
 - **Azure Storage Account**  resource


### 2.3 Verify your resources' creation

Go back to your `Azure Portal` and find your `Resource Group`that should by now contain 5 resources and look like this:

![image](https://github.com/user-attachments/assets/91215492-faaf-4696-aa5c-2b955fb2f7d5)


### 2.4 Verify `.env` setup

The default sample has an `.env.sample` file that shows the relevant environment variables that need to be configured in this project. The script should create a `.env` file that has these same variables _but populated with the right values_ for your Azure resources.

If the file is not created, simply copy over `.env.sample` to `.env` - then populate those values manually from the respective Azure resource pages using the Azure Portal.

## Conclusion
By reaching this section you should have every resource and installed the requirements necessary to conduct the hackathon. You have deployed an Azure AI Document Intelligence service, an Azure Cosmos DB account, an Azure Storage Account and Azure OpenAI Service.

In the next challenges, you will use these services to build a strong document processing workflow.
