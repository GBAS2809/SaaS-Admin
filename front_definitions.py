#DONE: 
#  que el programa pueda aguantar QUE NO HAYA CONEXION CON LA BASE DE DATOS.
# * VALIDAR las entradas de los entry.
# # * Necesito feedback para cuando se modifique y agreguen cosas !!!!!! 
# * cuando se realicen cambios deben actualizarse solos, agregar/modificar un producto.
# * Debo hacer que los botones de inventario me devuelvan los id de los productos para editarlo. Usar funcionees lambda y referencias locales del id en la iteracion
# ON IT RN* Hacer el frame para editar y borrar los productos. 
#TODO: 
# * IMPORTANTE: 

# * Hacer el frame de operacion de venta.
# * Por último la opción de cerrar el día. 
# Optimizar las funciones de crud_products, rate_engine, cust_db_functions, sales_functions
# dar listas vacias y valores válidos en caso de error


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

from crud_products import ReadProducts, AddProduct, cleanProductDB, EditProduct, getProduct, DeleteProduct
from functions_terminal import TurnIntoFloat
from sales_functions import ReadSales, MakeDictSale
 #los widgets entry y textbox son bidireccionales, el usuario puede interactuar con ellos
 #el label solo escupe información.




#This is my class for the main menu left option bar
class Win_Options(customtkinter.CTkFrame):
    def __init__(self, master, title):
        super().__init__(master)
        options=[("Mi inventario", self.master.DrawInventory), 
                 ("Mi Libro Diario", self.master.DrawSales),
                 #("Nueva venta", self.master.),
                 #("Reporte del día", self.master.),
                 #("Configuración", self.master.)

        ]

        self.frame_display=0 #no imprime ninguno de las opciones

        self.title=customtkinter.CTkLabel(self, text=title)
        self.title.grid(column=0, row=0, padx=10, pady=(10,0),sticky="ew")

        for i, button in enumerate(options):
            gen_button=customtkinter.CTkButton(self, text=button[0], command=button[1])
            gen_button.grid(column=0, row=i, padx=10, pady=(10, 0), sticky="ew")




#Sera una ventana que se va a dedicar principalmente en alarmar las notificaciones como
#faltas de productos.
class Win_Message(customtkinter.CTkToplevel):
    def __init__(self, master,title, text):
         super().__init__(master)

         self.geometry("400x100")
         self.title(title)

         self.message=customtkinter.CTkLabel(self, text=text)
         self.message.pack(padx=20, pady=20)


