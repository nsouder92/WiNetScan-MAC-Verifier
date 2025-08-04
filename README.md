# Wireless Network Scan MAC Verifier
## Overview
This Python application provides a graphical user interface (GUI) to filter a CSV file containing SSID and BSSID entries against a list of known MAC addresses. It identifies "Good" and "Bad" MACs based on the provided known MACs and saves the filtered results to a new CSV file.
## Features
- Select a CSV input file containing SSID and BSSID entries.
- Input a list of known MAC addresses.
- Filter the CSV to include only rows with SSID containing "expedient".
- Compare BSSID entries against the known MAC addresses.
- Save the results in a new CSV file with an indication of "Good MAC" or "Bad MAC".
## Requirements
- Python 3.x
- Pandas
- Tkinter
## Installation
1. Ensure you have Python 3.x installed on your system.
2. Install the required Python packages:
```
    pip install pandas tkinter
```
## Usage
1. Clone or download this repository.
2. Run the 'winetscan_mac_verifier.py file' to start the GUI application:
```
    python winetscan_mac_verifier.py
```
## Code Overview
### Main Functions
#### mac_check(input_file: str, known_macs: str) -> None
This function processes the input CSV file and filters the data based on known MAC addresses provided by the user.
- #### Parameters:
  - **input_file (str)**: Path to the CSV file to be manipulated/filtered.
  - **known_macs (str)**: List of known MAC addresses copied from the SOP.
#### select_input_file() -> None
This function opens a file dialog to select the CSV input file and updates the input entry field in the GUI.
#### execute_manipulation() -> None
This function grabs the input file path and known MAC list from the GUI and calls the **mac_check** function to process the data.

#### open_file(file_path: str) -> None

Automatically opens a file using the system's default application on Windows when bad MACs are detected.
