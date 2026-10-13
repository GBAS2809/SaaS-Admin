import psycopg
from psycopg.rows import dict_row
import os
from dotenv import load_dotenv
load_dotenv()

conninfo = f"dbname={os.getenv('DB_NAME')} user={os.getenv('DB_TABLES_USER')} password={os.getenv('DB_TABLES_PASS')} host={os.getenv('DB_HOST')} connect_timeout=3"

#------------------------DATA BASE RELATED FUNCTIONS------------------------
#EITHER THEY FETCH OR COMMIT DATA FROM THE DATABASE TO THE APP OR VICE VERSA


#Submit Sale is in charge of submitting all the info in the tables Sales, details_sales, pay sales. Therefore it updates the stock
#Substracting the sold products
def SubmitSale(payment_cent, customer_def,  products_list, totalref_cent, rate_snapshot_cent):
 try:

    with psycopg.connect(conninfo, row_factory=dict_row) as conn:
        with conn.cursor() as cur:

            cur.execute(""" INSERT INTO sales(customer_id, sales_total_cent_usd, sales_rate_cent_bs, sales_day)
                    VALUES (%s, %s, %s, CURRENT_DATE)
                    RETURNING sales_id;""", (customer_def['customer_id'], totalref_cent, rate_snapshot_cent))
            
            result=cur.fetchone()
            id_sale=result["sales_id"]

            for prod in products_list:
                cur.execute("""INSERT INTO detail_sales(sales_id, product_id, product_price, number_sold)
                       VALUES (%s, %s, %s, %s)""",(id_sale, prod['product_id'], int(prod['product_price']), prod['number_sold']))
                cur.execute("""UPDATE products
                       SET product_stock =product_stock -%s 
                       WHERE product_id= %s""", (prod['number_sold'], prod['product_id']))
                cur.execute("""SELECT product_stock from PRODUCTS
                       WHERE product_id=%s """, (prod['product_id'], ))
                
            for pay in payment_cent:   
                cur.execute("""INSERT INTO pay_sales(payment_cents, sales_id, method_id, value_usd_cents)
                        VALUES (%s, %s, %s, %s)""", (pay['payment_cents'], id_sale, pay['method_id'], pay['value_usd_cents']))
 except psycopg.OperationalError as e:
     return e


# UNABLES a sale, this may be handy for returns, delete sales or anything.      
def DeleteSale(sales_id):
 try:
    with psycopg.connect(conninfo) as conn:
        with conn.cursor() as cur:

            cur.execute(""" UPDATE sales
                       SET is_active = false
                       WHERE product_id= %s""", (sales_id, ))
 except psycopg.OperationalError:
    return

#ESTA FUNCION DA EL CIERRE DE HOY
#Devuelve todas las ventas y el cierre total. Da el cierre total.
def GetDailySales():
 try:
    with psycopg.connect(conninfo, row_factory=dict_row) as conn:
        with conn.cursor() as cur:

            cur.execute(""" SELECT sales.sales_id, sales.sales_rate_cent_bs, sales.sales_total_cent_usd,
                        sales.sales_change_cent_bs, sales.sales_change_cent_usd
                        FROM sales
                        WHERE sales_day= CURRENT_DATE
                        ORDER BY sales_id DESC
                        """)
            
            return cur.fetchall()

 except psycopg.OperationalError as e:
     return "NoDataBase" #RETURNS AN EMPTY LIST JUST IN CASE

#GETS THE DAILY SALES TO MAKE UP TO THE TOTAL SALES 
#Receive a dictionary list fetched from GetDailySales() it fetchs all the payments, and summarize all the sales to print the total amount
# of gross sales daily. The result is fetched in total, float numbers and it returns empty values if not exist
def makeDailyReport(dataDict):

    if dataDict== None:                                #ARREGLAR ESTA MIERDA!!!!!!!! 
                return                                 #que se supone que debo arreglar...?
            
    float_total_day=0
    float_bs=0
    float_usd=0

    try:

        with psycopg.connect(conninfo, row_factory=dict_row) as conn:
          with conn.cursor() as cur:

            for n in dataDict:

                cur.execute(""" SELECT pay_sales.payment_cents, pay_sales.method_id
                            FROM pay_sales
                            WHERE sales_id= %s""", (n['sales_id'], ))
                
                for i in cur.fetchall():

                    if i['method_id']==2 or i['method_id']==3 or i['method_id']==4:
                        
                        float_bs+=(float(i['payment_cents'])/100)
                    else:
                        float_usd+=int(i['payment_cents']/100)

                n['sales_rate_cent_bs']/=100
                n['sales_total_cent_usd']/=100
                n['sales_change_cent_bs']/=100
                n['sales_change_cent_usd']/=100

                float_total_day+=n['sales_total_cent_usd']

            return float(round(float_total_day, 2)), float(round(float_bs, 2)), float_usd

    except psycopg.OperationalError as e:
        return 0, 0, 0



