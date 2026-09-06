from werkzeug.security import generate_password_hash

from auth_database import initialize_auth_database, create_user


initialize_auth_database()

name = "System Administrator"
email = "admin@clinicalcdss.com"
password = "Admin@123"

password_hash = generate_password_hash(password)

try:

    user_id = create_user(
        name=name,
        email=email,
        password_hash=password_hash,
        role="admin"
    )

    print("Admin created successfully.")
    print("User ID:", user_id)
    print("Email:", email)

except Exception as error:

    print("Could not create admin:", error)