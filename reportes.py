from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
from reportlab.lib import colors
from reportlab.platypus import Table, TableStyle
from datetime import datetime
import os



class ReciboFactura():
    
    def __init__(self):
        fecha = datetime.now()
        titulo = 'Factura-{}-{}:{}:{}--{}:{}.pdf'.format(
            'XXX-XXX-XXX', fecha.day, fecha.month, fecha.year,
            fecha.hour, fecha.minute
        )
        nombre_pdf = os.path.join('Facturas/',titulo)

       
        self.factura = canvas.Canvas('prueba.pdf', pagesize=A4)
        self.crear_esqueleto()
        #self.dibujar_tabla()
        
    def crear_esqueleto(self):
        w, h = A4
        self.factura
        self.factura.drawString(240, h - 50, "FACTURA")
        self.factura.line(x1=20, x2=580, y1= h-70, y2= h-70)

        self.factura.drawString(60, h- 100,
            'Id del cliente : '
        )
        self.factura.drawString(420, h- 100,
            'Fecha : '
        )
        self.factura.drawString(60, h- 140,
            'Nombre del Cliente :'
        )
        
        self.factura.drawString(220, h - 200, "Detalle de la factura")
        self.factura.line(x1=20, x2=580, y1= h-210, y2= h-210)

        self.dibujar_tabla(h)
        self.factura.showPage()
        self.factura.save()

    def dibujar_tabla(self, h):
        
        data = [[' Codigo', 'Producto', 'Cantidad', 'Precio', 'Subtotal'],
            
        
        ]
        table = Table(data,colWidths=[100,180, 50, 80, 100],)
        table.setStyle(TableStyle(
            [
                ('BOX', (0,0), (-1,-1), 0.25, colors.black),
                ('INNERGRID', (0,0), (-1,-1), 0.25, colors.black),
            ])
        )
        table.wrapOn(self.factura, 100, 100)
        table.drawOn(self.factura, x=50, y=h-260)

   
ReciboFactura()