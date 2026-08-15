#DONE: 
#  que el programa pueda aguantar QUE NO HAYA CONEXION CON LA BASE DE DATOS.
# * VALIDAR las entradas de los entry.
# # * Necesito feedback para cuando se modifique y agreguen cosas !!!!!! 
# * cuando se realicen cambios deben actualizarse solos, agregar/modificar un producto.
# * Debo hacer que los botones de inventario me devuelvan los id de los productos para editarlo. Usar funcionees lambda y referencias locales del id en la iteracion
# ON IT RN* Hacer el frame para editar y borrar los productos. 
# Optimizar las funciones de crud_products, rate_engine, cust_db_functions, sales_functions
# dar listas vacias y valores válidos en caso de error
# ADD A NEW COLUMN is_active on sales table

#DOING RN: 
# * Hacer el frame de operacion de venta.

#TODO: 
# * IMPORTANTE: 
# * Validar los limites de los distintos frames para scrollear.
# * Por último la opción de cerrar el día. 



# Contemplar al terminar el PMV:
# *Identificar clientes por regularidad. I guess? consultar con samuel
# *Aplicar módulos para manejar de la mejor manera instalación, update y desinstalación.
# *Atajos de teclado para ejercer comandos.
# *Optimizar el código
# *Backup en la nube de ventas e inventario. (Guardado de manera eficiente)
# *Mejor manejo de inventario, estadisticas, etc

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

from crud_products import ReadProducts, AddProduct, cleanProductDB, EditProduct, getProduct, DeleteProduct, SearchProducts
from functions_terminal import TurnIntoFloat
from sales_functions import ReadSales, MakeDictSale, GetPay, GetDetails, makeDailyReport, GetDailySales, SubmitSale
from cust_db_functions import GetCustomer, AddCustomer
from rate_engine import GetRates
 #los widgets entry y textbox son bidireccionales, el usuario puede interactuar con ellos
 #el label solo escupe información.




#This is my class for the main menu left option bar
class Win_Options(customtkinter.CTkFrame):
    def __init__(self, master, title):
        super().__init__(master)
        options=[("Mi inventario", self.master.DrawInventory), 
                 ("Mi Libro Diario", self.master.DrawSales),
                 ("Nueva venta", self.master.DrawNewSale),
                 ("Reporte del día", self.master.DrawDailyReport),
                 #("Configuración", self.master.)

        ]

        self.frame_display=0 #no imprime ninguno de las opciones

        self.title=customtkinter.CTkLabel(self, text=title)
        self.title.grid(column=0, row=0, padx=10, pady=(10,0),sticky="ew")

        for i, button in enumerate(options):
            gen_button=customtkinter.CTkButton(self, text=button[0], command=button[1])
            gen_button.grid(column=0, row=i+1, padx=10, pady=(10, 0), sticky="ew")

        self.rate=customtkinter.CTkLabel(self, text="Tasas")
        self.rate.grid(column=0, row=len(options)+2, padx=10, pady=(10, 0))
        self.date=customtkinter.CTkLabel(self, text="")
        self.date.grid(column=0, row=len(options)+3, padx=10 , pady=(10,0))
        self.BCV_label=customtkinter.CTkLabel(self, text="")
        self.BCV_label.grid(column=0, row=len(options)+4, padx=10 , pady=(10,0))
        self.EUR_label=customtkinter.CTkLabel(self, text="")
        self.EUR_label.grid(column=0, row=len(options)+5, padx=10 , pady=(10,0))
        





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
          
