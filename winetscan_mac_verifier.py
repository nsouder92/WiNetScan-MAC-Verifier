from os import path
import os
import tkinter as tk
from tkinter import filedialog
from tkinter import messagebox
import pandas as pd

def mac_check(input_file: str, known_macs: str) -> dict:
    """
    Takes in a CSV file and list of known MACs, which is then filtered to save a new CSV
    containing a check on the BSSID and known MAC entries to determine any good or bad MACs
    in the rows.

    Parameters:
        input_file (str):
            CSV file to be manipulated/filtered.
        
        known_macs (str):
            List of known MACs that will be compared to BSSID column.
            
    Returns:
        dict: Contains the output file name and if a bad MAC was found.
    """
    try:
        df_input_file = pd.read_csv(input_file)

        # Only create the dataframe to have the first two columns.
        df_filtered = df_input_file[['SSID', 'BSSID']]

        # Filter out rows in column 'SSID' that don't contain 'expedient'.
        df_filtered = df_filtered[df_filtered['SSID'].str.contains('expedient', case=False, na=False)]

        # Lowercase both BSSID and known MACs for string comparison.
        df_filtered['BSSID'] = df_filtered['BSSID'].str.lower()
        known_macs = known_macs.lower().split('\n')

        mac_column = pd.DataFrame({'Known MACs': known_macs})

        # Lines up the indices of both dataframes.
        df_filtered.reset_index(drop=True, inplace=True)
        mac_column.reset_index(drop=True, inplace=True)

        df_mac = pd.concat([df_filtered, mac_column], axis=1)

        # Initialize new checked column with null data.
        checked_column = pd.DataFrame({'Checked': [''] * len(df_filtered)})

        bad_mac_found = False

        for index, row in df_filtered.iterrows():
            if row['BSSID'] in known_macs:
                checked_column.at[index, 'Checked'] = 'Good MAC'
            else:
                checked_column.at[index, 'Checked'] = 'Bad MAC'
                bad_mac_found = True

        df_final_csv = pd.concat([df_mac, checked_column], axis=1)

        # Save the modified data to a new CSV file with "_CHECKED" appended to the file name
        output_file_name, output_file_extension = path.splitext(input_file)
        output_file_checked = output_file_name + "_CHECKED" + output_file_extension
        df_final_csv.to_csv(output_file_checked, index=False)

        return {
            "file": output_file_checked,
            "bad_mac_found": bad_mac_found
        }

    except Exception as e:
        messagebox.showerror("Error", f"An error occurred while processing {input_file}: {str(e)}")
        return None

def open_file(file_path: str) -> None:
    """
    Automatically open a file using the system's default application on Windows. (This will only work on a Windows machine)

    Parameters:
        file_path (str):
            The file path of the file to be opened.
            
    Raises:
        Exception: If the file cannot be opened.
    """
    try:
        # Use os.startfile, which is Windows-specific
        os.startfile(file_path)
    except Exception as e:
        messagebox.showerror("Error", f"Failed to open the file: {str(e)}")

def select_input_files() -> None:
    """
    Opens a file dialog to select multiple CSV files for processing and updates
    the input entry field with the selected file paths.
    """
    input_file_paths = filedialog.askopenfilenames(filetypes=[("CSV files", "*.csv")])
    input_entry.delete(0, tk.END)
    input_entry.insert(0, ', '.join(input_file_paths))

def execute_manipulation() -> None:
    """
    Executes the main manipulation process for each selected file.
    It gathers the input files and known MAC list, processes each file,
    and displays a summary message indicating the results of the execution.
    """
    input_files = input_entry.get().split(', ')
    known_macs = mac_text.get("1.0", "end-1c")
    
    results = []

    for input_file in input_files:
        result = mac_check(input_file, known_macs)
        if result:
            results.append(result)

    if results:
        success_message = "Execution completed.\n\n"
        for result in results:
            success_message += f"File: {result['file']}\n"
            if result["bad_mac_found"]:
                success_message += "Status: Bad MAC(s) found. File opened.\n"
                open_file(result['file'])
            else:
                success_message += "Status: No Bad MAC(s) found.\n"
            success_message += "\n"

        messagebox.showinfo("Execution Summary", success_message)

# Create the main Tkinter window
root = tk.Tk()
root.title("Wireless Network Scan MAC Verifier")

# Create and place GUI components
input_label = tk.Label(root, text="Input Files:")
input_label.grid(row=0, column=0, padx=5, pady=5, sticky="e")
input_entry = tk.Entry(root, width=50)
input_entry.grid(row=0, column=1, padx=5, pady=5)
input_button = tk.Button(root, text="Browse", command=select_input_files)
input_button.grid(row=0, column=2, padx=5, pady=5)

mac_label = tk.Label(root, text="Known MACs (Separate by newlines\n" + "or copy & paste from Ticket Scheduler):")
mac_label.grid(row=2, column=0, padx=5, pady=5, sticky="e")
mac_text = tk.Text(root, width=50, height=10)
mac_text.grid(row=2, column=1, padx=5, pady=5)

execute_button = tk.Button(root, text="Execute", command=execute_manipulation)
execute_button.grid(row=3, column=1, padx=5, pady=5)

# Run the Tkinter event loop
root.mainloop()
