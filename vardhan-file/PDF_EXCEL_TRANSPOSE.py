import pdfplumber
import pandas as pd
import os

def clean_string(text):
    # Replace non-printable characters with 'ti'
    return ''.join(['ti' if not x.isprintable() else x for x in text])

def transpose_table(df, sheetname, output_folder):
    base = df.columns[1]
    df = df.iloc[:, 1:]  
    df_transposed = df.transpose()
    df_transposed.columns = df_transposed.iloc[0]
    df_transposed = df_transposed[1:] 
    df_transposed.reset_index(inplace=True)
    df_transposed.rename(columns={df_transposed.columns[0]: base}, inplace=True)
    
    os.makedirs(output_folder, exist_ok=True)
    
    output_file = os.path.join(output_folder, f'{sheetname}_transposed.csv')
    
    df_transposed.to_csv(output_file, index=False)
    print(f"Transposed data saved to: {output_file}")

def pdf_to_excel(pdf_path, excel_path):
    with pdfplumber.open(pdf_path) as pdf:
        dfs = []
        for page_num, page in enumerate(pdf.pages, start=1):
            tables = page.extract_tables()
            for table_num, table in enumerate(tables, start=1):
                cleaned_table = []
                for row in table:
                    cleaned_row = [clean_string(cell) for cell in row]
                    cleaned_table.append(cleaned_row)
                
                df = pd.DataFrame(cleaned_table[1:], columns=cleaned_table[0])
                sheet_name = f'Page{page_num}_Table{table_num}' if len(tables) > 1 else f'Page{page_num}'
                dfs.append((df, sheet_name))
    
    with pd.ExcelWriter(excel_path) as writer:
        for df, sheet_name in dfs:
            df.to_excel(writer, sheet_name=sheet_name, index=False)

def remove_blank_rows(excel_path, output_path):
    df = pd.read_excel(excel_path, engine='openpyxl')
    df_cleaned = df.dropna(how='all')
    df_cleaned.to_csv(output_path, index=False)
    df_cleaned.reset_index(drop=True, inplace=True) 
    transpose_table(df_cleaned, "Sheet1", os.path.splitext(output_path)[0] + '_transposed.csv')

def convertion_def(pdf_path, output_folder):
    os.makedirs(output_folder, exist_ok=True)

    base_name = os.path.splitext(os.path.basename(pdf_path))[0]
    excel_path = os.path.join(output_folder, f'{base_name}_output.xlsx')
    output_path = os.path.join(output_folder, f'{base_name}_final_result.csv')

    pdf_to_excel(pdf_path, excel_path)

    remove_blank_rows(excel_path, output_path)

    os.remove(excel_path)
    os.remove(output_path)

def append_csvs_to_xlsx(folder_name, output_file):
    current_directory = os.getcwd()
    output_folder = os.path.join(current_directory, folder_name)

    all_data = []

    if not os.path.exists(output_folder):
        raise FileNotFoundError(f"The directory '{output_folder}' does not exist.")

    for root, dirs, files in os.walk(output_folder):
        for filename in files:
            file_path = os.path.join(root, filename)
            if filename.endswith(".csv"):
                try:
                    df = pd.read_csv(file_path, header=None)
                    all_data.append(df)
                except Exception as e:
                    print(f"Error reading {file_path}: {e}")

    if all_data:
        combined_df = pd.concat(all_data, axis=0, ignore_index=True)
        print(f"Total records appended: {len(combined_df)}")
    else:
        combined_df = pd.DataFrame()
        print("No data found in CSV files.")

    with pd.ExcelWriter(output_file, engine='openpyxl') as writer:
        combined_df.to_excel(writer, index=False, header=False, sheet_name='Sheet1')

# List of PDF paths to process
pdf_paths = ['Western.pdf', 'Microstar-1.pdf']

# Output folder (modify as needed)
output_folder = 'output_folder'

# Process each PDF
for pdf in pdf_paths:
    convertion_def(pdf, output_folder)


output_file = 'appended_data.xlsx'

append_csvs_to_xlsx(output_folder, output_file)


# # python3 -m venv env
# # source env/bin/activate
# # python3 -m pip install --upgrade pip
# # pip install pdfplumber==0.11.0
# # pip install pandas
# # pip install tk
# # pip install pyinstaller
# # pip install openpyxl


# # pyinstaller --onefile --windowed Main.py
# pyinstaller --onefile --log-level=DEBUG --name=Main Main.py