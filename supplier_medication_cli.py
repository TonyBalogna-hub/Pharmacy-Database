
import os
import getpass
import mysql.connector
from mysql.connector import Error


def connect_to_database():
    password = os.getenv("DB_PASSWORD")
    if password is None:
        password = getpass.getpass("MySQL password: ")

    return mysql.connector.connect(
        host="127.0.0.1",
        user=os.getenv("DB_USER", "pharmacy_app"),
        password=password,
        database="pharmacy_database"
    )


def print_suppliers(connection):
    cursor = connection.cursor()
    try:
        cursor.execute(
            "SELECT SupplierID, CompanyName, PhoneNumber "
            "FROM Supplier ORDER BY SupplierID"
        )
        rows = cursor.fetchall()

        print("\n--- SUPPLIERS ---")
        if not rows:
            print("No suppliers are currently on file.")
        else:
            print("ID | Company | Phone Number")
            print("-" * 55)
            for supplier_id, name, phone in rows:
                print(f"{supplier_id} | {name} | {phone}")
    finally:
        cursor.close()


def print_medications(connection):
    cursor = connection.cursor()
    try:
        cursor.execute(
            "SELECT MedicationID, MedicationName, Dosage "
            "FROM Medication ORDER BY MedicationID"
        )
        rows = cursor.fetchall()

        print("\n--- MEDICATIONS ---")
        if not rows:
            print("No medications are currently on file.")
        else:
            print("ID | Medication | Dosage")
            print("-" * 55)
            for med_id, name, dosage in rows:
                print(f"{med_id} | {name} | {dosage}")
    finally:
        cursor.close()


def medications_by_supplier(connection):
    supplier_id = int(input("Supplier ID: "))

    cursor = connection.cursor()
    try:
        cursor.execute(
            """
            SELECT m.MedicationID, m.MedicationName, m.Dosage
            FROM Medication m
            JOIN SupplierMedication sm
                ON m.MedicationID = sm.MedicationID
            WHERE sm.SupplierID = %s
            ORDER BY m.MedicationName
            """,
            (supplier_id,)
        )
        rows = cursor.fetchall()

        print("\n--- SUPPLIER MEDICATIONS ---")
        if not rows:
            print("No medications are currently associated with this supplier.")
        else:
            print("ID | Medication | Dosage")
            print("-" * 55)
            for med_id, name, dosage in rows:
                print(f"{med_id} | {name} | {dosage}")
    finally:
        cursor.close()


def suppliers_by_medication(connection):
    med_id = int(input("Medication ID: "))

    cursor = connection.cursor()
    try:
        cursor.execute(
            """
            SELECT s.SupplierID, s.CompanyName, s.PhoneNumber
            FROM Supplier s
            JOIN SupplierMedication sm
                ON s.SupplierID = sm.SupplierID
            WHERE sm.MedicationID = %s
            ORDER BY s.CompanyName
            """,
            (med_id,)
        )
        rows = cursor.fetchall()

        print("\n--- MEDICATION SUPPLIERS ---")
        if not rows:
            print("No suppliers are currently associated with this medication.")
        else:
            print("ID | Company | Phone Number")
            print("-" * 55)
            for supplier_id, name, phone in rows:
                print(f"{supplier_id} | {name} | {phone}")
    finally:
        cursor.close()


def add_supplier_medication(connection):
    supplier_id = int(input("Supplier ID: "))
    med_id = int(input("Medication ID: "))

    cursor = connection.cursor()
    try:
        cursor.execute(
            """
            INSERT INTO SupplierMedication (SupplierID, MedicationID)
            VALUES (%s, %s)
            """,
            (supplier_id, med_id)
        )
        connection.commit()
        print("Supplier-medication record added successfully.")

    except Error as error:
        connection.rollback()
        print(f"Unable to add record: {error}")
    finally:
        cursor.close()


def remove_supplier_medication(connection):
    supplier_id = int(input("Supplier ID: "))
    med_id = int(input("Medication ID: "))

    cursor = connection.cursor()
    try:
        cursor.execute(
            """
            DELETE FROM SupplierMedication
            WHERE SupplierID = %s AND MedicationID = %s
            """,
            (supplier_id, med_id)
        )
        connection.commit()

        if cursor.rowcount > 0:
            print("Supplier-medication record removed successfully.")
        else:
            print("No matching record was found.")

    except Error as error:
        connection.rollback()
        print(f"Unable to remove record: {error}")
    finally:
        cursor.close()


def main():
    connection = None

    try:
        connection = connect_to_database()
        print("\nDatabase connection established.")

        while True:
            print("\n========================================")
            print("       PHARMACY INVENTORY SYSTEM")
            print("========================================")
            print("1. View Suppliers")
            print("2. View Medications")
            print("3. View Medications by Supplier")
            print("4. View Suppliers by Medication")
            print("5. Assign Medication to Supplier")
            print("6. Remove Medication from Supplier")
            print("Q. Exit")

            choice = input("\nSelect an option: ").strip().lower()

            try:
                if choice == "1":
                    print_suppliers(connection)
                elif choice == "2":
                    print_medications(connection)
                elif choice == "3":
                    medications_by_supplier(connection)
                elif choice == "4":
                    suppliers_by_medication(connection)
                elif choice == "5":
                    add_supplier_medication(connection)
                elif choice == "6":
                    remove_supplier_medication(connection)
                elif choice == "q":
                    print("Exiting Pharmacy Inventory System.")
                    break
                else:
                    print("Invalid selection. Please choose an option from the menu.")

            except ValueError:
                print("Invalid ID. Please enter a number.")

    except Error as error:
        print(f"Database connection failed: {error}")

    finally:
        if connection is not None and connection.is_connected():
            connection.close()


if __name__ == "__main__":
    main()
