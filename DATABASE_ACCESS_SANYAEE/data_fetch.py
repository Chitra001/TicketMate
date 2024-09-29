import sqlite3
from datetime import datetime, timedelta

# Function to get unique states from SQLite database
def get_states(database_path):
    try:
        conn = sqlite3.connect(database_path)
        cursor = conn.cursor()
        cursor.execute("SELECT DISTINCT State FROM museums WHERE State IS NOT NULL")
        states = [row[0] for row in cursor.fetchall()]
        conn.close()
        return states
    except Exception as e:
        print(f"Error loading states: {e}")
        return []

# Function to get unique districts for a given state from SQLite database
def get_districts(database_path, state_name):
    try:
        conn = sqlite3.connect(database_path)
        cursor = conn.cursor()
        cursor.execute("SELECT DISTINCT District FROM museums WHERE State = ? AND District IS NOT NULL", (state_name,))
        districts = [row[0] for row in cursor.fetchall()]
        conn.close()
        return districts
    except Exception as e:
        print(f"Error loading districts: {e}")
        return []

# Function to get unique museums for a given district from SQLite database
def get_museums(database_path, district_name):
    try:
        conn = sqlite3.connect(database_path)
        cursor = conn.cursor()
        cursor.execute("SELECT DISTINCT Museum FROM museums WHERE District = ? AND Museum IS NOT NULL", (district_name,))
        museums = [row[0] for row in cursor.fetchall()]
        conn.close()
        return museums
    except Exception as e:
        print(f"Error loading museums: {e}")
        return []

# Function to get ticket prices for a given museum from SQLite database
def get_ticket(database_path, museum_name):
    try:
        conn = sqlite3.connect(database_path)
        cursor = conn.cursor()
        cursor.execute("SELECT Adult, Child FROM museums WHERE Museum = ?", (museum_name,))
        museum_data = cursor.fetchone()
        conn.close()
        if museum_data:
            adult_price, child_price = int(museum_data[0]), int(museum_data[1])
            return [adult_price, child_price]
        else:
            return None
    except Exception as e:
        print(f"Error loading ticket information: {e}")
        return None

# Function to find the row number for a specific value in a given column from SQLite database
def find_row_number(database_path, column_name, value_to_find):
    try:
        conn = sqlite3.connect(database_path)
        cursor = conn.cursor()
        cursor.execute(f"SELECT rowid FROM museums WHERE {column_name} = ?", (value_to_find,))
        row_number = cursor.fetchone()
        conn.close()
        if row_number:
            return row_number[0]  # rowid is SQLite's internal row number starting from 1
        else:
            return f"Value '{value_to_find}' not found in column '{column_name}'"
    except Exception as e:
        print(f"Error finding row number: {e}")
        return None

# Function to get museum location from SQLite database
def get_museum_location(database_path, museum_name):
    try:
        conn = sqlite3.connect(database_path)
        cursor = conn.cursor()
        cursor.execute("SELECT Location FROM museums WHERE LOWER(Museum) = LOWER(?)", (museum_name,))
        location = cursor.fetchone()
        conn.close()
        if location:
            return location[0]
        else:
            return f"No museum found with the name '{museum_name}'."
    except Exception as e:
        print(f"Error loading museum location: {e}")
        return None

# Function to get date options (today, tomorrow, day after tomorrow)
def get_date_options():
    today = datetime.today()
    tomorrow = today + timedelta(days=1)
    day_after_tomorrow = today + timedelta(days=2)

    return today.strftime('%d-%m-%Y'), tomorrow.strftime('%d-%m-%Y'), day_after_tomorrow.strftime('%d-%m-%Y')

# Example database path (modify it accordingly)
database_path = "C:\\path\\to\\your\\database.db"