class Win_AddCustomer(customtkinter.CTkToplevel):
    def __init__(self, master, id_document):
        super().__init__(master)

        self.geometry("500x500")
        self.title("Añadir cliente.")



        self.subtitle=customtkinter.CTkLabel(self, text=" Ingrese los datos del nuevo cliente")
        self.subtitle.grid(column=0, row=0, padx=10, pady=(10,0), sticky="ew")

        self.nameEntry=customtkinter.CTkEntry(self, placeholder_text="Ingrese el nombre del cliente.")
        self.nameEntry.grid(column=0, row=1, padx=10, pady=(10,0), sticky="ew")

        self.documentEntry=customtkinter.CTkEntry(self, placeholder_text="Ingrese el número de cédula.")
        self.documentEntry.insert(0, id_document)
        self.documentEntry.grid(column=0, row=2, padx=10, pady=(10,0), sticky="ew")

        self.adressEntry=customtkinter.CTkEntry(self, placeholder_text="Ingrese dirección corta.")
        self.adressEntry.grid(column=0, row=3, padx=10, pady=(10,0), sticky="ew")

        self.feedback=customtkinter.CTkLabel(self, text="")
        self.feedback.grid(column=0, row=4, padx=10, pady=(10,0), sticky="ew")

        self.addBtn=customtkinter.CTkButton(self, text="Guardar cambios.", command=self.commitDatos)
        self.addBtn.grid(column=0, row=5, padx=10, pady=(10,0), sticky="ew")

    def commitDatos(self):

        if self.nameEntry.get()=="" or None:
            self.feedback.configure(text="El cliente Necesita un nombre!", text_color="red")
            return 

        if not int(self.documentEntry.get()):
            self.feedback.configure(text="El cliente necesita un numero de Cédula", text_color= "red")
            return

        if not self.adressEntry.get() or self.adressEntry.get()=="":
            self.feedback.configure(text="El cliente necesita una dirección.", text_color= "red")
            return

        customer={
            "name_customer":str(self.nameEntry.get().strip()),
            "id_document":int(self.documentEntry.get()),
            "type_document": 'V',
            "address":str(self.adressEntry.get().strip())
        }
        AddCustomer(customer)
        self.after(3000, self.feedback.configure(text="Cliente agregado exitosamente! Puede continuar con la compra"))
        self.destroy()

            
        



class Win_DetailedSale(customtkinter.CTkToplevel):
    def __init__(self,master, products_list, payments_list):
        super().__init__(master)

        self.geometry("500x500")
        self.title("Venta detallada.")

        self.subtitle1=customtkinter.CTkLabel(self, text="Productos")
        self.subtitle1.grid(column=0, row=0, padx=10, pady=(10, 0), sticky="ew", columnspan=4)

        self.header1=customtkinter.CTkLabel(self, text="Nombre del producto")
        self.header1.grid(column=0, row=1, padx=10, pady=(10, 0), sticky="ew")
        self.header2=customtkinter.CTkLabel(self, text="Cant. Vendida")
        self.header2.grid(column=1, row=1, padx=10, pady=(10, 0), sticky="ew")
        self.header3=customtkinter.CTkLabel(self, text="Precio Unitario")
        self.header3.grid(column=2, row=1, padx=10, pady=(10, 0), sticky="ew")
        self.header4=customtkinter.CTkLabel(self, text="Total")
        self.header4.grid(column=3, row=1, padx=10, pady=(10, 0), sticky="ew")

        for i, label in enumerate(products_list):

            self.genericL=customtkinter.CTkLabel(self, text=label["product_name"])
            self.genericL.grid(column=0, row=i+2, padx=10, pady=(10, 0), sticky="ew")
            self.genericL=customtkinter.CTkLabel(self, text=label["number_sold"])
            self.genericL.grid(column=1, row=i+2, padx=10, pady=(10, 0), sticky="ew")
            self.genericL=customtkinter.CTkLabel(self, text=label["product_price"])
            self.genericL.grid(column=2, row=i+2, padx=10, pady=(10, 0), sticky="ew")
            self.genericL=customtkinter.CTkLabel(self, text=str(label["number_sold"]*label["product_price"]))
            self.genericL.grid(column=3, row=i+2, padx=10, pady=(10, 0), sticky="ew")

        self.subtitle1=customtkinter.CTkLabel(self, text="Pagos detallados")
        self.subtitle1.grid(column=0, row=len(products_list)+2, padx=10, pady=(10, 0), sticky="ew", columnspan=4)

        self.header1=customtkinter.CTkLabel(self, text="Método de pago")
        self.header1.grid(column=0, row=len(products_list)+3, padx=10, pady=(10, 0), sticky="ew")
        self.header2=customtkinter.CTkLabel(self, text="Valor en Dólares")
        self.header2.grid(column=1, row=len(products_list)+3, padx=10, pady=(10, 0), sticky="ew")
        self.header3=customtkinter.CTkLabel(self, text="Monto pagado")
        self.header3.grid(column=2, row=len(products_list)+3, padx=10, pady=(10, 0), sticky="ew")


        for i, pay in enumerate(payments_list):

            self.genericL=customtkinter.CTkLabel(self, text=pay["method_name"])
            self.genericL.grid(column=0, row=i+len(products_list)+3, padx=10, pady=(10, 0), sticky="ew", columnspan=2)
            self.genericL=customtkinter.CTkLabel(self, text=f"{pay["value_usd_cents"]}$")
            self.genericL.grid(column=2, row=i+len(products_list)+3, padx=10, pady=(10, 0), sticky="ew")
            self.genericL=customtkinter.CTkLabel(self, text=f"{pay["payment_cents"]}")
            self.genericL.grid(column=3, row=i+len(products_list)+3, padx=10, pady=(10, 0), sticky="ew")

