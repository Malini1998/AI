Extracting details for missing net weight details and HSN code

Description:

This  python script connects to an Oracle Database and extracts details for specified SKUs (Stock Keeping Units), including their HSN codes and net weights.
It validates each SKU against the database, exports found SKUs to a CSV file, and logs missing SKUs to the console. 
The script is designed for flexibility, allowing dynamic database connection details and SKU input via command line or file.

Key Features:

Dynamic Oracle DB Connection: Accepts host, port, service, username, and password as arguments.(connect securely to an oracle database)
Flexible SKU Input: Provide SKUs directly via command line or from a text file.
Validation: Checks if each SKU exists in the database before extraction.
Data Extraction: Retrieves net weight and HSN code for each valid SKU.
CSV Export: Outputs results to a CSV file with columns: SKU, Net Weight, HSN Code.
Logging: Prints a message for each SKU not found in the database.

Setup instruction

1.Install Python

Install Required Python Packages

This project requires the cx_Oracle package to connect to Oracle databases. pip install cx_Oracle

Oracle Database Access

Ensure you have access to an Oracle database and the credentials (username, password, DSN/connection string).

Usage:

This script will extracting the data in SKU table and  reduces the manually efforts.

Output:

The script creates a CSV file (default: output.csv) with columns: SKU, Net Weight, HSN Code.
SKUs not found in the database are reported in the command line output.

