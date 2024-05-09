import pandas as pd

def select_nth_data_points(file_path, n, output_file):
    """
    Selects one out of every `n` data points from a CSV file and writes them to another CSV file.
    
    Prameters:
        file_path (str): The path to the input CSV file.
        n (int): The interval for selecting data points (e.g., 1 out of every `n` points). Defaults to 1 (include all data points).
        output_file (str): The path to the output CSV file. Defaults to 'selected_data.csv'.
    
    Returns:
        pd.DataFrame: A DataFrame containing the selected data points.
    """
    # Read the input CSV file
    data = pd.read_csv(file_path)

    # Select one out of every `n` data points
    selected_data = data.iloc[::n, :]

    # Write the selected data points to a new CSV file
    selected_data.to_csv(output_file, index=False)

    return selected_data

## select_nth_data_points("transformed_data.csv",5,'selected_data.csv')
