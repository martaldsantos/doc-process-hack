
![Design 12 (10)](https://github.com/user-attachments/assets/ad2aa654-444d-45b2-a4b8-8101434f2b8f)

# Intelligent Document Processing using Azure AI

Welcome to the Intelligent Document Processing using Azure AI Hackathon! Today, you're set to dive into the transformative world of AI, with a focus on utilizing the power of the Azure AI Platform. Prepare yourself for a day of intense learning, innovation, and hands-on experience that will elevate your understanding of AI integration in application development.


## Introduction
As participants, you will delve into innovative solutions that leverage AI to streamline workflows, reduce human error, and expedite the handling of critical documents. By integrating advanced vision technologies, you will create applications that not only improve operational efficiency but also elevate the overall customer experience at Contoso Bank. 

Prepare to unleash your creativity and technical skills as you embark on this exciting journey to shape the future of the financial services!

## Learning Objectives

By participating in this hackathon, you will learn how to:

- Gain Practical Experience with Azure Technologies
- Develop Competencies in Document Processing
- Understand the complecity behind typical Information Structuring
- Develop Prototype Applications


## Architecture

When a document is uploaded to an Azure Storage Account, it triggers an Azure Function App that begins by cleaning and preparing the document's content. Leveraging the Azure AI Document Intelligence, key information is extracted automatically. Additionally, for some of the documents the use of the Azure OpenAI Service is integrated to transform natural language to the desired json format, allowing the system to further enhance and semi-structure the document's data. Finally, the processed JSON files are stored in Azure Cosmos DB, ensuring scalable and efficient storage for easy access and future use.

![image](https://github.com/user-attachments/assets/8e237bc7-46ee-43e0-a383-46392534aeb4)


The data that will be used can be of 3 different formats: **Loan Forms, Loan Agreements and Pay Stubs**, and your solution should have the different specificities of each topic into consideration.



## Requirements

To successfully complete this hackathon, you will need the following:

1. An active **Azure subscription**
2. GitHub account to access the repository and run [GitHub Codespaces](https://github.com/features/codespaces)
3. Familiarity with Python programming, including handling JSON data and making API calls.
4. Ability to provision the following resources: 
- Azure Cosmos DB
- Azure Document Intelligence
- Azure OpenAI Service
- Azure Storage Account

In order for this provision to happen, you should be either the **Owner or Contributor in an active Azure Subscription**. 

## Challenges
1. Challenge 01: **[Hack Essentials: Crafting Services for Seamless Execution](Challenge1/readme.md)**
   - Creation of the Services necessary to conduct this Hack
2. Challenge 02: **[InsightExtractor: Leveraging Azure Document Intelligence for Data Retrieval](Challenge2/readme.md)**
   - Use Azure Document Intelligence Model to retrieve information from Text and Tables
3. Challenge 03: **[Data Modelling: From Retrieval to Upload](Challenge3/data_modelling.ipynb)**
   - Structuring the Retrieved Data and Upload it to a Cosmos DB
4. Challenge 04: **[AutoFlow: Streamlining Processes with Azure Functions](Challenge4/readme.md)**
   - Creation of a Function App that will Automate these Processes
5. Challenge 05: **[Set up CI/CD for Azure Function](Challenge5/readme.md)**
   - Creation of the CI/CD pipeline to automate the run of the Azure Function 

Each challenge comes with its own set of tasks and objectives. Feel free to explore the challenges, learn, and have fun during this hackathon! If you have any questions, don't hesitate to reach out to your coach.

Happy hacking! 


## Contributors
- Joao Gonçalves
- Marta Santos
- Tomas Szabo
