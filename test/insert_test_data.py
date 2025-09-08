import csv
import datetime
import os

import psycopg2
import requests
from dotenv import load_dotenv
from psycopg2.extras import execute_values

load_dotenv("container/.env")

DB_CONFIG = {
    "dbname": os.getenv("POSTGRES_DB", "ticketsdb"),
    "user": os.getenv("POSTGRES_USER", "postgres"),
    "password": os.getenv("POSTGRES_PASSWORD", "postgres"),
    "host": os.getenv("POSTGRES_HOST", "localhost"),
    "port": os.getenv("POSTGRES_PORT", "5432"),
}

dummy_bookings = [
    ("B001", "U001", "Hanoi", "Ho Chi Minh City", datetime.date(2025, 9, 10), "A1,A2"),
    ("B002", "U002", "Hanoi", "Da Nang", datetime.date(2025, 9, 11), "B3,B4"),
    ("B003", "U003", "Da Nang", "Hue", datetime.date(2025, 9, 12), "C1"),
    ("B004", "U004", "Hue", "Hanoi", datetime.date(2025, 9, 13), "D5,D6"),
    ("B005", "U005", "Ho Chi Minh City", "Nha Trang", datetime.date(2025, 9, 14), "E2"),
]

API_URL = "http://localhost:8024"
CSV_FILE = "test/data/faq_data.csv"


def insert_booking_data():
    conn = None
    try:
        conn = psycopg2.connect(**DB_CONFIG)
        cur = conn.cursor()

        query = """
        INSERT INTO booking_tickets (booking_id, user_id, start_location, destination, trip_date, seats)
        VALUES %s
        ON CONFLICT (booking_id) DO NOTHING;
        """
        execute_values(cur, query, dummy_bookings)

        conn.commit()
        print("✅ Dummy data inserted successfully!")

    except psycopg2.OperationalError as e:
        print(f"❌ Cannot connect to database '{DB_CONFIG['dbname']}'. Error: {e}")
        raise

    except Exception as e:
        print("❌ Error:", e)
        raise

    finally:
        if conn:
            cur.close()
            conn.close()


def insert_faq_data():
    with open(CSV_FILE, newline="", encoding="utf-8") as csvfile:
        reader = csv.DictReader(csvfile)
        if "question" not in reader.fieldnames or "answer" not in reader.fieldnames:
            raise ValueError("CSV must have 'question' and 'answer' columns")

        for row in reader:
            payload = {
                "question": row["question"],
                "answer": row["answer"],
            }
            try:
                resp = requests.post(f"{API_URL}/insert", json=payload)
                resp.raise_for_status()
                uuid_ = resp.json().get("uuid")
                print(f"✅ Inserted UUID: {uuid_} | Question: {row['question']}")
            except Exception as e:
                print(f"❌ Failed to insert row: {row} | Error: {e}")


if __name__ == "__main__":
    insert_booking_data()
    insert_faq_data()
