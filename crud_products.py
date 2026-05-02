import psycopg
from psycopg.rows import dict_row
import os
from dotenv import load_dotenv
load_dotenv()

conninfo = f"dbname={os.getenv('DB_NAME')} user={os.getenv('DB_TABLES_USER')} password={os.getenv('DB_TABLES_PASS')} host={os.getenv('DB_HOST')}"

#DEBO HACER UNA FUNCION CHECKSTOCK para hacer saltar una notificación en caso del que producto se acabe.

# AddProducts commits all the data to the database from a dictionary.
def AddProduct(product_dict):
    with psycopg.connect(conninfo) as conn:
        with conn.cursor() as cur:

            cur.execute("""INSERT INTO products(product_name, product_price, product_stock, product_cost, product_category)
                       VALUES (%s, %s, %s, %s, %s)
                       """,(product_dict["product_name"], product_dict["product_price"], product_dict["product_stock"],
                            product_dict["product_cost"], product_dict["product_category"]) )
            
# Updates the data of a product from a dictionary.
def EditProduct(product_dict, product_id):
    with psycopg.connect(conninfo) as conn:
        with conn.cursor() as cur:

            cur.execute(""" UPDATE products
                       SET product_name=%s, product_stock= %s, 
                       product_price= %s, product_cost= %s, product_category= %s
                       WHERE product_id= %s""",
                       (product_dict["product_name"], product_dict["product_stock"],
                        product_dict["product_price"], product_dict["product_cost"],
                        product_dict["product_category"], product_id))


# Deletes a product from the frontend. It only turns is_active to false            
def DeleteProduct(product_id):
    with psycopg.connect(conninfo) as conn:
        with conn.cursor() as cur:

            cur.execute(""" UPDATE products
                       SET is_active = false
                       WHERE product_id= %s""", (product_id, ))

# Fetchs the price on float, with the product id.
def GetPrice(product_id):

    with psycopg.connect(conninfo, row_factory=dict_row) as conn:
        with conn.cursor() as cur:
            cur.execute("""SELECT product_price
                        FROM products 
                        WHERE product_id= %s""", (product_id, ))
            
            result=cur.fetchone()
            price=result['product_price']/100

            return price

# Checks if a product exists or is active from the frontend. If deleted or does not exist, returns true.
# If active, then returns false.
def IsDeleted(product_id):
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
            
# Fetch every item from the invetory, I have to add a pagination.
def ReadProducts(page, quantity=100):
    offset=(page-1)*100
    with psycopg.connect(conninfo , row_factory=dict_row) as conn:
        with conn.cursor() as cur:

            cur.execute("""SELECT * FROM PRODUCTS
                        LIMIT %s OFFSET %s
                        ORDER BY product_id""", (quantity, offset))

            return cur.fetchall()
            
            

