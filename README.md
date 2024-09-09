
![Design 12 (9)](https://github.com/user-attachments/assets/f6648dcb-ffb0-468d-9f61-e8973dfc84d8)

# Intelligent Document Processing using Azure AI

Welcome to the Intelligent Document Processing using Azure AI Hackathon! Today, you're set to dive into the transformative world of AI, with a focus on utilizing the power of the Azure AI Platform. Prepare yourself for a day of intense learning, innovation, and hands-on experience that will elevate your understanding of AI integration in application development.


## Introduction
As participants, you will delve into innovative solutions that leverage AI to streamline workflows, reduce human error, and expedite the handling of critical documents. By integrating advanced vision technologies, you will create applications that not only improve operational efficiency but also elevate the overall customer experience at Contoso Bank. 

Prepare to unleash your creativity and technical skills as you embark on this exciting journey to shape the future of the financial services!

## Architecture

The Hackathon will be based on creating an automated document processing workflow using Azure services. When a document is uploaded to an Azure Storage Account, it triggers an Azure Function App that begins by cleaning and preparing the document's content. The data is then structured into a JSON format for further processing. Leveraging AI Document Intelligence, key information is extracted automatically, improving accuracy in data handling. Additionally, Azure OpenAI Service is integrated to transform natural language to a Desired JSON format, allowing the system to further enhance and structure the document's data. Finally, the processed JSON files are stored in Azure Cosmos DB, ensuring scalable and efficient storage for easy access and future use.

![image](https://github.com/user-attachments/assets/2eaec5e6-7327-4a63-b2d8-8f76ef33477c)



The data that will be used can be of 3 different formats: **Loan Forms, Loan Agreements and Pay Stubs**, and your solution should have the different specificities of each topic into consideration.
## Learning Objectives

By participating in this hackathon, you will learn how to:

- Gain Practical Experience with Azure Technologies
- Develop Competencies in Document Processing
- Understand the complecity behind typical Information Structuring
- Develop Prototype Applications
- Receive Feedback and Iterate

## Requirements

To successfully complete this hackathon, you will need the following:

1. An active **Azure subscription**

2. Install [Visual Studio Code](https://code.visualstudio.com/download)

3. Install the [Azure CLI](https://learn.microsoft.com/cli/azure/install-azure-cli) for your device OS

4. Install the [Azure Functions](https://marketplace.visualstudio.com/items?itemName=ms-azuretools.vscode-azurefunctions) in VSCode

5. Install the [Azure Functions Core Tools](https://learn.microsoft.com/en-gb/azure/azure-functions/functions-run-local?tabs=windows%2Cisolated-process%2Cnode-v4%2Cpython-v2%2Chttp-trigger%2Ccontainer-apps&pivots=programming-language-csharp) in VSCode

6. Familiarity with Python programming, including handling JSON data and making API calls.

7. Ability to provision the following resources: 
- Azure AI Search
- Azure Cosmos DB
- Azure Document Intelligence
- Azure OpenAI Service
- Azure Storage Account

In order for this provision to happen, you should be either the **Owner or Contributor in an Azure Subscription**. 

## Challenges
1. Challenge 01: **[Hack Essentials: Crafting Services for Seamless Execution](Challenge1/readme.md)**
   - Creation of the Services necessary to conduct this Hack
2. Challenge 02: **[InsightExtractor: Leveraging Azure Document Intelligence for Data Retrieval](Challenge2/doc-processing.ipynb)**
   - Use Azure Document Intelligence Model to retrieve information from Text and Tables
3. Challenge 03: **[Data Modelling: From Retrieval to Upload](Challenge3/data_modelling.ipynb)**
   - Structuring the Retrieved Data and Upload it to a Cosmos DB
4. Challenge 04: **[AutoFlow: Streamlining Processes with Azure Functions](Challenge4/readme.md)**
   - Creation of a Function App that will Automate these Processes
5. Challenge 05: **[Index & Inquire: AI-Enhanced Database Query Challenge](Challenge5/readme.md)**
   - Text and Table indexing and using with AOAI to ask questions to our DB
  


Each challenge comes with its own set of tasks and objectives. Feel free to explore the challenges, learn, and have fun during this hackathon! If you have any questions, don't hesitate to reach out to your coach.
Happy hacking! 


## Contributors
- André Vala
- Marta Santos
