import qrcode
from cryptography.fernet import Fernet

# Step 1: Array of data labeled from 1001 to 1026
data_array = [f"{i:04d}" for i in range(1001, 1027)]

# Step 2: Encrypt each data with a different key and generate corresponding QR codes
for data in data_array:
    # Generate a unique key for each data
    key = Fernet.generate_key()
    cipher_suite = Fernet(key)

    # Save the key to a file named based on the data
    key_file_name = f"{data}.key"
    with open(key_file_name, "wb") as key_file:
        key_file.write(key)

    # Encrypt the data
    encrypted_data = cipher_suite.encrypt(data.encode())

    # Create a QR code with the encrypted data
    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_H,
        box_size=10,
        border=4,
    )

    qr.add_data(encrypted_data)
    qr.make(fit=True)

    # Generate the QR code image
    qr_image = qr.make_image(fill="black", back_color="white")

    # Create a file name based on the data
    qr_file_name = f"{data}.png"

