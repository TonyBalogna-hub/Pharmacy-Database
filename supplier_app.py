
import os

import mysql.connector
from dotenv import load_dotenv

load_dotenv()
from flask import Flask, abort, redirect, render_template, request, url_for

app = Flask(__name__)


def connect():
    return mysql.connector.connect(
        host=os.environ["SQL_HOST"],
        user=os.environ["SQL_USER"],
        password=os.environ["SQL_PWD"],
        database=os.environ["SQL_DB"],
    )


def get_fields():
    return (
        request.form.get("company", "").strip(),
        request.form.get("phone", "").strip(),
        request.form.get("address", "").strip(),
    )


def validate_fields(company, phone, address):
    if not company or not phone or not address:
        return "Please fill out every field."
    if len(company) > 100 or len(phone) > 20 or len(address) > 200:
        return "One of the fields is too long."
    return None


@app.route("/", methods=["GET", "POST"])
def suppliers():
    error = None

    if request.method == "POST":
        company, phone, address = get_fields()
        error = validate_fields(company, phone, address)
        if error is None:
            connection = connect()
            cursor = connection.cursor()
            try:
                cursor.execute(
                    "INSERT INTO Supplier (CompanyName, PhoneNumber, Address) "
                    "VALUES (%s, %s, %s)",
                    (company, phone, address),
                )
                connection.commit()
            finally:
                cursor.close()
                connection.close()
            return redirect(url_for("suppliers"))

    connection = connect()
    cursor = connection.cursor(dictionary=True)
    try:
        cursor.execute(
            "SELECT SupplierID, CompanyName, PhoneNumber, Address "
            "FROM Supplier ORDER BY SupplierID"
        )
        rows = cursor.fetchall()
    finally:
        cursor.close()
        connection.close()

    return render_template("suppliers.html", suppliers=rows, error=error)


@app.route("/edit/<int:supplier_id>", methods=["GET", "POST"])
def edit_supplier(supplier_id):
    error = None
    connection = connect()
    cursor = connection.cursor(dictionary=True)
    try:
        cursor.execute(
            "SELECT SupplierID, CompanyName, PhoneNumber, Address "
            "FROM Supplier WHERE SupplierID = %s",
            (supplier_id,),
        )
        supplier = cursor.fetchone()
        if supplier is None:
            abort(404)

        if request.method == "POST":
            company, phone, address = get_fields()
            error = validate_fields(company, phone, address)
            if error is None:
                cursor.execute(
                    "UPDATE Supplier SET CompanyName = %s, PhoneNumber = %s, "
                    "Address = %s WHERE SupplierID = %s",
                    (company, phone, address, supplier_id),
                )
                connection.commit()
                return redirect(url_for("suppliers"))
            supplier.update(
                CompanyName=company, PhoneNumber=phone, Address=address
            )
    finally:
        cursor.close()
        connection.close()

    return render_template("edit_supplier.html", supplier=supplier, error=error)


@app.route("/delete/<int:supplier_id>", methods=["POST"])
def delete_supplier(supplier_id):
    connection = connect()
    cursor = connection.cursor()
    try:
        cursor.execute("DELETE FROM Supplier WHERE SupplierID = %s", (supplier_id,))
        connection.commit()
    finally:
        cursor.close()
        connection.close()
    return redirect(url_for("suppliers"))


@app.route("/supplier/<int:supplier_id>", methods=["GET", "POST"])
def supplier_medications(supplier_id):
    error = None
    connection = connect()
    cursor = connection.cursor(dictionary=True)

    try:
        cursor.execute(
            "SELECT SupplierID, CompanyName FROM Supplier "
            "WHERE SupplierID = %s",
            (supplier_id,)
        )
        supplier = cursor.fetchone()

        if supplier is None:
            abort(404)

        if request.method == "POST":
            medication_id = request.form.get("medication_id", "")

            if medication_id.isdigit():
                cursor.execute(
                    """
                    INSERT INTO SupplierMedication (SupplierID, MedicationID)
                    SELECT %s, MedicationID
                    FROM Medication
                    WHERE MedicationID = %s
                    AND NOT EXISTS (
                        SELECT 1 FROM SupplierMedication
                        WHERE SupplierID = %s AND MedicationID = %s
                    )
                    """,
                    (supplier_id, int(medication_id),
                     supplier_id, int(medication_id))
                )

                if cursor.rowcount == 1:
                    connection.commit()
                    return redirect(
                        url_for("supplier_medications", supplier_id=supplier_id)
                    )
                error = "Medication is invalid or already assigned."
            else:
                error = "Please select a medication."

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
        medications = cursor.fetchall()

        cursor.execute(
            """
            SELECT m.MedicationID, m.MedicationName, m.Dosage
            FROM Medication m
            WHERE NOT EXISTS (
                SELECT 1 FROM SupplierMedication sm
                WHERE sm.MedicationID = m.MedicationID
                AND sm.SupplierID = %s
            )
            ORDER BY m.MedicationName
            """,
            (supplier_id,)
        )
        available_medications = cursor.fetchall()

    finally:
        cursor.close()
        connection.close()

    return render_template(
        "supplier_medications.html",
        supplier=supplier,
        medications=medications,
        available_medications=available_medications,
        error=error
    )


if __name__ == "__main__":
    app.run(port=8000, debug=True, host="127.0.0.1")
