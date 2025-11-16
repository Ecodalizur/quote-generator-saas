from flask import Flask, render_template, request, send_file
from weasyprint import HTML
import tempfile


app = Flask(__name__)


@app.route("/")
def index():
return render_template("index.html")


@app.route("/generate", methods=["POST"])
def generate():
business_name = request.form.get("business_name")
client_name = request.form.get("client_name")
site_details = request.form.get("site_details")
sqft = request.form.get("sqft")
frequency = request.form.get("frequency")
notes = request.form.get("notes")


base_rate = 0.12
estimated_cost = float(sqft) * base_rate


pdf_html = f"""
<html>
<body style='font-family: Arial, sans-serif; padding: 40px;'>
<h1>Cleaning Service Proposal</h1>
<p><strong>Prepared for:</strong> {client_name}</p>
<p><strong>From:</strong> {business_name}</p>


<h2>Site Details</h2>
<p>{site_details}</p>
<p><strong>Square Footage:</strong> {sqft}</p>
<p><strong>Service Frequency:</strong> {frequency}</p>


<h2>Proposed Pricing</h2>
<p>Estimated monthly cost: <strong>${estimated_cost:,.2f}</strong></p>


<h2>Notes / Special Requirements</h2>
<p>{notes}</p>


<hr>
<p>This is an automatically generated demo proposal.</p>
</body>
</html>
"""


with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as tmp:
HTML(string=pdf_html).write_pdf(tmp.name)
return send_file(tmp.name, as_attachment=True, download_name="proposal.pdf")


if __name__ == '__main__':
app.run(host='0.0.0.0', port=5000)