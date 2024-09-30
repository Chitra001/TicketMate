from twilio.rest import Client
import cloudinary
import cloudinary.uploader

# Twilio credentials
account_sid = 'ACd4d0e93e789cfc54d55e740461ed6182'
auth_token = '88a1d431551b7f6122eadebb574a5634'
client = Client(account_sid, auth_token)

# Cloudinary credentials
cloudinary.config(
    cloud_name="djscjpzcx",
    api_key="476294555497622",
    api_secret="f_Tv9UsZioZ1mOcG5Q--sXw5xMI",  # Replace with your actual API secret
    secure=True
)

# Upload QR code to Cloudinary
upload_result = cloudinary.uploader.upload(r"C:\Users\DELL\Desktop\QR code.png", public_id="qr_code")
qr_code_url = upload_result["secure_url"]

# Send MMS with Twilio via WhatsApp
message = client.messages.create(
    from_='whatsapp:+14155238886',
    body='Here is your QR code:',
    to='whatsapp:+919830961329',
    media_url=qr_code_url  # Attach the QR code image
)

print(f"Message sent with SID: {message.sid}")

