import pandas as pd

# Define function to read JCAMP-DX file
def read_jcampdx_file(file_path):
    with open(file_path, 'r') as file:
        lines = file.readlines()
    return lines

# Define function to extract data from JCAMP-DX lines
def extract_data_from_jcampdx(lines):
    data_started = False
    data = []
    for line in lines:
        if '##XYDATA' in line:
            data_started = True
            continue
        if data_started:
            if '##END=' in line:
                break
            values = line.strip().split()
            data.append(values)
        
    return data

# Define function to export data to CSV
def export_to_csv(data, csv_path):
    # Define column names
    columns = ['Wavenumber (1/cm)'] + ['Transmittance_' + str(i) for i in range(1, len(data[0]))]
    df = pd.DataFrame(data, columns=columns)
    df = df.apply(pd.to_numeric)
    df.to_csv(csv_path, index=False)

# Main function
def get_csv(jcampdx_file_path, csv_export_path):
    # Read JCAMP-DX file
    jcampdx_lines = read_jcampdx_file(jcampdx_file_path)
    # Extract data
    data = extract_data_from_jcampdx(jcampdx_lines) 
    # Export to CSV
    export_to_csv(data, csv_export_path)


# Example usage

# jcampdx_file_path = '79-16-3-IR.jdx'
# csv_export_path = 'exported_data.csv'
# get_csv(jcampdx_file_path, csv_export_path)
