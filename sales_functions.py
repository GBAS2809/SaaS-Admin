import psycopg
from psycopg.rows import dict_row
import os
from dotenv import load_dotenv
load_dotenv()

conninfo = f"dbname={os.getenv('DB_NAME')} user={os.getenv('DB_TABLES_USER')} password={os.getenv('DB_TABLES_PASS')} host={os.getenv('DB_HOST')}"


#Submit Sale is in charge of submitting all the info in the tables Sales, details_sales, pay sales. Therefore it updates the stock
#Substracting the sold products
def SubmitSale(payment_cent, customer_def,  products_list, totalref_cent, rate_snapshot_cent):

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


#ESTA FUNCION DA EL CIERRE DE HOY
#Devuelve todas las ventas y el cierre total. Da el cierre total.
def GetDailyReport():
    with psycopg.connect(conninfo, row_factory=dict_row) as conn:
        with conn.cursor() as cur:

            cur.execute(""" SELECT sales.sales_id, sales.sales_rate_cent_bs, sales.sales_total_cent_usd,
                        sales.sales_change_cent_bs, sales.sales_change_cent_usd
                        FROM sales
                        WHERE sales_day= CURRENT_DATE
                        ORDER BY sales_id DESC
                        """)
            
            datadicc=cur.fetchall()

            if datadicc== None:
                print("\n\tNo hay ventas.\n")
                return
            
            float_total_day=0
            float_bs=0
            float_usd=0
            
            
            for n in datadicc:

                cur.execute(""" SELECT pay_sales.payment_cents, pay_sales.method_id
                            FROM pay_sales
                            WHERE sales_id= %s""", (n['sales_id'], ))
                res=cur.fetchall()
                for i in res:
                    if i['method_id']==2 or i['method_id']==3 or i['method_id']==4:
                        
                        float_bs+=(float(i['payment_cents'])/100)
                    else:
                        float_usd+=int(i['payment_cents']/100)
                      
                

                n['sales_rate_cent_bs']/=100
                n['sales_total_cent_usd']/=100
                n['sales_change_cent_bs']/=100
                n['sales_change_cent_usd']/=100



                float_total_day+=n['sales_total_cent_usd']

            

            return datadicc, round(float_total_day, 2), round(float_bs, 2), float_usd

                

#ESTA FUNCION TE DEVUELVE TODAS LAS VENTAS HECHAS HISTORICAMENTE
def ReadSales(page, quantity=50):

    offset=(page-1)*quantity
    with psycopg.connect(conninfo, row_factory=dict_row) as conn:
        with conn.cursor() as cur:
            cur.execute("""SELECT sales.sales_day, sales.sales_id, sales.sales_rate_cent_bs, sales.sales_total_cent_usd,
                        sales.sales_change_cent_bs, sales.sales_change_cent_usd
                        FROM sales
                        ORDER BY sales_id DESC
                        LIMIT %s OFFSET %s
                        """, (quantity, offset))
            
            
            return cur.fetchall()
        
##---IMPORTANTE---
##Debo aplicar un JOIN para sacar todos los datos de un solo golpe, ver como
##CARAJOS se hace y funciona eso.
##¿que quiero imprimir? el total, las cosas que se vendieron, como se pagó y a quienes se vendieron.
##la tasa

#Obtener los pagos y detalles de pago.
#Entra el id de una venta y sale una lista de diccionarios, con los detalles del pago.
def GetPay(sales_id):

    with psycopg.connect(conninfo, row_factory=dict_row) as conn:
        with conn.cursor() as cur:

            cur.execute("""SELECT  payment_cents, value_usd_cents, pay_methods.method_name
                        FROM pay_sales
                        JOIN pay_methods ON pay_sales.method_id=pay_methods.method_id
                        WHERE sales_id=%s""", (sales_id, ))
            

            lista=cur.fetchall()
            return lista 


#Obtener los detalles de la venta.
def GetDetails(sales_id):

    with psycopg.connect(conninfo, row_factory=dict_row) as conn:
        with conn.cursor() as cur:
            cur.execute("""SELECT detail_sales.number_sold, detail_sales.product_price, products.product_name
                        FROM detail_sales
                        JOIN products ON detail_sales.product_id=products.product_id
                        WHERE sales_id= %s """, (sales_id, ))
            
            detalles=cur.fetchall()
            return detalles


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
    