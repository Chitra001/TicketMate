import qrcode
from cryptography.fernet import Fernet

# Step 1: Generate a key for encryption
key = Fernet.generate_key()
cipher_suite = Fernet(key)

# Save the key to a file (optional)
with open("secret.key", "wb") as key_file:
    key_file.write(key)

# Step 2: Data to be encrypted and encoded in the QR code
data = "1AH78 24082024 04 01"

# Step 3: Encrypt the data
encrypted_data = cipher_suite.encrypt(data.encode())

# Step 4: Create a QR code with the encrypted data
qr = qrcode.QRCode(
    version=1,  # Adjust version to control the size
    error_correction=qrcode.constants.ERROR_CORRECT_H,  # High error correction level
    box_size=10,  # Size of each box in the QR code grid
    border=4,  # Border size of the QR code
)

# Add encrypted data to the QR code
qr.add_data(encrypted_data)
qr.make(fit=True)

# Generate the QR code image
qr_image = qr.make_image(fill="black", back_color="white")

# Save the QR code image
qr_image.save("encrypted_qrcode.png")

print("Encrypted QR code generated and saved as 'encrypted_qrcode.png'.")

# Save encrypted data to a file (optional)
with open("encrypted_data.txt", "wb") as encrypted_file:
    encrypted_file.write(encrypted_data)

print("Encryption key saved as 'secret.key'.")
print("Encrypted data saved as 'encrypted_data.txt'.")
