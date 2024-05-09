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

def transform_jdx_to_dataframe(jdx_file_path,csv_export_path,final_csv_path):
    # Read the JCAMP-DX file
    jdx_file = read_jcampdx_file(jdx_file_path)
    get_csv(jdx_file_path,csv_export_path)
    Wave_Transmittance = pd.read_csv(csv_export_path)

    # Extract FIRSTX, LASTX, and NPOINTS
    FIRSTX = None
    LASTX = None
    NPOINTS = None

    for line in jdx_file:
        if line.startswith('##FIRSTX='):
            FIRSTX = float(line.split('=')[1])
        elif line.startswith('##LASTX='):
            LASTX = float(line.split('=')[1])
        elif line.startswith('##NPOINTS='):
            NPOINTS = int(line.split('=')[1])

    # Calculate X_inc
    X_inc = (LASTX - FIRSTX) / (NPOINTS - 1)

    # Initialize new DataFrame
    new_data = {'Wavenumber (1/cm)': [], 'Transmittance': []}

    # Iterate over rows
    for index, row in Wave_Transmittance.iterrows():
        wavenumber = row['Wavenumber (1/cm)']
        for col in Wave_Transmittance.columns[1:]:
            transmittance = row[col]
            new_data['Wavenumber (1/cm)'].append(wavenumber)
            new_data['Transmittance'].append(transmittance)
            wavenumber += X_inc

    # Create transformed DataFrame
    transformed_df = pd.DataFrame(new_data)
    transformed_df.to_csv(final_csv_path, index=False)
    #return transformed_df

# Example use-case:
# transform_jdx_to_dataframe("79-16-3-IR.jdx","Wave.csv","transformed_data.csv")