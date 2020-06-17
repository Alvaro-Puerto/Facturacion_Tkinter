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

    def eliminar(self):
        pass

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

        self.cantidad = 0


    def calcular_subtotal(self):
        pass



    


    