#Esta otra tendrá un clase en donde podras agregar/modificarás las ventas.  Debo buscar la manera de mitigar el error humano   
class Win_NewSale(customtkinter.CTkToplevel):
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
             
              self.messageWin=Win_Message(self, "ERROR", "No se pudo establecer conexión con la base de datos. ")
              self.messageWin.after(100, self.messageWin.lift)
              self.messageWin.after(200, self.messageWin.focus_force)
          else:
               self.messageWin.lift
               self.messageWin.focus_force
      else:

          self.grid_columnconfigure((1, 2, 3, 4), weight=1)
          self.grid_columnconfigure((0,5), weight=0)

          self.lista_label=[]
          self.actual_page=page

          self.master_reference=master

          self.title=customtkinter.CTkLabel(self, text=title, fg_color="gray30", corner_radius=0, width=100, compound="top", justify="center")
          self.title.grid(column=0, row=0, padx=0, pady=(10, 0), columnspan=6, sticky="ew")

          self.addbutton=customtkinter.CTkButton(self, text="Añadir Producto", command=self.master_reference.openWinProd)
          self.addbutton.grid(column=0, row=1, padx=10, pady=(10,0),columnspan=6, sticky="ew")

          self.left=customtkinter.CTkButton(self, text="<", command=self.displayleft)
          self.left.grid(column=0, row=2, padx=0, pady=(10, 0), columnspan=3, sticky="ew")
          self.right=customtkinter.CTkButton(self, text=">", command=self.displayright)
          self.right.grid(column=3, row=2, padx=0, pady=(10, 0) , columnspan=3, sticky="ew")

          self.header_1=customtkinter.CTkLabel(self, text="Productos")
          self.header_1.grid(column=1, row=3, padx=15, pady=(10, 0), sticky="ew")
          self.header_2=customtkinter.CTkLabel(self, text= "Stock")
          self.header_2.grid(column=2, row=3, padx=15, pady=(10, 0), sticky="ew")
          self.header_3=customtkinter.CTkLabel(self, text= "Precio de Venta")
          self.header_3.grid(column=3, row=3, padx=15, pady=(10, 0), sticky="ew")
          self.header_4=customtkinter.CTkLabel(self, text= "Valor bruto total")
          self.header_4.grid(column=4, row=3, padx=15, pady=(10, 0), sticky="ew")
          self.header_5=customtkinter.CTkLabel(self, text= "   ")
          self.header_5.grid(column=5, row=3, padx=15, pady=(10, 0), sticky="ew")


          for i, prod in enumerate(self.lista):

               self.button=customtkinter.CTkButton(self, text="", command=lambda pid=prod["product_id"] : self.modProduct(pid), width=30)
               self.button.grid(row=i+4, column=0, padx=10, pady=(10,0), sticky="ew")

               self.texto=customtkinter.CTkLabel(self, text=prod["product_name"], justify="left", compound="left")
               self.texto.grid(row=i+4, column=1, padx=10, pady=(10,0), sticky="ew")
               
               self.stock=customtkinter.CTkLabel(self, text=str(prod["product_stock"]))
               self.stock.grid(row=i+4, column=2,padx=10, pady=(10,0), sticky="ew" )

               self.justify=customtkinter.CTkLabel(self, text=str(prod["product_price"]), justify="left", compound="left")
               self.justify.grid(row=i+4, column=3, padx=10, pady=(10,0), sticky="ew")

               self.justify=customtkinter.CTkLabel(self, text=f"{float(prod['product_price'])*float(prod['product_stock'])}$", justify="left", compound="left")
               self.justify.grid(row=i+4, column=4, padx=10, pady=(10,0), sticky="ew")


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

          self.grid_columnconfigure((1, 2, 3), weight=2)
          self.grid_columnconfigure((0), weight=1)

          
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
          self.header_2.grid(column=1, row=2, padx=10, pady=(10, 0), sticky="ew")
          self.header_3=customtkinter.CTkLabel(self, text= "Total referenciado")
          self.header_3.grid(column=2, row=2, padx=15, pady=(10, 0), sticky="ew")
          self.header_4=customtkinter.CTkLabel(self, text= "Vueltos")
          self.header_4.grid(column=3, row=2, padx=15, pady=(10, 0), sticky="ew")

          for i, sale in enumerate(self.lista):
               
               self.button=customtkinter.CTkButton(self, command=lambda pid=sale["sales_id"]:self.getDetailedSale(pid), text="", width=30 )
               self.button.grid(row=i+3, column=0,padx=10, pady=(10,0), sticky="ew")
          
               self.date_label=customtkinter.CTkLabel(self, text=(f" {sale["sales_day"]}"), justify="left", compound="left")
               self.date_label.grid(row=i+3, column=1, padx=10, pady=(10,0), sticky="ew")

               self.total_label=customtkinter.CTkLabel(self, text=(f"{sale["sales_total_cent_usd"]}$"))
               self.total_label.grid(row=i+3, column=2, padx=10, pady=(10,0), sticky="ew" )

               self.change_label=customtkinter.CTkLabel(self, text=(f"Bs. {sale["sales_change_cent_bs"]}\t Usd. {sale["sales_change_cent_bs"]} "))
               self.change_label.grid(row=i+3, column=3, padx=10, pady=(10,0 ), sticky="ew")
               
     
     def displayleft(self):
          if self.actual_page>1:
              self.actual_page-=1
              self.master_reference.UpdateFrameSales( self.actual_page)
     
     def displayright(self):
         if self.actual_page<5:
          self.actual_page+=1
          self.master_reference.UpdateFrameSales( self.actual_page) #debo encontrar una manera de marcar un limite

     def getDetailedSale(self, pid):
         try:
             self.DetailedWin=Win_DetailedSale(self, GetDetails(pid), GetPay(pid)) #hacer una funcion que me divida los montos en 100 
             self.DetailedWin.after(100, self.DetailedWin.lift)
             self.DetailedWin.after(200, self.DetailedWin.focus_force)

         except Exception as e:
            print(e)
            self.messageWin=Win_Message(self, "ERROR", str(e))
            self.messageWin.after(100, self.messageWin.lift)
            self.messageWin.after(200, self.messageWin.focus_force)
         

         
