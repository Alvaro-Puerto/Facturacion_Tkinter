from tkinter import Tk

from ventana_principal import Ventana_Principal

if __name__ == "__main__":
    root = Tk()
    root.title('Sistema Facturacion')
    root.geometry('1300x700')
    Ventana_Principal(root)
    root.mainloop()