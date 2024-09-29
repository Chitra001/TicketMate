from cryptography.fernet import Fernet

# Load the encryption key from a file
with open("secret.key", "rb") as key_file:
    key = key_file.read()

cipher_suite = Fernet(key)

# Load the encrypted data from a file or directly from a QR code scan
with open("encrypted_data.txt", "rb") as encrypted_file:
    encrypted_data = encrypted_file.read()

# Decrypt the data
decrypted_data = cipher_suite.decrypt(encrypted_data).decode()

print("Decrypted data:", decrypted_data)