class DisplayNewSale(customtkinter.CTkFrame):
    def __init__(self, master, rate):
        super().__init__(master)

        self.columnconfigure(0 , weight=1)
        self.rowconfigure(0, weight=1)

        self.master_reference=master

        self.Win_Pay=None
        self.actual_frame=None
        self.rate=rate
        
        self.total_usd=0
        self.total_bs=0

        self.winCustomer=None

        self.product_list=[]
        self.customer={}
        self.payment_list=[]
        self.totalref_cent=0
        self.rate_snapshot_cent=int(round(float(self.rate)*100))

            #ask for ID
            #get the products
            #get payments
            #commit sale
        self.frame_client=customtkinter.CTkFrame(self)
        self.frame_product=customtkinter.CTkFrame(self)
        self.frame_payment=customtkinter.CTkFrame(self)

        self.buildClient()
        self.buildProduct()
        self.buildPayment()

        self.frame_client.grid(column=0, row=0, sticky="nsew", columnspan=2)
        self.frame_product.grid_remove()
        self.frame_payment.grid_remove()

    def productStep(self):

            if self.entryClient.get()!="":

                 self.customer=GetCustomer(int(self.entryClient.get()))
                 if self.customer==False:

                                self.openWinCustomer(id_document=int(self.entryClient.get()))
                                self.feedbackClient.configure(text="Cliente nuevo, agregue los datos del cliente para poder continuar la venta.", text_color="white")

                                return
                 self.labelClient.configure(text=f"\tCLIENTE: {self.customer["name_customer"]}\t Cédula de identidad: {self.customer["id_document"]}")
                 self.totalLabel.configure(text=f"TOTAL: ") #PONER EL MONTO EN BS. AL DIA
                 self.showProductFrame()
            else:
                
                self.feedbackClient.configure(text="Ingrese una cedula! Campo vacío!", text_color="red")
    
    def showClientFrame(self):
        self.frame_product.grid_remove()
        self.frame_client.grid(column=0, row=0, sticky="nsew")

    def showProductFrame(self):
        self.frame_client.grid_remove()
        self.frame_payment.grid_remove()
        self.frame_product.grid(column=0, row=0, sticky="nsew", columnspan=2)

    def showPaymentFrame(self):
        self.frame_product.grid_remove()
        self.frame_payment.grid(column=0, row=0, sticky="nsew", columnspan=2)

    def openWinCustomer(self, id_document):
        if self.winCustomer is None or not self.winCustomer.winfo_exists():
                    self.winCustomer= Win_AddCustomer(self, id_document)
                    self.winCustomer.after(100, self.winCustomer.lift)
                    self.winCustomer.after(200, self.winCustomer.focus_force)
        else:
                    self.winCustomer.lift()
                    self.winCustomer.focus_force()

    def searchProduct(self, event=None):
         
         self.query=self.entryProduct.get().strip().lower()

         for widget in self.search_results_frame.winfo_children():
              widget.destroy()

         if not self.query.strip():
              return

         result_db=SearchProducts(self.query.strip())

         for i , prod in enumerate(result_db):

              prod["product_price"]/=100
              btn=customtkinter.CTkButton(self.search_results_frame,
                                           text=f"{prod["product_name"]} {prod["product_price"]}$",
                                           anchor="w",
                                           cursor="hand2",
                                           command=lambda p=prod : self.addToCart(p))

              self.search_results_frame.grid(column=1, row=2, sticky="ew", padx=10)
              btn.grid(column=0 ,row=i, padx=10, pady=2, sticky="ew")

    def addToCart(self, product):

         self.product_list.append(product)

         self.entryProduct.delete(0 , "end")

         for widget in self.search_results_frame.winfo_children():
              widget.destroy()

              self.refreshCart()
         self.search_results_frame.grid_remove()

    def refreshCart(self):
         self.total_usd=0
         
         if self.label_List:
              for widget in self.label_List:
               widget.destroy()
              self.label_List=[]

         for  i, label in enumerate(self.product_list):
                          label["number_sold"]=1
                          self.genLabel=customtkinter.CTkLabel(self.frame_product, text=f"{label["product_name"]} {label["product_price"]}$ X {label["number_sold"]} - {label["number_sold"]*label["product_price"]}$")
                          self.genLabel.grid(column=1,row=i+3, padx=10, pady=(10,0), sticky="ew")
                          self.label_List.append(self.genLabel)

                          self.total_usd+=label["product_price"]*label["number_sold"]

         self.total_bs=round(self.rate*self.total_usd, 2)
         self.totalref_cent=int(round(float(self.total_usd)*100))
         self.total_usdLabel.configure(text=f"Ref.{self.total_usd} \tBs {self.total_bs}")

    def DiscountPay(self, Id):
         
         

         if self.Win_Pay is None or not self.Win_Pay.winfo_exists():
              
              self.Win_Pay=customtkinter.CTkToplevel(self)
              self.Win_Pay.geometry("200x200")

              self.Win_Pay.label=customtkinter.CTkLabel(self.Win_Pay, text="MONTO A PAGAR:")
              self.Win_Pay.entry=customtkinter.CTkEntry(self.Win_Pay, placeholder_text="MONTO A PAGAR")
              if Id==1:
                   self.Win_Pay.entry.insert(0, f"{self.total_usd}")
                   
              else:
                   self.Win_Pay.entry.insert(0, f"{self.total_bs}")
              self.Win_Pay.btn=customtkinter.CTkButton(self.Win_Pay, text="Subir pago", command= lambda :self.AddPay(Id))

              self.Win_Pay.label.pack()
              self.Win_Pay.entry.pack()
              self.Win_Pay.btn.pack()

              self.Win_Pay.after(100, self.Win_Pay.lift)
              self.Win_Pay.after(200, self.Win_Pay.focus_force)


         else:
              self.Win_Pay.after(100, self.Win_Pay.lift)
              self.Win_Pay.after(200, self.Win_Pay.focus_force)

    #Disable the commit sale function 

    def AddPay(self, methodId ):
         

         if methodId==1:
          payment={
                                  "payment_cents":int(round(float(self.Win_Pay.entry.get())*100)) ,
                                  "method_id": methodId,
                                  "value_usd_cents":int(round(float(self.Win_Pay.entry.get())*100))
                             }
          
          self.total_usd-=payment["value_usd_cents"]/100
          self.total_bs-=round(((payment["value_usd_cents"]/100)*self.rate), 2 )

         else:
          payment={
                        "payment_cents":int(round(float(self.Win_Pay.entry.get())*100)) ,
                        "method_id": methodId,
                        "value_usd_cents": int(round((float(self.Win_Pay.entry.get())/self.rate)*100))
                   }
          self.total_bs-=payment["payment_cents"]/100
          self.total_usd-=payment["value_usd_cents"]/100

         self.payment_list.append(payment)
         self.total_usdLabel.configure(text=f"Ref.{self.total_usd} \tBs {self.total_bs}")


         if self.total_usd<=0:
              self.commitSale.configure(state="normal")

         if self.Win_Pay is not None:
              self.Win_Pay.destroy()
