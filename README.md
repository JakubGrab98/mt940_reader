
# README

## Overview
This repository contains a set of Python modules designed to process bank statement files in the MT940 format, perform FIFO (First In, First Out) cost calculations, and generate reports in Excel format. The application is structured to handle the entire workflow from reading and parsing bank statements, calculating transaction costs, and exporting the results to an Excel file.

## Requirements
The application requires the following Python packages, specified in the `requirements.txt` file:
- certifi==2024.7.4
- charset-normalizer==3.3.2
- et-xmlfile==1.1.0
- idna==3.7
- numpy==2.0.1
- openpyxl==3.1.5
- pandas==2.2.2
- python-dateutil==2.9.0.post0
- pytz==2024.1
- requests==2.32.3
- six==1.16.0
- tzdata==2024.1
- urllib3==2.2.2

Install these dependencies using pip:
```sh
pip install -r requirements.txt
```

## Files and Modules

### `main.py`
The entry point for the application. It sets up logging, processes the MT940 files, performs FIFO calculations, and exports the results to an Excel file.

### `mt940_parser.py`
A module to read and extract data from MT940 bank statement files.
- **Mt940Parser**: A class that reads and parses MT940 files to retrieve account numbers, statement numbers, transaction details, and rates.

### `fifo_calculator.py`
A module to calculate FIFO costs.
- **FifoCalculator**: A class that performs FIFO cost calculations for foreign exchange transactions.

### `fifo_excel_report.py`
A module to generate Excel reports from FIFO data.
- **FifoExcelReport**: A class that prepares and exports FIFO data to an Excel file.

### `files_management.py`
A module for managing bank statement files.
- **FileManagement**: A class that filters and retrieves new bank statement files from a directory.

### `nbp_rates.py`
A module to retrieve currency exchange rates from the NBP (National Bank of Poland) API.
- **Rates**: A class that retrieves average currency rates for specific dates.

### `utils.py`
A module containing utility functions and regular expressions for parsing MT940 files.
- **mt940_patterns**: A dictionary containing regex patterns for different parts of the MT940 file.

### `bank_account.py`
A simple data class to hold bank account information.
- **BankAccount**: A dataclass to store details of a bank account such as name, account number, and currency.

### `requirements.txt`
A file listing all the dependencies required by the project.

## Usage

1. **Set Up Logging Configuration**: Ensure you have a valid logging configuration file at `logging_configs/config.json`. This file is used by `main.py` to set up logging.

2. **Directory Structure**: Ensure your MT940 files are located in the directory specified in `SOURCE_DIRECTORY` in `main.py`.

3. **Run the Application**:
   ```sh
   python main.py
   ```
   This will process the MT940 files, perform FIFO calculations, and generate an Excel report at the path specified in `EXPORT_PATH`.

## Example

### MT940 File Structure
Ensure your MT940 files follow the standard format and naming conventions, with extensions `.mt940` or `.old`.

### Running the Application
Modify the `SOURCE_DIRECTORY` in `main.py` to the directory containing your MT940 files. The script will process these files, perform FIFO calculations on the transactions, and output the results in an Excel file.

## Logging
Errors and information are logged as the application processes files and performs calculations. Check the log files as specified in your logging configuration for details.

## License
This project is licensed under the MIT License. See the LICENSE file for details.

---

Feel free to contact the repository owner or submit issues if you encounter any problems or have questions about the application.