#ESTA FUNCION TE DEVUELVE TODAS LAS VENTAS HECHAS HISTORICAMENTE
def ReadSales(page, quantity=50):

 offset=(page-1)*quantity
 try:
    with psycopg.connect(conninfo, row_factory=dict_row) as conn:
        with conn.cursor() as cur:
            cur.execute("""SELECT sales.sales_day, sales.sales_id, sales.sales_rate_cent_bs, sales.sales_total_cent_usd,
                        sales.sales_change_cent_bs, sales.sales_change_cent_usd
                        FROM sales
                        WHERE is_active = true
                        ORDER BY sales_id DESC
                        LIMIT %s OFFSET %s
                        """, (quantity, offset))
            
            return cur.fetchall()
 except psycopg.OperationalError:
    return [] #It returns an empty list just in case
        
##---IMPORTANTE---
##Debo aplicar un JOIN para sacar todos los datos de un solo golpe, ver como
##CARAJOS se hace y funciona eso.
##¿que quiero imprimir? el total, las cosas que se vendieron, como se pagó y a quienes se vendieron.
##la tasa

#Obtener los pagos y detalles de pago.
#Entra el id de una venta y sale una lista de diccionarios, con los detalles del pago.
def GetPay(sales_id):
 try:

    with psycopg.connect(conninfo, row_factory=dict_row) as conn:
        with conn.cursor() as cur:

            cur.execute("""SELECT  payment_cents, value_usd_cents, pay_methods.method_name
                        FROM pay_sales
                        JOIN pay_methods ON pay_sales.method_id=pay_methods.method_id
                        WHERE sales_id=%s""", (sales_id, ))
            
            return cur.fetchall() 
 except psycopg.OperationalError:
    return [] #Returns an empty list just in case

def getLastIDSales():
   try: 
         with psycopg.connect(conninfo, row_factory=dict_row) as conn:
            with conn.cursor() as cur:
               cur.execute(""" SELECT MAX(sales_id) FROM sales""" )
               
               return cur.fetchone()
   except psycopg.OperationalError as e:
         return 0
   
#Obtener los detalles de la venta.
def GetDetails(sales_id):
 try:

    with psycopg.connect(conninfo, row_factory=dict_row) as conn:
        with conn.cursor() as cur:
            cur.execute("""SELECT detail_sales.number_sold, detail_sales.product_price, products.product_name
                        FROM detail_sales
                        JOIN products ON detail_sales.product_id=products.product_id
                        WHERE sales_id= %s """, (sales_id, ))
            
            
            return cur.fetchall()
 except psycopg.OperationalError as e:
    return [] #Returns an empty list just in case 


#------------------------CLEANING INFO RELATED FUNCTIONS------------------------
#FUNCTIONS TO USE WHEN PASSING AN ARGUMENT FROM ONE KIND OF VARIABLE TO ANOTHER TYPE
#OR NOT RELATED TO DATA BASE

#THIS FUNCTION TAKES ALL THE ARGUMENTS ON THE SALES DICCIONARIES FETCHED FROM DATABASE AND TURN THEM INTO FLOAT
# VALUES: Rate, total on usd, change in bs, change in usd
def turnIntoFloat(dataDictList):
   for D in dataDictList:
      
      if D["sales_rate_cent_bs"]:
            D["sales_rate_cent_bs"]/=100
      else: 
         D["sales_rate_cent_bs"]=0

      if D["sales_total_cent_usd"] :
            D["sales_total_cent_usd"] /=100
      else: 
         D["sales_total_cent_usd"]=0

      if D["sales_change_cent_bs"] :
            D["sales_change_cent_bs"] /=100
      else: 
         D["sales_change_cent_bs"]=0

      if D["sales_change_cent_usd"] :
            D["sales_change_cent_usd"] /=100
      else: 
         D["sales_change_cent_usd"]=0
   
   return dataDictList
      
      
      
   
    
def Create_Payment_Dicc(pay, id_method, value_usd_cent):

    payment={
        "payment_cents": pay,
        "method_id": id_method,
        "value_usd_cents": value_usd_cent
    }
    return payment


#Takes a sale list of dictionaries and prepares the date and money ammounts into floats so you can print them.
def MakeDictSale(dict_sales_list):

  for n in dict_sales_list:
    
    if n['sales_day']:
        date_date=n['sales_day']
        n['sales_day']=date_date.strftime("%d/ %m/ %Y")

    n['sales_rate_cent_bs']/=100
    n['sales_total_cent_usd']/=100
    
    if n['sales_change_cent_bs']:
      n['sales_change_cent_bs']/=100

    if n['sales_change_cent_usd']:
      n['sales_change_cent_usd']/=100

  return dict_sales_list



#Takes a list of products and the prices to pass it all from floats to integers for the DB 
def CleanSale( products_list, total, tbcv_dia, payments):

    products_list_cents=[]
    payments_list_cents=[]

    rate_snapshot_cents=(int(round(float(tbcv_dia)*100)))
    total_cents=(int(round(float(total)*100)))

    for n in products_list:

        products_dictionary={"product_id":(int(round(float(n['product_id'])*100))),
                     "product_price":(int(round(float(n['product_price'])*100))),
                     "number_sold": n['number_sold']
                     }
        products_list_cents.append(products_dictionary)

    for n in payments:
        payments_dictionary={
            "payment_cents": (int(round(float((n['payment_cents'])*100)))),
            "method_id": 'method_id',
            "value_usd_cents": (int(round(float((n['value_usd_cents'])*100))))
        }
        payments_list_cents.append(payments_dictionary)
        
        

    return rate_snapshot_cents, total_cents, products_list_cents, payments_list_cents
    