# payment_cent, customer_def,  products_list, totalref_cent, rate_snapshot_cent
    def submitSaleDB(self):
         SubmitSale(self.payment_list, self.customer, self.product_list, self.totalref_cent, self.rate_snapshot_cent)
         self.master_reference.DrawNewSale()
         #reiniciar la venta i guess

    def buildClient(self):
        self.frame_client.columnconfigure(0, weight=0)
        self.frame_client.columnconfigure(1 , weight=1)

        
        self.entryClient=customtkinter.CTkEntry(self.frame_client, placeholder_text="Ingrese la CI del cliente.")
        self.entryClient.grid(column=1, row=0, padx=10, pady=(10,0),sticky="ew")
        self.prodBtn=customtkinter.CTkButton(self.frame_client, text="Siguiente", command=self.productStep)
        self.prodBtn.grid(column=1, row=1, padx=10, pady=(10,0), sticky="ew")

        self.feedbackClient=customtkinter.CTkLabel(self.frame_client, text="")
        self.feedbackClient.grid(column=1, row=2, padx=10, pady=(10,0), sticky="ew")

    def buildProduct(self):
        self.frame_product.columnconfigure(0, weight=0)
        self.frame_product.columnconfigure(1 , weight=1)

        self.backClientBtn=customtkinter.CTkButton(self.frame_product, text="<-", command=self.showClientFrame)
        self.backClientBtn.grid(column=0, row=0, padx=10, pady=10, sticky="ew")

        self.entryProduct=customtkinter.CTkEntry(self.frame_product, placeholder_text="Busca los productos que quieres añadir al carrito")
        self.entryProduct.grid(column=1, row=1, padx=10, pady=(10,0),sticky="ew")
        self.entryProduct.bind("<KeyRelease>", self.searchProduct)
        self.label_List=[]

        self.search_results_frame = customtkinter.CTkFrame(self.frame_product)
        

        for  i, label in enumerate(self.product_list):
            self.genLabel=customtkinter.CTkLabel(self.frame_product, text=label["product_name"])
            self.genLabel.grid(column=1,row=i+7, padx=10, pady=(10,0), sticky="ew")
            self.label_List.append(self.genLabel)

        self.totalLabel=customtkinter.CTkLabel(self, text="")
        self.total_usdLabel=customtkinter.CTkLabel(self, text="")
        self.totalLabel.grid(column=0, row=len(self.product_list)+7, padx=10, pady=10, sticky="ew")
        self.total_usdLabel.grid(column=0, row=len(self.product_list)+8, padx=10, pady=10, sticky="ew")
        

        self.labelClient=customtkinter.CTkLabel(self, text="")
        self.labelClient.grid(column=1, row=len(self.product_list)+7, padx=10, pady=(10,0), sticky="ew")
        
        self.payBtn=customtkinter.CTkButton(self.frame_product, text="Pagar", command=self.showPaymentFrame)
        self.payBtn.grid(column=1, row=len(self.product_list)+8, padx=10, pady=(10,0) ,sticky="ew", columnspan=2)

    def buildPayment(self):
        self.total_usd=0
        self.total_bs=0

        self.frame_payment.columnconfigure((1, 2) , weight=1)
        self.frame_payment.rowconfigure((1,2), weight=1)

        self.backProductsBtn=customtkinter.CTkButton(self.frame_payment, text="<-", command=self.showProductFrame)
        self.backProductsBtn.grid(column=0, row=0, padx=10, pady=10, sticky="ew")

        self.pagomovilBtn=customtkinter.CTkButton(self.frame_payment, text="Pagomovil", command= lambda  :self.DiscountPay(4))
        self.pagomovilBtn.grid(column=1,row=1, padx=10, pady=(10,0), sticky="nsew")
        self.cashDollarBtn=customtkinter.CTkButton(self.frame_payment, text="Dolares Efectivo", command=lambda : self.DiscountPay(1))
        self.cashDollarBtn.grid(column=1,row=2, padx=10, pady=(10,0), sticky="nsew")
        self.cashBsBtn=customtkinter.CTkButton(self.frame_payment, text="Bolivares efectivo", command= lambda : self.DiscountPay(3))
        self.cashBsBtn.grid(column=2,row=1, padx=10, pady=(10,0), sticky="nsew")
        self.debitBtn=customtkinter.CTkButton(self.frame_payment, text="Debito/Credito",  command= lambda : self.DiscountPay(2))
        self.debitBtn.grid(column=2,row=2, padx=10, pady=(10,0), sticky="nsew")

        self.commitSale=customtkinter.CTkButton(self.frame_payment, text="Terminar venta", state="disabled", command= self.submitSaleDB)
        self.commitSale.grid(column=1, row=3, padx=10, pady=(10,0), columnspan=2, sticky="ew")

