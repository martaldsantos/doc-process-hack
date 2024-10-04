
![Design 12 (10)](https://github.com/user-attachments/assets/ad2aa654-444d-45b2-a4b8-8101434f2b8f)

# Intelligent Document Processing using Azure AI

Welcome to the Intelligent Document Processing using Azure AI Hackathon! Today, you're set to dive into the transformative world of AI, with a focus on utilizing the power of the Azure AI Platform. Prepare yourself for a day of intense learning, innovation, and hands-on experience that will elevate your understanding of AI integration in application development.


## Introduction
As a participant, you will delve into innovative solutions that leverage AI to streamline workflows, reduce human error, and expedite the handling of critical documents. By integrating advanced vision technologies, you will create applications that not only improve operational efficiency but also elevate the overall customer experience at Contoso Bank. 

Prepare to unleash your creativity and technical skills as you embark on this exciting journey to shape the future of the financial services!

## Learning Objectives

By participating in this hackathon, you will learn how to:

- **Process Documentation:** Understand the general structure of the outputs from a Azure Document Intelligence and explain how OCR can be leveraged in a document processing solution
- **Structure Information:** You will develop the competencies behind the cleaning and structuring of data both using common Python like Pandas and Numpy, but also leveraging [GPT-4o-2024-08-06](https://azure.microsoft.com/en-us/blog/announcing-a-new-openai-feature-for-developers-on-azure/?msockid=020102d7a56062ac18f017d0a4d46360), the new model focuses on enhancing productivity through Structured Outputs, like JSON Schemas.
- **Automate Workflows with Azure Functions:** Learn how to deploy Azure Functions to automate any workflows. Azure Functions allow you to execute code in response to triggers, such as file uploads or form submissions.
- **Orchestrate Pipelines with GitHub Actions:** Discover how to use GitHub Actions to automate and manage the entire lifecycle of your Azure Functions pipeline. 



## Architecture

When a document is uploaded to an Azure Storage Account, it triggers an Azure Function App that begins by cleaning and preparing the document's content. Leveraging the Azure AI Document Intelligence, key information is extracted automatically. Additionally, for some of the documents the use of the Azure OpenAI Service is integrated to transform natural language to the desired json format, allowing the system to further enhance and semi-structure the document's data. Finally, the processed JSON files are stored in Azure Cosmos DB, ensuring scalable and efficient storage for easy access and future use. 

![image](https://github.com/user-attachments/assets/9f431203-93d2-41ad-9f51-160607fde604)

The data that will be used can be of 3 different formats: **Loan Forms, Loan Agreements and Pay Stubs**, and your solution should have the different specificities of each topic into consideration.



## Requirements

To successfully complete this hackathon, you will need the following:

1. GitHub account to access the repository and run [GitHub Codespaces](https://github.com/features/codespaces)
2. Familiarity with Python programming, including handling JSON data and making API calls.
3. An active **Azure subscription**, with **Owner** or **Contributor** rights
4. Ability to provision the following resources in **Sweden Central**: 
- Azure Cosmos DB
- Azure Document Intelligence
- Azure Application Insights
- App Service plan
- Azure Function App
- Log Analytics workspace
- Azure Search service
- Azure OpenAI Service
- Azure Storage Account
- Event Grid System Topic

## Hackathon Format: Challenge-Based
This hackathon adopts a challenge-based format, offering you a unique opportunity to learn while dealing with practical problems. Each challenge includes one or more self-contained tasks designed to test and enhance your skills in specific aspects of AI app development. You will approach these challenges by:
- Analyzing the problem statement.
- Strategizing your approach to find the most effective solution.
- Leveraging the provided lab environment and Azure AI services.
- Collaborating with peers to refine and implement your solutions.

## Challenges
1. Challenge 01: **[Deployment of Resources in Azure](Challenge1/readme.md)**
   - Creation of the Services necessary to conduct this Hack
2. Challenge 02: **[Leveraging Azure Document Intelligence for Data Retrieval](Challenge2/readme.md)**
   - Use Azure Document Intelligence Model to retrieve information from Text and Tables
3. Challenge 03: **[Data Modelling and Structuring with Python and Cosmos DB](Challenge3/data_modelling.ipynb)**
   - Structuring the Retrieved Data and Upload it to a Cosmos DB
4. Challenge 04: **[Streamlining the Process with Azure Functions](Challenge4/readme.md)**
   - Creation of a Function App that will Automate these Processes
5. Challenge 05: **[Set up CI/CD for Azure Function](Challenge5/readme.md)**
   - Creation of the CI/CD pipeline to automate the run of the Azure Function 

Each challenge comes with its own set of tasks and objectives. Feel free to explore the challenges, learn, and have fun during this hackathon! If you have any questions, don't hesitate to reach out to your coach.

Happy hacking! 

# License
This repository is licensed under MIT license. More info can be found [here](https://github.com/Microsoft/WhatTheHack/blob/master/LICENSE).
