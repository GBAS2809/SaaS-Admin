#TODO: 
# * IMPORTANTE: que el programa pueda aguantar QUE NO HAYA CONEXION CON LA BASE DE DATOS.
# * VALIDAR las entradas de los entry. 
# * Debo hacer que los botones de inventario me devuelvan los id de los productos para editarlo. 
# * Por último la opción de cerrar el día. 
# * Necesito feedback para cuando se modifique y agreguen cosas !!!!!!
# *cuando se realicen cambios deben actualizarse solos, agregar/modificar un producto.

# Contemplar al terminar el PMV:
# *Aplicar módulos para manejar de la mejor manera instalación, update y desinstalación.
# *Atajos de teclado para ejercer comandos.
# *Optimizar el código
# *Backup en la nube de ventas e inventario. (Guardado de manera eficiente)
# *Mejor manejo de inventario

#Aquí pondré todas las definiciones para el front en términos de clases y funciones.
import customtkinter
#Hacer un prompt que imprima en pantalla los productos del inventario
 #Resolver como se usa el textbox
import sys
from pathlib import Path

 #obtengo la dirección actual
actual_path=Path(__file__).resolve()

 #nos vamos a la raíz de mi path actual
project_root=actual_path.parents[1]

 #inyecta la ruta en el inicio del sistema de py
sys.path.insert(0, str(project_root))

from crud_products import ReadProducts, AddProduct, cleanProductDB
from functions_terminal import TurnIntoFloat
from sales_functions import ReadSales, MakeDictSale
 #los widgets entry y textbox son bidireccionales, el usuario puede interactuar con ellos
 #el label solo escupe información.

#This is my class for the main menu left option bar
class Win_Options(customtkinter.CTkFrame):
    def __init__(self, master, title):
        super().__init__(master)

        self.frame_display=0 #no imprime ninguno de las opciones

        self.title=customtkinter.CTkLabel(self, text=title)
        self.title.grid(column=0, row=0, padx=10, pady=(10,0),sticky="ew")

        self.button_1=customtkinter.CTkButton(self, text="Mi inventario", command=self.master.DrawInventory)
        self.button_1.grid(column=0, row=1, padx=10, pady=(10,0), sticky="ew")

        self.button_2=customtkinter.CTkButton(self, text="Mi Libro Diario", command=self.master.DrawSales)
        self.button_2.grid(column=0, row=2, padx=10, pady=(10,0), sticky="ew")

        self.button_3=customtkinter.CTkButton(self, text="Opciones")
        self.button_3.grid(column=0, row=3, padx=10, pady=(10,0), sticky="ew")

#Sera una ventana que se va a dedicar principalmente en alarmar las notificaciones como
#faltas de productos.
class Win_Message(customtkinter.CTkToplevel):
    def __init__(self, master):
         super().__init__(master)

         self.geometry("200x200")
         self.title("WARNING!")




#tambien debo enseñar los detalles de una venta.Hacer un modulo que escupa los detalles de la venta
    
        
#todavia faltan las funciones para agregar desde el frontend.
#debo agregarlas.

#Esta clase tendrá ventanas popups en donde agregarás/modificarás los productos.
class Win_Prod(customtkinter.CTkToplevel):
     def __init__(self, master):
          super().__init__()
          self.geometry("500x500")
          self.grid_columnconfigure(0, weight=1)
          self.label_stringList=["Nombre del producto","Cantidad del producto (Stock)","Precio de venta",  "Costo" ,"Categoría del producto"]
          self.label_List=[]
          self.entryDataList=[]
          self.master_reference=master
          j=0

          self.title=customtkinter.CTkLabel(self, text="Ingrese los datos del producto")
          self.title.grid(column=0, row=0, padx=10, pady=(10,0), sticky="nsew")

          for i,label in enumerate(self.label_stringList):           #We make the entrys using the list of the options.
               generic_label=customtkinter.CTkEntry(self, placeholder_text=label)
               generic_label.grid(column=0, row=i+1, padx=10, pady=(0,10), sticky="nsew")
               self.label_List.append(generic_label)
               j=i
          self.commitButton=customtkinter.CTkButton(self, text="Guardar cambios", command=self.Commit_datos)
          self.commitButton.grid(column=0, row=i+2, padx=10, pady=(10,0), sticky="nsew")


     def Commit_datos(self):
          for label in self.label_List:
               self.entryDataList.append(label.get())
               label.delete(0, 50)

               
       
#  *OK. Entre estas dos líneas de código debo validar la entrada. JUSTO AQUÍ
          dictionary=cleanProductDB(self.entryDataList)
          AddProduct(dictionary)
          self.entryDataList=[] #limpiamos en caso de que nos salgan duplicados y nos curamos de todo mal
          
               
               

