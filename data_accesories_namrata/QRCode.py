import qrcode
import os
from datetime import datetime, timedelta
from cryptography.fernet import Fernet




def generate_key():
    """Generate a key and save it into a file"""
    key = Fernet.generate_key()
    with open("secret.key", "wb") as key_file:
        key_file.write(key)
    return key

def encrypt_message(message, key):
    """
    Encrypts a message
    """
    encoded_message = message.encode()
    f = Fernet(key)
    encrypted_message = f.encrypt(encoded_message)
    return encrypted_message

# Generate and save key
key = generate_key()



def do_qr(data):
    # Determine the date based on data[1]
    if data[1] == 1:
        date_to_use = datetime.now()  # Today's date
    elif data[1] == 2:
        date_to_use = datetime.now() + timedelta(days=1)  # Tomorrow's date
    elif data[1] == 3:
        date_to_use = datetime.now() + timedelta(days=2)  # Day after tomorrow's date
    else:
        raise ValueError("Invalid date indicator. Use 1 for today, 2 for tomorrow, or 3 for day after tomorrow.")

    # Format the date as a string in ddmmyyyy format
    date_str = date_to_use.strftime("%d%m%Y")

    # Data to be encoded in the QR code
    row_number = str(data[0]).zfill(4)
    adult_number = str(data[2]).zfill(2)
    child_number = str(data[3]).zfill(2)
    invoice_number = str(data[4]).zfill(5)

    # Combine all parts to form the final data string
    encoded_data = f"{row_number} {date_str} {adult_number} {child_number} {invoice_number}"
    print("Data encoded in QR Code:", encoded_data)

    encrypted_message = encrypt_message(encoded_data, key)
    print("Encrypted:", encrypted_message)


    # Generate QR code
    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_H,
        box_size=10,
        border=4
    )
    qr.add_data(encrypted_message)
    qr.make(fit=True)

    # Create an image from the QR Code instance
    img = qr.make_image(fill_color="black", back_color="white")

    # Directory to save the QR code
    save_directory = "C:\\Users\\CHITRADEEP\\OneDrive\\Desktop\\hack heritage\\QR"

    # Ensure the directory exists
    if not os.path.exists(save_directory):
        os.makedirs(save_directory)

    # Save the QR code image using the invoice number as the filename in the specified directory
    filename = os.path.join(save_directory, f"{invoice_number}.png")
    img.save(filename)
    print(f"QR Code generated and saved as {filename}")

# Example usage
data_array = [168, 2, 4, 2, 55555]  # The second element controls the date
do_qr(data_array)






# Encrypt the message

