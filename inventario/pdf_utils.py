"""
Utilidades para generar PDFs de reportes de inventario.
"""

from io import BytesIO
from datetime import datetime, date
from django.http import HttpResponse
from reportlab.lib.pagesizes import letter, A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer, PageBreak
from reportlab.lib import colors
from reportlab.lib.enums import TA_CENTER, TA_LEFT, TA_RIGHT
from .models import Producto


def generar_pdf_inventario(fecha_inicio=None, fecha_fin=None, usuario=None):
    """
    Genera un PDF con el reporte de inventario.
    
    Args:
        fecha_inicio: Fecha inicial del reporte (opcional)
        fecha_fin: Fecha final del reporte (opcional)
        usuario: Usuario que genera el reporte
    
    Returns:
        HttpResponse con el PDF
    """
    
    # Obtener productos activos
    productos = Producto.objects.filter(activo=True).order_by('nombre_producto')
    
    # Calcular estadísticas
    total_productos = productos.count()
    total_stock = sum(p.stock for p in productos)
    productos_bajo_stock = productos.filter(stock__lte=10).count()
    productos_criticos = productos.filter(stock__lte=5).count()
    
    # Crear el buffer para el PDF
    buffer = BytesIO()
    
    # Configurar el documento
    doc = SimpleDocTemplate(
        buffer,
        pagesize=letter,
        rightMargin=0.5*inch,
        leftMargin=0.5*inch,
        topMargin=0.5*inch,
        bottomMargin=0.5*inch,
    )
    
    # Lista de elementos para el documento
    elements = []
    
    # Estilos
    styles = getSampleStyleSheet()
    title_style = ParagraphStyle(
        'CustomTitle',
        parent=styles['Heading1'],
        fontSize=18,
        textColor=colors.HexColor('#003366'),
        spaceAfter=6,
        alignment=TA_CENTER,
        fontName='Helvetica-Bold'
    )
    
    subtitle_style = ParagraphStyle(
        'Subtitle',
        parent=styles['Normal'],
        fontSize=10,
        textColor=colors.grey,
        alignment=TA_CENTER,
        spaceAfter=12
    )
    
    section_style = ParagraphStyle(
        'SectionTitle',
        parent=styles['Heading2'],
        fontSize=12,
        textColor=colors.HexColor('#003366'),
        spaceAfter=6,
        spaceBefore=12,
        fontName='Helvetica-Bold'
    )
    
    # Título
    titulo = "REPORTE DE INVENTARIO"
    elements.append(Paragraph(titulo, title_style))
    
    # Información del reporte
    fecha_generacion = datetime.now().strftime('%d/%m/%Y %H:%M:%S')
    info_lines = [f"Generado: {fecha_generacion}"]
    
    if usuario:
        info_lines.append(f"Por: {usuario}")
    
    if fecha_inicio or fecha_fin:
        rango = ""
        if fecha_inicio:
            rango += f"Desde: {fecha_inicio}"
        if fecha_fin:
            if rango:
                rango += f" | Hasta: {fecha_fin}"
            else:
                rango = f"Hasta: {fecha_fin}"
        if rango:
            info_lines.append(rango)
    
    info_text = " | ".join(info_lines)
    elements.append(Paragraph(info_text, subtitle_style))
    elements.append(Spacer(1, 0.2*inch))
    
    # ==================== RESUMEN ====================
    elements.append(Paragraph("RESUMEN EJECUTIVO", section_style))
    
    # Tabla de resumen
    summary_data = [
        [
            f"<b>Total de Productos</b><br/>{total_productos}",
            f"<b>Total en Stock</b><br/>{total_stock} unidades",
            f"<b>Stock Bajo (≤10)</b><br/>{productos_bajo_stock}",
            f"<b>Stock Crítico (≤5)</b><br/>{productos_criticos}"
        ]
    ]
    
    summary_table = Table(summary_data, colWidths=[1.5*inch]*4)
    summary_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, -1), colors.HexColor('#E8F4F8')),
        ('TEXTCOLOR', (0, 0), (-1, -1), colors.black),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
        ('FONTNAME', (0, 0), (-1, -1), 'Helvetica'),
        ('FONTSIZE', (0, 0), (-1, -1), 9),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 12),
        ('TOPPADDING', (0, 0), (-1, -1), 12),
        ('GRID', (0, 0), (-1, -1), 1, colors.HexColor('#99CCFF')),
        ('ROWBACKGROUNDS', (0, 0), (-1, -1), [colors.HexColor('#F5F5F5'), colors.white]),
    ]))
    elements.append(summary_table)
    elements.append(Spacer(1, 0.3*inch))
    
    # ==================== TABLA DE PRODUCTOS ====================
    elements.append(Paragraph("DETALLE DE PRODUCTOS", section_style))
    
    # Preparar datos para la tabla
    table_data = [
        ['ID', 'Producto', 'Precio', 'Stock', 'Stock Mín.', 'Total', 'Estado']
    ]
    
    for producto in productos:
        total_value = producto.stock * float(producto.precio)
        
        # Determinar estado
        if producto.stock <= 5:
            estado = "🔴 Crítico"
        elif producto.stock <= 10:
            estado = "🟠 Bajo"
        else:
            estado = "🟢 OK"
        
        table_data.append([
            str(producto.id),
            producto.nombre_producto[:25],  # Limitar a 25 caracteres
            f"${producto.precio:.2f}",
            str(producto.stock),
            str(producto.stock_minimo),
            f"${total_value:.2f}",
            estado
        ])
    
    # Crear tabla
    table = Table(table_data, colWidths=[0.4*inch, 2*inch, 0.7*inch, 0.6*inch, 0.6*inch, 0.8*inch, 1*inch])
    table.setStyle(TableStyle([
        # Encabezado
        ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#003366')),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
        ('ALIGN', (0, 0), (-1, 0), 'CENTER'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, 0), 9),
        ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
        ('TOPPADDING', (0, 0), (-1, 0), 8),
        
        # Cuerpo de la tabla
        ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
        ('TEXTCOLOR', (0, 1), (-1, -1), colors.black),
        ('ALIGN', (0, 1), (-1, -1), 'CENTER'),
        ('FONTNAME', (0, 1), (-1, -1), 'Helvetica'),
        ('FONTSIZE', (0, 1), (-1, -1), 8),
        ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, colors.HexColor('#F5F5F5')]),
        ('GRID', (0, 0), (-1, -1), 1, colors.grey),
        ('VALIGN', (0, 1), (-1, -1), 'MIDDLE'),
        ('LEFTPADDING', (0, 0), (-1, -1), 4),
        ('RIGHTPADDING', (0, 0), (-1, -1), 4),
        ('BOTTOMPADDING', (0, 1), (-1, -1), 8),
        ('TOPPADDING', (0, 1), (-1, -1), 8),
    ]))
    
    elements.append(table)
    elements.append(Spacer(1, 0.3*inch))
    
    # Pie de página
    pie_texto = f"Reporte generado automáticamente el {fecha_generacion}"
    elements.append(Paragraph(pie_texto, ParagraphStyle(
        'Footer',
        parent=styles['Normal'],
        fontSize=8,
        textColor=colors.grey,
        alignment=TA_CENTER
    )))
    
    # Construir el PDF
    doc.build(elements)
    
    # Preparar respuesta
    buffer.seek(0)
    response = HttpResponse(buffer.getvalue(), content_type='application/pdf')
    response['Content-Disposition'] = f'attachment; filename="Reporte_Inventario_{date.today().strftime("%d_%m_%Y")}.pdf"'
    
    return response


