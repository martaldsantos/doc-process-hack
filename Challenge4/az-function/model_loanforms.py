import re
import json
import pandas as pd


def model_loanforms(loanform):
    # Process the loan application
    loanform_structured = process_loan_application(loanform).iloc[1:].reset_index(drop=True)
    loanform_structured.replace("Applicant's Signature:,", '', regex=True, inplace=True)
    loanform_structured.replace("\,", '', regex=True,  inplace=True)

    # Convert DataFrame to JSON
    json_loanform = loanform_structured.to_json(orient="records")

    # Convert JSON string to a Python dictionary
    data = json.loads(json_loanform)
    
    document = {
        'id': str(data[0].get('id')),  # Generate a unique ID for the document
        'content': data,  # Store the plain text as 'content'
    }
    return document

def create_structured_tables(tables):
    structured_tables = []
    combined_rows = []
    
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
        
        # Combine the last row with the previous one if the table has 5 columns and 3 rows
        if row_count == 3 and column_count == 5:
            combined_row = [structured_table[1][i] + " " + structured_table[2][i] for i in range(column_count)]
            structured_table[1] = combined_row
            structured_table = structured_table[:2]
            combined_rows.append(combined_row)
        
        # Append the structured table to the list
        structured_tables.append(structured_table)
    
    return structured_tables, combined_rows

def clean_form_recognizer_result(data):
    text_data = []
    table_encountered = False
    
    for page in data.get("pages", []):
        for line in page.get("lines", []):
            # Check if the line contains the word "table"
            if "table" in line.get("text", "").lower():
                table_encountered = True
                continue  # Skip the line if "table" is in the text
            
            if not table_encountered:
                # Collect the "text" information
                text_data.append(line.get("text", ""))
            
            # Keep only the "text" key
            line_keys = list(line.keys())
            for key in line_keys:
                if key != "text":
                    del line[key]
    
    # Create structured tables
    structured_tables, combined_rows = create_structured_tables(data.get("tables", []))
    data["structured_tables"] = structured_tables
    data["combined_rows"] = combined_rows
    data["text_data"] = text_data
    
    return data

def tables_to_dataframes(structured_tables):
    dataframes = []
    for table in structured_tables:
        df = pd.DataFrame(table)
        dataframes.append(df)
    return dataframes

def clean_loan_application_file(text):
    cleaned_data = {}

    # Extract the category from the first three words
    category_match = re.search(r'(\w+\s+\w+\s+\w+)', text)
    if category_match:
        cleaned_data['Category'] = category_match.group(1)
    
    # Extract Applicant Information
    applicant_info = re.search(r'Applicant Information(.*?)Employment and Income Details', text, re.DOTALL)
    if applicant_info:
        applicant_info_text = applicant_info.group(1)
        cleaned_data['Applicant Information'] = {
            'id': re.search(r'Customer ID:\s*(.*?)Full Name:', applicant_info_text, re.DOTALL).group(1).strip(),
            'Full Name': re.search(r'Full Name:\s*(.*?)Date of Birth:', applicant_info_text, re.DOTALL).group(1).strip(),
            'Date of Birth': re.search(r'Date of Birth:\s*(.*?)Social Security Number:', applicant_info_text, re.DOTALL).group(1).strip(),
            'Social Security Number': re.search(r'Social Security Number:\s*(.*?)Contact Number:', applicant_info_text, re.DOTALL).group(1).strip(),
            'Contact Number': re.search(r'Contact Number:\s*(.*?)Email Address:', applicant_info_text, re.DOTALL).group(1).strip(),
            'Email Address': re.search(r'Email Address:\s*(.*?)Physical Address:', applicant_info_text, re.DOTALL).group(1).strip(),
            'Physical Address': re.search(r'Physical Address:\s*(.*)', applicant_info_text, re.DOTALL).group(1).strip(),
        }

    # Extract Loan Information
    loan_info = re.search(r'Loan Information(.*)', text, re.DOTALL)
    if loan_info:
        loan_info_text = loan_info.group(1)
        cleaned_data['Loan Information'] = {
            'Loan Amount Requested': re.search(r'Loan Amount Requested:\s*\$?(.*?)Purpose of Loan:', loan_info_text, re.DOTALL).group(1).strip(),
            'Purpose of Loan': re.search(r'Purpose of Loan:\s*(.*?)Loan Term Desired:', loan_info_text, re.DOTALL).group(1).strip(),
            'Loan Term Desired': re.search(r'Loan Term Desired:\s*(.*)', loan_info_text, re.DOTALL).group(1).strip(),
        }

    return cleaned_data

def process_loan_application(data):
    # Clean form recognizer result to extract structured tables and text
    cleaned_data = clean_form_recognizer_result(data)
    
    # Convert extracted tables to dataframes
    dataframes = tables_to_dataframes(cleaned_data["structured_tables"]) 
    # Combine all table dataframes into one
    combined_df = pd.concat(dataframes, ignore_index=True) 
    combined_df.columns = combined_df.iloc[0]
    combined_df = combined_df[1:]
    combined_df.reset_index(drop=True, inplace=True)
    combined_df.rename(columns={"Contact Number": "Employer Contact Number"}, inplace=True)
    combined_df = combined_df.dropna(how='all')

    # Clean the extracted text using regex
    combined_text = ' '.join(cleaned_data['text_data'])
    text_data = clean_loan_application_file(combined_text)

    def clean_loan_application(data):
    # Extract applicant and loan info
        applicant_info = data['Applicant Information']
        loan_info = data['Loan Information']
        
        # Combine keys and values for the two categories
        fields = list(applicant_info.keys()) + list(loan_info.keys())
        values = list(applicant_info.values()) + list(loan_info.values())
        
        # Create the 2x10 DataFrame without 'Category'
        df = pd.DataFrame({
            'Field': fields,
            'Value': values
        })
        
        return df.set_index('Field').T

    df_cleaned = clean_loan_application(text_data)

    # Convert the text data to a DataFrame
    text_df = pd.DataFrame(df_cleaned)

    # Concatenate the text dataframe with the tables dataframe
    final_df = pd.concat([text_df, combined_df], axis=1)

    def remove_empty_cells_and_push_up(df):
        for column in df.columns:
            non_empty_values = df[column].replace('', pd.NA).dropna().values
            df[column] = pd.Series(non_empty_values).reindex(df.index, fill_value='')
        return df
    return remove_empty_cells_and_push_up(final_df)