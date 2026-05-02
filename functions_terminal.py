#Aqui haré las funciones del backend
#las funciones que se van a comunicar con el frontend.
#La funcion para recibir datos y convertirlos a un diccionario 
#
#
#
#
# crearventa() va a abrir la venta para poder ser visualizada y gestionada  antes del pago
# aquí se ingresan los productos, clientes y toda la informacion necesaria para generar una venta 

# cerrarventa() solo se encarga de pasar la informacion de python a informacion de database. 
# Para cerrar la venta y realizar el respectivo commit
#

#hace los datos en un diccionario tipo producto con el precio en cents para guardar en el db

#sale es una lista de diccionario con la informacion de los productos a guardar, nombre precio en divisas
#customer es un diccionario con la informacion del cliente

#customer { 'id_document' , 'name' , 'id_customer' }
def AskCustomer(CI):

  nombre_string=input("Ingrese el nombre y apellido del cliente")
  address_string=input("Zona de residencia")
  type_document=input("Ingrese tipo de documento V- J-")
  if not CI:
    while True:
      try:
       int_CI=int(input("Ingrese cedula del cliente"))
       if(int_CI<0):
        raise ValueError
       CI=int_CI
       break
      except ValueError:
       print("valor invalido")
    
  customer_definition={
  "id_document": CI,
  "name_customer": nombre_string,
  "type_document": type_document,
  "address": address_string
  } 
  return customer_definition
    

    



from cust_db_functions import GetCustomer, AddCustomer


def AskProduct():
 
 name_product=input("Ingrese nombre del producto:\t")
 while True:
  try:
   int_stock=int(input("Ingrese el stock actual:\t"))
   if int_stock <=0:
     raise ValueError
   break
  except ValueError:
    print("ERROR valor invalido intente de nuevo.")

 while True:
  try:
   float_price=float(input("Ingrese precio del producto:\t"))
   if float_price <=0:
     raise ValueError
   break
  except ValueError:
     print("ERROR intenta de nuevo ")

 while True:
    try:
      float_cost=float(input("Ingrese la costo del producto:\t"))
      if float_cost <0:
        raise ValueError
      break
    except ValueError:
      print("ERROR: El costo debe ser numérico y no negativo.")

 string_category=input("Ingrese una categoria del producto:\t")

 return name_product, float_price, int_stock, float_cost, string_category
       
def AskID():
  while True: 
     try:
       product_id=int(input("Ingrese el id de la operación:\t"))
       if product_id <=0:
         raise ValueError
       break
     except ValueError:
       print("El id debe ser mayor a 0 y positivo.\n")
  return product_id

#payment es un diccionario que deberia contener monto y forma de pago
# { 'efectivo_usd': int, 'efectivo_bs':int, 'debito': float, 'pagomovil': float, 'zelle': float}
#price_usd es el precio total de la venta reflejado en BS



#Makes a dictionary that can be further used in add at the data base, with all data base labels
def MakeDictProduct_DB(string_name, int_stock, float_price, float_cost, string_category):
    
    if (string_name!= None) and (float_price !=None) and (int_stock != None):
     price_cent=(int(round(float(float_price)*100)))
     cost_cent=(int(round(float(float_cost)*100)))

     datos_dicc={"product_name": string_name.strip(),
                "product_price": price_cent, 
                "product_stock": int_stock, 
                "product_cost": cost_cent, 
                "product_category": string_category
                      }
     return datos_dicc
    
    else: return None


#Takes a generic dictionary with database integers, then looks for integer values and chages them to floats for python 
#Modify to make it work with all project keys. Price, cost, total, rates, change_usd, change_bs.
def TurnIntoFloat(Inventario):
  for prod in Inventario:
    prod['product_price']=prod['product_price']/100
    prod['product_cost']=prod['product_cost']/100
  return Inventario






from cust_db_functions import GetCustomer, AddCustomer
from crud_products import GetPrice

#Ask everything and fetchs it all for customer management.
def AskCustomerForTerminal():
  
    CI=int(input("Ingrese la cedula del cliente."))
    idcustomer=GetCustomer(CI)

    while(idcustomer==False):
      customerinfo=AskCustomer(CI)
      
      if customerinfo:
        AddCustomer(customerinfo)
        print(f"\n\t-----INFO CLIENTE-----\n\tNombre: {idcustomer["name_customer"]}\tCI:{CI}\n")
        return customerinfo
        
    
    print(f"\n\t-----INFO CLIENTE-----\n\tNombre: {idcustomer["name_customer"]}\tCI:{CI}\n")
  
    return idcustomer



def AskSale():
  products_list=[]
  #total=0

  while True:

    print("Ingrese el ID del producto que se vendió")
    id=AskID()
    float_price=GetPrice(id)

    while True:
        try:
          number_sold=int(input("Cuantos vendiste del producto"))
          if number_sold<=0: 
            raise ValueError
          break
        except:
          print("Debe ser mayor a cero.")
      
    #total+=(number_sold*float_price)
    
    dicc={"product_id":id,
           "product_price":float_price,
           "number_sold": number_sold}
      
    products_list.append(dicc)
      
    ent=int(input("continuar? si=1 no=2"))
    if ent==2:
        break
  return products_list
  
  

def AskPayment(products_list, rate_bcv):
    payment_list = []
    float_total= 0
    
    # Calcular total
    for n in products_list:
        float_total += (n['number_sold'] * n['product_price'])
        
    to_pay = float_total
    
    print(f"\n\t---TOTAL A PAGAR: {float_total}$---")
    
    # Un solo bucle: Mientras haya deuda, seguimos cobrando.
    while to_pay > 0:
        print(f"\n\t[!] Faltan por pagar: {to_pay}$")
        print("""
            1) Efectivo Dolares
            2) Debito Bolivares
            3) Efectivo Bolivares
            4) Pagomovil
            5) Zelle""")
        
        int_method = int(input("\nInserte método de pago: "))
        # Cambiado a float para aceptar decimales en los pagos
        reference_usd = float(input("Indique cuánto paga referenciado en $: ")) 
        
        # Conversión a Bolívares si aplica
        if int_method in [2, 3, 4]:
            float_amount_paid = reference_usd * rate_bcv
        else:
            float_amount_paid = reference_usd

        # Crear diccionario del pago actual
        dictionary = {
            "payment_cents": float_amount_paid,
            "method_id": int_method,
            "value_usd_cents": reference_usd
        }
        
        payment_list.append(dictionary)
        
        # Restamos sin condiciones. Si paga de más, el restante queda negativo (eso es el vuelto).
        to_pay -= reference_usd 

    # El bucle termina naturalmente cuando restante es 0 o menor (saldo a favor).
    return payment_list, float_total


  
    


#submitsale(payment, customerdef, saledet, 20 ,43820)

    
      
    


    

