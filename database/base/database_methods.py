import pandas as pd
class DefaultDatabase:
    conn = None

    def get (self , query , params = None):
        with self.conn.cursor() as cursor:
            cursor.execute(query , params)
            return cursor.fetchall()

    def post (self , query , params = None, fetch=False):
        with self.conn.cursor() as cursor:
            cursor.execute(query , params)
            if fetch:
                return cursor.fetchall()

    def post_many (self , query , params = None,commit=True):
        with self.conn.cursor() as cursor:
            cursor.executemany(query , params)
            if commit:
                self.conn.commit()
            return

    def get_df(self, query, params = None, columns = None):
        rows = self.get(query, params)
        if columns:
            return pd.DataFrame(rows , columns = columns)

        return pd.DataFrame(rows)

    def close(self):
        self.conn.close()