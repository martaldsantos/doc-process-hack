# Challenge 2 - Leveraging Azure Document Intelligence for Data Retrieval

**Expected Duration:** 90 minutes

## Introduction
Your goal in this challenge is to get introduced to the concept of document processing and how it can help automate and streamline workflows using Azure AI services. You will learn how to analyze and extract information from documents, such as text, tables, and layout details, using the Azure Document Intelligence service. Additionally, you will learn how to save and manage the extracted data in Azure Blob Storage, enabling efficient document handling and further processing.

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


## Guide 1 : Analyze your first document using the Azure AI Document Intelligence Studio
1. Navigate to the [Azure portal](https://portal.azure.com/#home) and login with your account.
2. Navigate to your resource group.
3. Click on the **Document intelligence** resource .
4. Click on the`Go to Document Intelligence Studio` button on the prompted screen.
5. You will now find all the options for document processing that we have discussed in the beggining of this chapter

![image](https://github.com/user-attachments/assets/bf8ec313-5356-4124-8e60-39acdc9f15d0)

We will now find our desired format for the analysis of our documents. As we are working with documents that contain both tables and text with a specific layout we will therefore:

6. Inside the `Document Analysis` section, click on `Layout`. If prompted to sign in, please use your desired credentials to do so.

You will now find some sample documents that you can explore by running the `Run Analysis` button. 
Let's now add our documents.

7. On the right hand part of your screen you will find the button `Browse for files` button
   
![image](https://github.com/user-attachments/assets/44f9fca5-629a-46c8-bcb7-bb5e998bda43)

Select the `paystubjanesmith.pdf`file and load it into the portal. 

8. Click on `Run Analysis`.
9. Your screen should look similar to:

![image](https://github.com/user-attachments/assets/6e3096a9-3b44-4b5d-ab97-c0b954d37b4c)

Explore the several components that are inside your file. You can see now that there are several paragraphs and text highlighted, as well as tables. 

10. On your left-hand side you will find the options to see the result of this extraction as a JSON file:

![image](https://github.com/user-attachments/assets/46f932c7-ece3-4f83-893b-a5ee857e6277)

Explore all the components of this file. The several components include:

**For Text**

- pageNumber: Indicates the page number of the document being analyzed. 
- angle: Represents the rotation angle of the page in radians. A negative value indicates a slight counterclockwise rotation.
- width and height: Specify the dimensions of the page in the unit provided (in this case, inches).
- unit: The unit of measurement for the page dimensions, which is "inch" here.
- words: An array of objects, each representing a word detected on the page. Each word object contains:
    - content: The actual text content of the word.
    - polygon: An array of coordinates defining the bounding polygon of the word on the page.
    - confidence: A confidence score (between 0 and 1) indicating the accuracy of the word detection.
    - span: An object containing:
    - offset: The starting position of the word in the text.
    - length: The length of the word in characters.

**For Tables**

- kind: Indicates the type of cell. 
- rowIndex: The row index of the cell, starting from 0. 
- columnIndex: The column index of the cell, starting from 0. 
- content: The text content of the cell.
- boundingRegions: An array of objects representing the regions on the page where the cell is located. Each bounding region object contains:
    - pageNumber: The page number where the cell is located. 
    - polygon: An array of coordinates defining the bounding polygon of the cell on the page. The coordinates specify the vertices of the polygon that encloses the cell.

The complexity of the information coming out of a ADI analysis is considerably extensive, however, for now, don't bother too much about these details. 
Let's go to Guide 2 to see how to process this information in a code-based solution.

## Guide 2 : Use the Python SDK to analyse your documents

Please jump over to the `doc-processing.ipynb` file to complete this guide.


## Conclusion
In this challenge, you learned how to process and analyze documents using Azure AI services. You utilized the Azure Document Intelligence service to extract and interpret various elements from documents, such as text, tables, and layout information. You created functions to analyze the layout of documents, extract specific content, and save the analysis results to Azure Blob Storage. Additionally, you learned how to handle and visualize the extracted data for further processing. The concepts learned in this challenge are applicable to other scenarios where document processing and analysis are required, enabling you to automate and streamline document-related workflows.
