from reportlab.lib.pagesizes import letter
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.lib import colors
from reportlab.platypus import SimpleDocTemplate, Paragraph, Table, TableStyle, Image
from reportlab.pdfgen import canvas

def create_receipt(filename, receipt_details):
    doc = SimpleDocTemplate(filename, pagesize=letter)
    story = []

    # Styles
    styles = getSampleStyleSheet()
    header_style = styles['Title']
    header_style.alignment = 1  # Center alignment
    subheader_style = styles['Heading2']
    subheader_style.alignment = 1  # Center alignment
    normal_style = styles['Normal']

    # Header Section
    header_image = ("C:\\Users\\parth\\OneDrive\\Desktop\\download.png") 
    header = Table([[Image(header_image, width=3*inch, height=1*inch)]], colWidths=[3*inch])
    header.setStyle(TableStyle([
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
    ]))
    story.append(header)
    
    story.append(Paragraph('<b>Receipt</b>', header_style))
    story.append(Paragraph('Thank you for shopping with us!', normal_style))
    story.append(Paragraph('<br/>', normal_style))  # Adding some space

    # Receipt Information
    receipt_info = [
        ['Receipt Number:', receipt_details.get('receipt_number', '0000')],
        ['Date:', receipt_details.get('date', 'YYYY-MM-DD')],
        ['Customer Name:', receipt_details.get('customer_name', 'Customer Name')]
    ]
    table = Table(receipt_info, colWidths=[2.5*inch, 4.5*inch])
    table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.lightgrey),
        ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.black),
        ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
        ('GRID', (0, 0), (-1, -1), 1, colors.black),
    ]))
    story.append(table)
    story.append(Paragraph('<br/>', normal_style))  # Adding some space

    # Items List
    item_data = [['Item Description', 'Price']]
    item_data.extend([[item, '$' + price] for item, price in receipt_details.get('items', [])])
    item_table = Table(item_data, colWidths=[3*inch, 1.5*inch])
    item_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.lightblue),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.black),
        ('ALIGN', (1, 1), (1, -1), 'RIGHT'),
        ('GRID', (0, 0), (-1, -1), 1, colors.black),
    ]))
    story.append(item_table)
    story.append(Paragraph('<br/>', normal_style))  # Adding some space

    # Total Amount
    total_amount = Paragraph(f'<b>Total Amount: ${receipt_details.get("total_amount", "0.00")}</b>', subheader_style)
    story.append(total_amount)
    story.append(Paragraph('<br/>', normal_style))  # Adding some space

    # Footer Section
    footer_text = '''
    <font size=10>
    Visit us at: 123 Tech Street, Tech City<br/>
    Phone: (123) 456-7890<br/>
    Website: www.techshop.com<br/>
    Thank you for your business!
    </font>
    '''
    footer = Paragraph(footer_text, normal_style)
    story.append(footer)

    # Build the PDF
    doc.build(story)

# Example usage
receipt_details = {
    'company_name': 'Tech Shop',
    'receipt_number': '123456',
    'date': '2024-08-18',
    'customer_name': 'Parth Deshpande',
    'items': [
        ('Item 1', '10.00'),
        ('Item 2', '15.50'),
        ('Item 3', '7.25')
    ],
    'total_amount': '32.75'
}

create_receipt("Receipt.pdf", receipt_details)