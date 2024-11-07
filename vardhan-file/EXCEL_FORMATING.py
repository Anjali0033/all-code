import pandas as pd
import re

dbdf = pd.read_excel('U05A60P1_removed (1) (2).xlsx')

num_rows, num_cols = dbdf.shape
data = []

def is_name(text):
    return 'Name:' in str(text)

for i in range(num_rows):
    for j in range(num_cols):
        cell_value = dbdf.iat[i, j]
        if is_name(cell_value):
            # Extract name and check for voter ID
            name = cell_value.split('Name:')[1].strip()
            voter_id_match = re.search(r'\b(NBJ\d{7}|LLC\d{7}|TZP\d{7}|TUF\d{7}|SFJ\d{7}|CGR\d{7}|UWQ\d{7}|KKX\d{7}|DTZ\d{7}|NBJ\d{7}|TCE\d{7})\b', cell_value)
            voter_id = voter_id_match.group() if voter_id_match else None
            
            # Check for additional voter ID if not found in the name cell
            if voter_id is None:
                voter_id_match = re.search(r'\b(NBJ\d{7}|LLC\d{7}|TZP\d{7}|TUF\d{7}|SFJ\d{7}|CGR\d{7}|UWQ\d{7}|KKX\d{7}|DTZ\d{7}|NBJ\d{7}|TCE\d{7})\b', ' '.join(dbdf.iloc[i, j+1:].astype(str)))
                voter_id = voter_id_match.group() if voter_id_match else None

            if voter_id is None:
                # Calculate the index to go back to the row above (i - 1)
                back_index_1 = i - 1  # Going back one row


                for col in range(num_cols):
                    value_above = dbdf.iat[back_index_1, col]
                    if re.match(r'\b(NBJ\d{7}|LLC\d{7}|TZP\d{7}|TUF\d{7}|SFJ\d{7}|CGR\d{7}|UWQ\d{7}|KKX\d{7}|DTZ\d{7}|NBJ\d{7}|TCE\d{7})\b', str(value_above)):
                        voter_id = (value_above)


            data_row = i + 1
            personal_data = None
            while data_row < num_rows:
                if is_name(dbdf.iat[data_row, j]):
                    break
                if pd.notnull(dbdf.iat[data_row, j]):
                    personal_data = dbdf.iat[data_row, j]
                    break
                data_row += 1
            print(f"Name: {name}")
            print(f"Voter ID: {voter_id}")

            if personal_data is None:
                print("No personal data found.")
                continue

            # Convert personal_data to string if it's not already
            personal_data = str(personal_data)

            pattern2 = r"Husband's Name\s*:\s*(.*?)\s*House Number\s*:\s*(.*?)\s*Age\s*:\s*(.*?)\s*Sex\s*:\s*(\w+)"
            pattern3 = r"Father's Name\s*:\s*(.*?)\s*House Number\s*:\s*(.*?)\s*Age\s*:\s*(.*?)\s*Sex\s*:\s*(\w+)"
            pattern4 = r"Mother's Name\s*:\s*(.*?)\s*House Number\s*:\s*(.*?)\s*Age\s*:\s*(.*?)\s*Sex\s*:\s*(\w+)"

            if "Husband" in personal_data:
                match = re.search(pattern2, personal_data)
                if match:
                    husband_name = match.group(1)
                    house_number = match.group(2)
                    age = match.group(3)
                    sex = match.group(4)
                    data.append({
                        "Name": name,
                        "Voter ID" : voter_id,
                        "Husband's Name" : husband_name,
                        "House Number" : house_number,
                        "Age" : age,
                        "Sex" :sex
                    })
            elif "Father" in personal_data:
                match = re.search(pattern3, personal_data)
                if match:
                    father_name = match.group(1)
                    house_number = match.group(2)
                    age = match.group(3)
                    sex = match.group(4)
                    data.append({
                        "Name": name,
                        "Voter ID" : voter_id,
                        "Father's Name" : father_name,
                        "House Number" : house_number,
                        "Age" : age,
                        "Sex" :sex
                    })
            elif "Mother" in personal_data:
                match = re.search(pattern4, personal_data)
                if match:
                    mother_name = match.group(1)
                    house_number = match.group(2)
                    age = match.group(3)
                    sex = match.group(4)
                    data.append({
                        "Name": name,
                        "Voter ID" : voter_id,
                        "Mother's Name" : mother_name,
                        "House Number" : house_number,
                        "Age" : age,
                        "Sex" :sex
                    })
            else:
                print("No personal data found.")
                continue

print(data)

df = pd.DataFrame(data)

# Export to CSV
df.to_csv('Result_file.csv', index=False)

print("Data exported to 'extracted_data.csv'")


