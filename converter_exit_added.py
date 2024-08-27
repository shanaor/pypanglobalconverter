import pandas as pd
import os
import sys

def detect_file_type(file_path):
    _, extension = os.path.splitext(file_path)
    return extension.lower()[1:]  # Remove the dot

def read_file(file_path):
    file_type = detect_file_type(file_path)
    if file_type == 'csv':
        return pd.read_csv(file_path)
    elif file_type == 'json':
        return pd.read_json(file_path)
    elif file_type == 'xml':
        return pd.read_xml(file_path)
    elif file_type in ['xls', 'xlsx']:
        return pd.read_excel(file_path)
    elif file_type in ['hdf', 'h5']:
        return pd.read_hdf(file_path)
    elif file_type == 'feather':
        return pd.read_feather(file_path)
    elif file_type == 'parquet':
        return pd.read_parquet(file_path)
    elif file_type in ['pickle', 'pkl']:
        return pd.read_pickle(file_path)
    elif file_type == 'fwf':
        return pd.read_fwf(file_path)
    elif file_type == 'html':
        return pd.read_html(file_path)[0]  # read_html returns a list of DataFrames
    elif file_type == 'orc':
        return pd.read_orc(file_path)
    elif file_type == 'sas':
        return pd.read_sas(file_path)
    elif file_type == 'spss':
        return pd.read_spss(file_path)
    elif file_type in ['sql', 'db']:
        # This requires a database connection, so we'll just show a message
        print("Reading from SQL requires a database connection.")
        return None
    elif file_type == 'stata':
        return pd.read_stata(file_path)
    else:
        raise ValueError(f"Unsupported file type: {file_type}")

def write_file(df, output_path, output_type):
    try:
        if output_type == 'csv':
            df.to_csv(output_path, index=False)
        elif output_type == 'json':
            df.to_json(output_path, orient='records')
        elif output_type == 'xml':
            df.to_xml(output_path)
        elif output_type in ['xls', 'xlsx']:
            df.to_excel(output_path, index=False)
        elif output_type in ['hdf', 'h5']:
            df.to_hdf(output_path, key='data', mode='w')
        elif output_type == 'feather':
            df.to_feather(output_path)
        elif output_type == 'parquet':
            df.to_parquet(output_path)
        elif output_type in ['pickle', 'pkl']:
            df.to_pickle(output_path)
        elif output_type == 'clipboard':
            df.to_clipboard(index=False)
            print("Data has been copied to clipboard.")
        elif output_type == 'fwf':
            df.to_csv(output_path, sep='\t', index=False)  # Using tab as separator
        elif output_type == 'gbq':
            print("Writing to Google BigQuery requires additional setup.")
        elif output_type == 'html':
            df.to_html(output_path, index=False)
        elif output_type == 'orc':
            print("Writing to ORC format requires additional setup.")
        elif output_type == 'sas':
            print("Writing to SAS format is not directly supported by pandas.")
        elif output_type == 'spss':
            print("Writing to SPSS format is not directly supported by pandas.")
        elif output_type == 'sql':
            print("Writing to SQL requires a database connection.")
        elif output_type == 'stata':
            df.to_stata(output_path, write_index=False)
        else:
            raise ValueError(f"Unsupported output type: {output_type}")
    except Exception as e:
        print(f"An error occurred while writing the file: {str(e)}")
        sys.exit(1)

def get_user_input(prompt, exit_allowed=True):
    while True:
        user_input = input(prompt)
        if exit_allowed and user_input.lower() == 'exit':
            print("Exiting the program. Goodbye!")
            sys.exit(0)
        if user_input:
            return user_input
        print("Invalid input. Please try again.")

def main():
    input_file = get_user_input("Enter the path to the input file (or 'exit' to quit): ")
    
    output_types = [
        'csv', 'json', 'xml', 'xlsx', 'xls', 'hdf', 'h5', 'feather', 
        'parquet', 'pickle', 'pkl', 'clipboard', 'fwf', 'gbq', 'html', 'orc',
        'sas', 'spss', 'sql', 'stata'
    ]
    print("Available output formats:")
    for i, fmt in enumerate(output_types, 1):
        print(f"{i}. {fmt}")
    print(f"{len(output_types) + 1}. Exit program")
    
    while True:
        choice = get_user_input("Enter the number of the desired output format (or 'exit' to quit): ")
        if choice.isdigit():
            choice = int(choice)
            if 1 <= choice <= len(output_types):
                output_type = output_types[choice - 1]
                break
            elif choice == len(output_types) + 1:
                print("Exiting the program. Goodbye!")
                sys.exit(0)
        print("Invalid choice. Please try again.")
    
    if output_type != 'clipboard':
        # Generate output filename in the current directory
        input_filename = os.path.basename(input_file)
        output_filename = f"converted_{os.path.splitext(input_filename)[0]}.{output_type}"
        output_file = os.path.join(os.getcwd(), output_filename)
        
        confirm = get_user_input(f"The file will be saved as '{output_file}'. Proceed? (y/n/exit): ")
        if confirm.lower() != 'y':
            print("Operation cancelled. Exiting the program.")
            sys.exit(0)
    else:
        output_file = 'clipboard'  # dummy value for clipboard option
    
    try:
        df = read_file(input_file)
        if df is not None:
            write_file(df, output_file, output_type)
            if output_type != 'clipboard':
                print(f"File has been successfully converted and saved as '{output_file}'")
            else:
                print("Data has been successfully copied to clipboard.")
    except Exception as e:
        print(f"An error occurred: {str(e)}")

if __name__ == "__main__":
    main()