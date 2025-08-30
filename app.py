import os
import subprocess
from flask import Flask, request, send_file, render_template_string
import razorpay
from pypdf import PdfReader

app = Flask(__name__)

# Razorpay credentials (Render Environment Variables से load करें)
razorpay_client = razorpay.Client(auth=(
    os.getenv("RAZORPAY_KEY_ID"),
    os.getenv("RAZORPAY_KEY_SECRET")
))

# HTML template
UPLOAD_PAGE = """
<!doctype html>
<title>Mahamaya Word → PDF Converter</title>
<h2>📄 Mahamaya Word → PDF Converter</h2>
<p>Free up to 25 pages or 10 MB. Above that, ₹10 charge via Razorpay.</p>
<form action="/convert" method=post enctype=multipart/form-data>
  <input type=file name=file accept=".doc,.docx">
  <input type=submit value="Convert to PDF">
</form>
"""

@app.route("/")
def index():
    return render_template_string(UPLOAD_PAGE)

@app.route("/convert", methods=["POST"])
def convert():
    file = request.files["file"]
    if not file:
        return "No file uploaded", 400

    input_path = os.path.join("/tmp", file.filename)
    output_path = input_path.rsplit(".", 1)[0] + ".pdf"
    file.save(input_path)

    # File size rule (10 MB = 10 * 1024 * 1024 bytes)
    file_size = os.path.getsize(input_path)
    if file_size > 10 * 1024 * 1024:
        return razorpay_payment()

    # Convert DOCX → PDF using LibreOffice
    try:
        subprocess.run(
            ["libreoffice", "--headless", "--convert-to", "pdf", "--outdir", "/tmp", input_path],
            check=True
        )
    except subprocess.CalledProcessError as e:
        return f"Conversion failed: {str(e)}", 500

    # Count PDF pages
    reader = PdfReader(output_path)
    num_pages = len(reader.pages)

    if num_pages > 25:
        return razorpay_payment()

    # Send file if free
    return send_file(output_path, as_attachment=True)

def razorpay_payment():
    order = razorpay_client.order.create(dict(amount=1000, currency="INR"))
    return {
        "error": "payment_required",
        "order_id": order["id"],
        "amount": order["amount"]
    }, 402

@app.route("/healthz")
def health():
    return "OK", 200

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
