from os import path
import tkinter as tk
from tkinter import filedialog
from tkinter import messagebox
import pandas as pd

def mac_check(input_file:str, known_macs:str) -> None:
    '''
    Takes in a CSV file and list of known MACs, which is then filtered to save a new CSV
    containing a check on the BSSID and known MAC entries to determine any good or bad MACs
    in the rows.

        Parameters:
                input_file (str):
                    CSV file to be manipulated/filtered.
                
                known_macs (str):
                    List of known MACs that will be compared to BSSID column.
    '''
    try:
        df_input_file = pd.read_csv(input_file)

        # Only create the dataframe to have the first two columns.
        df_filtered = df_input_file[['SSID', 'BSSID']]

        # Filter out rows in column 'SSID' that don't contain 'expedient'.
        df_filtered = df_filtered[df_filtered['SSID'].str.contains('expedient', case=False, na=False)]

        # lowercase both BSSID and known MACs for string comparison.
        df_filtered['BSSID'] = df_filtered['BSSID'].str.lower()
        known_macs = known_macs.lower().split('\n')

        mac_column = pd.DataFrame({'Known MACs': known_macs})

        # Lines up the indices of both dataframes.
        df_filtered.reset_index(drop=True, inplace=True)
        mac_column.reset_index(drop=True, inplace=True)

        df_mac = pd.concat([df_filtered, mac_column], axis=1)

        # Initialize new checked column with null data.
        checked_column = pd.DataFrame({'Checked': [''] * len(df_filtered)})

        for index, row in df_filtered.iterrows():
            checked_column.at[index, 'Checked'] = 'Good MAC' if row['BSSID'] in known_macs else 'Bad MAC'

        df_final_csv = pd.concat([df_mac, checked_column], axis=1)

        # Save the modified data to a new CSV file with "_CHECKED" appended to the file name
        # Set index=False to exclude the DataFrame index from the CSV file
        output_file_name, output_file_extension = path.splitext(input_file)
        output_file_checked = output_file_name + "_CHECKED" + output_file_extension
        df_final_csv.to_csv(output_file_checked, index=False)

        messagebox.showinfo("Success", "Excel file manipulation completed successfully!\n\n" +
                            "New file saved at: " + output_file_checked)

    except Exception as e:
        messagebox.showerror("Error", f"An error occurred: {str(e)}")

def select_input_file() -> None:
    '''
    CSV input file for filtering.
    '''
    input_file_path = filedialog.askopenfilename(filetypes=[("Excel files", "*.csv")])
    input_entry.delete(0, tk.END)
    input_entry.insert(0, input_file_path)

def execute_manipulation() -> None:
    '''
    Grabs the input file and known MAC list, executing the main manipulation function.
    '''
    input_file = input_entry.get()
    known_macs = data_text.get("1.0", "end-1c")
    mac_check(input_file, known_macs)

# Create the main Tkinter window
root = tk.Tk()
root.title("Wireless Network Scan MAC Verifier")

# Create and place GUI components
input_label = tk.Label(root, text="Input File:")
input_label.grid(row=0, column=0, padx=5, pady=5, sticky="e")
input_entry = tk.Entry(root, width=50)
input_entry.grid(row=0, column=1, padx=5, pady=5)
input_button = tk.Button(root, text="Browse", command=select_input_file)
input_button.grid(row=0, column=2, padx=5, pady=5)
data_label = tk.Label(root, text="Known MACs (Separate by newlines\n" + "or copy & paste from Ticket Scheduler):")
data_label.grid(row=2, column=0, padx=5, pady=5, sticky="e")
data_text = tk.Text(root, width=50, height=10)
data_text.grid(row=2, column=1, padx=5, pady=5)

execute_button = tk.Button(root, text="Execute", command=execute_manipulation)
execute_button.grid(row=3, column=1, padx=5, pady=5)

# Run the Tkinter event loop
root.mainloop()
