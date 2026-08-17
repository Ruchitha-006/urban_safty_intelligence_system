from pathlib import Path
import sqlite3
from typing import Optional


BASE_DIR = Path(__file__).resolve().parent.parent
DB_PATH = BASE_DIR / "urban_safety.db"


def get_connection() -> sqlite3.Connection:
    connection = sqlite3.connect(DB_PATH)
    connection.row_factory = sqlite3.Row
    return connection


def init_db() -> None:
    connection = get_connection()

    cursor = connection.cursor()

    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE NOT NULL,
            email TEXT UNIQUE NOT NULL,
            password_hash TEXT NOT NULL,
            city TEXT DEFAULT 'Bengaluru',
            created_at TEXT DEFAULT CURRENT_TIMESTAMP
        )
        """
    )

    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS sos_events (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT,
            latitude REAL NOT NULL,
            longitude REAL NOT NULL,
            message TEXT,
            created_at TEXT DEFAULT CURRENT_TIMESTAMP
        )
        """
    )

    connection.commit()
    connection.close()


def create_user(
    username: str,
    email: str,
    password_hash: str,
    city: str,
) -> bool:
    connection = get_connection()

    try:
        connection.execute(
            """
            INSERT INTO users
            (username, email, password_hash, city)
            VALUES (?, ?, ?, ?)
            """,
            (
                username,
                email,
                password_hash,
                city,
            ),
        )

        connection.commit()
        return True

    except sqlite3.IntegrityError:
        return False

    finally:
        connection.close()


def get_user(username: str) -> Optional[sqlite3.Row]:
    connection = get_connection()

    user = connection.execute(
        """
        SELECT *
        FROM users
        WHERE username = ?
        """,
        (username,),
    ).fetchone()

    connection.close()

    return user


def create_sos_event(
    username: Optional[str],
    latitude: float,
    longitude: float,
    message: str,
) -> None:
    connection = get_connection()

    connection.execute(
        """
        INSERT INTO sos_events
        (username, latitude, longitude, message)
        VALUES (?, ?, ?, ?)
        """,
        (
            username,
            latitude,
            longitude,
            message,
        ),
    )

    connection.commit()
    connection.close()