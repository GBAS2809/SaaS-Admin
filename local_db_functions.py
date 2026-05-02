import psycopg
import os
from dotenv import load_dotenv

load_dotenv()
createinfo = f"dbname={os.getenv('DB_NAME')} user={os.getenv('DB_CREATE_USER')} password={os.getenv('DB_CREATE_PASS')} host={os.getenv('DB_HOST')}"


#Tables Integrity inicializes the tables if doesn't exist.
#The tables are normalized so if two tables refers to the same thing, they use the same name.
def TablesIntegrity():

    with psycopg.connect(createinfo) as conn:
        with conn.cursor() as cur:

            #For customers it is added id, type of the id document, the id document, first and last name, and address. 
            cur.execute(""" 
                        CREATE TABLE IF NOT EXISTS customers(
                        customer_id SERIAL NOT NULL PRIMARY KEY,
                        type_document CHARACTER(1) NOT NULL,
                        id_document INTEGER NOT NULL UNIQUE,
                        name_customer TEXT NOT NULL,
                        address VARCHAR(60))""")
            
            #Products holds price, cost, stock, demand on week, and barcode 
            cur.execute("""
                        CREATE TABLE IF NOT EXISTS products(
	                    product_id SERIAL NOT NULL PRIMARY KEY,
	                    product_name TEXT NOT NULL,
	                    product_stock INTEGER,
	                    product_price INTEGER NOT NULL,
	                    product_cost INTEGER DEFAULT 0,
	                    product_demand_week	INTEGER DEFAULT 0,
	                    product_category VARCHAR(50) DEFAULT 'general',
                        product_sinc INTEGER DEFAULT 0,
                        is_active BOOL DEFAULT true,
                        product_barcode VARCHAR(20) UNIQUE)""")
            
            #Sales 
            cur.execute("""
                        CREATE TABLE IF NOT EXISTS sales(
                        sales_id SERIAL NOT NULL PRIMARY KEY,
                        sales_day date not null,
                        sales_rate_cent_bs INTEGER NOT NULL DEFAULT 0,
                        sales_total_cent_usd INTEGER NOT NULL DEFAULT 0,
                        sales_change_cent_bs INTEGER NOT NULL DEFAULT 0,
                        sales_change_cent_usd INTEGER NOT NULL DEFAULT 0,
                        customer_id INTEGER NOT NULL,
                        FOREIGN KEY(customer_id) REFERENCES customers(customer_id))""")
            #rate is used for the daily used rate 
            #change_usd and bs is for cash change.
            #total_cent usd and bs is for whole sale. either in Usd or bs
            cur.execute(""" 
                        CREATE TABLE IF NOT EXISTS detail_sales(
                        detail_id SERIAL NOT NULL PRIMARY KEY,
                        product_id INTEGER NOT NULL,
                        sales_id INTEGER NOT NULL,
                        number_sold INTEGER NOT NULL,
                        product_price INTEGER NOT NULL,
                        FOREIGN KEY(product_id) REFERENCES products(product_id),
                        FOREIGN KEY(sales_id) REFERENCES sales(sales_id))""")
            

            cur.execute("""CREATE TABLE IF NOT EXISTS pay_methods(
                        method_id SERIAL NOT NULL PRIMARY KEY,
                        method_name TEXT NOT NULL,
                        method_currency TEXT)""")
            #rate_cent_usd es la tasa de cambio usada para la venta, puede ser la que sea
            #npro is for number products sold
            #prod_price es para no descuadrar los libros de ventas si el precio del producto cambia referenciado en usd
            cur.execute("""
                        CREATE TABLE IF NOT EXISTS pay_sales(
                        payment_id SERIAL NOT NULL PRIMARY KEY,
                        payment_cents INTEGER NOT NULL,
                        sales_id INTEGER NOT NULL,
                        value_usd_cents INTEGER,
                        method_id INTEGER,
                        FOREIGN KEY (method_id) REFERENCES pay_methods(method_id),
                        FOREIGN KEY(sales_id) REFERENCES sales(sales_id))""")
          
            
#Insert Methods inserts the methods only if are not inserted.
def InsertMethods():
    with psycopg.connect(createinfo) as conn:
        with conn.cursor() as cur:
            cur.execute("""  INSERT INTO pay_methods(method_id, method_name, method_currency)
                   SELECT 1, 'efectivo_usd', 'USD'
                   WHERE NOT EXISTS(
                   SELECT 1 FROM pay_methods WHERE method_id =1 );""")
            cur.execute("""  INSERT INTO pay_methods(method_id, method_name, method_currency)
                   SELECT 2, 'debito_bs', 'BS' 
                   WHERE NOT EXISTS(
                   SELECT 2 FROM pay_methods WHERE method_id =2 );""")
            cur.execute("""  INSERT INTO pay_methods(method_id, method_name, method_currency)
                   SELECT 3, 'efectivo_bs', 'BS' 
                   WHERE NOT EXISTS(
                   SELECT 3 FROM pay_methods WHERE method_id =3 );""")
            cur.execute("""  INSERT INTO pay_methods(method_id, method_name, method_currency)
                   SELECT 4, 'pagomovil', 'BS' 
                   WHERE NOT EXISTS(
                   SELECT 4 FROM pay_methods WHERE method_id =4 );""")
            cur.execute(""" INSERT INTO pay_methods( method_id, method_name, method_currency)
                   SELECT 5 , 'zelle', 'USD'
                   WHERE NOT EXISTS (
                   SELECT 5 FROM pay_methods WHERE method_id=5)""")

if __name__=="__main__":

    try:
        TablesIntegrity()
        print("tablas añadidas")
        InsertMethods()
        print("metodos insertados")
    except Exception as e:
        print(f"Error al inicializar las tablas. Revisa:\n\t {e}")
        exit()
    try:
        InsertMethods()
        print("metodos insertados")
    except Exception as e:
        print(f"Error al insertar los métodos de pago. Revisa:\n\t{e}")
        exit()

    print("revisa postgres todo deberia estar bien")




