from flask import Flask, send_file

app = Flask(__name__)

@app.route("/")
def medication_inventory():
    return send_file("medications.html")

if __name__ == "__main__":
    app.run(debug=True)