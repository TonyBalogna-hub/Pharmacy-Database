import os

import mysql.connector
from flask import Flask, redirect, render_template, request, url_for

app = Flask(__name__)


def connect():
    return mysql.connector.connect(
        host=os.environ["SQL_HOST"],
        user=os.environ["SQL_USER"],
        password=os.environ["SQL_PWD"],
        database=os.environ["SQL_DB"],
    )


@app.route("/", methods=["GET", "POST"])
def suppliers():
    error = None

    if request.method == "POST":
        company = request.form.get("company", "").strip()
        phone = request.form.get("phone", "").strip()
        address = request.form.get("address", "").strip()

        if not company or not phone or not address:
            error = "Please fill out every field."
        elif len(company) > 100 or len(phone) > 20 or len(address) > 200:
            error = "One of the fields is too long."
        else:
            connection = connect()
            cursor = connection.cursor()
            try:
                # The values are parameters, which prevents SQL injection.
                # SupplierID is left out so MySQL assigns it automatically.
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

    # Flask/Jinja escapes the supplier text in the HTML template.
    return render_template("suppliers.html", suppliers=rows, error=error)


if __name__ == "__main__":
    app.run(port=8000, debug=True, host="127.0.0.1")
