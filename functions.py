import os
import re
import shutil
import subprocess

def copy_folder(folders,source_dir):
    # ADD DESCRIPTION

    for folder in folders:
        destination_dir = os.path.join(os.getcwd(), os.path.basename(os.path.join(source_dir,folder)))
        # Check if the destination directory exists
        if not os.path.exists(destination_dir):
            # Copy the directory if it does not exist
            shutil.copytree(os.path.join(source_dir,folder), destination_dir)
            print(f"Directory copied to {destination_dir}")
        else:
            print(f"Directory '{os.path.basename(os.path.join(source_dir,folder))}' already exists in the current directory. Skipping.")

def copy_files(files,source_dir):
    # ADD DESCRIPTION

    destination_dir = os.getcwd()

    # Copy each file to the current directory
    for file_path in files:
        source_file = os.path.join(source_dir,file_path)
        destination_file = os.path.join(destination_dir, file_path)

        # Check if the file exists in the source directory
        if os.path.exists(source_file):
            # Check if the file already exists in the destination
            if not os.path.exists(destination_file):
                shutil.copy(source_file, destination_file)
                print(f"Copied {file_path} to {destination_dir}")
            else:
                print(f"{file_path} already exists in {destination_dir}. Skipping.")
        else:
            print(f"{file_path} does not exist in {source_file}. Skipping.")

def filter_files(folder_path, start_patterns=None, ms_values=None):
    """
    Filters files in the specified folder by starting patterns and wind speeds (values before 'ms').

    Parameters:
        folder_path (str): The path to the folder containing the files.
        start_patterns (list): A list of starting patterns to include (e.g., ['1_1_1', '1_2_1']).
                              If None, includes all files regardless of start pattern.
        ms_values (list): A list of specific integers or decimals before 'ms' to filter by (e.g., [4, 8]).
                       If None, includes all files regardless of the value before 'ms'.

    Returns:
        list: A list of filtered file names excluding anything after 'ms'.
    """
    # Compile a regex to match the integer or decimal before 'ms'
    ms_regex = re.compile(r".*?(\d+(?:\.\d+)?)ms")

    # Reset filtered_files array each time the function is called
    filtered_files = []

    for file_name in os.listdir(folder_path):
        # Check if the file name matches the starting pattern
        if start_patterns:
            if not any(file_name.startswith(pattern) for pattern in start_patterns):
                continue

        # Check if the value before 'ms' matches any of the specified values
        if ms_values is not None:
            match = ms_regex.search(file_name)
            if match:
                ms_float = float(match.group(1))
                if ms_float not in ms_values:
                    continue
            else:
                continue

        # Truncate the file name to exclude anything after 'ms'
        if ms_regex.search(file_name):
            truncated_name = file_name[:ms_regex.search(file_name).end()]
            filtered_files.append(truncated_name)
        else:
            filtered_files.append(file_name)

    return filtered_files

def run_htc(file):
    # ADD DESCRIPTION
    
    #File should inclde the directory and .htc
    # Define the directory where you want to execute the command
    working_directory = os.getcwd()
    
    # Define the full command
    #command = r"C:\HAWC2_13.1.15\HAWC2MB.exe htc\IEA_15MW_RWT_UMaineSemi_steady_8ms.htc"
    file_clean = file.lstrip("./")

    command = "C:\HAWC2_13.1.15\HAWC2MB.exe %s"%file_clean


    # Run the command
    try:
        result = subprocess.run(
            command, 
            shell=True,               # Enable shell execution
            cwd=working_directory,    # Set the working directory
            capture_output=True,      # Capture the output
            text=True                 # Ensure output is in string format
        )

        # Print the standard output and error
        print("Output:")
        print(result.stdout)
        print("\nError:")
        print(result.stderr)

        # Check if the command was successful
        if result.returncode == 0:
            print("\nCommand executed successfully.")
        else:
            print("\nCommand failed with return code:", result.returncode)

    except Exception as e:
        print(f"An error occurred: {e}")
