from flask import Flask, request, send_file, render_template_string
from docx2pdf import convert
import os

app = Flask(__name__)

HTML = """
<h2>📄 Word ➝ PDF Converter (Mahamaya Stationery)</h2>
<p>Free ≤ 25 pages or 10 MB, else ₹10 via Razorpay</p>
<form method="post" enctype="multipart/form-data">
  <input type="file" name="word_file" accept=".doc,.docx" required>
  <button type="submit">Convert</button>
</form>
"""

@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        word_file = request.files["word_file"]
        input_path = "input.docx"
        output_path = "output.pdf"

        # Save uploaded file
        word_file.save(input_path)

        # Convert DOCX → PDF
        convert(input_path, output_path)

        return send_file(output_path, as_attachment=True)

    return render_template_string(HTML)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
