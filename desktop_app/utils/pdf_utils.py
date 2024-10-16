from PyPDF2 import PdfFileWriter, PdfFileReader
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter
import io
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.asymmetric import padding
from cryptography.hazmat.primitives.asymmetric import rsa
from cryptography.hazmat.backends import default_backend
import os

def create_pdf(config, template_name, form_data, author):
    # This is a placeholder implementation. You'll need to replace this with actual Word template filling.
    packet = io.BytesIO()
    can = canvas.Canvas(packet, pagesize=letter)
    can.drawString(100, 100, f"Template: {template_name}")
    for key, value in form_data.items():
        can.drawString(100, 120, f"{key}: {value}")
    can.save()

    packet.seek(0)
    new_pdf = PdfFileReader(packet)
    output = PdfFileWriter()
    output.addPage(new_pdf.getPage(0))

    # Add signature
    signature = author.decrypt_signature(config)
    if signature:
        packet = io.BytesIO()
        can = canvas.Canvas(packet, pagesize=letter)
        can.drawImage(io.BytesIO(signature), 100, 100, 100, 50)  # Adjust position and size as needed
        can.save()
        packet.seek(0)
        sig_pdf = PdfFileReader(packet)
        page = output.getPage(0)
        page.mergePage(sig_pdf.getPage(0))

    # Create fingerprint
    fingerprint = create_fingerprint(output)
    
    # Add verification URL and other variables
    packet = io.BytesIO()
    can = canvas.Canvas(packet, pagesize=letter)
    can.drawString(100, 80, f"Verification URL: {config.get('Verification', 'url')}")
    can.drawString(100, 60, f"Fingerprint: {fingerprint}")
    can.save()
    packet.seek(0)
    extra_pdf = PdfFileReader(packet)
    page = output.getPage(0)
    page.mergePage(extra_pdf.getPage(0))

    # Digitally sign the PDF
    output = sign_pdf(output, config.get('Paths', 'private_key'))

    # Save the PDF
    output_path = os.path.join(config.get('Paths', 'output_dir'), f"{template_name}_{author.short_name}.pdf")
    with open(output_path, "wb") as output_stream:
        output.write(output_stream)

    return output_path

def create_fingerprint(pdf):
    # This is a simple implementation. You might want to use a more sophisticated method.
    return hash(pdf.getPage(0).extractText())

def sign_pdf(pdf, private_key_path):
    with open(private_key_path, "rb") as key_file:
        private_key = serialization.load_pem_private_key(
            key_file.read(),
            password=None,
            backend=default_backend()
        )

    pdf_content = io.BytesIO()
    pdf.write(pdf_content)
    pdf_bytes = pdf_content.getvalue()

    signature = private_key.sign(
        pdf_bytes,
        padding.PSS(
            mgf=padding.MGF1(hashes.SHA256()),
            salt_length=padding.PSS.MAX_LENGTH
        ),
        hashes.SHA256()
    )

    # In a real implementation, you would embed this signature in the PDF
    # For this example, we'll just return the original PDF
    return pdf

def verify_pdf(pdf_path, public_key_path):
    with open(public_key_path, "rb") as key_file:
        public_key = serialization.load_pem_public_key(
            key_file.read(),
            backend=default_backend()
        )

    with open(pdf_path, "rb") as pdf_file:
        pdf_bytes = pdf_file.read()

    # In a real implementation, you would extract the signature from the PDF
    # For this example, we'll assume the entire PDF was signed
    try:
        public_key.verify(
            signature,
            pdf_bytes,
            padding.PSS(
                mgf=padding.MGF1(hashes.SHA256()),
                salt_length=padding.PSS.MAX_LENGTH
            ),
            hashes.SHA256()
        )
        return True
    except:
        return False