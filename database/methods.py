"""Database class based on sqlite3"""
from sqlite3 import (connect as sqlite3_connect, Error as sqlite3Error,
                     Connection, Cursor)
from contextlib import contextmanager
from typing import Generator, Optional

from utils import Event


TABLE_NAME = 'LinkRegistry'


@contextmanager
def cursor_session(conn: Connection) -> Generator[Cursor, None, None]:
    """
    :param conn:
    :return:
    """
    cursor = conn.cursor()
    yield cursor

    try:
        conn.commit()
    except sqlite3Error:
        conn.rollback()
    finally:
        cursor.close()


class Database:
    """SQL-query methods"""

    def __init__(self) -> None:
        self.conn = None

    def connect(self) -> None:
        """Creates connection taking possible problems into account

        :return:
        """
        try:
            self.conn = sqlite3_connect('links.db', check_same_thread=False)
        except sqlite3Error as e:
            print(e)

    def create_link_table(self) -> None:
        """
        :return:
        """
        with cursor_session(self.conn) as cursor:
            cursor.execute(f'''CREATE TABLE IF NOT EXISTS {TABLE_NAME}
                           (ID INTEGER PRIMARY KEY AUTOINCREMENT,
                           InsDate DATETIME DEFAULT CURRENT_TIMESTAMP,
                           ChatID INTEGER,
                           Link TEXT,
                           RemoveDatetime DATETIME,
                           UNIQUE(ChatID, Link))''')

    def get_random_link(self, chat_id: int) -> Optional[str]:
        """
        :param chat_id:
        :return:
        """
        with cursor_session(self.conn) as cursor:
            random_link = cursor.execute(f'''WITH RANDOM_LINK AS (SELECT ID,
                                         Link FROM {TABLE_NAME}
                                         WHERE ChatID = {chat_id}
                                         AND RemoveDatetime IS NULL
                                         ORDER BY RANDOM() LIMIT 1)
                                         UPDATE {TABLE_NAME}
                                         SET RemoveDatetime = CURRENT_TIMESTAMP
                                         WHERE ID = (SELECT ID
                                         FROM RANDOM_LINK) RETURNING Link'''
                                         ).fetchone()

            if random_link:
                return random_link[0]

    def save_link(self, chat_id: int, text: str) -> bool:
        """
        :param chat_id:
        :param text:
        :return: True if it's managed to save, False otherwise
        """
        with cursor_session(self.conn) as cursor:
            if cursor.execute(f'''INSERT OR IGNORE INTO {TABLE_NAME}
                              (ChatID, Link) VALUES ({chat_id}, '{text}')
                              RETURNING ID''').fetchone():
                return True
            return False

    def get_event_list(self, chat_id: int) -> list[Event]:
        """
        :param chat_id:
        :return:
        """
        with cursor_session(self.conn) as cursor:
            event_tuples = cursor.execute(f'''SELECT InsDate AS ActionDatetime,
                                          Link, 'save'
                                          FROM {TABLE_NAME}
                                          WHERE ChatID = {chat_id}
                                          UNION
                                          SELECT RemoveDatetime AS
                                          ActionDatetime, Link, 'get'
                                          FROM {TABLE_NAME}
                                          WHERE ChatID = {chat_id}
                                          AND RemoveDatetime IS NOT NULL
                                          ORDER BY ActionDatetime'''
                                          ).fetchall()
            return [Event(action_datetime=row[0], link=row[1], action=row[2])
                    for row in event_tuples]