#Esta otra tendrá un clase en donde podras agregar/modificarás las ventas.  Debo buscar la manera de mitigar el error humano   
class Win_Sell(customtkinter.CTkToplevel):
     def __init__(self, master):
          super().__init__()
          self.geometry("500x500")

          self.title=customtkinter.CTkLabel(self, text="Ingrese los datos de la venta")
          self.title.grid(column=0, row=0, padx=10, pady=(10,0), sticky="ew")

#Display inventory is a frame that displays all products on inventory, paged. It holds the labels and the scrollable frame class.

class DisplayInventory(customtkinter.CTkScrollableFrame):
     
     def __init__(self, master,title, page):
          super().__init__(master)
          self.lista=[]

          
          self.lista=(TurnIntoFloat(ReadProducts(page)))
         
               
          

          self.grid_columnconfigure(1, weight=2)
          self.grid_columnconfigure(2, weight=1)
          self.grid_columnconfigure(0, weight=0)

          self.lista_label=[]
          self.actual_page=page

          self.master_reference=master

          self.title=customtkinter.CTkLabel(self, text=title, fg_color="gray30", corner_radius=0, width=100, compound="top", justify="center")
          self.title.grid(column=0, row=0, padx=0, pady=(10, 0), columnspan=4, sticky="ew")

          self.addbutton=customtkinter.CTkButton(self, text="Añadir Producto", command=self.master_reference.openWinProd)
          self.addbutton.grid(column=0, row=1, padx=10, pady=(10,0),columnspan=4, sticky="ew")

          self.left=customtkinter.CTkButton(self, text="<", command=self.displayleft)
          self.left.grid(column=0, row=2, padx=0, pady=(10, 0), columnspan=2, sticky="ew")
          self.right=customtkinter.CTkButton(self, text=">", command=self.displayright)
          self.right.grid(column=2, row=2, padx=0, pady=(10, 0) , columnspan=2, sticky="ew")

          self.header_1=customtkinter.CTkLabel(self, text="Productos")
          self.header_1.grid(column=1, row=3, padx=10, pady=(0, 0), sticky="ew", rowspan=2)
          self.header_2=customtkinter.CTkLabel(self, text= "Stock")
          self.header_2.grid(column=2, row=3, padx=15, pady=(10, 0), sticky="ew")

          for i, prod in enumerate(self.lista):

               self.button=customtkinter.CTkButton(self, text=str(prod["product_id"]), command=self.callback, width=30)
               self.button.grid(row=i+4, column=0, padx=10, pady=(10,0), sticky="ew")

               self.texto=customtkinter.CTkLabel(self, text=prod["product_name"], justify="left", compound="left")
               self.texto.grid(row=i+4, column=1, padx=10, pady=(10,0), sticky="ew")
               
               self.stock=customtkinter.CTkLabel(self, text=str(prod["product_stock"]))
               self.stock.grid(row=i+4, column=2,padx=10, pady=(10,0), sticky="ew" )

               self.justify=customtkinter.CTkLabel(self, text="", justify="left", compound="left", width=30)
               self.justify.grid(row=i+4, column=3, padx=10, pady=(10,0), sticky="ew")

               

     def displayleft(self):
                   if self.actual_page>1:
                       self.actual_page-=1
                       self.master_reference.UpdateFrameInventory(self.actual_page)
                       
     def displayright(self):
                   if self.actual_page<5:
                       self.actual_page+=1
                       self.master_reference.UpdateFrameInventory(self.actual_page)

     def callback(self):
          self.button.get()
          

