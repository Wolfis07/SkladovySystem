import sys
import io
from src.repositories import ProductRepository
from src.services import OrderService, ImportService, ReportService

# 1. MAGICKÝ ŘÁDEK PRO OPRAVU ČEŠTINY V DOCKERU/WINDOWS
# Donutí Python posílat text v UTF-8, i když si konzole myslí něco jiného.
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

def print_header():
    print("\n" + "="*40)
    print("      ŠÉFŮV SKLADOVÝ SYSTÉM      ")
    print("="*40)

def print_menu():
    print("1. Seznam produktů (Tabulka)")
    print("2. Objednat (Transakce)")
    print("3. Import CSV")
    print("4. Report tržeb")
    print("5. Konec")
    print("-" * 40)

def main():
    # Inicializace služeb
    repo = ProductRepository()
    order_service = OrderService()
    import_service = ImportService()
    report_service = ReportService()

    while True:
        print_header()
        print_menu()
        
        choice = input("Volba: ")

        if choice == '1':
            # --- ZDE JE TA OPRAVA VÝPISU (TABULKA) ---
            try:
                products = repo.get_all()
                print("\n--- SKLAD ---")
                # Formátování hlavičky: <5 znamená zarovnat vlevo na 5 znaků, <25 na 25 znaků atd.
                print(f"{'ID':<5} {'Název':<25} {'Kategorie':<15} {'Cena':<10} {'Sklad':<8}")
                print("-" * 70)
                
                for p in products:
                    # Ošetření, aby to nespadlo, kdyby nějaká hodnota chyběla
                    pid = p.get('Id', '-')
                    name = p.get('Name', 'Neznámý')
                    cat = p.get('CategoryName', '-')
                    price = p.get('Price', 0)
                    stock = p.get('StockQuantity', 0)
                    
                    print(f"{pid:<5} {name:<25} {cat:<15} {price:<10} {stock:<8}")
                print("-" * 70)
                input("\n[Enter] pro návrat do menu...")
            except Exception as e:
                print(f"Chyba při výpisu: {e}")

        elif choice == '2':
            print("\n--- NOVÁ OBJEDNÁVKA ---")
            try:
                user_id = input("User ID (např. 1): ")
                product_id = input("Product ID: ")
                quantity = input("Množství: ")
                
                # Konverze na čísla
                order_service.create_order(int(user_id), int(product_id), int(quantity))
            except ValueError:
                print("CHYBA: Musíš zadat čísla!")
            except Exception as e:
                print(f"CHYBA: {e}")
            input("\n[Enter] pro pokračování...")

        elif choice == '3':
            print("\n--- IMPORT DAT ---")
            import_service.import_csv('data.csv')
            input("\n[Enter] pro pokračování...")

        elif choice == '4':
            # Report necháme jak je ve službě, nebo ho taky můžeš zformátovat, 
            # ale ProductRepository je ten hlavní problém.
            report_service.show_report()
            input("\n[Enter] pro pokračování...")

        elif choice == '5':
            print("Končím. Čau!")
            break
        else:
            print("Neplatná volba, zkus to znovu.")

if __name__ == "__main__":
    main()