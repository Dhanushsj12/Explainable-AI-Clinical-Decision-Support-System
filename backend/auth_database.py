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
# INITIALIZE AUTH DATABASE & SEED DEFAULT USERS
# =========================================================

def seed_default_users():
    default_users = [
        {
            "name": "System Administrator",
            "email": "admin@hospital.com",
            "password": "Admin@123",
            "role": "admin"
        },
        {
            "name": "Dr. Dhanush (Lead Cardiologist)",
            "email": "doctor@hospital.com",
            "password": "Doctor@123",
            "role": "doctor"
        },
        {
            "name": "Clinical Staff Member",
            "email": "staff@hospital.com",
            "password": "Staff@123",
            "role": "staff"
        }
    ]

    connection = get_connection()
    for user_info in default_users:
        existing = connection.execute(
            "SELECT id, role FROM users WHERE email = ?",
            (user_info["email"],)
        ).fetchone()

        pwd_hash = generate_password_hash(user_info["password"])

        if not existing:
            connection.execute(
                """
                INSERT INTO users (name, email, password_hash, role)
                VALUES (?, ?, ?, ?)
                """,
                (user_info["name"], user_info["email"], pwd_hash, user_info["role"])
            )
            print(f"Created default {user_info['role']} account: {user_info['email']}")
        else:
            # Keep credentials active and correct
            connection.execute(
                """
                UPDATE users
                SET password_hash = ?, role = ?
                WHERE email = ?
                """,
                (pwd_hash, user_info["role"], user_info["email"])
            )

    connection.commit()
    connection.close()


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

    # Pre-seed the 3 guaranteed accounts (Admin, Doctor, Staff)
    seed_default_users()


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