from tkinter import *
from tkinter.ttk import Treeview, Combobox
from datetime import datetime

from modelos import Producto, ProductoFacturar, Factura, Cliente
from funciones_auxiliares import solo_numero, conexion_consulta
from reportes import ReciboFactura

class Ventana_Principal():
    
    
    def __init__(self, master):

        self.master = master
        self.menu()                         #Invoca los metodos para 
        self.buscar()                       #crear los widget de cada
        self.ventana_productos()            #Seccion
        self.menu_inferior()
        self.listar_productos()
        #self.widget_facturacion()
        

        self.factura = Factura()
        #self.nueva_factura()

        self.validatecommand = self.master.register(solo_numero)

        self.validate_subtotal = self.master.register(self.mostrar_sub_total)
      
    def menu(self):
        imagenes = {
            'nuevo' : PhotoImage(file='imagenes/001-mas.png'),
            'editar' : PhotoImage(file='imagenes/002-lapiz.png'),
            'eliminar' : PhotoImage(file='imagenes/003-eliminar.png'),
            'reportes' : PhotoImage(file='imagenes/004-actualizar.png'),

        }
       
        self.labelframe_superior = LabelFrame(self.master, 
            width='800', height='100'
        )
        self.labelframe_superior.place(x=2, y=0)

        self.label_producto = LabelFrame(self.labelframe_superior, text='Opciones del inventario',
            width=323, height=90
        )
        self.label_producto.place(x=2, y=1)

        self.Btnproducto = Button(self.label_producto, image=imagenes['nuevo'],text='Nuevo', 
            command=self.widgets_producto, compound=TOP
        )
        self.Btnproducto.image = imagenes['nuevo']
        self.Btnproducto.place(x=5, y=5)

        self.Btneditar = Button(self.label_producto, image=imagenes['editar'], 
            command=self.widget_buscar, text='Editar', compound=TOP
        )
        self.Btneditar.image = imagenes['editar']
        self.Btneditar.place(x=74, y=5)

        self.Btninactivar = Button(self.label_producto, image=imagenes['eliminar'],
            command=self.inactivar_producto, text='Inactivar', compound=TOP
        )
        self.Btninactivar.image = imagenes['eliminar']
        self.Btninactivar.place(x=139, y=5)

        self.BtnReportes = Button(self.label_producto, image=imagenes['reportes'],
            command=self.listar_productos, text='Refrescar', compound=TOP
        )
        self.BtnReportes.image = imagenes['reportes']
        self.BtnReportes.place(x=223, y=5)

        self.label_conf_reporte = LabelFrame(self.labelframe_superior, text='Configuracion',
            width=128, height=90
        )
        self.label_conf_reporte.place(x=327, y=1)

        images_config = {
            'config' : PhotoImage(file='imagenes/002-configuraciones.png'),
        }

        self.btn_config = Button(self.label_conf_reporte, text='Configuracion',
            image=images_config['config'], compound=TOP, height=45, 
        )
        self.btn_config.image = images_config['config']
        self.btn_config.place(x=2, y=5)

        self.label_reportes = LabelFrame(self.labelframe_superior, text='Reportes',
            width=200,  height=90
        )
        self.label_reportes.place(x=457, y=1)


        fecha = datetime.now()
        fecha_conv = '{} - {} - {}'.format(fecha.day, fecha.month, fecha.year)

        self.lb_fecha = Label(self.labelframe_superior ,text='FECHA :')
        self.lb_fecha.place(x=640, y=5)

        self.lb_fecha_actual = Label(self.labelframe_superior, text= fecha_conv)
        self.lb_fecha_actual.place(x=700, y=5)

    def buscar(self):
        self.labelframe_buscador =LabelFrame(self.master, width=800, height=50)
        self.txtBuscar = Entry(self.labelframe_buscador, width=80)
        self.txtBuscar.bind('<Return>', self.buscar_productos)
        self.btnBuscar = Button(self.labelframe_buscador, text='Buscar', command=lambda: self.buscar_productos(1))

        self.labelframe_buscador.place(x=2, y=110)
        self.txtBuscar.place(x=5, y=10)
        self.btnBuscar.place(x=670, y=7)

    def buscar_productos(self, event):
        
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
            text='Nueva venta', image = images_inferior['new'],  compound=LEFT,
            command=self.nueva_factura
        )
        self.BtnNuevo.image=images_inferior['new']

        self.BtnCancelar = Button(self.label_inferior, text='Cancelar',
            image=images_inferior['cancelar'],  compound=LEFT
        
        )
        self.BtnCancelar.image = images_inferior['cancelar']
        self.BtnBloquear = Button(self.label_inferior, text='Bloquear sistema',
            image=images_inferior['block'], compound=LEFT, command=self.bloquear
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

        self.codigo_factura = StringVar()
        self.txt_cod_factura = Entry(self.label_facturacion, state='readonly', textvariable=self.codigo_factura)
        self.txt_cod_factura.place(x=10, y=80)

        self.lb_num_venta = Label(self.label_facturacion, text='# Venta :')
        self.txt_num_venta = Entry(self.label_facturacion, state='readonly')
        self.lb_num_venta.place(x=220, y=60)
        self.txt_num_venta.place(x=220, y=80)

        self.lb_cliente = Label(self.label_facturacion, text='Cliente :')
        self.lb_cliente.place(x=10, y=110)
        self.cliente = Combobox(self.label_facturacion, state='readonly', width=45)
        self.cliente.place(x=10, y=130)

        self.btn_add_clte = Button(self.label_facturacion, text='Nuevo',
            command=self.widget_cliente
        )
        self.btn_add_clte.place(x=390, y=125)

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


        self.total = StringVar()
        self.lb_total = Label(self.label_facturacion, text='TOTAL :')
        self.lb_total.place(x=230, y=550)
        self.tx_total = Entry(self.label_facturacion, state='readonly', textvariable=self.total)
        self.tx_total.place(x=300, y=550)

        self.lb_pago = Label(self.label_facturacion, text='PAGO :')
        self.txt_pago = Entry(self.label_facturacion,
           validate='key', validatecommand=(self.validatecommand, "%S")
         )
        self.lb_pago.place(x=230, y=580)
        self.txt_pago.place(x=300, y=580)

        self.cambio = StringVar()
        self.lb_cambio = Label(self.label_facturacion, text='Cambio')
        self.tx_cambio = Entry(self.label_facturacion, state='readonly', textvariable=self.cambio)
        self.lb_cambio.place(x=230, y=610)
        self.tx_cambio.place(x=300, y=610)
        self.txt_pago.bind('<Return>',self.calcular_cambio)

        self.lb_moneda = Label(self.label_facturacion, text='Moneda :')
        self.lb_moneda.place(x=10, y=550)
        self.tipo_moneda = Combobox(self.label_facturacion, values=['$-USD', 'CORD-NIO '], width=10)
        self.tipo_moneda.place(x=80, y=550)

        imagen_facturar = PhotoImage(file='imagenes/comprobar.png')
        self.BtnFacturar = Button(self.label_facturacion, text='FACTURAR ', image=imagen_facturar, compound=LEFT,
            width=180, height=50, command=self.guardar_factura
        )
        self.BtnFacturar.image = imagen_facturar
        self.BtnFacturar.place(x=10, y=590)
       
    def agregar_producto_factura(self,):
        producto_factura = ProductoFacturar()
        producto_factura.id_factura = self.codigo_factura.get()
        producto_factura.id = self.codigo.get()
        producto_factura.nombre = self.nombre.get()
        producto_factura.precio_venta = float(self.precio.get())
        producto_factura.cantidad = int(self.txt_cantidad.get())
        producto_factura.sub_total = str(producto_factura.calcular_subtotal())

        id = self.validar_producto_existente_factura(producto_factura.nombre)

        if id:
            self.factura.remover_producto(producto_factura.nombre)
            producto_facturar_edit = self.detalle_factura.item(id)
            producto_viejo_valores = producto_facturar_edit['values']
            producto_factura_cant_ant = int(producto_viejo_valores[0])
            self.detalle_factura.delete(id)
            nueva_cantidad = int(producto_factura.cantidad) + int(producto_factura_cant_ant)
            producto_factura.cantidad = nueva_cantidad
            producto_factura.sub_total = str(producto_factura.calcular_subtotal())
            self.detalle_factura.insert('', 0, text = producto_factura.nombre, values=(
                producto_factura.cantidad,producto_factura.precio_venta, producto_factura.sub_total), iid=id)
            
        else:
            self.detalle_factura.insert('', 0, text = producto_factura.nombre, values=(
                producto_factura.cantidad,producto_factura.precio_venta, producto_factura.sub_total)
                                         )
        self.factura.lista_productos.append(producto_factura)

        self.producto_factura.destroy()

        
        self.total.set(str(self.factura.calcular_total()))
        
    def mostrar_sub_total(self, event):
        sub_total = float(self.precio.get()) *  int(self.txt_cantidad.get())

        self.sub_total.set(str(sub_total))
       
    def widget_agregar_producto_factura(self, event):

        id = self.listdetalle.focus()
        producto_focus = self.listdetalle.item(id)
        lista = []
        for atributos in producto_focus['values']:
            lista.append(atributos)
            

        self.producto_factura = Toplevel()
        self.producto_factura.geometry('350x300')
        self.producto_factura.wait_visibility()
        self.producto_factura.grab_set()
        self.producto_factura.transient(master=self.master)
        
        self.lb_cod_producto =  Label(self.producto_factura, text='Codigo producto   : ')
        self.lb_cod_producto.place(x=20, y=30)

        self.codigo = StringVar()
        self.tx_codigo = Entry(self.producto_factura, state='readonly', textvariable=self.codigo).place(x=150, y=20)
        self.codigo.set(producto_focus['text'])
        
       
        self.lb_nb_producto = Label(self.producto_factura, text='Nombre producto : ',)
        self.lb_nb_producto.place(x=20, y=70)

        
        self.nombre = StringVar()
        self.txt_nb_producto = Entry(self.producto_factura, state='readonly', textvariable=self.nombre).place(x=150, y=70)
        self.nombre.set(lista[0])
        
        self.lb_precio = Label(self.producto_factura, text='Precio producto    : ')
        self.lb_precio.place(x=20, y=110)

        self.precio = StringVar()
        
        self.txt_precio = Entry(self.producto_factura, state='readonly', textvariable=self.precio).place(x=150, y=110)
        self.precio.set(lista[1])

        self.lb_cantidad = Label(self.producto_factura, text='Cantidad          :')
        self.lb_cantidad.place(x=20, y=150) 
        self.cantidad = StringVar()
        self.cantidad.set('1')
        self.txt_cantidad = Entry(self.producto_factura, textvariable=self.cantidad,
            validate='key', validatecommand=(self.validatecommand, "%S")
        )
        self.txt_cantidad.bind('<Return>', self.mostrar_sub_total)
       
        self.txt_cantidad.place(x=150, y=150)

        self.lb_sub_total = Label(self.producto_factura, text='Sub-total        : ')
        self.lb_sub_total.place(x=20, y=190)

        self.sub_total = StringVar()
        self.txt_sub_total = Entry(self.producto_factura, state='readonly', textvariable=self.sub_total,
          
        )
        self.txt_sub_total.place(x=150, y=190)


        self.btAdd = Button(self.producto_factura, text='Añadir a la factura', command=(self.agregar_producto_factura))
        self.btAdd.place(x=120, y=240)

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
        consulta = 'SELECT * FROM producto WHERE estado=1 AND inventario >0'
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
        self.listdetalle.bind('<Double-1>', self.widget_agregar_producto_factura)

    def nueva_factura(self):
        #Limpiar productos en facturas 
        self.widget_facturacion()
        self.master.geometry('1300x700')
        id_detalle = self.detalle_factura.get_children()
        for item in id_detalle:
            self.detalle_factura.delete(item)

        self.total.set('')
        self.tipo_moneda.current(1)
        self.cambio.set('')
        self.txt_pago.delete(0, END)

        nuevo_codigo_fact = self.factura.obtener_numero_factura()
        self.codigo_factura.set(nuevo_codigo_fact)

        lista_clientes = self.obtener_clientes()

        for clientes in lista_clientes:
            self.cliente['values'] = str(clientes[0]) + '_' + str(clientes[1])
        
        self.cliente.current(0)

    def validar_producto_existente_factura(self, nombre):
        lista_producto = self.detalle_factura.get_children()
        
        for productos in lista_producto[::-1]:
            producto_agregado = self.detalle_factura.item(productos)
            if nombre == producto_agregado['text']:
                return productos
            else:
                return False

    def calcular_cambio(self, event):
        billete = float(self.txt_pago.get())
        cambio =   billete - float(self.total.get())
        self.cambio.set(str(cambio))

    def obtener_clientes(self):
        
        consulta = 'SELECT * FROM Cliente '
        return conexion_consulta(consulta,parametros=())
        
    def guardar_factura(self):
        if self.txt_pago != '':
            factura = self.factura

            for productos_factura in self.factura.lista_productos:
                productos_factura.guardar()
            
            factura.id_factura = self.codigo_factura.get()
            id_cliente = self.cliente.get()
            lista_cliente = id_cliente.split('_')
            factura.id_cliente = lista_cliente[0]
            fecha = datetime.now()
            factura.fecha_creacion = '{}-{}-{}'.format(fecha.day, fecha.month, fecha.year)
            factura.hora_creacion = '{}:{}'.format(fecha.hour, fecha.day)
            factura.pago = self.txt_pago.get()
            factura.cambio = self.cambio.get()
            recibo = ReciboFactura()
            recibo.detalles_factura(factura)
            recibo.save()
            recibo.__del__()

            factura.guardar()
            factura.lista_productos.clear()
            self.nueva_factura()
            self.listar_productos()
        else:
            pass
       
       
        pass
        
    def bloquear(self):
        self.label_facturacion.place_forget()
        self.master.geometry('810x700')

    def widget_cliente(self):
        self.ventana = Toplevel()
        self.ventana.title = 'Nuevo cliente'
        self.ventana.wait_visibility()

     
        self.ventana.grab_set()
        
        self.ventana.transient(master=self.master)
        self.ventana.geometry('200x250')

        lbl_codigo = Label(self.ventana, text='Codigo del cliente :').place(x=10, y=10)
        lbl_nombre = Label(self.ventana, text='Nombre del cliente :').place(x=10, y=50)
        lbl_direccion = Label(self.ventana, text='Direccion del cliente :').place(x=10, y=90)

        self.txt_codigo = Entry(self.ventana)
        self.txt_codigo.place(x=10, y=30)
        self.txt_nombre = Entry(self.ventana)
        self.txt_nombre.place(x=10, y=70)
        self.txt_direccion = Entry(self.ventana)
        self.txt_direccion.place(x=10, y=110)

        self.btn_guardar = Button(self.ventana, text='Guardar', command=self.guardar_cliente).place(x=60, y=150)

    def guardar_cliente(self):
        cliente = Cliente()
        cliente.id = self.txt_codigo.get()
        cliente.nombre = self.txt_nombre.get()
        cliente.direccion = self.txt_direccion.get()

        cliente.guardar()
        self.ventana.destroy()
        self.obtener_clientes()

    
    