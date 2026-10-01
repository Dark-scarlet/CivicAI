import sqlite3

connection = sqlite3.connect("civicai.db")

cursor = connection.cursor()

cursor.execute("""
CREATE TABLE IF NOT EXISTS schemes (

    id INTEGER PRIMARY KEY AUTOINCREMENT,

    country TEXT,

    scheme_name TEXT,

    target_group TEXT,

    benefit TEXT,

    documents TEXT
)
""")

schemes = [

    (
        "India",
        "PM Kisan",
        "Farmers",
        "6000 INR per year",
        "Aadhaar Card;Bank Account;Land Records"
    ),

    (
        "India",
        "Ayushman Bharat",
        "Low Income Families",
        "Health insurance coverage",
        "Aadhaar Card;Income Certificate"
    ),

    (
        "India",
        "National Scholarship Portal",
        "Students",
        "Scholarship support",
        "Student ID;Income Certificate"
    ),

    (
        "India",
        "Sukanya Samriddhi Yojana",
        "Girls",
        "High-interest savings scheme",
        "Birth Certificate;Parent ID"
    ),

    (
        "India",
        "Atal Pension Yojana",
        "Senior Citizens",
        "Monthly pension benefits",
        "Aadhaar Card;Bank Account"
    )

]

cursor.executemany("""

INSERT INTO schemes (

    country,
    scheme_name,
    target_group,
    benefit,
    documents

)

VALUES (?, ?, ?, ?, ?)

""", schemes)

connection.commit()

connection.close()

print("Database created successfully!")