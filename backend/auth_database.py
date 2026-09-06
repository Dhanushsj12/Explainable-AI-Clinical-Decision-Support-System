import os
import sqlite3

from werkzeug.security import generate_password_hash


# =========================================================
# DATABASE PATH
# =========================================================

DATABASE = os.path.join(
    os.path.dirname(os.path.abspath(__file__)),
    "users.db"
)


# =========================================================
# DATABASE CONNECTION
# =========================================================

def get_connection():

    connection = sqlite3.connect(DATABASE)

    connection.row_factory = sqlite3.Row

    return connection


# =========================================================
# INITIALIZE AUTH DATABASE
# =========================================================

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


# =========================================================
# CREATE USER
# =========================================================

def create_user(
    name,
    email,
    password_hash,
    role="staff"
):

    connection = get_connection()

    cursor = connection.execute(
        """
        INSERT INTO users
        (name, email, password_hash, role)
        VALUES (?, ?, ?, ?)
        """,
        (
            name,
            email,
            password_hash,
            role
        )
    )

    connection.commit()

    user_id = cursor.lastrowid

    connection.close()

    return user_id


# =========================================================
# GET USER BY EMAIL
# =========================================================

def get_user_by_email(email):

    connection = get_connection()

    user = connection.execute(
        """
        SELECT
            id,
            name,
            email,
            password_hash,
            role
        FROM users
        WHERE email = ?
        """,
        (email,)
    ).fetchone()

    connection.close()

    return user


# =========================================================
# GET ALL USERS
# =========================================================

def get_all_users():

    connection = get_connection()

    users = connection.execute(
        """
        SELECT
            id,
            name,
            email,
            role,
            created_at
        FROM users
        ORDER BY id
        """
    ).fetchall()

    connection.close()

    return users


# =========================================================
# UPDATE USER ROLE
# =========================================================

def update_user_role(
    user_id,
    role
):

    connection = get_connection()

    connection.execute(
        """
        UPDATE users
        SET role = ?
        WHERE id = ?
        """,
        (
            role,
            user_id
        )
    )

    connection.commit()

    updated = connection.execute(
        """
        SELECT
            id,
            name,
            email,
            role,
            created_at
        FROM users
        WHERE id = ?
        """,
        (user_id,)
    ).fetchone()

    connection.close()

    return updated


# =========================================================
# BOOTSTRAP ADMIN
#
# Creates the first Admin account on the hosted server.
#
# Admin credentials are taken from Render environment
# variables and are NOT stored in the source code.
#
# If the configured email already exists as another role,
# that existing account will be promoted to Admin.
# =========================================================

def create_bootstrap_admin():

    admin_email = os.environ.get(
        "BOOTSTRAP_ADMIN_EMAIL"
    )

    admin_password = os.environ.get(
        "BOOTSTRAP_ADMIN_PASSWORD"
    )

    admin_name = os.environ.get(
        "BOOTSTRAP_ADMIN_NAME",
        "System Administrator"
    )

    # -----------------------------------------------------
    # If environment variables are not configured,
    # do nothing.
    # -----------------------------------------------------

    if not admin_email or not admin_password:

        print(
            "Bootstrap admin environment variables "
            "are not configured. Skipping admin creation."
        )

        return

    # -----------------------------------------------------
    # Normalize email
    # -----------------------------------------------------

    admin_email = admin_email.strip().lower()

    # -----------------------------------------------------
    # Check whether the Admin already exists
    # -----------------------------------------------------

    existing_user = get_user_by_email(
        admin_email
    )

    # -----------------------------------------------------
    # If account already exists
    # -----------------------------------------------------

    if existing_user:

        # If the existing account is not Admin,
        # promote it to Admin.
        if existing_user["role"] != "admin":

            update_user_role(
                existing_user["id"],
                "admin"
            )

            print(
                f"Existing user promoted to admin: "
                f"{admin_email}"
            )

        else:

            print(
                f"Bootstrap admin already exists: "
                f"{admin_email}"
            )

        return

    # -----------------------------------------------------
    # Hash Admin password
    # -----------------------------------------------------

    password_hash = generate_password_hash(
        admin_password
    )

    # -----------------------------------------------------
    # Create Admin account
    # -----------------------------------------------------

    create_user(
        name=admin_name,
        email=admin_email,
        password_hash=password_hash,
        role="admin"
    )

    print(
        f"Bootstrap admin created successfully: "
        f"{admin_email}"
    )