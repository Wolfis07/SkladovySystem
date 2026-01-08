from src.database import Database

class ProductRepository:
    def get_all(self):
        conn = Database().get_connection()
        # V pymssql je as_dict nastaveno už při připojení
        cursor = conn.cursor() 
        try:
            # MSSQL syntaxe je stejná pro SELECT
            cursor.execute("SELECT * FROM v_ProductDetails") 
            return cursor.fetchall()
        except Exception as e:
            print(f"DB Error: {e}")
            return []
        finally:
            conn.close()

    def add(self, name, price, stock, cat_id):
        conn = Database().get_connection()
        cursor = conn.cursor()
        try:
            # %s funguje v pymssql stejně jako v MySQL
            sql = "INSERT INTO Products (Name, Price, StockQuantity, CategoryId) VALUES (%s, %s, %s, %s)"
            cursor.execute(sql, (name, price, stock, cat_id))
            conn.commit()
        finally:
            conn.close()