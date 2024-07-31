import os
import psycopg2

from .database_methods import DefaultDatabase

class ServerConnection(DefaultDatabase):
    """
    Live database with realtime data
    used for inference
    """
    def __init__(self, frontend = False):
        self.Frontend() if frontend else self.Server()
        self.conn = psycopg2.connect(
            dbname = self._DBNAME ,
            user = self._USERNAME ,
            password = self._PASSWORD ,
            host = self._HOST ,
            port = self._PORT
            )

    def Server(self):
        self._HOST = os.environ.get('lowLatencyHost')
        self._PORT = os.environ.get('lowLatencyPort')
        self._USERNAME = os.environ.get('lowLatencyUser', 'postgres')
        self._PASSWORD = os.environ.get('lowLatencyPassword')
        self._DBNAME = os.environ.get('lowLatencyDatabase')

    def Frontend(self):
        self._HOST = os.environ.get('lowLatencyWebHost')
        self._PORT = os.environ.get('lowLatencyWebPort')
        self._DBNAME = os.environ.get('lowLatencyWebDatabase')
        self._USERNAME = os.environ.get('lowLatencyWebUser', 'postgres')
        self._PASSWORD = os.environ.get('lowLatencyWebPassword')