def generar_pdf_ventas(ventas, fecha_inicio=None, fecha_fin=None, usuario=None, total_ventas=0):
    """
    Genera un PDF con el reporte de ventas.
    """
    buffer = BytesIO()
    doc = SimpleDocTemplate(
        buffer,
        pagesize=letter,
        rightMargin=0.5*inch,
        leftMargin=0.5*inch,
        topMargin=0.5*inch,
        bottomMargin=0.5*inch,
    )
    
    elements = []
    styles = getSampleStyleSheet()
    
    title_style = ParagraphStyle(
        'CustomTitle',
        parent=styles['Heading1'],
        fontSize=18,
        textColor=colors.HexColor('#003366'),
        spaceAfter=6,
        alignment=TA_CENTER,
        fontName='Helvetica-Bold'
    )
    
    # Título
    elements.append(Paragraph("REPORTE DE VENTAS", title_style))
    
    # Información
    fecha_generacion = datetime.now().strftime('%d/%m/%Y %H:%M:%S')
    info_text = f"Generado: {fecha_generacion} | Total de Ventas: ${total_ventas:.2f} | Transacciones: {ventas.count()}"
    elements.append(Paragraph(info_text, styles['Normal']))
    elements.append(Spacer(1, 0.2*inch))
    
    # Tabla
    table_data = [['ID', 'Fecha', 'Cliente', 'Total', 'Estado']]
    for venta in ventas:
        table_data.append([
            str(venta.id),
            venta.fecha_venta.strftime('%d/%m/%Y'),
            venta.cliente.nombre,
            f"${venta.calcular_total():.2f}",
            venta.estado.upper()
        ])
    
    table = Table(table_data, colWidths=[0.8*inch, 1.2*inch, 2*inch, 1*inch, 1*inch])
    table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#003366')),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
        ('ALIGN', (0, 0), (-1, 0), 'CENTER'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('GRID', (0, 0), (-1, -1), 1, colors.grey),
        ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, colors.HexColor('#F5F5F5')]),
    ]))
    
    elements.append(table)
    doc.build(elements)
    
    buffer.seek(0)
    response = HttpResponse(buffer.getvalue(), content_type='application/pdf')
    response['Content-Disposition'] = f'attachment; filename="Reporte_Ventas_{date.today().strftime("%d_%m_%Y")}.pdf"'
    
    return response


