# web_app.py — versi lengkap & sesuai alur
from flask import Flask, render_template, request, redirect, url_for, flash
from src.auth import Auth
from src.data_loader import load_all_data, create_user_item_matrix
from src.recommender import get_user_similarity, predict_ratings, recommend_songs
from src.storage import add_rating
import pandas as pd
import os

app = Flask(__name__)
app.secret_key = "musewave-2025-secure"  # wajib untuk flash()
auth = Auth()

# ------------------------------
@app.route("/")
def index():
    return redirect(url_for("login"))

# ------------------------------
@app.route("/login", methods=["GET", "POST"])
def login():
    error = None
    if request.method == "POST":
        email = request.form["email"]
        password = request.form["password"]
        user = auth.login(email, password)
        if user:
            flash("✅ Login berhasil! Selamat datang di Musewave.", "success")
            return redirect(url_for("home", email=email))
        else:
            error = "Email atau password salah."
    return render_template("login.html", error=error)

# ------------------------------
@app.route("/register", methods=["GET", "POST"])
def register():
    error = None
    if request.method == "POST":
        email = request.form["email"]
        password = request.form["password"]
        try:
            auth.register(email, password)
            flash("✅ Akun berhasil dibuat. Silakan login.", "success")
            return redirect(url_for("login"))
        except ValueError as e:
            error = str(e)
    return render_template("register.html", error=error)

# ------------------------------
@app.route("/home")
def home():
    email = request.args.get("email")
    if not email:
        return redirect(url_for("login"))

    # Ambil user_id dari users.csv
    users_df = pd.read_csv("data/users.csv")
    user_row = users_df[users_df["email"] == email]
    if user_row.empty:
        flash("⚠️ Pengguna tidak ditemukan.", "danger")
        return redirect(url_for("login"))
    user_id = int(user_row.iloc[0]["user_id"])

    try:
        # 📊 Muat data
        songs_df, ratings_df = load_all_data()
        user_item_matrix = create_user_item_matrix(ratings_df, songs_df)

        # 🔍 Hitung kesamaan user (cosine similarity)
        user_similarity = get_user_similarity(user_item_matrix)

        # 🎯 Prediksi rating lagu yang belum didengar
        pred_ratings = predict_ratings(user_item_matrix, user_similarity)

        # 🌟 Rekomendasikan lagu
        recommendations = recommend_songs(
            user_id=user_id,
            user_item_matrix=user_item_matrix,
            pred_ratings=pred_ratings,
            songs_df=songs_df,
            top_n=5
        )
    except Exception as e:
        flash(f"⚠️ Gagal memuat rekomendasi: {e}", "warning")
        recommendations = []

    return render_template(
        "home.html",
        user_email=email,
        user_id=user_id,
        songs=songs_df.to_dict("records"),
        recommendations=recommendations
    )

# ------------------------------
@app.route("/like", methods=["POST"])
def like_song():
    user_id = int(request.form["user_id"])
    song_id = int(request.form["song_id"])
    email = request.form["email"]

    # 💖 Simpan rating = 5 (like penuh)
    add_rating(user_id, song_id, rating=5)

    flash("❤️ Lagu disukai! Rekomendasi diperbarui berdasarkan preferensimu.", "success")
    return redirect(url_for("home", email=email))

# ------------------------------
if __name__ == "__main__":
    # Pastikan file minimal ada
    os.makedirs("data", exist_ok=True)
    if not os.path.exists("data/ratings.csv"):
        pd.DataFrame(columns=["user_id", "song_id", "rating"]).to_csv("data/ratings.csv", index=False)
    app.run(debug=True)