class DisplayDailyReport(customtkinter.CTkFrame):
    def __init__(self, master):
          super().__init__(master)

          self.columnconfigure(0 , weight=1)


          self.DailySales_DicList=GetDailySales()
          self.float_Total, self.floatBs, self.floatUsd=makeDailyReport(self.DailySales_DicList)

          self.scrollableFrame=customtkinter.CTkScrollableFrame(self)

          self.title=customtkinter.CTkLabel(self, text=" Reporte diario.")
          self.title.grid(column=0, row=0, pady=10, padx=10, sticky="nsew")
          self.buildFrame()
          self.scrollableFrame.grid(column=0, row=1, pady=10, padx=10, sticky="nsew")
          self.totalLabel=customtkinter.CTkLabel(self, text="TOTAL: ")


    def buildFrame(self):
          if not self.DailySales_DicList:
               
               return
          
          for i, sale in enumerate(self.DailySales_DicList):
               label=customtkinter.CTkLabel(self.scrollableFrame, text=f"VENTA total: {sale["sales_total_cent_usd"]}$ Vuelto: {sale["sales_change_cent_bs"]}Bs {sale["sales_change_cent_usd"]}$ Tasa:{sale["sales_rate_cent_bs"]}.Bs")
               label.grid(column=0, row=i, padx=10, pady=10, sticky="ew")



          




     
