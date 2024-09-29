from flask import Flask, request
from twilio.twiml.messaging_response import MessagingResponse
import pandas as pd
from datetime import datetime, timedelta

app = Flask(__name__)

# Store user language preferences and step tracking globally
user_language = {}
user_step = {}
selected_state = {}
selected_district = {}
selected_museum = {}
user_array = {}  # To store row number, date, number of adults, and number of children for each user
ticket_prices_store = {}  # To store ticket prices for each user






database_path = "D:\Museam_Dummy(1) - Copy.xlsx"

@app.route("/whatsapp", methods=["POST"])
def whatsapp_reply():
    global user_language, user_step, selected_state, selected_district, selected_museum, user_array, ticket_prices_store

    incoming_msg = request.values.get('Body', '').lower()
    sender_number = request.values.get('From', '')
    sender_name = request.values.get('ProfileName', '')
    response = MessagingResponse()
    print(sender_name)
    # If user says 'hi', restart the conversation
    if incoming_msg == 'hi':
        user_language.pop(sender_number, None)
        user_step.pop(sender_number, None)
        selected_state.pop(sender_number, None)
        selected_district.pop(sender_number, None)
        selected_museum.pop(sender_number, None)
        user_array.pop(sender_number, None)  # Clear user array when restarting
        ticket_prices_store.pop(sender_number, None)  # Clear ticket prices when restarting
        response.message(
            f"Hello! *{sender_name}* Welcome to *PRAGYA AI*. Please select your preferred language:\n*1. English*\n*2. हिंदी*\n*3. বাংলা*")
        user_step[sender_number] = "language_selection"

    # If no language is selected yet, ask for language selection
    elif sender_number not in user_language:
        if user_step.get(sender_number) == "language_selection":
            if incoming_msg == '1':
                user_language[sender_number] = 'english'
                response.message(
                    "You have selected English. Please choose an option:\n1. Book a ticket\n2. Get a previously booked ticket\n3. Get directions\n4. Cultural overview\n5. Things to see along a direction")
                user_step[sender_number] = "english_options"
            elif incoming_msg == '2':
                user_language[sender_number] = 'hindi'
                response.message(
                    "आपने हिंदी चुना है। कृपया एक विकल्प चुनें:\n1. टिकट बुक करें\n2. पहले से बुक किया गया टिकट प्राप्त करें\n3. निर्देश प्राप्त करें\n4. सांस्कृतिक अवलोकन\n5. दिशा में देखने योग्य चीजें")
                user_step[sender_number] = "hindi_options"
            elif incoming_msg == '3':
                user_language[sender_number] = 'bengali'
                response.message(
                    "আপনি বাংলা নির্বাচন করেছেন। দয়া করে একটি বিকল্প নির্বাচন করুন:\n1. টিকেট বুক করুন\n2. আগে বুক করা টিকেট পান\n3. নির্দেশ পান\n4. সাংস্কৃতিক ওভারভিউ\n5. নির্দেশে দেখার জন্য জিনিসগুলি")
                user_step[sender_number] = "bengali_options"
            else:
                response.message("Invalid choice. Please select a language:\n1. English\n2. Hindi\n3. Bengali")
        else:
            response.message("Please select your preferred language:\n1. English\n2. Hindi\n3. Bengali")
            user_step[sender_number] = "language_selection"

    # After language is selected, handle the ticket booking process
    else:
        if user_language[sender_number] == 'english':
            if user_step[sender_number] == "english_options":
                if incoming_msg == '1':
                    response.message("Would you like to search by:\n1. State\n2. Current location\n3. Pincode")
                    user_step[sender_number] = "ticket_booking"
                elif incoming_msg == '2':
                    response.message("Fetching your previously booked ticket...")
                elif incoming_msg == '3':  # User selects 'Get directions'
                    if selected_museum.get(sender_number):
                        museum_name = selected_museum[sender_number]
                        location_url = get_museum_location(database_path, museum_name)
                        if location_url:
                            response.message(f"Here is the location for {museum_name}:\n{location_url}")
                        else:
                            response.message(f"Location for {museum_name} not found.")
                    else:
                        response.message("Please select a museum first.")
                elif incoming_msg == '4':
                    response.message("Here is a cultural overview of the location you're interested in.")
                elif incoming_msg == '5':
                    response.message("Please provide a direction to find things to see along the way.")
                else:
                    response.message(
                        "Invalid choice. Please select an option:\n1. Book a ticket\n2. Get a previously booked ticket\n3. Get directions\n4. Cultural overview\n5. Things to see along a direction")

            elif user_step[sender_number] == "ticket_booking":
                if incoming_msg == '1':
                    states = get_states(database_path)
                    response.message("Please select a state from the following options:\n" + "\n".join(
                        [f"{i + 1}. {state}" for i, state in enumerate(states)]))
                    user_step[sender_number] = "search_by_state"
                elif incoming_msg == '2':
                    response.message("Using your current location to search for tickets...")
                    user_step[sender_number] = "search_by_location"
                elif incoming_msg == '3':
                    response.message("Please enter the pincode to search for tickets.")
                    user_step[sender_number] = "search_by_pincode"
                else:
                    response.message(
                        "Invalid choice. Please select how you'd like to search:\n1. State\n2. Current location\n3. Pincode")

            # Handle state selection
            elif user_step[sender_number] == "search_by_state":
                states = get_states(database_path)
                try:
                    selected_index = int(incoming_msg) - 1
                    if 0 <= selected_index < len(states):
                        selected_state[sender_number] = states[selected_index]
                        state_name = selected_state[sender_number]
                        districts = get_districts(database_path, state_name)
                        if len(districts) > 0:
                            response.message(f"Here are the districts in {state_name}:\n" + "\n".join(
                                [f"{i + 1}. {district}" for i, district in enumerate(districts)]))
                            user_step[sender_number] = "search_by_district"
                        else:
                            response.message(f"No districts found for {state_name}.")
                    else:
                        response.message("Invalid selection. Please select a valid state number from the list.")
                except ValueError:
                    response.message("Invalid input. Please enter the number corresponding to the state.")

            # Handle district selection
            elif user_step[sender_number] == "search_by_district":
                state_name = selected_state.get(sender_number)
                districts = get_districts(database_path, state_name)
                try:
                    selected_index = int(incoming_msg) - 1
                    if 0 <= selected_index < len(districts):
                        selected_district[sender_number] = districts[selected_index]
                        district_name = selected_district[sender_number]
                        response.message(f"You have selected {district_name}. Fetching museums in this district...")
                        museums = get_museums(database_path, district_name)
                        if len(museums) > 0:
                            response.message(f"Here are the museums in {district_name}:\n" + "\n".join(
                                [f"*{i + 1}. {museum}*" for i, museum in enumerate(museums)]))
                            user_step[sender_number] = "select_museum"
                        else:
                            response.message(f"No museums found in {district_name}.")
                    else:
                        response.message("Invalid selection. Please select a valid district number from the list.")
                except ValueError:
                    response.message("Invalid input. Please enter the number corresponding to the district.")

            # Handle museum selection
            elif user_step[sender_number] == "select_museum":
                district_name = selected_district.get(sender_number)
                museums = get_museums(database_path, district_name)
                try:
                    selected_index = int(incoming_msg) - 1
                    if 0 <= selected_index < len(museums):
                        selected_museum[sender_number] = museums[selected_index]
                        museum_name = selected_museum[sender_number]

                        # Find the row number of the selected museum and store it in user_array
                        row_number = find_row_number(database_path, 'Museum', museum_name)
                        user_array[sender_number] = [row_number]  # Initialize with row number
                        response.message(f"You have selected {museum_name}. Fetching ticket prices...")
                        print(museum_name)
                        # Fetch and display the ticket prices
                        ticket_prices = get_ticket(database_path, museum_name)
                        if ticket_prices[0]!=0 & ticket_prices[1]!=0:
                            # Store ticket prices in a dictionary for future reference
                            ticket_prices_store[sender_number] = ticket_prices
                            response.message(f"Ticket Details:\nAdult: {ticket_prices[0]}\nChild: {ticket_prices[1]}")
                            user_step[sender_number] = "enter_date"

                            # Offer date options: Today, Tomorrow, Day after Tomorrow
                            today, tomorrow, day_after_tomorrow = get_date_options()
                            response.message(f"Please select a date:\n1. Today ({today})\n2. Tomorrow ({tomorrow})\n3. Day after Tomorrow ({day_after_tomorrow})")
                        else:
                            response.message(f"Visiting *{museum_name}* is free!!!.")
                    else:
                        response.message("Invalid selection. Please select a valid museum number from the list.")
                except ValueError:
                    response.message("Invalid input. Please enter the number corresponding to the museum.")

            # Handle date selection and ask for the number of adults
            elif user_step[sender_number] == "enter_date":
                selected_date = None
                if incoming_msg == '1':
                    selected_date = 1  # Today
                elif incoming_msg == '2':
                    selected_date = 2  # Tomorrow
                elif incoming_msg == '3':
                    selected_date = 3  # Day after tomorrow
                else:
                    response.message("Invalid selection. Please choose 1, 2, or 3.")
                    return str(response)

                # Add the selected date (1, 2, or 3) to user_array
                if sender_number in user_array:
                    user_array[sender_number].append(selected_date)

                # Ask for the number of adults
                response.message("How many adults are going?")
                user_step[sender_number] = "enter_adults"

            # Handle number of adults
            elif user_step[sender_number] == "enter_adults":
                try:
                    num_adults = int(incoming_msg)
                    if num_adults > 0:
                        # Add the number of adults to user_array
                        user_array[sender_number].append(num_adults)

                        # Ask for the number of children
                        response.message("How many children are going?")
                        user_step[sender_number] = "enter_children"
                    else:
                        response.message("Please enter a valid number of adults.")
                except ValueError:
                    response.message("Invalid input. Please enter a valid number.")

            # Handle number of children
            elif user_step[sender_number] == "enter_children":
                try:
                    num_children = int(incoming_msg)
                    if num_children >= 0:
                        # Add the number of children to user_array
                        user_array[sender_number].append(num_children)

                        # Calculate total cost
                        adult_price = ticket_prices_store[sender_number][0]
                        child_price = ticket_prices_store[sender_number][1]
                        total_cost = (user_array[sender_number][2] * adult_price) + (
                                    user_array[sender_number][3] * child_price)

                        # Format date for display
                        today, tomorrow, day_after_tomorrow = get_date_options()
                        selected_date_str = ""
                        if user_array[sender_number][1] == 1:
                            selected_date_str = today
                        elif user_array[sender_number][1] == 2:
                            selected_date_str = tomorrow
                        elif user_array[sender_number][1] == 3:
                            selected_date_str = day_after_tomorrow

                        # Get the selected museum name
                        museum_name = selected_museum[sender_number]

                        # Provide a final confirmation with all details, including museum name
                        response.message(
                            f"Thank you! You have selected:\nMuseum: *{museum_name}*\nDate: {selected_date_str}\nNumber of adults: {user_array[sender_number][2]}\nNumber of children: {user_array[sender_number][3]}\nTotal cost: ₹{total_cost}")
                        user_step[sender_number] = "booking_confirmation"
                    else:
                        response.message("Please enter a valid number of children.")
                except ValueError:
                    response.message("Invalid input. Please enter a valid number.")
                print(user_step[sender_number])
        # Similar handling for Hindi and Bengali as needed

    return str(response)


if __name__ == "__main__":
    app.run(port=8080)
