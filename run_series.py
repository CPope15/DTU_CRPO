
import os
import asyncio
import functions

res_folder = "htc"
cases = [#"1_1_1", 
         #"1_1_2",
         #"1_2_1",
         "1_3_1",
         #"2_1_1",
         #"2_1_2",
         #"3_1_1",
         #"3_1_2"
         ]
ms_filter = None
#working_directory = r"C:\CRPO\02_Running_area\DTU_Thesis\0_Local_testing\Manual_conversion_IEA15MW\HAWC2\IEA-15-240-RWT-UMAINESEMI" # do i need this? or os.get.cwd()
working_directory = os.getcwd() # runs in the current directory where code is

filtered_files = functions.filter_files(res_folder,start_patterns=cases,ms_values=ms_filter)

print(filtered_files)

async def run_command(working_directory, partial_file_names):
    """
    Run multiple commands asynchronously based on partial file names.
    """
    # Define the base command
    base_command = r"C:\HAWC2_13.1.15\HAWC2MB.exe htc"

    # Build the commands array dynamically
    commands = [f"{base_command}\\{file_name}.htc" for file_name in partial_file_names]

    async def execute_command(command):
        """
        Execute a single command asynchronously.
        """
        try:
            # Start the subprocess
            process = await asyncio.create_subprocess_exec(
                *command.split(),
                cwd=working_directory,
                stdout=asyncio.subprocess.PIPE,  # Capture standard output
                stderr=asyncio.subprocess.PIPE  # Capture error output
            )
            
            # Wait for the process to complete and capture its output
            stdout, stderr = await process.communicate()
            
            print(f"\nCommand: {command}")
            print("Output:")
            print(stdout.decode())
            print("Error:")
            print(stderr.decode())
            
            # Check the return code
            if process.returncode == 0:
                print("Command executed successfully.")
            else:
                print(f"Command failed with return code: {process.returncode}")

        except Exception as e:
            print(f"An error occurred while running {command}: {e}")

    # Create tasks for all commands
    tasks = [execute_command(cmd) for cmd in commands]

    # Run all tasks concurrently
    await asyncio.gather(*tasks)

async def main():
    partial_file_names = filtered_files
    await run_command(working_directory, partial_file_names)

# Run the asyncio event loop
asyncio.run(main())