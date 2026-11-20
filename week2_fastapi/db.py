import sqlite3
from datetime import datetime


DATABASE = "conversation.db"


def get_connection():
    connection = sqlite3.connect(DATABASE)

    connection.execute("PRAGMA foreign_keys = ON")

    return connection


def init_db():
    connection = get_connection()

    cursor = connection.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS sessions (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            created_at TEXT NOT NULL,
            summary TEXT DEFAULT ''
        )
    """)

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS messages (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            session_id INTEGER NOT NULL,
            role TEXT NOT NULL,
            content TEXT NOT NULL,
            created_at TEXT NOT NULL,
            FOREIGN KEY (session_id)
                REFERENCES sessions(id)
                ON DELETE CASCADE
        )
    """)

    connection.commit()
    connection.close()


def create_session():
    connection = get_connection()

    cursor = connection.cursor()

    cursor.execute(
        """
        INSERT INTO sessions (created_at, summary)
        VALUES (?, ?)
        """,
        (datetime.now().isoformat(), "")
    )

    session_id = cursor.lastrowid

    connection.commit()
    connection.close()

    return session_id


def session_exists(session_id):
    connection = get_connection()

    cursor = connection.cursor()

    cursor.execute(
        """
        SELECT id
        FROM sessions
        WHERE id = ?
        """,
        (session_id,)
    )

    result = cursor.fetchone()

    connection.close()

    return result is not None


def save_message(session_id, role, content):
    connection = get_connection()

    cursor = connection.cursor()

    cursor.execute(
        """
        INSERT INTO messages (
            session_id,
            role,
            content,
            created_at
        )
        VALUES (?, ?, ?, ?)
        """,
        (
            session_id,
            role,
            content,
            datetime.now().isoformat()
        )
    )

    connection.commit()
    connection.close()


def get_messages(session_id):
    connection = get_connection()

    cursor = connection.cursor()

    cursor.execute(
        """
        SELECT role, content
        FROM messages
        WHERE session_id = ?
        ORDER BY id ASC
        """,
        (session_id,)
    )

    rows = cursor.fetchall()

    connection.close()

    return [
        {
            "role": role,
            "content": content
        }
        for role, content in rows
    ]


def get_session_summary(session_id):
    connection = get_connection()

    cursor = connection.cursor()

    cursor.execute(
        """
        SELECT summary
        FROM sessions
        WHERE id = ?
        """,
        (session_id,)
    )

    result = cursor.fetchone()

    connection.close()

    if result:
        return result[0] or ""

    return ""


def update_session_summary(session_id, summary):
    connection = get_connection()

    cursor = connection.cursor()

    cursor.execute(
        """
        UPDATE sessions
        SET summary = ?
        WHERE id = ?
        """,
        (summary, session_id)
    )

    connection.commit()
    connection.close()