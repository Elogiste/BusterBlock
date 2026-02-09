import mariadb

class BaseDAO:
    def __init__(self, config):
        self.host = config["host"]
        self.user = config["user"]
        self.password = config["password"]
        self.database = config["database"]
        self.port = config["port"]
        
        self.conn = None
        self.cur = None

    def get_connexion(self):
        return mariadb.connect(
            host=self.host,
            user=self.user,
            password=self.password,
            database=self.database,
            port=self.port
        )

    def ouvrir_connexion(self):
        self.conn = self.get_connexion()
        self.cur = self.conn.cursor()

    def fermer_connexion(self):
        if self.cur:
            self.cur.close()
        if self.conn:
            self.conn.close()

    def vider_tables(self, tables: list[str]):
        conn = self.get_connexion()
        cur = conn.cursor()

        for table in tables:
            cur.execute(f"DELETE FROM {table};")

        conn.commit()
        cur.close()
        conn.close()

    def __enter__(self):
        self.ouvrir_connexion()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.fermer_connexion()
