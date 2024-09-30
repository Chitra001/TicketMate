from flask import Flask, request
from twilio.twiml.messaging_response import MessagingResponse
import cloudinary
import cloudinary.uploader

app = Flask(__name__)

# Cloudinary configuration
cloudinary.config(
    cloud_name="djscjpzcx",
    api_key="476294555497622",
    api_secret="f_Tv9UsZioZ1mOcG5Q--sXw5xMI",
    secure=True
)

@app.route("/whatsapp", methods=["POST"])
def whatsapp_reply():
    incoming_msg = request.values.get('Body', '').strip().lower()
    from_number = request.values.get('From', '')  # Capture the sender's number

    print(f"Received message: {incoming_msg}")
    print(f"From number: {from_number}")

    if incoming_msg == "qr":
        try:
            # Upload QR code to Cloudinary
            upload_result = cloudinary.uploader.upload(r"C:\Users\DELL\Desktop\QR code.png", public_id="qr_code")
            qr_code_url = upload_result["secure_url"]

            # Create a Twilio response object
            resp = MessagingResponse()
            resp.message(f"Here is your QR code, sent from {from_number}:").media(qr_code_url)
            return str(resp)
        except Exception as e:
            print(f"Error uploading to Cloudinary: {e}")
            resp = MessagingResponse()
            resp.message("There was an error processing your request. Please try again later.")
            return str(resp)
    else:
        resp = MessagingResponse()
        resp.message("Send 'QR' to receive a QR code.")
        return str(resp)

if __name__ == "__main__":
    app.run(port=8080)