#This class contains the window where you modify the values of an existing product. 
# It´s vulnerable since it only acepts dictionary info in a certain way. 
class Win_ModifyProd(customtkinter.CTkToplevel):
    def __init__(self, master, productDict, productID):
        super().__init__()
        self.geometry("500x500")
        self.grid_columnconfigure( 0, weight=1)
        self.grid_columnconfigure( 1, weight=1)

        self.placeholder_List=["Nombre del producto" ,"Precio de venta" ,"Cantidad del producto (Stock)",  "Costo" ,"Categoría del producto"]
        self.auxList=[productDict["product_name"], productDict["product_price"], productDict["product_stock"], productDict["product_cost"], productDict["product_category"]]
        self.master_reference=master
        self.pid=productID
        self.entryList=[]

        self.title=customtkinter.CTkLabel(self, text="Datos del producto")
        self.title.grid(column=0, row=0, padx=10, pady=(10, 0), sticky="nsew", columnspan=2)

        for i, entry in enumerate(self.placeholder_List):
            self.generic_entry=customtkinter.CTkEntry(self, placeholder_text=entry)
            self.generic_entry.insert(0, self.auxList[i])
            self.generic_entry.grid(column=0, row=i+1, padx=10, pady=(10,0), sticky="nsew", columnspan=2)
            self.entryList.append(self.generic_entry)
        
        

        self.feedbackLabel=customtkinter.CTkLabel(self, text="")
        self.feedbackLabel.grid(column=0, row=len(self.placeholder_List)+2, padx=10, pady=(10,0), columnspan=2, sticky="nsew")

        self.saveButton=customtkinter.CTkButton(self, text="Guardar", command= self.commitData, fg_color="green")
        self.saveButton.grid(column=0, row=len(self.auxList)+3, padx=10, pady=(10, 0), sticky="ew")

        self.eraseButton=customtkinter.CTkButton(self, text="Borrar", command=self.eraseProduct, fg_color="red") 
        self.eraseButton.grid(column=1, row=len(self.auxList)+3, padx=10, pady=(10, 0), sticky="ew")


    def commitData(self):
        self.entryDataList= [entry.get().strip() for entry in self.entryList]
        
        if not self.entryDataList[0]:
            self.feedbackLabel.configure(text="¡El producto necesita un nombre!", text_color="red")
            return
        if not self.entryDataList[1] or not self.entryDataList[2]:
            self.feedbackLabel.configure(text="¡Stock y Precio de venta son obligatorios!", text_color="red")
            return
        try:
            EditProduct(cleanProductDB(self.entryDataList), self.pid)
            self.feedbackLabel.configure(text="Producto Modificado exitosamente")
            self.after(3000, self.destroy())
            self.master_reference.refreshInventory()

        except Exception as e:
            self.feedbackLabel.configure(text=str(e), text_color="red")

    def eraseProduct(self):
     
        
        try:  
            DeleteProduct(self.pid)
            self.feedbackLabel.configure(text="Se borró el producto de manera exitosa.")
            self.after(3000, self.destroy())
            self.master_reference.refreshInventory()
        except Exception as e:
            self.feedbackLabel.configure(text=f"No se pudo borrar el producto.{str(e)}", color_text="red")
     
         






#tambien debo enseñar los detalles de una venta. Hacer un modulo que escupa los detalles de la venta
#todavia faltan las funciones para agregar desde el frontend.
#debo agregarlas.

#Esta clase tendrá ventanas popups en donde agregarás/modificarás los productos.
class Win_Prod(customtkinter.CTkToplevel):
     def __init__(self, master):
          super().__init__()
          self.geometry("500x500")
          self.grid_columnconfigure(0, weight=1)
          self.label_stringList=["Nombre del producto" ,"Precio de venta" ,"Cantidad del producto (Stock)",  "Costo" ,"Categoría del producto"]
          self.master_reference=master
          self.entryDataList=[]
          self.label_List=[]

          self.title=customtkinter.CTkLabel(self, text="Ingrese los datos del producto")
          self.title.grid(column=0, row=0, padx=10, pady=(10,0), sticky="nsew")

          for i,label in enumerate(self.label_stringList):           #We make the entrys using the list of the options.
               generic_label=customtkinter.CTkEntry(self, placeholder_text=label)
               generic_label.grid(column=0, row=i+1, padx=10, pady=(0,10), sticky="nsew")
               self.label_List.append(generic_label)

          self.feedbackLabel=customtkinter.CTkLabel(self, text="")
          self.feedbackLabel.grid(column=0, row=len(self.label_stringList)+1, padx=10, pady=10, sticky="nsew")

          self.commitButton=customtkinter.CTkButton(self, text="Guardar cambios", command=self.Commit_datos)
          self.commitButton.grid(column=0, row=len(self.label_stringList)+2, padx=10, pady=(10,0), sticky="nsew")

     def Commit_datos(self):                                 #ARREGLAR el mensaje parece quedarse trabado cuando actualizo luego de tener un error
      
      self.entryDataList = [label.get().strip() for label in self.label_List]
      # 2. Validaciones básicas en caliente antes de ir a la base de datos
      if not self.entryDataList[0]: # Si el nombre está vacío
               self.feedbackLabel.configure(text="¡El producto necesita un nombre!", text_color="red")
               return
      if not self.entryDataList[1] or not self.entryDataList[2]: # Si stock o precio están vacíos
               self.feedbackLabel.configure(text="¡Stock y Precio de venta son obligatorios!", text_color="red")
               return
      try:
          AddProduct(cleanProductDB(self.entryDataList))
          self.entryDataList=[] #limpiamos en caso de que nos salgan duplicados y nos curamos de todo mal

          for label in self.label_List:
              label.delete(0, customtkinter.END)
          
          self.feedbackLabel.configure(text="Agregado de manera exitosa!", text_color= "white")
          self.after(3000, lambda: self.feedbackLabel.configure(text=""))
          self.master_reference.refreshInventory()
          
      except Exception as e:
          self.feedbackLabel.configure(text=f"ERROR: No se pudo conectar con la base de datos: {e}", text_color="red")
          print(e)
          
               
               

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
      self.messageWin=None
      self.lista=(TurnIntoFloat(ReadProducts(page)))

      if self.lista==[]:
          if self.messageWin==None or not self.messageWin.winfo_exists():
              self.messageWin=Win_Message(self, "ERROR", "No se pudo establecer conexión con la base de datos.")
              self.messageWin.after(100, self.messageWin.lift)
              self.messageWin.after(200, self.messageWin.focus_force)
          else:
               self.messageWin.lift
               self.messageWin.focus_force
      else:

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

               self.button=customtkinter.CTkButton(self, text=str(prod["product_id"]), command=lambda pid=prod["product_id"] : self.modProduct(pid), width=30)
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
     
         
     def modProduct(self, pid):
         productDict=TurnIntoFloat(getProduct(pid))
         self.master_reference.modWinProd( productDict, pid)

         
          
          