class App(customtkinter.CTk):

    def __init__(self):
          super().__init__()


          self.actual_page=1

          self.columnconfigure((0), weight=0)
          self.columnconfigure((1), weight=1)

          self.rowconfigure(0, weight=1)

          self.title("Prueba de generación")
          self.geometry("1000x500")

          self.menu=Win_Options(self, "Test App")
          self.menu.grid(column=0, row=0,sticky="nsew")

          
          self.actual_frame=None #Debemos declarar variables para que existan hp

          self.addProdWin=None
          self.addSaleWin=None
          self.editProdWin=None

          self.messageWin=None

          tbcv_dia=0
          tpll_dia=0
          tprm_dia=0 
          teuro=0 
          dateString=""
          self.defaultRate=0

          self.updateRate(tbcv_dia, tpll_dia, tprm_dia,teuro, dateString)
          

    def updateRate(self, tbcv_dia, tpll_dia, tprm_dia,teuro, dateString):
          try:
                        #display a label showing rates are loading
                        self.menu.BCV_label.configure(text="Cargando...")
                        self.menu.EUR_label.configure(text="Cargando...")
                        tbcv_dia, tpll_dia, tprm_dia, teuro, dateString=GetRates()
                        #print(f"{tbcv_dia}\t{teuro}\t{dateString}")

                        if not tbcv_dia or not teuro:
                             raise AttributeError
                        else:
                             self.menu.date.configure(text=f"{dateString[0:10]}")
                             self.menu.BCV_label.configure(text=f"BCV: {tbcv_dia} Bs")
                             self.menu.EUR_label.configure(text=f"Euro: {teuro} Bs")
                             #display a label showing the rates
                             self.defaultRate=tbcv_dia
          except AttributeError as e:
                      #print(e)
                      if self.messageWin is None or self.messageWin.winfo_exists():
                                      self.messageWin=Win_Message(self, "ERROR!", "No se encontraron tasas para trabajar")
                                      self.messageWin.after(100, self.messageWin.lift)
                                      self.messageWin.after(100, self.messageWin.focus_force)
                                      
                      else:
                                      self.messageWin.lift
                                      self.messageWin.focus_force
         
    

