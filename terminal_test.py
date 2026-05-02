

#Cuerpo principal del sistema de inventario
Inventariodef=[
    {
   "product_name" : "Cuchilla de oster",
   "product_price" : 1400 ,
   "product_stock" : 0,
   "product_cost" : 0,
   "product_category" : "general"
  },
  {
   "product_name" : "Acople Oster",
   "product_price" :  500,
   "product_stock" : 40,
   "product_cost" : 0,
   "product_category" : "general"
   },
   {
    "product_name" : "Goma Ecko",
    "product_price" : 600,
    "product_stock" : 15,
   "product_cost" : 0,
   "product_category" : "general"
}
  
]
#datoscust ={ 'id_document', 'name', 'type_document', 'personaldata'}
customerdef={
  "customer_id": 1,
  "id_document": 31490509,
  "name_customer": "Gabriel Baez",
  "type_document": "V",
  "address": "El paraiso"
}
#payment de prueba
payment=[
{ "payment_cents":1500,
 "method_id":1,
 "value_usd_cents":1500
},
{"payment_cents":219100,
 "method_id":2,
 "value_usd_cents":500
}
]

#saledet { 'id' , 'unitprice' , 'quantity'}
saledet=[
  {"product_id":1,
   "product_price":1400,
   "number_sold": 1
  }, {"product_id":3,
   "product_price":600,
   "number_sold": 1
  }
]



#Esta funcion va a subir una venta preestablecida con la fecha de hoy para las pruebas
def submittestsale(snaprate, customer):
  five=(snaprate*5)
  #payment de pruebas dinamico, cambia según la tasa del dia.
  paymentdaily=[
    { "payment_cents":1500,
     "method_id":1,
     "value_usd_cents":1500
     },
     {"payment_cents":five*100,
      "method_id":2,
      "value_usd_cents":500
      }
      ]
  saledet=[
  {"product_id":1,
   "product_price":1400,
   "number_sold": 1
  }, {"product_id":3,
   "product_price":600,
   "number_sold": 1
  }
  ]
  snaprate_cent=int(round(float(snaprate)*100))
  
  totalref=0
  for n in paymentdaily:
    totalref+=n['value_usd_cents']

  SubmitSale(paymentdaily, customer,  saledet, totalref, snaprate_cent)

#Esta funcion imprime el inventario en la consola del terminal
def PrintInventory(Inventario):
    
    print("\n\t--- REPORTE DE INVENTARIO ---\n")
    for prod in Inventario:
     print(f"""--\tID: {prod['product_id']}\t{prod['product_name']} \tPrecio:{prod['product_price']}$ \tStock:{prod['product_stock']}\n\t
           """)
#Esta funcion imprime las ventas en la consola del terminal
def PrintSales(sales):
  print("\n\t--- REPORTE DE VENTAS ---\n")
  
  for n in sales:
    
    print(f"""\n--\tID venta: {n['sales_id']}\t{n['sales_day']}\t{n['sales_rate_cent_bs']}\n
          Total: {n['sales_total_cent_usd']}$\tVuelto: {n['sales_change_cent_usd']}$, Bs. {n['sales_change_cent_bs']}\n 
          """)

def PrintDetails(details, payments):

  print("\n\t---Metodos de pago---")
  for n in payments:
       print(f"""\n\t{n['method_name']}:\t{n['payment_cents']/100}""")
       print("\n\t---Productos Vendidos---\n\tProducto\tCant.\tPrecio Uni.\tTotal")
  for n in details:
       print(f"""\n\t{n['product_name']}\t {n['number_sold']} X {n['product_price']/100}\t{n['number_sold']*(n['product_price']/100)}""")
       pauseclean()

def PrintDailyReport(salesDiccList, float_totalsold, float_bs, float_usd):
  print("\n\t------REPORTE DIARIO------")

  for n in salesDiccList:
    print(f"""\t\t-----------------------\n
          \t{n['sales_id']}).\tTasa:{n['sales_rate_cent_bs']}\tTotal venta:{n['sales_total_cent_usd']}\n
          Cambio: \tBs.{n['sales_change_cent_bs']}\t{n['sales_change_cent_usd']}$
\t\t-----------------------
""")
  print(f"Total Vendido al dia: {float_totalsold}$\n\tPagados:Bs.{float_bs}\t{float_usd}$")

import os 
#Esto es solo para pausar el sistema
def pauseclean():
  os.system('pause')
  os.system('cls')
#Esta funcion limpia la consola del terminal
def clean():
  os.system('cls')

from local_db_functions import TablesIntegrity,  InsertMethods
from cust_db_functions import AddCustomer, GetCustomer
from crud_products import AddProduct, EditProduct, DeleteProduct, ReadProducts, IsDeleted
from sales_functions import ReadSales, SubmitSale, GetPay, GetDetails, MakeDictSale, CleanSale, GetDailyReport
from functions_terminal import  AskProduct, AskID, MakeDictProduct_DB, AskPayment , AskCustomerForTerminal, AskSale, TurnIntoFloat
from rate_engine import GetRates

TablesIntegrity()
InsertMethods()
try:
 print("\n\tActualizando las tasas del dia...\n\t")
 tbcv_dia, tpll_dia, tprm_dia, teuro, fecha=GetRates()
 if tbcv_dia==None or teuro==None:
   raise AttributeError
 else:
   print(f"""Tasas submited.\tUsando las siguientes tasas al cambio dia {fecha[0:10]}.\n
         \tTasa BCV dólar:\t{tbcv_dia}
         \tTasa BCV euro:\t{teuro}
         \tTasa paralelo:\t{tpll_dia}
         \tTasa promedio:\t{tprm_dia}
         """)
   pauseclean()
