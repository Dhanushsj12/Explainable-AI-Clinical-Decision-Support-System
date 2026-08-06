import sqlite3

DATABASE = "predictions.db"


def create_table():

    conn = sqlite3.connect(DATABASE)

    cursor = conn.cursor()

    cursor.execute("""

        CREATE TABLE IF NOT EXISTS prediction_history(

            id INTEGER PRIMARY KEY AUTOINCREMENT,

            patient_id TEXT,

            patient_name TEXT,

            prediction TEXT,

            probability REAL,

            risk_level TEXT,

            date TIMESTAMP DEFAULT CURRENT_TIMESTAMP

        )

    """)

    conn.commit()

    conn.close()


def save_prediction(patient, result):

    conn = sqlite3.connect(DATABASE)

    cursor = conn.cursor()

    cursor.execute("""

        INSERT INTO prediction_history(

            patient_id,

            patient_name,

            prediction,

            probability,

            risk_level

        )

        VALUES(?,?,?,?,?)

    """,

    (

        patient["patient_id"],

        patient["patient_name"],

        result["prediction"],

        result["probability"],

        result["risk_level"]

    )

    )

    conn.commit()

    conn.close()


def get_predictions():

    conn = sqlite3.connect(DATABASE)

    conn.row_factory = sqlite3.Row

    cursor = conn.cursor()

    cursor.execute("""

        SELECT *

        FROM prediction_history

        ORDER BY id DESC

    """)

    rows = cursor.fetchall()

    conn.close()

    return [dict(row) for row in rows]