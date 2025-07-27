#!/usr/bin/env python3
"""
extract_sku_details.py

Usage:
  python extract_sku_details.py --host HOST --port PORT --service SERVICE --user USER --password PASSWORD --skus SKU1 SKU2 ...
  python extract_sku_details.py --host HOST --port PORT --service SERVICE --user USER --password PASSWORD --sku-file sku_list.txt

- Outputs found SKUs to output.csv (columns: SKU, Net Weight, HSN Code)
- Logs missing SKUs to the console
- Requires: cx_Oracle
"""
import argparse
import csv
import sys
import cx_Oracle


def parse_args():
    parser = argparse.ArgumentParser(description="Extract SKU details from Oracle DB.")
    parser.add_argument('--host', required=True, help='Oracle DB host')
    parser.add_argument('--port', required=True, help='Oracle DB port')
    parser.add_argument('--service', required=True, help='Oracle DB service name')
    parser.add_argument('--user', required=True, help='Oracle DB username')
    parser.add_argument('--password', required=True, help='Oracle DB password')
    # Only one of --skus or --sku-file must be provided
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument('--skus', nargs='+', help='List of SKUs to check')
    group.add_argument('--sku-file', help='File containing SKUs (one per line)')
    parser.add_argument('--output', default='output.csv', help='Output CSV file name')
    return parser.parse_args()


def get_sku_list(args):
    if args.skus:
        # If SKUs are provided directly, strip whitespace and return
        return [sku.strip() for sku in args.skus]
    else:
        # If a SKU file is provided, attempt to read it
        try:
            with open(args.sku_file, 'r') as f:
                return [line.strip() for line in f if line.strip()]
        except Exception as e:
            # Validation: File read error
            print(f"Error reading SKU file: {e}", file=sys.stderr)
            sys.exit(1)


def connect_db(args):
    # Build the DSN (Data Source Name) for Oracle connection
    dsn = cx_Oracle.makedsn(args.host, args.port, service_name=args.service)
    try:
        # Attempt to connect to the Oracle database
        conn = cx_Oracle.connect(user=args.user, password=args.password, dsn=dsn)
        return conn
    except cx_Oracle.DatabaseError as e:
        # Validation: Database connection error
        print(f"Database connection error: {e}", file=sys.stderr)
        sys.exit(1)


def fetch_sku_details(conn, sku_id):
    try:
        with conn.cursor() as cur:
            # Query for the SKU in the database
            cur.execute("SELECT sku_id, net_weight, hsn_code FROM sku WHERE sku_id = :sku_id", {'sku_id': sku_id})
            row = cur.fetchone()
            if row:
                # Validation: Check for None in net_weight and hsn_code
                return {
                    'SKU': row[0],
                    'Net Weight': row[1] if row[1] is not None else '',
                    'HSN Code': row[2] if row[2] is not None else ''
                }
            else:
                # Validation: SKU not found
                return None
    except Exception as e:
        # Validation: Query error
        print(f"Error querying SKU {sku_id}: {e}", file=sys.stderr)
        return None


def main():
    args = parse_args()
    sku_list = get_sku_list(args)
    conn = connect_db(args)
    found_skus = []
    try:
        for sku in sku_list:
            details = fetch_sku_details(conn, sku)
            if details:
                found_skus.append(details)
            else:
                # Validation: SKU not available in database
                print(f"SKU {sku} not available")
    finally:
        # Always close the DB connection
        conn.close()

    if found_skus:
        try:
            # Attempt to write the found SKUs to the output CSV file
            with open(args.output, 'w', newline='', encoding='utf-8') as csvfile:
                writer = csv.DictWriter(csvfile, fieldnames=['SKU', 'Net Weight', 'HSN Code'])
                writer.writeheader()
                writer.writerows(found_skus)
            print(f"Exported {len(found_skus)} SKUs to {args.output}")
        except Exception as e:
            # Validation: File write error
            print(f"Error writing CSV: {e}", file=sys.stderr)
            sys.exit(1)
    else:
        # Validation: No SKUs found to export
        print("No SKUs found to export.")


if __name__ == "__main__":
    main() 