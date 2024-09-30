import pandas as pd
from difflib import get_close_matches

# Load museum data from Excel File
df = pd.read_excel('C:/Users/DELL/Desktop/Acfd/Copy of Museam_Dummy(1).xlsx')
df = df.dropna(axis=1, how='all')  # Clean up any empty columns


# State input function
def check_state(state_input):
    state_list = df['State'].dropna().unique().tolist()  # List of unique states
    state_list_lower = [state.lower() for state in state_list]  # Lowercase version for matching

    # Check if input is numeric (index) or string (state name)
    try:
        state_index = int(state_input) - 1
        if 0 <= state_index < len(state_list):  # Valid index
            selected_state = state_list[state_index]
            return get_districts_by_state(selected_state), None
        else:
            return "Invalid index. Please choose a valid option.", None
    except ValueError:
        # Case-insensitive match for state name
        state_input_lower = state_input.strip().lower()
        if state_input_lower in state_list_lower:
            selected_state = state_list[state_list_lower.index(state_input_lower)]
            return get_districts_by_state(selected_state), None
        else:
            # 70% match for suggestions
            close_matches = get_close_matches(state_input_lower, state_list_lower, n=1, cutoff=0.7)
            if close_matches:
                closest_state = state_list[state_list_lower.index(close_matches[0])]
                return f"Did you mean *{closest_state}*? Yes or No", closest_state
            else:
                return "Invalid input, please re-enter the state.", None


# Get districts by state
def get_districts_by_state(state):
    districts_museums = df[df['State'] == state]['District'].dropna().unique()
    response = f"Please choose a district from {state}:\n"
    for idx, district in enumerate(districts_museums, 1):
        response += f"{idx}. {district}\n"
    return response


# District input function (for museums by district)
def get_museums_by_district(district_input, state):
    district_list = df[df['State'] == state]['District'].dropna().unique()
    district_list_lower = [district.lower() for district in district_list]

    try:
        district_index = int(district_input) - 1
        if 0 <= district_index < len(district_list):
            selected_district = district_list[district_index]
            return get_museums(selected_district, state)
        else:
            return "Invalid district index. Please choose a valid option."
    except ValueError:
        district_input_lower = district_input.strip().lower()
        if district_input_lower in district_list_lower:
            selected_district = district_list[district_list_lower.index(district_input_lower)]
            return get_museums(selected_district, state)
        else:
            return "Invalid district, please re-enter."


# Function to fetch museums by district and state
def get_museums(district, state):
    museums = df[(df['State'] == state) & (df['District'] == district)]['Museum'].dropna()
    if museums.empty:
        return f"No museums found in {district}, {state}."

    response = f"Museums in {district}, {state}:\n"
    for idx, museum in enumerate(museums, 1):
        response += f"{idx}. {museum}\n"
    return response





