from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
from reportlab.lib.units import inch
from datetime import datetime, timedelta


def create_receipt(invoice_number, booking_datetime, visitor_whatsapp, museum_name, museum_address, ticket_type,
                   ticket_price, subtotal, total, ministry_of_culture_address):
    # Define the PDF file name
    pdf_file_name = f"Receipt_{invoice_number}.pdf"

    # Set up the canvas
    c = canvas.Canvas(pdf_file_name, pagesize=A4)
    width, height = A4

    # Define the receipt size and position within the page
    receipt_width = 5 * inch
    receipt_height = 9 * inch
    receipt_x = (width - receipt_width) / 2
    receipt_y = (height - receipt_height) / 2

    # Add a border with double black lines around the receipt
    c.setStrokeColor("black")
    c.setLineWidth(2)
    c.rect(receipt_x - 5, receipt_y - 5, receipt_width + 10, receipt_height + 10)  # Outer border
    c.setLineWidth(1)
    c.rect(receipt_x - 10, receipt_y - 10, receipt_width + 20, receipt_height + 20)  # Inner border

    # Add Ministry of Culture emblem and details centered
    y_position = receipt_y + receipt_height - 0.5 * inch
    c.setFont("Helvetica-Bold", 16)
    c.drawCentredString(width / 2, y_position, "Emblem")

    y_position -= 20
    c.setFont("Helvetica-Bold", 14)
    c.drawCentredString(width / 2, y_position, "Ministry of Culture")

    y_position -= 20
    c.setFont("Helvetica", 10)
    c.drawCentredString(width / 2, y_position, ministry_of_culture_address)

    y_position -= 100
    c.drawCentredString(width / 2, y_position,
                        f"Booking Date and Time: {booking_datetime.strftime('%Y-%m-%d %H:%M:%S')}")
    y_position -= 20
    c.drawCentredString(width / 2, y_position, f"Invoice Number: {invoice_number}")
    y_position -= 20
    c.drawCentredString(width / 2, y_position, f"Visitor's WhatsApp: {visitor_whatsapp}")

    # Add Museum details
    y_position -= 30
    c.setFont("Helvetica-Bold", 12)
    c.drawCentredString(width / 2, y_position, museum_name)

    y_position -= 20
    c.setFont("Helvetica", 10)
    c.drawCentredString(width / 2, y_position, museum_address)

    y_position -= 20
    c.drawCentredString(width / 2, y_position,
                        f"Booked Date and Time: {booking_datetime.strftime('%Y-%m-%d %H:%M:%S')}")

    # Add ticket type and price
    y_position -= 30
    c.drawCentredString(width / 2, y_position, f"Ticket Type: {ticket_type} - ${ticket_price:.2f}")

    # Add subtotal and total
    y_position -= 40
    c.drawCentredString(width / 2, y_position, f"Subtotal: ${subtotal:.2f}")
    y_position -= 20
    c.drawCentredString(width / 2, y_position, f"Total Amount Paid: ${total:.2f}")

    # Add terms and conditions
    y_position -= 50
    c.setFont("Helvetica", 8)
    c.drawCentredString(width / 2, y_position, "Terms and Conditions: No refunds, non-transferable.")
    y_position -= 12
    c.drawCentredString(width / 2, y_position, "Rules for entry: Outside food not allowed, pets not allowed.")
    y_position -= 12
    c.drawCentredString(width / 2, y_position, f"Contact: {ministry_of_culture_address}")

    # Footer note
    y_position -= 30
    c.setFont("Helvetica", 9)
    c.drawCentredString(width / 2, y_position,
                        "This receipt is digitally signed and does not require an additional signature.")

    # Save the PDF
    c.save()

    print(f"Receipt {pdf_file_name} created successfully.")


# Example usage
invoice_number = "123456"
booking_datetime = datetime.now()
visitor_whatsapp = "+1234567890"
museum_name = "National Museum"
museum_address = "123 Museum St, City, State"
ticket_type = "Adult"
ticket_price = 20.00
subtotal = 20.00
total = 20.00
ministry_of_culture_address = "Ministry of Culture, 456 Culture Ave, Capital City, State"

create_receipt(invoice_number, booking_datetime, visitor_whatsapp, museum_name, museum_address, ticket_type,
               ticket_price, subtotal, total, ministry_of_culture_address)