except AttributeError as e:
  print(f"No hay tasas para trabajar.")
  exit()

#!!!!!!!!!NOTA: LIMPIAR EL PUTO PERRO CODIGO ARCHIVO POR ARCHIVO SEGUN EL CODIGO LIMPIO PARA NO SER TAN DESASTROSO.
#voy a romper algo mrc estoy seguro, pero bueno es mejor a largo plazo hacerlo ya.

#AddProduct(Inventariodef[0])
#AddProduct(Inventariodef[1])
#AddProduct(Inventariodef[2])
#AddCustomer(customerdef)
#SubmitSale(payment, customerdef, saledet, 20 ,43820)
#submittestsale(tbcv_dia, customerdef)


while True:
 clean()
 print("\n\t---MENU PRINCIPAL---")
 print("Ingresar al inventario o al libro de ventas\n\t1) Inventario.\n\t2)Libro Diario.\n\t3)Nueva venta.\n\t4)Cierre del dia.")
 page=1
 while True:
   try:
     OP=int(input("Inserta la opcion 1/3:\t"))
     if OP !=1 and OP!=2 and OP!=3 and OP!=4:
       raise ValueError
     break
   except ValueError:
     print("Valor invalido\n")
 while OP==4:
   
   salesDiccList, float_totalsold, float_bs, float_usd=GetDailyReport()
   if salesDiccList!=None:
     PrintDailyReport(salesDiccList, float_totalsold, float_bs, float_usd)
     
   pauseclean()
   OP=0
   break

 while OP==3:
  while True:
   try:
     customerdef=AskCustomerForTerminal()
     
     salesdetails=AskSale()
     
     payments, float_total=AskPayment(salesdetails,tbcv_dia)
     
     rate_snapshot_cents, total_cents, saledet_cents, payment_cents=CleanSale(salesdetails, float_total, tbcv_dia, payments)
     
     SubmitSale(payment_cents, customerdef, saledet_cents, total_cents ,rate_snapshot_cents)
     

     ent=int(input("continuar? si=1 no=2"))
     if ent==2:
        OP=0
        break
   except BaseException as e:
     print(f"Error mrc no se estoy cansado: {e}")
   #Gr33cc02809*#$$
 while OP==2:
   
   clean()
   print("\n\t\t---LIBRO DIARIO---\n")
   print("\n\t\t---Página ---\n")
   datos=ReadSales(page)
   
   salespy=MakeDictSale(datos)
  
   PrintSales(salespy)
   while True:
     try:
       case=int(input("\n\t¿Siguiente página? si\\1"))

       if case<=0 or case>=4 : raise ValueError
       break
     except ValueError:
       print("Valor inválido")


   while True:
     try:
       det=int(input("\n\n\t ¿Te gustaría tener los detalles de una venta? \n1=si, 2=no"))
       if det<=0 or det>=3: raise ValueError
       break
     except ValueError:
       print("opcion invalida")

   if det==1:
     
     id=AskID()
     payments=GetPay(id)
     details=GetDetails(id)
     PrintDetails(details, payments)

     

   elif det==2:
     OP=0
     break
    
 while OP==1:
  pauseclean()
  print(""" \n\n\t---Sistema de Inventario---\n
       \tIngrese por teclado una de las siguientes opciones numéricas\n
       \t1) Reporte del Inventario Total\n
       \t2) Añadir producto en el inventario\n
       \t3) Modificar productos al inventario\n
       \t4) Borrar Productos del inventario\n
       \t5) Ir al menú principal.\n\n\t
       """)
 
  while True:
   try:
    opcion=int(input("Introduzca una de las opciones"))
    if opcion<=0 or opcion>=6: raise ValueError
    break

   except ValueError:
    print("ERROR introduzca una opcion valida")

   #opcion 1 Reporte total del inventario
  if opcion==1:
    
     Inventario=ReadProducts()
     Inventariopy=TurnIntoFloat(Inventario)
     PrintInventory(Inventariopy)
     
 #opcion 2 añadir algo al inventario
  elif opcion==2:
      try:  

        name_product, price,stock, cost, category= AskProduct()
        prod=MakeDictProduct_DB(name_product, stock, price, cost, category)

        AddProduct(prod)
      except Exception as e:
        print(f"\n\terror {e}")

 #opcion 3 modificar valores de un productos existente
  elif opcion==3:
    Inventario=ReadProducts()
    Inventariopy=TurnIntoFloat(Inventario)
    PrintInventory(Inventariopy) 
   
   
    while True:

     id_product=AskID()
     bool_result=IsDeleted(id_product)
     if not bool_result:
       break
     print("\t\nEl producto no existe. Intente de nuevo\n")
     

    clean()
   
    print("Ingrese los nuevos datos para el producto:\n")    
    name_product, price,stock, cost, category= AskProduct()
    prod=MakeDictProduct_DB(name_product, stock, price, cost, category)
    EditProduct(prod, id_product)

   #opcion 4 borrar  un producto
  elif opcion==4:
    Inventario=ReadProducts()
    Inventariopy=TurnIntoFloat(Inventario)
    PrintInventory(Inventariopy)

    id_product=AskID()
    DeleteProduct(id_product)
  elif opcion==5:
    OP=0
    break 