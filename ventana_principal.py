from tkinter import *
from tkinter.ttk import Treeview, Combobox


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
        self.widget_facturacion()

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

        self.Btneditar = Button(self.labelframe_superior, image=imagenes['editar'], command=self.widget_buscar)
        self.Btneditar.image = imagenes['editar']
        self.Btneditar.place(x=90, y=5)

        self.Btninactivar = Button(self.labelframe_superior, image=imagenes['eliminar'], command=self.inactivar_producto)
        self.Btninactivar.image = imagenes['eliminar']
        self.Btninactivar.place(x=170, y=5)

        self.BtnReportes = Button(self.labelframe_superior, image=imagenes['reportes'], command=self.listar_productos)
        self.BtnReportes.image = imagenes['reportes']
        self.BtnReportes.place(x=250, y=5)

    def buscar(self):
        self.labelframe_buscador =LabelFrame(self.master, width=800, height=50)
        self.txtBuscar = Entry(self.labelframe_buscador, width=80)
        self.btnBuscar = Button(self.labelframe_buscador, text='Buscar', command=self.buscar_productos)

        self.labelframe_buscador.place(x=2, y=110)
        self.txtBuscar.place(x=5, y=10)
        self.btnBuscar.place(x=670, y=7)

    def buscar_productos(self):
        
        varia = str(self.txtBuscar.get())
        consulta = "SELECT * FROM producto WHERE nombre LIKE '%' || ? ||'%'"
        parametros = [varia]

        producto_qs = conexion_consulta(consulta, parametros)
        
        if producto_qs:
            p = producto_qs
            self.llenar_registros(p)

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
        self.listdetalle.bind('<<TreeviewSelect>>', self.widget_agregar_producto_factura)
        
    def menu_inferior(self):
        self.label_inferior = LabelFrame(self.master, text='Opciones de facturacion',
            width=800, height=110
        )
        self.label_inferior.place(x=3, y=580)

        images_inferior = {
            'new' : PhotoImage(file='imagenes/003-new-window.png'),
            'block' : PhotoImage(file='imagenes/002-padlock.png'),
            'cancelar' : PhotoImage(file='imagenes/004-forbidden.png')
        }

        self.BtnNuevo = Button(self.label_inferior,
            text='Nueva venta', image = images_inferior['new'],  compound=LEFT
    
            
        )
        self.BtnNuevo.image=images_inferior['new']

        self.BtnCancelar = Button(self.label_inferior, text='Cancelar',
            image=images_inferior['cancelar'],  compound=LEFT
        
        )
        self.BtnCancelar.image = images_inferior['cancelar']
        self.BtnBloquear = Button(self.label_inferior, text='Bloquear sistema',
            image=images_inferior['block'], compound=LEFT
        )
        self.BtnBloquear.images = images_inferior['block']
        
        self.BtnNuevo.place(x=3, y=2)
        self.BtnBloquear.place(x=200, y=2)
        self.BtnCancelar.place(x=430, y=2)


    def widget_buscar(self):
        self.VtBuscar = Toplevel()
        self.VtBuscar.geometry('270x200')
        self.VtBuscar.title('Editar u Eliminar')
        self.VtBuscar.grab_set()
        self.VtBuscar.transient(master=self.master)

        self.lbCodigoED = Label(self.VtBuscar, text='Codigo del producto')
        self.txtCodigoED = Entry(self.VtBuscar, width=30)

        self.btnED = Button(self.VtBuscar, text='Buscar', command=self.actualizar_producto)
        self.btnED.place(x=90, y=100)

        self.lbCodigoED.place(x=60, y=25)
        self.txtCodigoED.place(x=10, y=50)

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

        self.BtnGuardar = Button(self.nuevo_producto, text='Guardar', command= lambda : self.crear_o_editar_producto(1))
        self.BtnGuardar.place(x=110, y=360)

    def widget_facturacion(self):
        self.label_facturacion = LabelFrame(self.master, text='Facturacion', width=480, height=687)
        self.label_facturacion.place(x=810, y=1)

        self.titulo_fact = Label(self.label_facturacion, text='Facturacion de productos ')
        self.titulo_fact.place(x=140, y=20)

        self.lb_cod_factura = Label(self.label_facturacion, text='Codigo de factura :'
        )
        self.lb_cod_factura.place(x=10, y=60)

        self.txt_cod_factura = Entry(self.label_facturacion, state='readonly')
        self.txt_cod_factura.place(x=10, y=80)

        self.lb_num_venta = Label(self.label_facturacion, text='# Venta :')
        self.txt_num_venta = Entry(self.label_facturacion, state='readonly')
        self.lb_num_venta.place(x=220, y=60)
        self.txt_num_venta.place(x=220, y=80)

        self.lb_cliente = Label(self.label_facturacion, text='Cliente :')
        self.lb_cliente.place(x=10, y=110)
        self.cliente = Combobox(self.label_facturacion, state='readonly', width=45)
        self.cliente.place(x=10, y=130)

        self.detalle_factura = Treeview(self.label_facturacion,
            columns=('#0','#1','#2',), height=16
        )
        self.detalle_factura.place(x=10, y=190)
        self.detalle_factura.column('#0', width = 180)
        self.detalle_factura.column('#1', width = 80)
        self.detalle_factura.column('#2', width = 100)
        self.detalle_factura.column('#3', width = 100)
        

        self.detalle_factura.heading('#0', text='Producto')
        self.detalle_factura.heading('#1', text='Cantidad')
        self.detalle_factura.heading('#2', text='P. Unit')
        self.detalle_factura.heading('#3',text='Subtotal')

        self.lb_detalle = Label(self.label_facturacion, text='Detalle de factura')
        self.lb_detalle.place(x=150, y=160)

        self.lb_total = Label(self.label_facturacion, text='TOTAL :')
        self.lb_total.place(x=230, y=550)
        self.tx_total = Entry(self.label_facturacion, state='readonly')
        self.tx_total.place(x=300, y=550)

        self.lb_pago = Label(self.label_facturacion, text='PAGO :')
        self.txt_pago = Entry(self.label_facturacion, )
        self.lb_pago.place(x=230, y=580)
        self.txt_pago.place(x=300, y=580)

        self.lb_cambio = Label(self.label_facturacion, text='Cambio')
        self.tx_cambio = Entry(self.label_facturacion, state='readonly')
        self.lb_cambio.place(x=230, y=610)
        self.tx_cambio.place(x=300, y=610)

        self.lb_moneda = Label(self.label_facturacion, text='Moneda :')
        self.lb_moneda.place(x=10, y=550)
        self.tipo_moneda = Combobox(self.label_facturacion, values=['$-USD', 'CORD-NIO '], width=10)
        self.tipo_moneda.place(x=80, y=550)

        imagen_facturar = PhotoImage(file='imagenes/comprobar.png')
        self.BtnFacturar = Button(self.label_facturacion, text='FACTURAR ', image=imagen_facturar, compound=LEFT)
        self.BtnFacturar.image = imagen_facturar
        self.BtnFacturar.place(x=10, y=590)
       
    def agregar_producto_factura(self):
        pass

    def widget_agregar_producto_factura(self, event):
        self.producto_factura = Toplevel()
        self.producto_factura.geometry('500x300')
       
        self.producto_factura.transient(master=self.master)
        self.producto_factura.grab_set()

    def crear_o_editar_producto(self, op):
        producto = Producto()

        producto.id = self.txtCodigo.get()
        producto.nombre = self.txtNombre.get()
        producto.precio_compra = float(self.txtPrecio_compra.get())
        producto.precio_venta = float( self.txtPrecio_venta.get())
        producto.stock = int(self.txtStock.get())
        producto.estado = self.valor.get()

        if producto.validar():
            if op == 1:
                if producto.guardar():
                    self.listar_productos()
                    self.nuevo_producto.destroy()
            elif op==2:
                
                print('OPCION |1')
                if producto.actualizar():
                    self.nuevo_producto.destroy()
                    self.listar_productos()

            
        else:
            self.lbError['text'] = 'Datos erroneos'

    def actualizar_producto(self):
        producto = Producto()
        producto.id = self.txtCodigoED.get()

        producto_editar = producto.seleccionar()

        if producto_editar:
            self.VtBuscar.destroy()

            for producto_edit in producto_editar:

                self.widgets_producto()
                self.nuevo_producto.title('Editar producto')
                self.txtCodigo.insert(0,producto_edit[0])
                self.txtNombre.insert(0,producto_edit[1])
                self.txtPrecio_compra['validate']='none'
                self.txtPrecio_venta['validate']='none'

                self.txtPrecio_compra.insert(END,float(producto_edit[2]) )
                self.txtPrecio_compra['validate']='key'
                self.txtPrecio_venta.insert(END,float(producto_edit[3]) )
                self.txtPrecio_compra['validate']='key'
                self.txtStock.insert(0,(producto_edit[4]))
                self.valor.set(producto_edit[5])
                
                self.BtnGuardar['command']=lambda: self.crear_o_editar_producto(2)
                
    def inactivar_producto(self):

        id = self.listdetalle.focus()
        elementos = self.listdetalle.item(id)
        producto = Producto()
        producto.id = elementos['text']
        producto.estado = False

        if producto.inactivar():
            self.listar_productos()

    def listar_productos(self):
        consulta = 'SELECT * FROM producto WHERE estado=1'
        productos_qs = conexion_consulta(consulta, parametros=())
        p = productos_qs
        self.llenar_registros(p)
        
    def llenar_registros(self, p):
        registros = self.listdetalle.get_children()
        p = p
        for items in registros:
            self.listdetalle.delete(items)

        for element in p:
             self.listdetalle.insert('', 0, text = element[0], values = (element[1],
                                                                         element[3],
                                                                         element[4],
                                                                        )
                                     )

        

        
        
            
        





    
    