#Display sales is a frame that displays all sales, paged. It holds the labels and the scrollable frame class.
class DisplaySales(customtkinter.CTkScrollableFrame):
     
     def __init__(self, master,title, page):
      super().__init__(master)
      self.messageWin=None

      self.lista=(MakeDictSale(ReadSales(page)))
      if self.lista==[]:
          if self.messageWin==None or self.messageWin.winfo_exists():
              self.messageWin=Win_Message(self, "ERROR!", "No se logró establecer conexión con la base de datos.")
              self.messageWin.after(100, self.messageWin.lift)
              self.messageWin.after(100, self.messageWin.focus_force)
          else:
              self.messageWin.lift
              self.messageWin.focus_force
              
           
      else:

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
          self.actual_frame=None #Debemos declarar variables para que existan hp

          self.addProdWin=None
          self.addSaleWin=None
          self.editProdWin=None



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
    
    def refreshInventory(self):
      
        if self.actual_frame is not None and isinstance(self.actual_frame, DisplayInventory):
            current_page = self.actual_frame.actual_page
            self.UpdateFrameInventory(current_page)
    
    def modWinProd(self, productDict, pid): #Ventana para modificar el producto 
        if self.editProdWin is None or not self.editProdWin.winfo_exists():
            self.editProdWin= Win_ModifyProd(self, productDict, pid)
            self.editProdWin.after(100, self.editProdWin.lift)
            self.editProdWin.after(200, self.editProdWin.focus_force)
        else:
            self.editProdWin.lift()
            self.editProdWin.focus_force()


    def openWinProd(self):      #Ventana para crear producto 
        if self.addProdWin is None or not self.addProdWin.winfo_exists():
            self.addProdWin = Win_Prod(self)  # create window if its None or destroyed
            self.addProdWin.after(100, self.addProdWin.lift)        # Fuerza a subir en la pila de ventanas
            self.addProdWin.after(200, self.addProdWin.focus_force) # Fuerza el foco del sistema operativo
        else:
            self.addProdWin.lift()          # Trae al frente si ya existía
            self.addProdWin.focus_force()   # Fuerza el foco de inmediato
    
    def openWinSell(self):
         if self.addSaleWin is None or not self.addSaleWin.winfo_exists():
              self.addSaleWin= Win_Sell(self)
              self.addSaleWin.after(100, self.addSaleWin.lift)        # Fuerza a subir en la pila de ventanas
              self.addSaleWin.after(200, self.addSaleWin.focus_force) # Fuerza el foco del sistema operativo
         else: 
              self.addSaleWin.lift()          # Trae al frente si ya existía
              self.addSaleWin.focus_force()   # Fuerza el foco de inmediato

if __name__=="__main__":
 

 Miapp=App()
 Miapp.mainloop()