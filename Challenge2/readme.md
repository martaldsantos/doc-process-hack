# Challenge 2 - Leveraging Azure Document Intelligence for Data Retrieval

**Expected Duration:** 60 minutes

## Introduction
[textoooo]

## Introduction to Azure AI Document Intelligence

Azure AI Document Intelligence (formerly known as Azure Form Recognizer) is a suite of AI-powered tools designed to extract information from documents and forms. 

The main components of Azure AI Document Intelligence are:

- **Prebuilt Models:** These models are trained on specific types of documents and can extract information without the need for custom training. Examples include:
    - Invoice: Extracts information like invoice number, dates, and amounts.
    - Receipt: Extracts data from receipts, such as store name, total amount, and date.
    - Identity Document: Extracts data from identity cards and passports.

- **Custom Models:** Allows you to train models on your specific types of documents. This involves:
    - Form Recognizer Labeling Tool: A web-based tool to label and annotate training data.
    - Training: Upload labeled data to train custom models that can handle documents not covered by the prebuilt models.
- **Layout API:** Extracts text, tables, and structure from documents. It’s useful for documents where you need to understand the layout and organization.

- **Document Analysis:** Provides detailed analysis of the document’s content. This can include extracting key-value pairs, tables, and hierarchical structures from the document.

Each component is designed to handle different aspects of document processing, from extracting specific fields and values to understanding the overall layout and structure.


And now you might be wondering, how can you interact with this tool? There are 2 main ways to use this service:

- **Document Intelligence Studio:** A web-based interactive tool that helps you test, analyze, and improve your models. It allows you to visually inspect how models are extracting data and make adjustments as needed.

- **API Endpoints:** The core functionality is accessed via RESTful APIs, which allow developers to integrate document processing into their applications and workflows.


Let's learn how to leverage this service to the fullest by using both scenarios. Let's start with the no-code option.


## Our Scenario

At Contoso Bank, we will start by analyzing some sample documents that the main branch manager has kindly provided for us to analyse. These documents can be found in our *data* folder inside this challenge. We are working with 3 types of documents:
- **Loan Forms:** The document that a person submits when they want to apply for a loan with some basic information on ID, wage, loan amount desired, etc.
- **Pay Stubs:** An official declaration of income from the company the customer that applied for a loan work's at.
- **Loan Contract:** For those customers whose loan application's have been accepted, a loan contract will be signed and processed by Contoso's branches. 


## Guide: Analyze your first document using the Azure AI Document Intelligence Studio
1. Navigate to the [Azure portal](https://portal.azure.com/#home) and login with your account.
2. Navigate to your resource group.
3. Click on the **Document intelligence** resource .
4. Click on the <img src="image.png" alt="alt text" width="200" height="20"> button on the prompted screen.
5. You will now find all the options for document processing that we have discussed in the beggining of this chapter

![alt text](image-1.png)



## Guide: Use the Python SDK to analyse your documents

Please jump over to the doc-processing.ipynb file to complete this step



## Conclusion
In this challenge, you learned how to incorporate your data with LLMs and how to use the Azure AI services to build a call center chat assistant. You created an index with the SOPs and used the LLM to generate responses based on the information present in the SOPs. You also learned how to guide the model to behave as expected by crafting a proper *System Message*. The concepts learned in this challenge are reproducible to other scenarios where you need to use LLMs to assist in the decision-making process.
