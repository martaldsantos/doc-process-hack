import re
import pandas as pd

def model_paystubs(paystub):
    cleaned_data = clean_form_recognizer_result(paystub)
    dataframes = tables_to_dataframes(cleaned_data["structured_tables"])

    structured_data = {
        "pay stub details": parse_pay_stub(cleaned_data["plain_text_content"]),
    }

    attribute_titles_earnings = {
    "1": "Hours Worked",
    "2": "Rate",
    "3": "Current Earnings",
    "4": "Year-to-Date Earnings"
    }

    attribute_titles_deductions = {
        "1": "Current Amount",
        "2": "Year-to-Date Amount"
    }

    # Process the earnings and deductions DataFrames
    earnings_dict = process_dataframe(dataframes[0])
    deductions_dict = process_dataframe(dataframes[1])
    # Append the processed DataFrames to the JSON structure
    structured_data["earnings"] = earnings_dict
    structured_data["deductions"] = deductions_dict

    structured_data = clean_pay_stub_section(structured_data)

    paystub_final = update_attribute_keys(structured_data, "earnings", attribute_titles_earnings)
    paystub_final = structured_data = update_attribute_keys(structured_data, "deductions", attribute_titles_deductions)

    customer_id = paystub_final["pay stub details"]["id"]
    
    document = {
        'id': str(customer_id),  # Generate a unique ID for the document
        'content': paystub_final,  # Store the plain text as 'content'
    }

    return document

def clean_form_recognizer_result(data):
    text_content = []
    
    for page in data.get("pages", []):
        for line in page.get("lines", []):
            # Check if the line contains the word "table"
            if "table" in line.get("text", "").lower():
                continue  # Keep everything if "table" is in the text
            # Keep only the "text" key
            line_keys = list(line.keys())
            for key in line_keys:
                if key != "text":
                    del line[key]
            # Collect the text content
            text_content.append(line.get("text", ""))
    
    # Create structured tables
    structured_tables = create_structured_tables(data.get("tables", []))
    
    # Concatenate all text content into a single string
    plain_text_content = " ".join(text_content)
    
    data["structured_tables"] = structured_tables
    data["plain_text_content"] = plain_text_content

    return data

def parse_pay_stub(pay_stub_text):
        # Dictionary to store parsed data
        parsed_data = {}

        # Regular expressions to match the required fields
        pay_stub_patterns = {
            'id': r'Customer ID: (\d+)',
            'Company Name': r'^(.+?) Pay Stub for:',
            'Employee Name': r'Pay Stub for: (.+?) Pay Period:',
            'Pay Period': r'Pay Period: (.+?) Pay Date:',
            'Pay Date': r'Pay Date: (.+?) Employee ID:',
            'Employee ': r'Employee ID: (.+?) Employee Information:',
            'Employee Address': r'Address: (.+?), Social Security',
            'Social_Security': r'Social Security Number: (XXX-XX-\d{4})'
        }

        # Apply regex patterns and store matches in the dictionary
        for key, pattern in pay_stub_patterns.items():
            match = re.search(pattern, pay_stub_text)
            if match:
                parsed_data[key] = match.group(1)
        return parsed_data

def create_structured_tables(tables):
    structured_tables = []
    for table in tables:
        row_count = table.get("row_count", 0)
        column_count = table.get("column_count", 0)
        cells = table.get("cells", [])
        
        # Initialize an empty table
        structured_table = [["" for _ in range(column_count)] for _ in range(row_count)]
        
        # Populate the table with cell content
        for cell in cells:
            row_index = cell.get("row_index", 0)
            column_index = cell.get("column_index", 0)
            content = cell.get("content", "")
            structured_table[row_index][column_index] = content
        
        structured_tables.append(structured_table)
    
    return structured_tables

def tables_to_dataframes(structured_tables):
    dataframes = []
    for table in structured_tables:
        df = pd.DataFrame(table)
        dataframes.append(df)
    return dataframes

def process_dataframe(df):
    result = {}
    columns = df.columns[1:]  # Ignore the first column
    for i in range(1, len(df)):  # Ignore the first row
        row_name = df.iloc[i, 0]
        result[row_name] = {}
        for col in columns:
            result[row_name][col] = f"{row_name} {col}: {df.at[i, col]}"
    return result

def rename_json_attributes(json_obj, attribute_titles):
    """
    Rename the keys of a JSON object based on the provided attribute titles.

    Parameters:
    json_obj (dict): The JSON object to rename.
    attribute_titles (dict): A dictionary where keys are the current attribute names and values are the new attribute names.

    Returns:
    dict: The updated JSON object with renamed keys.
    """
    updated_json = {}
    for old_key, new_key in attribute_titles.items():
        if old_key in json_obj:
            updated_json[new_key] = json_obj[old_key]
        else:
            updated_json[old_key] = json_obj.get(old_key, None)
    return updated_json

def clean_pay_stub_section(data):
    # Check for 'deductions' and 'earnings' in the data
    for section in ['deductions', 'earnings']:
        if section in data:
            for key, values in data[section].items():
                # For each entry, clean up the values by removing everything before the colon
                for subkey in values:
                    # Split the string by colon and take the second part, stripping whitespace
                    values[subkey] = values[subkey].split(":")[1].strip()
    return data

def update_attribute_keys(data, section, key_mapping):
    # Ensure the section exists in the data (either "earnings" or "deductions")
    if section in data:
        # Iterate over each type within the earnings or deductions section
        for entry_type, attributes in data[section].items():
            # Create a new dictionary to store the updated attributes
            updated_attributes = {}
            
            # Loop through each attribute in that entry (e.g. 1, 2, 3)
            for old_key, value in attributes.items():
                # Map the old key (which is an integer) to the new descriptive key using key_mapping
                if str(old_key) in key_mapping:  # Convert old_key to string to match the mapping
                    new_key = key_mapping[str(old_key)]
                else:
                    new_key = old_key  # If no mapping is found, retain the old key
                
                # Update the dictionary with the new key
                updated_attributes[new_key] = value

            # Replace the old attributes with the updated attributes in the data
            data[section][entry_type] = updated_attributes

    return data
