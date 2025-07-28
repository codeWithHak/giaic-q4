import sqlite3
import json

try:
    # Connect to your database
    connection = sqlite3.connect(r"D:\huzair\coding\email-automation-system\mails.db")
    cursor = connection.cursor()

    # Replace 'emails' with your actual table name
    cursor.execute("SELECT * FROM huzair_mails")
    columns = [description[0] for description in cursor.description]
    rows = cursor.fetchall()

    # Convert to list of dicts
    emails_data = [dict(zip(columns, row)) for row in rows]

    # Save to JSON
    with open("mails.json", "w", encoding="utf-8") as f:
        json.dump(emails_data, f, indent=4, ensure_ascii=False)

    print("Exported to mails.json successfully!")

except Exception as e:
    print("Error:", e)

finally:
    connection.close()