#----------CLEAN AND DRAW FRAME FUNCTIONS----------
#FUNCTIONS THAT DRAW, CLEAN OR MODIFY A FRAME OF ANY TYPE IN ANY WAY.
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

    def DrawNewSale(self):
        self.CleanFrame()
        self.actual_frame=1
        self.actual_frame=DisplayNewSale(self, self.defaultRate)
        self.actual_frame.grid(row=0, column=1, padx=10, pady=(0,10), sticky="nsew")
    
    def DrawDailyReport(self):
         self.CleanFrame()
         self.actual_frame=1
         self.actual_frame=DisplayDailyReport(self)
         self.actual_frame.grid(row=0, column=1, padx=10, pady=(0,10), sticky="nsew")

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

#-----------WINDOW RELATED FUNCTIONS-----------
#FUNCTIONS THAT MAINLY MANAGE TO OPEN A WINDOW OF A TOPLEVEL WINDOW CLASS

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
              self.addSaleWin= Win_NewSale(self)
              self.addSaleWin.after(100, self.addSaleWin.lift)        # Fuerza a subir en la pila de ventanas
              self.addSaleWin.after(200, self.addSaleWin.focus_force) # Fuerza el foco del sistema operativo
         else: 
              self.addSaleWin.lift()          # Trae al frente si ya existía
              self.addSaleWin.focus_force()   # Fuerza el foco de inmediato

if __name__=="__main__":
 

 Miapp=App()
 Miapp.mainloop()