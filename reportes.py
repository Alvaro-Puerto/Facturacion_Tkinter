from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
from reportlab.lib import colors
from reportlab.platypus import Table, TableStyle
from datetime import datetime
import os



class ReciboFactura():
    '''Objeto para crear un recibo asociado a una factura'''
    
    def __init__(self):
        '''Inicializa el titulo de la factura'''
        fecha = datetime.now()
        titulo = 'Factura-{}-{}:{}:{}--{}:{}:{}.pdf'.format(
            'XXX-XXX-XXX', fecha.day, fecha.month, fecha.year,
            fecha.hour, fecha.minute, fecha.second
        )
        nombre_pdf = os.path.join('Facturas/',titulo)
        self.factura = canvas.Canvas(nombre_pdf, pagesize=A4)
        
    def crear_esqueleto(self):
        _, h = A4
        self.factura
        self.factura.drawString(240, h - 50, "FACTURA")
        self.factura.line(x1=20, x2=580, y1= h-70, y2= h-70)

        self.factura.drawString(60, h- 100,
            'Id Factura : '
        )
        self.factura.drawString(420, h- 100,
            'Fecha : '
        )
        self.factura.drawString(60, h- 140,
            'Nombre del Cliente :'
        )
        
        self.factura.drawString(220, h - 200, "Detalle de la factura")
        self.factura.line(x1=20, x2=580, y1= h-210, y2= h-210)

        
        

    def dibujar_tabla(self, lista_productos):
        _, h = A4
        centinela = 0
        data = [[' Codigo', 'Producto', 'Cantidad', 'Precio', 'Subtotal'],
        ]
        for productos in lista_productos:
            lista = []
            lista.append(str(productos.id))
            lista.append(str(productos.nombre))
            lista.append(str(productos.cantidad))
            lista.append(str(productos.precio_venta))
            lista.append(str(productos.sub_total))
            data.append(lista)
            centinela = centinela+20
   
        table = Table(data,colWidths=[100,180, 50, 80, 100],)
        table.setStyle(TableStyle(
            [
                ('BOX', (0,0), (-1,-1), 0.25, colors.black),
                ('INNERGRID', (0,0), (-1,-1), 0.25, colors.black),
            ])
        )

        punto_separacion = h-260-centinela
        table.wrapOn(self.factura, 100, 100)
        table.drawOn(self.factura, x=50, y=h-260-centinela)

        self.factura.drawString(430, punto_separacion-20,
            'Total : '
        )
        self.factura.drawString(430, punto_separacion-40,
            'Pago : '
        )
        self.factura.drawString(418, punto_separacion-60,
            'Cambio : '
        )
        return punto_separacion
        


    def detalles_factura(self, object):
        obj_factura = object
        punto = self.dibujar_tabla(obj_factura.lista_productos)
        self.crear_esqueleto()
        self.llenar_factura(obj_factura, punto)

    def llenar_factura(self, object, punto):
        w, h = A4

        self.factura.drawString(140, h- 100,
            str(object.id_factura)
        )
        self.factura.drawString(180, h- 140,
            str(object.id_cliente)
        )
        self.factura.drawString(480, punto-20,
            str(object.total)
        )
        self.factura.drawString(480, punto-40,
            str(object.pago)
        )
        self.factura.drawString(480, punto-60,
            str(object.cambio)
        )

    def save(self):
        self.factura.showPage()
        self.factura.save()

    def __del__(self):
        pass