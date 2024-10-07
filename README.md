# Wireless Network Scan MAC Verifier

## Overview

This Python application provides a graphical user interface (GUI) to filter CSV files containing SSID and BSSID entries against a list of known MAC addresses. It identifies "Good" and "Bad" MACs based on the provided known MACs and saves the filtered results to a new CSV file. The application automatically opens the result file if any "Bad MAC" values are detected.

## Features

- Select one or more CSV input files containing SSID and BSSID entries.
- Input a list of known MAC addresses.
- Filter the CSV to include only rows with SSID containing "expedient".
- Compare BSSID entries against the known MAC addresses.
- Save the results in a new Excel file, highlighting "Bad MAC" entries in red.
- Automatically open result files if any "Bad MACs" are detected.

## Requirements

- Python 3.x
- Tkinter (usually included with Python)
- Pandas

## Installation

1. Ensure you have Python 3.x installed on your system.
2. Clone or download this repository.
3. Navigate to the project directory and install the required Python packages:
```bash
   pip install -r requirements.txt
```
## Usage
1. Clone or download this repository.
2. Run the 'winetscan_mac_verifier.py' to start the GUI application:
```
    python winetscan_mac_verifier.py
```
## Code Overview
### Main Functions

#### `mac_check(input_file: str, known_macs: str) -> dict`

This function processes the input CSV file(s) and filters the data based on known MAC addresses provided by the user.

- **Parameters:**
  - `input_file (str)`: Path to the CSV file to be manipulated/filtered.
  - `known_macs (str)`: List of known MAC addresses separated by newlines.
- **Returns**: A dictionary with the output file name and a flag indicating if "Bad MACs" were found.

#### `select_input_files() -> None`

This function opens a file dialog to select one or more CSV input files and updates the input entry field in the GUI.

#### `execute_manipulation() -> None`

This function gathers the input file paths and known MAC list from the GUI, processes each file, and opens any file containing a "Bad MAC".

#### `open_file(file_path: str) -> None`

Automatically opens a file using the system's default application on Windows when bad MACs are detected.
