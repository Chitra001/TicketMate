import os
from groq import Groq

# Initialize the Groq client
client = Groq(
    api_key=os.environ.get("GROQ_API_KEY"),
)

# Define an array of Indian museums
museums = [
    "National Museum",
    "Indian Museum",
    "Chhatrapati Shivaji Maharaj Vastu Sangrahalaya",
    "Prince of Wales Museum",
    "Dr. Bhau Daji Lad Museum"
]

# Function to get user selection by index
def get_user_selection():
    print("Select a museum by index from the list:")
    for idx, museum in enumerate(museums):
        print(f"{idx}. {museum}")
    choice = int(input("Enter the index of your choice: "))
    if 0 <= choice < len(museums):
        return museums[choice]
    else:
        print("Invalid index. Please select a valid index from the list.")
        return get_user_selection()

# Get the selected museum from the user
selected_museum = get_user_selection()

# Create a chat completion request to get information about the selected museum
chat_completion = client.chat.completions.create(
    messages=[
        {
            "role": "system",
            "content": "You are a helpful assistant that provides brief information about Indian museums. Each sentence should be on a new line."
        },
        {
            "role": "user",
            "content": f"Give a brief overview of the {selected_museum} in India. Write a concise description where each sentence is on a new line, aiming for around 50 words."
        }
    ],
    model="llama3-8b-8192",
)

# Print the response from the model, ensuring each sentence is on a new line
response = chat_completion.choices[0].message.content.strip()
formatted_response = "\n".join(response.split(". "))  # Ensure each sentence starts on a new line
print(formatted_response)
