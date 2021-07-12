from tkinter import ttk
from tkinter import *

import sqlite3

class product:
    NombreBaseDatos = "BaseDatos.db"
    def __init__(self,window):
        self.wind = window
        self.wind.title("Administración de productos ")
        frame = LabelFrame(self.wind,text="Ingresa nuevo producto")
        frame.grid(row=0,column=0,columnspan=3,pady=20)
        #INgresar Nombre del producto
        Label(frame,text="Nombre: ").grid(row=1,column=0)
        self.name = Entry(frame)
        self.name.focus()
        self.name.grid(row=1,column=1)
        #INgresar precio del producto
        Label(frame,text="Precio").grid(row=2,column=0)
        self.precio = Entry(frame)
        self.precio.grid(row=2,column=1)
        #Boton para agregar el producto
        ttk.Button(frame, text="Guadar", command=self.AgregarProductos).grid(row=3,columnspan=2,sticky=W+E)
        #Mensaje de guadardo
        self.mensaje = Label(text= "", fg = "green")
        self.mensaje.grid(row=3, column=0,columnspan=2,sticky=W+E)
      
        estilo = ttk.Style()
        estilo.configure("mystyle.Treeview", highlightthickness=0,
        bd=0, background='red', font=('Lucida Console', 9))
        #tabla
        self.tree = ttk.Treeview(height=10,columns=2,style="mystyle.Treeview")
        self.tree.grid(row=4,column=0,columnspan=2)
        self.tree.heading("#0",text="Nombre",anchor = CENTER)
        self.tree.heading("#1",text="Precio",anchor = CENTER)
        ttk.Button(text="Eliminar",command=self.EliminarProductos).grid(row=5,column=0,sticky=W+E)
        ttk.Button(text="Editar",command=self.EditarPorductos).grid(row=5,column=1,sticky=W+E)


        
        
        self.obtenerLosProductos() #LLENAR FIlas
    # BASE DE DATOS
    def EjecutarConsulta(self,consulta,parametros = () ):
        with sqlite3.connect(self.NombreBaseDatos) as conexion:
            cursor = conexion.cursor()
            resultado = cursor.execute(consulta,parametros)
            conexion.commit()
        return resultado
    def obtenerLosProductos(self):
        #LIMPIANDO LA TABLA
        records = self.tree.get_children() #OBTENEMOS LOS DATOS QUE ESTAN DENTRO DE LA TABLA DE LA BASE DE DATOS
        for element in records:
            self.tree.delete(element)
        consulta = "SELECT * FROM products ORDER BY Nombre DESC"
        DatosObtenidosConsulta = self.EjecutarConsulta(consulta)
        for fila in DatosObtenidosConsulta:
            self.tree.insert("",0,text=fila[1],values = fila[2] )
    def ValidarProductosIngresados(self):
        return len(self.name.get()) != 0 and len(self.precio.get()) !=0 #Si AMBOS ELEMENTOS NO ESTAN VACIOS RETORNA UN TRUE
    def AgregarProductos(self):
        if self.ValidarProductosIngresados() == True:
            consulta = "INSERT INTO products VALUES(NULL,?,?)"
            parametros = (self.name.get(),self.precio.get())
            self.EjecutarConsulta(consulta,parametros)
            self.mensaje["fg"] = "green"
            self.mensaje["text"] = "Producto {} se agregó con éxito".format(self.name.get())
            self.name.delete(0, END)
            self.precio.delete(0,END)
        else:
            self.mensaje["fg"] = "red"
            self.mensaje["text"] = "ATENCIÓN: Nombre y precio son requeridos"
            self.name.delete(0, END)
            self.precio.delete(0,END)
        self.obtenerLosProductos()
    
    def EliminarProductos(self):
        self.mensaje["text"] = ""
        try:
            self.tree.item(self.tree.selection())["text"][0]
        except IndexError as e:
            self.mensaje["fg"] = "red"
            self.mensaje["text"] = "Por favor seleccione un producto"
            return
        self.mensaje["text"] = ""
        nombreDelProducto = self.tree.item(self.tree.selection())["text"]
        consulta = "DELETE FROM products WHERE Nombre = ?"
        self.EjecutarConsulta(consulta, (nombreDelProducto, ))
        self.mensaje["fg"] = "green"
        self.mensaje["text"] = "Se eliminó el producto {}".format(nombreDelProducto)
        self.obtenerLosProductos()

    def EditarDatos(self, nuevo_nombre,nombre_viejo,nuevo_precio,precio_viejo):
        consulta = "UPDATE products SET Nombre = ?, Precio = ? WHERE Nombre = ? AND Precio = ?"
        parametros = (nuevo_nombre,nuevo_precio,nombre_viejo,precio_viejo)
        self.EjecutarConsulta(consulta,parametros)
        self.VentadaEditar.destroy()
        self.mensaje["text"] = "Los Datos se guardaron con éxito"
        self.obtenerLosProductos()

    def EditarPorductos(self):
        self.mensaje["text"] = ""
        try:
            self.tree.item(self.tree.selection())["text"][0]
        except IndexError as e:
            self.mensaje["fg"] = "red"
            self.mensaje["text"] = "Por favor seleccione un producto"
            return
        self.mensaje["text"] = ""
        Nombre = self.tree.item(self.tree.selection())["text"]
        PrecioAnterior = self.tree.item(self.tree.selection())["values"][0]
        self.VentadaEditar = Toplevel()
        self.VentadaEditar.title = "Editar el producto"
        #Nombre antiguo
        Label(self.VentadaEditar,text="Nombre anterior: ").grid(row=0,column=1)
        Entry(self.VentadaEditar, textvariable=StringVar(self.VentadaEditar,value=Nombre),state="readonly").grid(row=0,column=2)
        #Nombre nuevo
        Label(self.VentadaEditar,text="Nuevo nombre: ").grid(row=1,column=1)
        nuevoNombre=Entry(self.VentadaEditar)
        nuevoNombre.grid(row=1,column=2)
        #Precio antiguo
        Label(self.VentadaEditar,text="Precio anterior: ").grid(row=2,column=1)
        Entry(self.VentadaEditar, textvariable=StringVar(self.VentadaEditar,value=PrecioAnterior),state="readonly").grid(row=2,column=2)
        #Precio nuevo
        Label(self.VentadaEditar,text="Nuevo Precio: ").grid(row=3,column=1)
        nuevoPrecio=Entry(self.VentadaEditar)
        nuevoPrecio.grid(row=3,column=2)
        Button(self.VentadaEditar, text = "Guardar cambios",command=lambda: self.EditarDatos(nuevoNombre.get(),Nombre,nuevoPrecio.get(),PrecioAnterior)).grid(row=4,column=2,sticky=W)


if __name__ == "__main__":
    window = Tk()
    app = product(window)
    window['bg'] = '#49A'
    window.mainloop()



