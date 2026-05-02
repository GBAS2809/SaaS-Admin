import psycopg
from psycopg.rows import dict_row
import os
from dotenv import load_dotenv
load_dotenv()

conninfo = f"dbname={os.getenv('DB_NAME')} user={os.getenv('DB_TABLES_USER')} password={os.getenv('DB_TABLES_PASS')} host={os.getenv('DB_HOST')}"
#DEBO LIMPIAR ESTA PARTE

#Looks for a customer in the DB by the Id Document, this case a CI. If the Customer does not exist returns false.
def GetCustomer(id_document):

    with psycopg.connect(conninfo, row_factory=dict_row) as conn:
        with conn.cursor() as cur:

            result=cur.execute("""SELECT customer_id, name_customer  FROM customers
                   WHERE id_document= %s
                            """, (id_document, ))
            
            fila=result.fetchone()
            if fila== None:
                #print("\n\tEL cliente no existe.")
                return False
            else: 
                
                return fila
            

#Makes charge of commit all data for a new customer, from a dictionary.
def AddCustomer(customer_dict):

    with psycopg.connect(conninfo) as conn:
        with conn.cursor() as cur:

            cur.execute("""INSERT INTO customers(id_document, name_customer, type_document, address)
                   VALUES ( %s, %s, %s, %s)
                   """,( customer_dict['id_document'], customer_dict['name_customer'], customer_dict['type_document'], customer_dict['address']))
            
            



