from funciones_auxiliares import conexion_consulta

class Producto():
  
    def __init__(self, *args, **kwargs):

        self.id = None
        self.nombre = None
        self.precio_compra = None
        self.precio_venta = None
        self.stock = None
        self.estado = None

    def seleccionar(self):
        consulta = 'SELECT * FROM producto WHERE id=?'
        parametros = [self.id]
        return conexion_consulta(consulta, parametros)


    def guardar(self):
        consulta = 'INSERT INTO producto VALUES(?, ?, ?, ?, ?, ?)'
        parametros = [(parametro[1]) for parametro in self.__dict__.items()]
        
        return conexion_consulta(consulta, parametros)

    def actualizar(self):
        consulta = '''UPDATE producto set id=?, nombre=?, precio_compra=?,
                    precio_venta=?, inventario=?, estado=? WHERE id=?
                    '''
        parametros = [(parametro[1]) for parametro in self.__dict__.items()]
        parametros.append(self.id)
        print(parametros)

        return conexion_consulta(consulta, parametros)


    def inactivar(self):
        consulta = 'UPDATE producto set estado=? WHERE id=?'
        parametros = [self.estado, self.id]
        return conexion_consulta(consulta, parametros)

    def validar(self): # Metodo que valida que los inputs no ingrese valores nulos
        atributos = self.__dict__.items()
        centinela = True

        for datos in atributos:
            if datos[1] is '':
                centinela = False
                break
            elif datos[1] is not None:
                centinela = True

        return centinela


class ProductoFacturar(Producto):
    
    def __init__(self, *args, **kwargs):
        super(Producto, self).__init__(*args, **kwargs)
        self.id_factura = ''
        self.cantidad = 0
        self.sub_total = 0


    def calcular_subtotal(self):
        return self.precio_venta * self.cantidad
    
    def convertir_dic(self):
        return {'codigo':self.id, 
                'nombre':self.nombre,
                'precio_venta':self.precio_venta,
                'cantidad':self.cantidad,
                'sub-total':self.sub_total
                }
    
    def guardar(self):
        consulta = 'INSERT INTO detallefact VALUES(?, ?, ?, ?, ?)'
        parametros=[self.id_factura, self.id, self.precio_venta, self.cantidad, self.sub_total]
        conexion_consulta(consulta, parametros)
        self.reducir_existencia()

    def reducir_existencia(self):
        producto_reducir = self.seleccionar()
        for producto_reducido in producto_reducir:
            stock = int(producto_reducido[4])
        
        nuevo_stock = stock-self.cantidad

        consulta = 'UPDATE producto set inventario=? WHERE id=?'
        parametros = [nuevo_stock, self.id]
        conexion_consulta(consulta, parametros)



class Factura():
    
    def __init__(self, *args, **kwargs):
        super(Factura, self).__init__(*args, **kwargs)

        self.id_factura = ''
        self.id_cliente = ''
        self.fecha_creacion = ''
        self.hora_creacion = ''
        self.lista_productos = []
        self.total = 0
        self.pago = 0
        self.cambio = 0
        
    

    def guardar(self):
        consulta = 'INSERT INTO Factura VALUES(?, ?, ?, ?, ?, ?, ?)'
        parametros=[
            self.id_factura, self.id_cliente, self.fecha_creacion,
            self.hora_creacion, self.total, self.pago, self.cambio
        ]
        conexion_consulta(consulta, parametros)
    
    def obtener_numero_factura(self):
        consulta = 'SELECT id_factura FROM Factura ORDER BY id_factura DESC LIMIT 1'
        codigo = conexion_consulta(consulta, parametros=())

        for identifacdor in codigo:
            nuevo_codigo = identifacdor[0]
        
        dividiendo_digitos = nuevo_codigo.split("-")
        nuevo_codigo = int(dividiendo_digitos[1]) + 1

        return dividiendo_digitos[0] + '-' + str(nuevo_codigo)

    def remover_producto(self, nombre):
        for lista_productos in self.lista_productos:
            if nombre == lista_productos.nombre:
                self.lista_productos.remove(lista_productos)
        return True


    def calcular_total(self):
        total = 0
        for sub_total in self.lista_productos:
            total = float(sub_total.calcular_subtotal()) + total
        self.total = total
        return total
    
    


    