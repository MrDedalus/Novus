import logging
from typing import Dict, Union, List, Optional
from psycopg2.pool import SimpleConnectionPool
import psycopg2

logging.basicConfig(level=logging.INFO)


class DatabaseError(Exception):
    pass


class Database:
    def __init__(self, config: Dict):
        self.config = config
        self.connection_pool = None
        self.dpias = {}

    def _create_connection_pool(self) -> SimpleConnectionPool:
        try:
            if 'database' not in self.config:
                raise DatabaseError("Database configuration not found")
            db_config = self.config['database']
            return SimpleConnectionPool(1, 20, user=db_config.get('postgres'),
                                        password=db_config.get('password'),
                                        host=db_config.get('host'),
                                        port=db_config.get('port', 5432),
                                        database=db_config.get('dpia_db'))
        except (psycopg2.Error, KeyError) as error:
            raise DatabaseError("Error while connecting to the database") from error

    def connect(self) -> None:
        """Establishes a connection to the database."""
        try:
            self.connection_pool = self._create_connection_pool()
        except DatabaseError as error:
            raise error

    def fetch_dpias(self):
        try:
            with self.connection_pool.getconn() as connection:
                with connection.cursor() as cursor:
                    cursor.execute("SELECT * FROM dpia_table")
                    dpia_records = cursor.fetchall()
                    for dpia_record in dpia_records:
                        dpia_id = dpia_record[0]
                        dpia = DPIA(dpia_id, dpia_record[1], dpia_record[2], dpia_record[3], dpia_record[4])
                        self.dpias[dpia_id] = dpia
        except (psycopg2.Error, KeyError) as error:
            raise DatabaseError("Error while fetching DPIAs from the database") from error

    def get_dpia_by_id(self, dpia_id: Optional[str]) -> Union['DPIA', None]:
        return self.dpias.get(dpia_id)

    def add_conversation(self, dpia_id: str, question: str, response: str) -> None:
        dpia = self.get_dpia_by_id(dpia_id)
        if dpia:
            dpia.add_conversation(question, response)
        else:
            raise ValueError(f"DPIA with ID '{dpia_id}' not found")

    def update_conversation(self, dpia_id: str, question: str, new_response: str) -> None:
        dpia = self.get_dpia_by_id(dpia_id)
        if dpia:
            dpia.update_conversation(question, new_response)
        else:
            raise ValueError(f"DPIA with ID '{dpia_id}' not found")

    def get_conversations(self, dpia_id: str) -> List['DPIAConversation']:
        dpia = self.get_dpia_by_id(dpia_id)
        if dpia:
            return dpia.get_conversations()
        else:
            raise ValueError(f"DPIA with ID '{dpia_id}' not found")
