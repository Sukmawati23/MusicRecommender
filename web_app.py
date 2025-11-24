from flask import Flask, render_template, request, redirect, url_for
from src.auth import Auth

app = Flask(__name__)
auth = Auth()


@app.route("/")
def index():
    return redirect(url_for("login"))


@app.route("/login", methods=["GET", "POST"])
def login():
    error = None
    if request.method == "POST":
        email = request.form["email"]
        password = request.form["password"]

        user = auth.login(email, password)
        if user:
            return redirect(url_for("home"))
        else:
            error = "Email atau password salah."

    return render_template("login.html", error=error)


@app.route("/register", methods=["GET", "POST"])
def register():
    error = None
    if request.method == "POST":
        email = request.form["email"]
        password = request.form["password"]

        try:
            auth.register(email, password)
            return redirect(url_for("login"))
        except ValueError as e:
            error = str(e)

    return render_template("register.html", error=error)


@app.route("/home")
def home():
    return render_template("home.html")


if __name__ == "__main__":
    app.run(debug=True)