from src.database import Database
import csv
import os

class OrderService:
    def create_order(self, user_id, product_id, quantity):
        conn = Database().get_connection()
        cursor = conn.cursor()
        try:
            # V pymssql se transakce zahajuje automaticky, pokud autocommit=False
            
            # 1. Kontrola skladu
            cursor.execute("SELECT Price, StockQuantity FROM Products WHERE Id = %s", (product_id,))
            prod = cursor.fetchone()
            if not prod: raise Exception("Produkt neexistuje")
            
            # Pymssql vrací dict, musíme přistupovat přes klíče
            price = prod['Price']
            stock = prod['StockQuantity']

            if stock < quantity: raise Exception("Nedostatek zboží!")

            # 2. Vytvořit objednávku + ZÍSKAT ID (MSSQL trik)
            # MSSQL neumí cursor.lastrowid spolehlivě, použijeme SCOPE_IDENTITY()
            cursor.execute("INSERT INTO Orders (UserId) VALUES (%s); SELECT SCOPE_IDENTITY() as LastID", (user_id,))
            
            result = cursor.fetchone()
            order_id = int(result['LastID']) # Získání ID z MSSQL

            # 3. Vytvořit položku
            cursor.execute("INSERT INTO OrderItems (OrderId, ProductId, Quantity, UnitPrice) VALUES (%s, %s, %s, %s)", 
                           (order_id, product_id, quantity, price))

            # 4. Odečíst sklad
            cursor.execute("UPDATE Products SET StockQuantity = StockQuantity - %s WHERE Id = %s", (quantity, product_id))

            conn.commit()
            print("Objednávka OK!")
        except Exception as e:
            conn.rollback()
            print(f"CHYBA TRANSAKCE: {e}")
        finally:
            conn.close()

class ImportService:
    def import_csv(self, filename):
        base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        path = os.path.join(base_dir, filename)
        
        if not os.path.exists(path):
            print("Soubor neexistuje!")
            return

        conn = Database().get_connection()
        cursor = conn.cursor()
        try:
            with open(path, 'r', encoding='utf-8') as f: # Pozor na encoding
                reader = csv.reader(f)
                for row in reader:
                    if len(row) < 4: continue
                    # MSSQL Insert
                    sql = "INSERT INTO Products (Name, Price, StockQuantity, CategoryId) VALUES (%s, %s, %s, %s)"
                    cursor.execute(sql, (row[0], float(row[1]), int(row[2]), int(row[3])))
            conn.commit()
            print("Import OK.")
        except Exception as e:
            print(f"Chyba importu: {e}")
            conn.close()
            
class ReportService:
    def show_report(self):
        conn = Database().get_connection()
        cursor = conn.cursor()
        try:
            cursor.execute("SELECT * FROM v_OrderSummary") 
            print("\n--- REPORT ---")
            for r in cursor.fetchall():
                print(r)
        except Exception as e:
            print(f"Chyba reportu: {e}")
        finally:
            conn.close()