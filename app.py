from flask import Flask, render_template, request, send_file
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Image, Table, TableStyle
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
import tempfile
import os
import openai


openai.api_key = os.environ.get("OPENAI_API_KEY")

app = Flask(__name__)

def generate_scope_text(sqft, frequency, notes):
    prompt = f"""
    Generate a professional commercial cleaning proposal section for a client.
    Include cleaning plan, suggested frequency, and notes based on:
    - Square Footage: {sqft}
    - Frequency: {frequency}
    - Notes: {notes}
    Keep it concise, formal, and persuasive.
    """
    
    response = openai.ChatCompletion.create(
        model="gpt-4",
        messages=[{"role": "user", "content": prompt}],
        temperature=0.5,
    )
    
    return response.choices[0].message.content

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
  
  
  styles = getSampleStyleSheet()
  story = []
  
  
  # Optional: Add Logo (replace 'logo.png' with your file in /static/)
  # story.append(Image('static/logo.png', width=150, height=50))
  # story.append(Spacer(1, 12))
  
  
  # Title & Client Info
  story.append(Paragraph(f"<b>{business_name} - Cleaning Service Proposal</b>", styles['Title']))
  story.append(Spacer(1, 12))
  story.append(Paragraph(f"Prepared for: {client_name}", styles['Normal']))
  story.append(Paragraph(f"From: {business_name}", styles['Normal']))
  story.append(Spacer(1, 12))
  
  
  # Site Details Table
  data = [
    ['Location / Site Details', site_details],
    ['Square Footage', sqft],
    ['Service Frequency', frequency]
  ]
  table = Table(data, colWidths=[150, 350])
  table.setStyle(TableStyle([
    ('BACKGROUND', (0,0), (-1,0), colors.lightgrey),
    ('TEXTCOLOR', (0,0), (-1,0), colors.black),
    ('GRID', (0,0), (-1,-1), 1, colors.black),
    ('VALIGN', (0,0), (-1,-1), 'TOP'),
    ('FONTNAME', (0,0), (-1,-1), 'Helvetica')
  ]))
  story.append(table)
  story.append(Spacer(1, 12))
  
  
  # Pricing Section
  story.append(Paragraph(f"<b>Estimated Monthly Cost:</b> ${estimated_cost:,.2f}", styles['Heading2']))
  story.append(Spacer(1, 12))


  # Notes / Special Requirements
  story.append(Paragraph(f"<b>Notes / Special Requirements:</b>", styles['Heading2']))
  story.append(Paragraph(notes, styles['Normal']))
  story.append(Spacer(1, 24))

  scope_text = generate_scope_text(sqft, frequency, notes)
  story.append(Paragraph("<b>Scope of Work:</b>", styles['Heading2']))
  story.append(Paragraph(scope_text, styles['Normal']))
  story.append(Spacer(1, 12))


  # Footer / Call to Action
  story.append(Paragraph("Thank you for considering our services. Please contact us to accept this proposal or discuss further.", styles['Normal']))


  with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as tmp:
    doc = SimpleDocTemplate(tmp.name, pagesize=letter)
    doc.build(story)
    return send_file(tmp.name, as_attachment=True, download_name="proposal.pdf")


if __name__ == '__main__':
  app.run(host='0.0.0.0', port=5000)
