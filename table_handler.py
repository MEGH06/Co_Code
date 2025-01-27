from docx import Document
import pandas as pd
from file_handler.pdf_handler import extract_pdf_content  # Import dictionary from pdf_handler
from file_handler.docx_handler import extract_docx_content  # Import dictionary from docx_handler
from file_handler.ppt_handler import extract_text_from_pptx  # Import dictionary from ppt_handler

pdf_file_path=""
docx_file_path=""
ppt_file_path=""

tables=extract_pdf_content(pdf_file_path)["tables"]
tables=tables.append(extract_docx_content(docx_file_path)["tables"])
tables=tables.append(extract_text_from_pptx(ppt_file_path)["tables"])

# Function to extract tables from the dictionaries
def extract_tables_from_files(file_dicts):
    tables = []
    for file_dict in file_dicts:
        # The second item in each dictionary contains the tables
        tables.append(file_dict[1])  # Assuming key 1 holds the tables
    return tables

# Function to combine tables from multiple sources
def combine_tables(tables):
    combined_df = pd.DataFrame()
    for table in tables:
        # Ensure consistent column names
        table.columns = [col.strip().lower() for col in table.columns]
        combined_df = pd.concat([combined_df, table], axis=0, ignore_index=True)
    return combined_df

# Filter important rows based on a condition
def filter_important_data(df, column_name, threshold):
    if column_name in df.columns:
        filtered_df = df[df[column_name] > threshold]
        return filtered_df
    else:
        print(f"Column '{column_name}' not found in the dataframe.")
        return df

# Save the final table to a Word document
def save_to_word(df, output_file):
    doc = Document()
    table = doc.add_table(rows=1, cols=len(df.columns))
    
    # Add column headers
    for i, col_name in enumerate(df.columns):
        table.cell(0, i).text = col_name
    
    # Add rows
    for _, row in df.iterrows():
        row_cells = table.add_row().cells
        for i, value in enumerate(row):
            row_cells[i].text = str(value)
    
    doc.save(output_file)
    print(f"Table saved to {output_file}")

# Main script
if __name__ == "__main__":
    # Step 1: Extract tables from each handler
    file_dicts = [pdf_data, docx_data, ppt_data]  # Add dictionaries from all handlers
    extracted_tables = extract_tables_from_files(file_dicts)
    
    # Step 2: Combine tables into a single DataFrame
    combined_table = combine_tables(extracted_tables)
    
    # Step 3: Filter important data (example: rows where 'value' > 50)
    filtered_table = filter_important_data(combined_table, column_name='value', threshold=50)
    
    # Step 4: Save the filtered table to a Word document
    save_to_word(filtered_table, output_file='final_table.docx')
