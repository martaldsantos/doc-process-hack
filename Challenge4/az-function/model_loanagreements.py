import re
import json
import os
from pydantic import BaseModel
from openai import AzureOpenAI

def model_loanagreements(loan_agreement):
   
    loanagreement_structured, customer_id = clean_json_data(loan_agreement)

    finaljsonstr = create_structured_json(loanagreement_structured)
    
    result_json = formatted_data_cleaning(finaljsonstr)

    document = {
        'id': str(customer_id),
        'content': result_json
    }
    return document

def clean_json_data(json_data):
    # Extract relevant text content from the JSON
    content = []

    # Extract text from paragraphs
    paragraphs = json_data.get("paragraphs", [])
    for paragraph in paragraphs:
        content.append(paragraph.get("text", "").strip())

    # Extract text from pages and lines
    pages = json_data.get("pages", [])
    for page in pages:
        for line in page.get("lines", []):
            content.append(line.get("text", "").strip())

    # Join all text content into a single string with spaces between components
    plain_text_content = " ".join(content)

    # Extract Customer ID using regex
    pattern = r"Customer ID:\s*(\d+)"
    match = re.search(pattern, plain_text_content)
    customer_id = match.group(1) if match else None
    return plain_text_content, customer_id

def formatted_data_cleaning(json_string):
    """
    Replaces the first 'id' in the JSON string with the 'customer_id' and returns the JSON with only the parsed information.

    Args:
        json_string (str): The original JSON string.

    Returns:
        dict: The modified JSON object with 'id' replaced by 'customer_id' and only the parsed information included.
    """
    # Load the JSON string into a Python dictionary
    data = json.loads(json_string)

    # Extract the parsed information
    parsed_info = data["choices"][0]["message"]["parsed"]

    # Replace the first id with the customer_id
    data["id"] = parsed_info["customer_id"]

    # Create a new dictionary with only the parsed information
    result = {
        "id": data["id"],
        **parsed_info
    }

    return result

def create_structured_json(loanagreement_structured):
    client = AzureOpenAI(
    azure_endpoint = os.getenv("AZURE_OPENAI_ENDPOINT"),
    api_key=os.getenv("AZURE_OPENAI_KEY"),
    api_version= "2024-08-01-preview"
    )

    model = os.getenv("AZURE_OPENAI_MODEL")

    class CalendarEvent(BaseModel):
        lender_information: str
        borrower_informaiton: str
        customer_id: str
        loan_amount: str
        purpose_of_loan: str
        interest_rate: str
        term_years: str
        commencing_date: str
        ending_date: str
        monthly_payment: str
        late_payment_fee: str
        collateral: str

    completion = client.beta.chat.completions.parse(
        model=model, # replace with the model deployment name of your gpt-4o 2024-08-06 deployment
        messages=[
            {"role": "system", "content": "Extract the information about this loan agreement contract."},
            {"role": "user", "content": loanagreement_structured},
        ],
        response_format=CalendarEvent,
    )

    finaljsonstr = completion.model_dump_json(indent=2)
    return finaljsonstr