import sqlite3
import pandas as pd

# Function to create a connection to the SQLite database
def create_connection(db_path):
    conn = None
    try:
        conn = sqlite3.connect(db_path)
        print(f"Connected to SQLite database: {db_path}")
    except sqlite3.Error as e:
        print(f"Error connecting to SQLite: {e}")
    return conn

# Function to create the 'museums' table if it doesn't exist
def create_table(conn):
    try:
        cursor = conn.cursor()
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS museums (
                State TEXT,
                District TEXT,
                Museum TEXT,
                Adult INTEGER,
                Child INTEGER,
                Location TEXT
            )
        ''')
        conn.commit()
        print("Museums table created or already exists.")
    except sqlite3.Error as e:
        print(f"Error creating table: {e}")

# Function to insert data from Excel into SQLite database
def insert_data_from_excel(conn, excel_file):
    try:
        # Read data from the Excel file
        df = pd.read_excel(excel_file)

        # Ensure that the data columns match the table structure
        if set(['State', 'District', 'Museum', 'Adult', 'Child', 'Location']).issubset(df.columns):
            # Insert data into the museums table
            df.to_sql('museums', conn, if_exists='append', index=False)
            print("Data inserted successfully into the museums table.")
        else:
            print("Excel file does not contain the required columns: State, District, Museum, Adult, Child, Location.")
    except Exception as e:
        print(f"Error inserting data: {e}")

# Main function to run the interface
def run_interface(excel_file, db_file):
    # Create SQLite connection
    conn = create_connection(db_file)

    if conn:
        # Create the museums table if not exists
        create_table(conn)

        # Insert data from Excel file into SQLite
        insert_data_from_excel(conn, excel_file)

        # Close the connection after insertion
        conn.close()

# Specify the path to your Excel file and SQLite database
excel_file = "C:\\path\\to\\your\\file.xlsx"
db_file = "C:\\path\\to\\your\\database.db"

# Run the interface
run_interface(excel_file, db_file)
