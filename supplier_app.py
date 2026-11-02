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


if __name__ == "__main__":
    app.run(port=8000, debug=True, host="127.0.0.1")
