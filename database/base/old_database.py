import os
import psycopg2
from .database_methods import DefaultDatabase

class Connection(DefaultDatabase):
    """
    The old database which contains months of data
    used for training
    """
    def __init__(self, localhost):
        self.local() if localhost else self.online()

        self.conn = psycopg2.connect(
            dbname = self._DBNAME ,
            user = self._USERNAME ,
            password = self._PASSWORD ,
            host = self._HOST ,
            port = self._PORT
            )

    def local(self):
        self._HOST = os.environ.get('rsLocalHost')
        self._PORT = os.environ.get('rsLocalPort')
        self._USERNAME = os.environ.get('rsLocalUsername', 'postgres')
        self._PASSWORD = os.environ.get('rsPassword')
        self._DBNAME = os.environ.get('runescape_database_name')

    def online(self):
        self._HOST = os.environ.get('rsHost')
        self._PORT = os.environ.get('rsPort')
        self._USERNAME = os.environ.get('rsLocalUsername', 'postgres')
        self._PASSWORD = os.environ.get('rsPassword')
        self._DBNAME = os.environ.get('runescape_database_name')


