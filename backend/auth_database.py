import os
import sqlite3

DATABASE = os.path.join(
    os.path.dirname(os.path.abspath(__file__)),
    "users.db"
)


def get_connection():
    connection = sqlite3.connect(DATABASE)
    connection.row_factory = sqlite3.Row
    return connection


def initialize_auth_database():
    connection = get_connection()

    connection.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            email TEXT UNIQUE NOT NULL,
            password_hash TEXT NOT NULL,
            role TEXT NOT NULL DEFAULT 'staff',
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)

    connection.commit()
    connection.close()


def create_user(name, email, password_hash, role="staff"):
    connection = get_connection()

    cursor = connection.execute(
        """
        INSERT INTO users
        (name, email, password_hash, role)
        VALUES (?, ?, ?, ?)
        """,
        (name, email, password_hash, role)
    )

    connection.commit()

    user_id = cursor.lastrowid

    connection.close()

    return user_id


def get_user_by_email(email):
    connection = get_connection()

    user = connection.execute(
        """
        SELECT id, name, email, password_hash, role
        FROM users
        WHERE email = ?
        """,
        (email,)
    ).fetchone()

    connection.close()

    return user
def get_all_users():
    connection = get_connection()

    users = connection.execute(
        """
        SELECT id, name, email, role, created_at
        FROM users
        ORDER BY id
        """
    ).fetchall()

    connection.close()

    return users


def update_user_role(user_id, role):
    connection = get_connection()

    connection.execute(
        """
        UPDATE users
        SET role = ?
        WHERE id = ?
        """,
        (role, user_id)
    )

    connection.commit()

    updated = connection.execute(
        """
        SELECT id, name, email, role, created_at
        FROM users
        WHERE id = ?
        """,
        (user_id,)
    ).fetchone()

    connection.close()

    return updated