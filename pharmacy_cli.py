"""Simple command-line program for the pharmacy database project.

Works with the Medication table from pharmacy_database_setup.sql.
"""

import getpass
import os

import mysql.connector
from mysql.connector import Error


def connect_to_database():
    user = os.getenv("DB_USER", "antonio")
    password = os.getenv("DB_PASSWORD")
    if password is None:
        password = getpass.getpass("MySQL password: ")

    return mysql.connector.connect(
        host=os.getenv("DB_HOST", "localhost"),
        user=user,
        password=password,
        database=os.getenv("DB_NAME", "pharmacy_database"),
    )


def display_medications(connection):
    cursor = connection.cursor()
    try:
        cursor.execute(
            "SELECT MedicationID, MedicationName, Dosage, QuantityInStock "
            "FROM Medication ORDER BY MedicationID"
        )
        rows = cursor.fetchall()
        if not rows:
            print("No medications found.")
        else:
            print("\nID | Medication | Dosage | Quantity in Stock")
            print("-" * 55)
            for med_id, name, dosage, quantity in rows:
                print(f"{med_id} | {name} | {dosage} | {quantity}")
    finally:
        cursor.close()


def read_quantity():
    while True:
        try:
            value = int(input("Quantity in stock: "))
            if value >= 0:
                return value
        except ValueError:
            pass
        print("Please enter a nonnegative whole number.")


def read_id():
    while True:
        try:
            value = int(input("Medication ID: "))
            if value >= 0:
                return value
        except ValueError:
            pass
        print("Please enter a nonnegative whole number.")


def insert_medication(connection):
    med_id = read_id()
    name = input("Medication name: ").strip()
    dosage = input("Dosage: ").strip()
    quantity = read_quantity()

    if not name or not dosage:
        print("Medication name and dosage cannot be empty.")
        return

    cursor = connection.cursor()
    try:
        cursor.execute(
            "INSERT INTO Medication (MedicationID, MedicationName, Dosage, QuantityInStock) "
            "VALUES (%s, %s, %s, %s)",
            (med_id, name, dosage, quantity),
        )
        connection.commit()
        print("Medication inserted.")
    finally:
        cursor.close()


def update_medication(connection):
    med_id = read_id()
    name = input("New medication name: ").strip()
    dosage = input("New dosage: ").strip()
    quantity = read_quantity()

    if not name or not dosage:
        print("Medication name and dosage cannot be empty.")
        return

    cursor = connection.cursor()
    try:
        cursor.execute(
            "UPDATE Medication SET MedicationName = %s, Dosage = %s, "
            "QuantityInStock = %s WHERE MedicationID = %s",
            (name, dosage, quantity, med_id),
        )
        connection.commit()
        if cursor.rowcount:
            print("Medication updated.")
        else:
            print("No row changed. Check the ID or whether the values are already the same.")
    finally:
        cursor.close()


def delete_medication(connection):
    med_id = read_id()
    confirm = input(f"Delete medication {med_id}? (y/n): ").strip().lower()
    if confirm != "y":
        print("Deletion cancelled.")
        return

    cursor = connection.cursor()
    try:
        cursor.execute("DELETE FROM Medication WHERE MedicationID = %s", (med_id,))
        connection.commit()
        if cursor.rowcount:
            print("Medication deleted.")
        else:
            print("No medication found with that ID.")
    finally:
        cursor.close()


def main():
    try:
        connection = connect_to_database()
    except Error as error:
        print(f"Could not connect to database: {error}")
        return

    print("Connected to pharmacy database.")
    try:
        while True:
            print("\n1) Display contents of table")
            print("2) Insert new row to table")
            print("3) Update a row of the table")
            print("4) Delete a row of the table")
            print("q) Quit")
            choice = input("Choose an option: ").strip().lower()

            if choice == "q":
                break

            try:
                if choice == "1":
                    display_medications(connection)
                elif choice == "2":
                    insert_medication(connection)
                elif choice == "3":
                    update_medication(connection)
                elif choice == "4":
                    delete_medication(connection)
                else:
                    print("Invalid option.")
            except Error as error:
                connection.rollback()
                print(f"Database error: {error}")
    finally:
        connection.close()
        print("Goodbye.")


if __name__ == "__main__":
    main()
