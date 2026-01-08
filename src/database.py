import pymssql
import json

class Database:
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(Database, cls).__new__(cls)
            cls._instance.config = cls._instance._load_config()
        return cls._instance

    def _load_config(self):
        try:
            with open('config.json', 'r') as f:
                return json.load(f)['database']
        except FileNotFoundError:
            raise Exception("Soubor config.json nebyl nalezen!")

    def get_connection(self):
        cfg = self.config
        try:
            # Připojení pro MSSQL
            conn = pymssql.connect(
                server=cfg['host'],
                user=cfg['user'],
                password=cfg['password'],
                database=cfg['database'],
                port=cfg['port'],
                as_dict=True,  # Aby vracel výsledky jako slovník (důležité!)
                autocommit=False,
                charset='UTF-8'
            )
            return conn
        except Exception as e:
            print(f"CHYBA PŘIPOJENÍ K MSSQL: {e}")
            raise e