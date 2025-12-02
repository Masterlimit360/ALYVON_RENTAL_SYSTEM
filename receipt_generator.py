"""
PDF Receipt Generator for ALYVON Rental Management System
"""
from reportlab.lib.pagesizes import letter, A4
from reportlab.lib import colors
from reportlab.lib.units import inch
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer, Image
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.enums import TA_CENTER, TA_LEFT, TA_RIGHT
from datetime import datetime
import os

class ReceiptGenerator:
    def __init__(self, company_name="ALYVON Rentals", company_phone="", company_email="", company_address=""):
        self.company_name = company_name
        self.company_phone = company_phone
        self.company_email = company_email
        self.company_address = company_address
        
    def generate_receipt(self, rental_data, output_path=None):
        """
        Generate a PDF receipt for a rental
        
        Args:
            rental_data: Dictionary containing:
                - rental_id: Rental ID
                - customer_name: Customer name
                - customer_phone: Customer phone
                - customer_address: Customer address
                - rental_date: Start date
                - return_date: Return date
                - items: List of dicts with 'name', 'quantity', 'daily_rate', 'days', 'subtotal'
                - subtotal: Total before discount
                - discount_percent: Discount percentage
                - discount_amount: Discount amount
                - total_amount: Final total
                - currency: Currency symbol (default: GHS)
            output_path: Path to save PDF (if None, auto-generates in receipts folder)
        
        Returns:
            Path to generated PDF file
        """
        if output_path is None:
            # Create receipts directory if it doesn't exist
            receipts_dir = "receipts"
            os.makedirs(receipts_dir, exist_ok=True)
            
            # Generate filename with rental ID and timestamp
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"Rental_{rental_data.get('rental_id', timestamp)}_{timestamp}.pdf"
            output_path = os.path.join(receipts_dir, filename)
        
        # Create PDF document
        doc = SimpleDocTemplate(output_path, pagesize=A4,
                               rightMargin=0.75*inch, leftMargin=0.75*inch,
                               topMargin=0.75*inch, bottomMargin=0.75*inch)
        
        # Container for the 'Flowable' objects
        story = []
        
        # Define styles
        styles = getSampleStyleSheet()
        title_style = ParagraphStyle(
            'CustomTitle',
            parent=styles['Heading1'],
            fontSize=24,
            textColor=colors.HexColor('#2c3e50'),
            spaceAfter=30,
            alignment=TA_CENTER,
            fontName='Helvetica-Bold'
        )
        
        heading_style = ParagraphStyle(
            'CustomHeading',
            parent=styles['Heading2'],
            fontSize=14,
            textColor=colors.HexColor('#34495e'),
            spaceAfter=12,
            fontName='Helvetica-Bold'
        )
        
        normal_style = ParagraphStyle(
            'CustomNormal',
            parent=styles['Normal'],
            fontSize=10,
            textColor=colors.HexColor('#2c3e50'),
            spaceAfter=6
        )
        
        # Try to add company logo
        logo_path = "ALYVON logo.png"
        if os.path.exists(logo_path):
            try:
                logo = Image(logo_path, width=2*inch, height=2*inch)
                logo.hAlign = 'CENTER'
                story.append(logo)
                story.append(Spacer(1, 0.2*inch))
            except:
                pass
        
        # Company header
        story.append(Paragraph(self.company_name, title_style))
        
        if self.company_address:
            story.append(Paragraph(self.company_address, normal_style))
            story.append(Spacer(1, 0.1*inch))
        if self.company_phone:
            story.append(Paragraph(f"Phone: {self.company_phone}", normal_style))
        if self.company_email:
            story.append(Paragraph(f"Email: {self.company_email}", normal_style))
        
        story.append(Spacer(1, 0.3*inch))
        
        # Receipt title
        story.append(Paragraph("RENTAL RECEIPT", heading_style))
        story.append(Spacer(1, 0.2*inch))
        
        # Receipt details
        receipt_info = [
            ['Receipt No:', f"#{rental_data.get('rental_id', 'N/A')}"],
            ['Date:', datetime.now().strftime("%B %d, %Y")],
            ['Time:', datetime.now().strftime("%I:%M %p")],
        ]
        
        receipt_table = Table(receipt_info, colWidths=[2*inch, 4*inch])
        receipt_table.setStyle(TableStyle([
            ('FONTNAME', (0, 0), (-1, -1), 'Helvetica'),
            ('FONTSIZE', (0, 0), (-1, -1), 10),
            ('TEXTCOLOR', (0, 0), (0, -1), colors.HexColor('#7f8c8d')),
            ('TEXTCOLOR', (1, 0), (1, -1), colors.HexColor('#2c3e50')),
            ('FONTNAME', (0, 0), (0, -1), 'Helvetica-Bold'),
            ('ALIGN', (0, 0), (0, -1), 'LEFT'),
            ('ALIGN', (1, 0), (1, -1), 'LEFT'),
            ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 8),
            ('TOPPADDING', (0, 0), (-1, -1), 8),
        ]))
        
        story.append(receipt_table)
        story.append(Spacer(1, 0.3*inch))
        
        # Customer information
        story.append(Paragraph("CUSTOMER INFORMATION", heading_style))
        
        customer_info = [
            ['Customer Name:', rental_data.get('customer_name', 'N/A')],
            ['Phone:', rental_data.get('customer_phone', 'N/A')],
        ]
        
        if rental_data.get('customer_address'):
            customer_info.append(['Address:', rental_data.get('customer_address', 'N/A')])
        
        customer_table = Table(customer_info, colWidths=[2*inch, 4*inch])
        customer_table.setStyle(TableStyle([
            ('FONTNAME', (0, 0), (-1, -1), 'Helvetica'),
            ('FONTSIZE', (0, 0), (-1, -1), 10),
            ('TEXTCOLOR', (0, 0), (0, -1), colors.HexColor('#7f8c8d')),
            ('TEXTCOLOR', (1, 0), (1, -1), colors.HexColor('#2c3e50')),
            ('FONTNAME', (0, 0), (0, -1), 'Helvetica-Bold'),
            ('ALIGN', (0, 0), (0, -1), 'LEFT'),
            ('ALIGN', (1, 0), (1, -1), 'LEFT'),
            ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
            ('GRID', (0, 0), (-1, -1), 0.5, colors.HexColor('#ecf0f1')),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 8),
            ('TOPPADDING', (0, 0), (-1, -1), 8),
            ('BACKGROUND', (0, 0), (0, -1), colors.HexColor('#f8f9fa')),
        ]))
        
        story.append(customer_table)
        story.append(Spacer(1, 0.3*inch))
        
        # Rental period
        story.append(Paragraph("RENTAL PERIOD", heading_style))
        
        period_info = [
            ['Start Date:', rental_data.get('rental_date', 'N/A')],
            ['Return Date:', rental_data.get('return_date', 'N/A')],
        ]
        
        period_table = Table(period_info, colWidths=[2*inch, 4*inch])
        period_table.setStyle(TableStyle([
            ('FONTNAME', (0, 0), (-1, -1), 'Helvetica'),
            ('FONTSIZE', (0, 0), (-1, -1), 10),
            ('TEXTCOLOR', (0, 0), (0, -1), colors.HexColor('#7f8c8d')),
            ('TEXTCOLOR', (1, 0), (1, -1), colors.HexColor('#2c3e50')),
            ('FONTNAME', (0, 0), (0, -1), 'Helvetica-Bold'),
            ('ALIGN', (0, 0), (0, -1), 'LEFT'),
            ('ALIGN', (1, 0), (1, -1), 'LEFT'),
            ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
            ('GRID', (0, 0), (-1, -1), 0.5, colors.HexColor('#ecf0f1')),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 8),
            ('TOPPADDING', (0, 0), (-1, -1), 8),
            ('BACKGROUND', (0, 0), (0, -1), colors.HexColor('#f8f9fa')),
        ]))
        
        story.append(period_table)
        story.append(Spacer(1, 0.3*inch))
        
        # Items table
        story.append(Paragraph("ITEMS RENTED", heading_style))
        
        currency = rental_data.get('currency', 'GHS')
        items = rental_data.get('items', [])
        
        # Table header
        items_data = [['Item', 'Quantity', 'Daily Rate', 'Days', 'Subtotal']]
        
        # Add items
        for item in items:
            items_data.append([
                item.get('name', 'N/A'),
                str(item.get('quantity', 0)),
                f"{currency} {item.get('daily_rate', 0):.2f}",
                str(item.get('days', 0)),
                f"{currency} {item.get('subtotal', 0):.2f}"
            ])
        
        items_table = Table(items_data, colWidths=[2.5*inch, 0.8*inch, 1*inch, 0.7*inch, 1*inch])
        items_table.setStyle(TableStyle([
            # Header row
            ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#34495e')),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, 0), 11),
            ('ALIGN', (0, 0), (-1, 0), 'CENTER'),
            ('VALIGN', (0, 0), (-1, 0), 'MIDDLE'),
            ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
            ('TOPPADDING', (0, 0), (-1, 0), 12),
            
            # Data rows
            ('FONTNAME', (0, 1), (-1, -1), 'Helvetica'),
            ('FONTSIZE', (0, 1), (-1, -1), 10),
            ('TEXTCOLOR', (0, 1), (-1, -1), colors.HexColor('#2c3e50')),
            ('ALIGN', (0, 1), (0, -1), 'LEFT'),  # Item name left-aligned
            ('ALIGN', (1, 1), (-1, -1), 'CENTER'),  # Numbers center-aligned
            ('VALIGN', (0, 1), (-1, -1), 'MIDDLE'),
            ('GRID', (0, 0), (-1, -1), 0.5, colors.HexColor('#ecf0f1')),
            ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, colors.HexColor('#f8f9fa')]),
            ('BOTTOMPADDING', (0, 1), (-1, -1), 8),
            ('TOPPADDING', (0, 1), (-1, -1), 8),
        ]))
        
        story.append(items_table)
        story.append(Spacer(1, 0.3*inch))
        
        # Summary table
        subtotal = rental_data.get('subtotal', 0)
        discount_percent = rental_data.get('discount_percent', 0)
        discount_amount = rental_data.get('discount_amount', 0)
        total_amount = rental_data.get('total_amount', 0)
        
        summary_data = [
            ['Subtotal:', f"{currency} {subtotal:.2f}"],
        ]
        
        if discount_percent > 0:
            summary_data.append([f'Discount ({discount_percent}%):', f"-{currency} {discount_amount:.2f}"])
        
        summary_data.append(['TOTAL:', f"{currency} {total_amount:.2f}"])
        
        summary_table = Table(summary_data, colWidths=[4.5*inch, 1.5*inch])
        summary_table.setStyle(TableStyle([
            ('FONTNAME', (0, 0), (0, -1), 'Helvetica-Bold'),
            ('FONTNAME', (1, 0), (1, -1), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, -1), 11),
            ('TEXTCOLOR', (0, 0), (-1, -2), colors.HexColor('#2c3e50')),
            ('TEXTCOLOR', (0, -1), (-1, -1), colors.HexColor('#27ae60')),  # Total in green
            ('TEXTCOLOR', (1, -1), (1, -1), colors.HexColor('#27ae60')),
            ('FONTSIZE', (0, -1), (-1, -1), 14),  # Larger font for total
            ('ALIGN', (0, 0), (0, -1), 'RIGHT'),
            ('ALIGN', (1, 0), (1, -1), 'RIGHT'),
            ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
            ('GRID', (0, 0), (-1, -1), 1, colors.HexColor('#34495e')),
            ('BACKGROUND', (0, -1), (-1, -1), colors.HexColor('#ecf0f1')),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 10),
            ('TOPPADDING', (0, 0), (-1, -1), 10),
        ]))
        
        story.append(Paragraph("TOTAL AMOUNT", heading_style))
        story.append(Spacer(1, 0.1*inch))
        story.append(summary_table)
        story.append(Spacer(1, 0.4*inch))
        
        # Footer
        footer_text = "Thank you for choosing " + self.company_name + "!<br/>" + \
                     "Please return items on or before the return date.<br/>" + \
                     "For inquiries, please contact us using the information above."
        
        footer_style = ParagraphStyle(
            'Footer',
            parent=styles['Normal'],
            fontSize=9,
            textColor=colors.HexColor('#7f8c8d'),
            alignment=TA_CENTER,
            fontStyle='Italic'
        )
        
        story.append(Paragraph(footer_text, footer_style))
        
        # Build PDF
        doc.build(story)
        
        return output_path