def generar_pdf_compras(compras, fecha_inicio=None, fecha_fin=None, usuario=None, total_compras=0):
    """
    Genera un PDF con el reporte de compras.
    """
    buffer = BytesIO()
    doc = SimpleDocTemplate(
        buffer,
        pagesize=letter,
        rightMargin=0.5*inch,
        leftMargin=0.5*inch,
        topMargin=0.5*inch,
        bottomMargin=0.5*inch,
    )
    
    elements = []
    styles = getSampleStyleSheet()
    
    title_style = ParagraphStyle(
        'CustomTitle',
        parent=styles['Heading1'],
        fontSize=18,
        textColor=colors.HexColor('#003366'),
        spaceAfter=6,
        alignment=TA_CENTER,
        fontName='Helvetica-Bold'
    )
    
    # Título
    elements.append(Paragraph("REPORTE DE COMPRAS", title_style))
    
    # Información
    fecha_generacion = datetime.now().strftime('%d/%m/%Y %H:%M:%S')
    info_text = f"Generado: {fecha_generacion} | Total de Compras: ${total_compras:.2f} | Transacciones: {compras.count()}"
    elements.append(Paragraph(info_text, styles['Normal']))
    elements.append(Spacer(1, 0.2*inch))
    
    # Tabla
    table_data = [['ID', 'Fecha', 'Proveedor', 'Total', 'Estado']]
    for compra in compras:
        table_data.append([
            str(compra.id),
            compra.fecha_compra.strftime('%d/%m/%Y'),
            compra.proveedor.nombre_proveedor,
            f"${compra.calcular_total():.2f}",
            compra.estado.upper()
        ])
    
    table = Table(table_data, colWidths=[0.8*inch, 1.2*inch, 2*inch, 1*inch, 1*inch])
    table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#003366')),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
        ('ALIGN', (0, 0), (-1, 0), 'CENTER'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('GRID', (0, 0), (-1, -1), 1, colors.grey),
        ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, colors.HexColor('#F5F5F5')]),
    ]))
    
    elements.append(table)
    doc.build(elements)
    
    buffer.seek(0)
    response = HttpResponse(buffer.getvalue(), content_type='application/pdf')
    response['Content-Disposition'] = f'attachment; filename="Reporte_Compras_{date.today().strftime("%d_%m_%Y")}.pdf"'
    
    return response
