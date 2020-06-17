from tkinter import *
from tkinter.ttk import Treeview


from modelos import Producto
from funciones_auxiliares import solo_numero, conexion_consulta


class Ventana_Principal():
    
    
    def __init__(self, master):

        self.master = master
        self.menu()                         #Invoca los metodos para 
        self.buscar()                       #crear los widget de cada
        self.ventana_productos()            #Seccion
        self.menu_inferior()
        self.listar_productos()


        self.validatecommand = self.master.register(solo_numero)
        

    def menu(self):
        imagenes = {
            'nuevo' : PhotoImage(file='imagenes/001-mas.png'),
            'editar' : PhotoImage(file='imagenes/002-lapiz.png'),
            'eliminar' : PhotoImage(file='imagenes/003-eliminar.png'),
            'reportes' : PhotoImage(file='imagenes/005-navegador.png'),

        }

        self.labelframe_superior = LabelFrame(self.master, text='Menu Principal',
            width='800', height='100'
        )
        self.labelframe_superior.place(x=2, y=0)

        self.Btnproducto = Button(self.labelframe_superior, image=imagenes['nuevo'],text='Nuevo', command=self.widgets_producto)
        self.Btnproducto.image = imagenes['nuevo']
        self.Btnproducto.place(x=10, y=5)

        self.Btneditar = Button(self.labelframe_superior, image=imagenes['editar'])
        self.Btneditar.image = imagenes['editar']
        self.Btneditar.place(x=90, y=5)

        self.Btninactivar = Button(self.labelframe_superior, image=imagenes['eliminar'])
        self.Btninactivar.image = imagenes['eliminar']
        self.Btninactivar.place(x=170, y=5)

        self.BtnReportes = Button(self.labelframe_superior, image=imagenes['reportes'])
        self.BtnReportes.image = imagenes['reportes']
        self.BtnReportes.place(x=250, y=5)

    def buscar(self):
        self.labelframe_buscador =LabelFrame(self.master, width=800, height=50)
        self.txtBuscar = Entry(self.labelframe_buscador, width=80)
        self.btnBuscar = Button(self.labelframe_buscador, text='Buscar')

        self.labelframe_buscador.place(x=2, y=110)
        self.txtBuscar.place(x=5, y=10)
        self.btnBuscar.place(x=670, y=7)

    def ventana_productos(self):
        self.labelproductos = LabelFrame(self.master, width=800, height=400,
            text='Listado productos'
        )
        self.labelproductos.place(x=2, y=170)
        self.listdetalle = Treeview(self.labelproductos ,
                                    columns = ('#0','#1', '#2'),
                                    height=16
                                    )
        
        self.listdetalle.column('#0', width = 150)
        self.listdetalle.column('#1', width = 450)
        self.listdetalle.column('#2', width = 130)
        self.listdetalle.column('#3', width = 50)
       
        
        self.listdetalle.heading('#0', text = 'ID')
        self.listdetalle.heading('#1', text = 'Producto ')
        self.listdetalle.heading('#2', text = 'Precio Unitario')
        self.listdetalle.heading('#3', text = 'Stock')
        
        self.listdetalle.place(x = 3, y = 20)
        
    def menu_inferior(self):
        self.label_inferior = LabelFrame(self.master, text='Opciones de facturacion',
            width=800, height=100
        )
        self.label_inferior.place(x=3, y=580)
        
    def widgets_producto(self):
        self.nuevo_producto = Toplevel()
        self.nuevo_producto.title('Nuevo producto')
        self.nuevo_producto.geometry('300x450')
        self.nuevo_producto.transient(master=self.master)
        self.nuevo_producto.grab_set()

        #Widgets para añadir un producto

        self.lbCodigo = Label(self.nuevo_producto, text='Codigo :')
        self.lbNombre = Label(self.nuevo_producto, text='Nombre :')
        self.lbPrecio_compra = Label(self.nuevo_producto, text='Precio de compra :')
        self.lbPrecio_venta = Label(self.nuevo_producto, text='Precio de venta :')
        self.lbStock = Label(self.nuevo_producto, text='Inventario :')
        self.estado = Label(self.nuevo_producto, text='Disponible :')
        self.lbError = Label(self.nuevo_producto, text='', foreground="red")
        self.lbError.place(x=100, y=400)

        self.txtCodigo = Entry(self.nuevo_producto, width=30)
        self.txtNombre = Entry(self.nuevo_producto, width=30)
        self.txtPrecio_compra = Entry(self.nuevo_producto, width=30, validate='key',
            validatecommand=(self.validatecommand, "%S")
            )
        self.txtPrecio_venta = Entry(self.nuevo_producto, width=30,validate='key',
            validatecommand=(self.validatecommand, "%S")
        )
        self.txtStock = Entry(self.nuevo_producto, width=30,validate='key',
            validatecommand=(self.validatecommand, "%S")
        )
        self.valor = BooleanVar()
        self.txtEstado = Checkbutton(self.nuevo_producto, variable=self.valor, onvalue=True, offvalue=False)

        self.lbCodigo.place(x=30, y=20)
        self.txtCodigo.place(x=30, y=50 )
        self.lbNombre.place(x=30, y=80)
        self.txtNombre.place(x=30, y=110)
        self.lbPrecio_compra.place(x=30, y=140)
        self.txtPrecio_compra.place(x=30, y=170)
        self.lbPrecio_venta.place(x=30, y=200)
        self.txtPrecio_venta.place(x=30, y=230)
        self.lbStock.place(x=30, y=260)
        self.txtStock.place(x=30, y=290)
        self.estado.place(x=30, y=320)
        self.txtEstado.place(x=100, y=320)

        #Botones 

        self.BtnGuardar = Button(self.nuevo_producto, text='Guardar', command=self.crear_producto)
        self.BtnGuardar.place(x=110, y=360)


    def crear_producto(self):
        producto = Producto()

        producto.id = self.txtCodigo.get()
        producto.nombre = self.txtNombre.get()
        producto.precio_compra = float(self.txtPrecio_compra.get())
        producto.precio_venta = float( self.txtPrecio_venta.get())
        producto.stock = int(self.txtStock.get())
        producto.estado = self.valor.get()

        if producto.validar():
            if producto.guardar():
                self.listar_productos()
                self.nuevo_producto.destroy()
            
        else:
            self.lbError['text'] = 'Datos erroneos'


    def actualizar_producto(self):
        pass

    def inactivar_producto(self):
        pass


    def listar_productos(self):
        registros = self.listdetalle.get_children()
        for items in registros:
            self.listdetalle.delete(items)

        
        consulta = 'SELECT * FROM producto WHERE estado=1'
        productos_qs = conexion_consulta(consulta, parametros=())

        for element in productos_qs:
             self.listdetalle.insert('', 0, text = element[0], values = (element[1],
                                                                         element[3],
                                                                         element[4],
                                                                        
                                                                         )
                                     )
        

        
        
            
        





    
    