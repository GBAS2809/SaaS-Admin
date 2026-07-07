import psycopg
from psycopg.rows import dict_row
import os
from dotenv import load_dotenv
load_dotenv()

conninfo = f"dbname={os.getenv('DB_NAME')} user={os.getenv('DB_TABLES_USER')} password={os.getenv('DB_TABLES_PASS')} host={os.getenv('DB_HOST')} connect_timeout=5"

#DEBO HACER UNA FUNCION CHECKSTOCK para hacer saltar una notificación en caso del que producto se acabe.

# AddProducts commits all the data to the database from a dictionary.
def AddProduct(product_dict):
 try:
    with psycopg.connect(conninfo) as conn:
        with conn.cursor() as cur:

            cur.execute("""INSERT INTO products(product_name, product_price, product_stock, product_cost, product_category)
                       VALUES (%s, %s, %s, %s, %s)
                       """,(product_dict["product_name"], product_dict["product_price"], product_dict["product_stock"],
                            product_dict["product_cost"], product_dict["product_category"]) )
 except psycopg.OperationalError as e:
     return None
            
# Updates the data of a product from a dictionary.
def EditProduct(product_dict, product_id):
 try:
    with psycopg.connect(conninfo) as conn:
        with conn.cursor() as cur:

            cur.execute(""" UPDATE products
                       SET product_name=%s, product_stock= %s, 
                       product_price= %s, product_cost= %s, product_category= %s
                       WHERE product_id= %s""",
                       (product_dict["product_name"], product_dict["product_stock"],
                        product_dict["product_price"], product_dict["product_cost"],
                        product_dict["product_category"], product_id))
 except psycopg.OperationalError as e:
     return []
     


# Deletes a product from the frontend. It only turns is_active to false            
def DeleteProduct(product_id):
 try:
    with psycopg.connect(conninfo) as conn:
        with conn.cursor() as cur:

            cur.execute(""" UPDATE products
                       SET is_active = false
                       WHERE product_id= %s""", (product_id, ))
 except psycopg.OperationalError:
    return None
# Fetchs the price on float, with the product id.
def GetPrice(product_id):
 try:
    with psycopg.connect(conninfo, row_factory=dict_row) as conn:
        with conn.cursor() as cur:
            cur.execute("""SELECT product_price
                        FROM products 
                        WHERE product_id= %s""", (product_id, ))
            
            result=cur.fetchone()
            price=result['product_price']/100

            return price
 except psycopg.OperationalError as e:
    return 0
# Checks if a product exists or is active from the frontend. If deleted or does not exist, returns true.
# If active, then returns false.
def IsDeleted(product_id):
 try:
    with psycopg.connect(conninfo, row_factory=dict_row) as conn:
        with conn.cursor() as cur:

            cur.execute(""" SELECT is_active
                   FROM products
                   WHERE product_id= %s""", (product_id, ))
            
            row=cur.fetchone()
            if row== None or row['is_active']==False:
                #print("El producto no existe.")
                return True
            
            if row['is_active']==True:
                return False
 except psycopg.OperationalError as e:
    return None
            
# Fetch every item from the invetory, I have to add a pagination.
def ReadProducts(page, quantity=100):
 offset=(page-1)*100
 try:

    with psycopg.connect(conninfo , row_factory=dict_row) as conn:
        with conn.cursor() as cur:

            cur.execute("""SELECT * FROM PRODUCTS
                        ORDER BY product_id
                        LIMIT %s OFFSET %s""", (quantity, offset))

            return cur.fetchall()
 except psycopg.OperationalError as e:
    return []

#    *Cleans all the data before fetching into the database 
def cleanProductDB(entryDataList):
       
    dictionary={"product_name": entryDataList[0].strip(), "product_price": entryDataList[2], "product_stock": entryDataList[1], "product_cost": entryDataList[3], "product_category": entryDataList[4]}


    
    if (dictionary["product_name"]!= None) and (dictionary["product_price"] !=None) and (dictionary["product_stock"] != None):
     dictionary["product_price"]=(int(round(float(dictionary["product_price"])*100)))
     dictionary["product_cost"]=(int(round(float(dictionary["product_cost"])*100)))
     dictionary["product_name"]=dictionary["product_name"].strip()

     
     return dictionary
    
    else: return None
            

