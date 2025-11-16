from flask import Flask, render_template, request, send_file
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib.pagesizes import letter


def generate():
business_name = request.form.get("business_name")
client_name = request.form.get("client_name")
site_details = request.form.get("site_details")
sqft = request.form.get("sqft")
frequency = request.form.get("frequency")
notes = request.form.get("notes")


base_rate = 0.12
estimated_cost = float(sqft) * base_rate


styles = getSampleStyleSheet()
story = []


story.append(Paragraph(f"<b>Cleaning Service Proposal</b>", styles['Title']))
story.append(Spacer(1, 12))
story.append(Paragraph(f"Prepared for: {client_name}", styles['Normal']))
story.append(Paragraph(f"From: {business_name}", styles['Normal']))
story.append(Spacer(1, 12))
story.append(Paragraph(f"<b>Site Details</b>", styles['Heading2']))
story.append(Paragraph(site_details, styles['Normal']))
story.append(Paragraph(f"Square Footage: {sqft}", styles['Normal']))
story.append(Paragraph(f"Service Frequency: {frequency}", styles['Normal']))
story.append(Spacer(1, 12))
story.append(Paragraph(f"<b>Estimated Monthly Cost: ${estimated_cost:,.2f}</b>", styles['Heading2']))
story.append(Spacer(1, 12))
story.append(Paragraph(f"<b>Notes:</b> {notes}", styles['Normal']))


with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as tmp:
doc = SimpleDocTemplate(tmp.name, pagesize=letter)
doc.build(story)
return send_file(tmp.name, as_attachment=True, download_name="proposal.pdf")(tmp.name, as_attachment=True, download_name="proposal.pdf")


if __name__ == '__main__':
app.run(host='0.0.0.0', port=5000)
