
import sqlite3
from contextlib import contextmanager

from config.settings import DATABASE_PATH


def get_connection():
    """
    Create and return a SQLite database connection.

    Foreign key support is enabled for relational integrity.
    """
    connection = sqlite3.connect(
        DATABASE_PATH,
        timeout=30
    )

    # Enable foreign key constraints
    connection.execute("PRAGMA foreign_keys = ON")

    # Return query results as dictionary-like rows
    connection.row_factory = sqlite3.Row

    return connection


@contextmanager
def get_db_connection():
    """
    Manage database connections automatically.

    Commits changes when successful and rolls back
    transactions if an error occurs.
    """
    connection = get_connection()

    try:
        yield connection
        connection.commit()

    except Exception:
        connection.rollback()
        raise

    finally:
        connection.close()


def create_tables():
    """
    Create chats and messages tables if they do not exist.
    """

    with get_db_connection() as connection:

        cursor = connection.cursor()

        # Create chats table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS chats (
                id TEXT PRIMARY KEY,
                title TEXT NOT NULL,
                created_at TEXT NOT NULL,
                updated_at TEXT NOT NULL
            )
        """)

        # Create messages table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS messages (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                chat_id TEXT NOT NULL,
                role TEXT NOT NULL CHECK (
                    role IN ('user', 'assistant', 'system')
                ),
                content TEXT NOT NULL,
                created_at TEXT NOT NULL,

                FOREIGN KEY (chat_id)
                REFERENCES chats(id)
                ON DELETE CASCADE
            )
        """)

        # Index to retrieve messages by chat efficiently
        cursor.execute("""
            CREATE INDEX IF NOT EXISTS
            idx_messages_chat_id
            ON messages(chat_id)
        """)

        # Index for sorting recent conversations
        cursor.execute("""
            CREATE INDEX IF NOT EXISTS
            idx_chats_updated_at
            ON chats(updated_at DESC)
        """)


def check_database():
    """
    Verify that database tables have been created.
    """

    with get_db_connection() as connection:

        cursor = connection.cursor()

        cursor.execute("""
            SELECT name
            FROM sqlite_master
            WHERE type = 'table'
            ORDER BY name
        """)

        tables = cursor.fetchall()

        return [table["name"] for table in tables]
