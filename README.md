Django CSV Uploader

A Django web application that allows users to upload a CSV file containing user data. The system validates the records, filters out duplicates and invalid entries, and saves the valid records to the database.

---

Features

- Upload .csv files containing user data.
- Validates each row using Django REST Framework serializers.
- Rejects:
  - Duplicate emails (both in DB and file)
  - Missing/empty required fields
  - Invalid email or phone formats
  - Age outside valid range (0–120)
- Shows success and rejection summary.
- Provides a user list page with filters.
- Allows deletion of users.

---


Sample CSV Format

Located in: Sample CSV-file/user-data

```csv
name,email,age,phone_number,gender,address
Ajmal,ajmal@example.com,25,1234567890,Male,Kerala
Ammu,ammu@example.com,28,9876543210,Female,Kozhikode

Installation

pip install -r requirements.txt
python manage.py migrate
python manage.py runserver




Steps:

Go to the URL: http://127.0.0.1:8000/

Choose a sample CSV file (user-data.csv) provided in the Sample CSV-file/ folder.

Click Upload.

The app will:

Validate each row

Save valid records to the database

Show a summary of total, successful, and rejected records

click user_list nav button to see saved users


for unit test run
python manage.py test