#Display sales is a frame that displays all sales, paged. It holds the labels and the scrollable frame class.
class DisplaySales(customtkinter.CTkScrollableFrame):
     
     def __init__(self, master,title, page):
          super().__init__(master)

          self.lista=(MakeDictSale(ReadSales(page)))

          self.actual_page=page

          self.master_reference=master

          self.page_limit=self.lista[0]["sales_id"]/100 #debo aplicar un limite para las ventas pidele a una funcion del backend
          #pida la ultima linea y me la devuelva

          self.grid_columnconfigure(1, weight=2)
          self.grid_columnconfigure(2, weight=1)
          self.grid_columnconfigure(0, weight=0)
          
          self.lista_label=[]

          self.title=customtkinter.CTkLabel(self, text=title, fg_color="gray30", corner_radius=0, width=100, compound="top", justify="center")
          self.title.grid(column=0, row=0, padx=0, pady=(10, 0), columnspan=4, sticky="ew")

          self.left=customtkinter.CTkButton(self, text="<", command=self.displayleft)
          self.left.grid(column=0, row=1, padx=0, pady=(10, 0), columnspan=2, sticky="ew")
          self.right=customtkinter.CTkButton(self, text=">", command=self.displayright)
          self.right.grid(column=2, row=1, padx=0, pady=(10, 0) , columnspan=2, sticky="ew")

          self.header_1=customtkinter.CTkLabel(self, text="Fecha")
          self.header_1.grid(column=0, row=2, padx=10, pady=(10,0), sticky="ew" )
          self.header_2=customtkinter.CTkLabel(self, text="Número de venta")
          self.header_2.grid(column=1, row=2, padx=10, pady=(0, 0), sticky="ew")
          self.header_3=customtkinter.CTkLabel(self, text= "Total referenciado")
          self.header_3.grid(column=2, row=2, padx=15, pady=(10, 0), sticky="ew")
          self.header_4=customtkinter.CTkLabel(self, text= "Vueltos")
          self.header_4.grid(column=3, row=2, padx=15, pady=(10, 0), sticky="ew", rowspan=2)

          



          for i, sale in enumerate(self.lista):

               self.date_label=customtkinter.CTkLabel(self, text=(f" {sale["sales_day"]}"), justify="left", compound="left")
               self.date_label.grid(row=i+3, column=0, padx=10, pady=(10,0), sticky="ew")
               

               self.id_label=customtkinter.CTkLabel(self, text=(f"ID: {str(sale["sales_id"])}"))
               self.id_label.grid(row=i+3, column=1,padx=10, pady=(10,0), sticky="ew" )

               self.total_label=customtkinter.CTkLabel(self, text=(f"{sale["sales_total_cent_usd"]}."))
               self.total_label.grid(row=i+3, column=2, padx=10, pady=(10,0), sticky="ew" )

               self.change_label=customtkinter.CTkLabel(self, text=(f"Bs. {sale["sales_change_cent_bs"]}\t Usd. {sale["sales_change_cent_bs"]} "))
               self.change_label.grid(row=i+3, column=3, padx=10, pady=(10,0 ), sticky="ew", rowspan=2)
               
     
     def displayleft(self):
          if self.actual_page>1:
              self.actual_page-=1
              self.master_reference.UpdateFrameSales( self.actual_page)
     
     def displayright(self):
         if self.actual_page<5:
          self.actual_page+=1
          self.master_reference.UpdateFrameSales( self.actual_page) #debo encontrar una manera de marcar un limite



     
class App(customtkinter.CTk):

    def __init__(self):
          super().__init__()

          self.actual_page=1

          self.columnconfigure((0,1), weight=1)
          self.rowconfigure(0, weight=1)

          self.title("Prueba de generación")
          self.geometry("1000x500")

          self.menu=Win_Options(self, "Test App")
          self.menu.grid(column=0, row=0,sticky="nsew")

          self.actual_frame=None
          self.toplevel_window=None #Debemos declarar variables para que existan hp



    def CleanFrame(self):
        if self.actual_frame is not None:
            self.actual_frame.destroy()
        

    def DrawInventory(self):
     self.CleanFrame()
     self.actual_frame=1
     self.actual_frame=DisplayInventory(self, "Inventario.", page=self.actual_page)
     self.actual_frame.grid(row=0, column=1, padx=10, pady=(0, 10), sticky="nsew")
      

    def DrawSales(self):
     self.CleanFrame()
     self.actual_frame=1
     self.actual_frame=DisplaySales(self, "Libro diario.", page=self.actual_page)
     self.actual_frame.grid(row=0, column=1, padx=10, pady=(0, 10), sticky="nsew")

    def UpdateFrameSales(self, page):
        self.CleanFrame()
        self.actual_frame=DisplaySales(self, "Libro diario.", page)
        self.actual_frame.grid(row=0, column=1, padx=10, pady=(0, 10), sticky="nsew")
    
    def UpdateFrameInventory(self, page):
        self.CleanFrame()
        self.actual_frame=DisplayInventory(self, "Inventario.", page)
        self.actual_frame.grid(row=0, column=1, padx=10, pady=(0, 10), sticky="nsew")

    def openWinProd(self):
        if self.toplevel_window is None or not self.toplevel_window.winfo_exists():
            self.toplevel_window = Win_Prod(self)  # create window if its None or destroyed
            self.toplevel_window.after(100, self.toplevel_window.lift) # Fuerza a subir en la pila de ventanas
            self.toplevel_window.after(200, self.toplevel_window.focus_force) # Fuerza el foco del sistema operativo
        else:
            self.toplevel_window.lift()          # Trae al frente si ya existía
            self.toplevel_window.focus_force()   # Fuerza el foco de inmediato
    
    def openWinSell(self):
         if self.toplevel_window is None or not self.toplevel_window.winfo_exists():
              self.toplevel_window= Win_Sell(self)
              self.toplevel_window.after(100, self.toplevel_window.lift) # Fuerza a subir en la pila de ventanas
              self.toplevel_window.after(200, self.toplevel_window.focus_force) # Fuerza el foco del sistema operativo
         else: 
              self.toplevel_window.lift()          # Trae al frente si ya existía
              self.toplevel_window.focus_force()   # Fuerza el foco de inmediato


if __name__=="__main__":
 

 Miapp=App()
 Miapp.mainloop()