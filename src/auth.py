import csv
import os
import hashlib


class Auth:
    def __init__(self, filepath: str = "data/users.csv"):
        self.filepath = filepath
        self._ensure_file()

    # -------------------------------------------------
    # Pastikan file users.csv ada + header benar
    # -------------------------------------------------
    def _ensure_file(self):
        os.makedirs(os.path.dirname(self.filepath), exist_ok=True)

        # kalau file belum ada atau kosong -> buat header baru
        if (not os.path.exists(self.filepath)
                or os.path.getsize(self.filepath) == 0):
            with open(self.filepath, "w", newline="", encoding="utf-8") as f:
                writer = csv.writer(f)
                writer.writerow(["user_id", "email", "password_hash"])

    # -------------------------------------------------
    # Load semua user dari CSV
    # -------------------------------------------------
    def _load_users(self):
        self._ensure_file()
        users = []
        with open(self.filepath, "r", newline="", encoding="utf-8") as f:
            reader = csv.DictReader(f)
            for row in reader:
                # skip kalau tidak lengkap (jaga-jaga kalau ada file lama)
                if "user_id" not in row or "email" not in row or "password_hash" not in row:
                    continue
                users.append({
                    "user_id": int(row["user_id"]),
                    "email": row["email"],
                    "password_hash": row["password_hash"],
                })
        return users

    # -------------------------------------------------
    # Simpan user ke CSV
    # -------------------------------------------------
    def _save_users(self, users):
        with open(self.filepath, "w", newline="", encoding="utf-8") as f:
            fieldnames = ["user_id", "email", "password_hash"]
            writer = csv.DictWriter(f, fieldnames=fieldnames)
            writer.writeheader()
            for user in users:
                writer.writerow(user)

    # -------------------------------------------------
    # Hash password
    # -------------------------------------------------
    def _hash_password(self, password: str) -> str:
        return hashlib.sha256(password.encode("utf-8")).hexdigest()

    # -------------------------------------------------
    # REGISTER: tambah user baru + auto user_id
    # -------------------------------------------------
    def register(self, email: str, password: str):
        users = self._load_users()

        # cek email sudah dipakai belum
        for u in users:
            if u["email"].lower() == email.lower():
                raise ValueError("Email sudah terdaftar.")

        # cari user_id terbesar lalu +1
        last_id = max((u["user_id"] for u in users), default=0)
        new_id = last_id + 1

        new_user = {
            "user_id": new_id,
            "email": email,
            "password_hash": self._hash_password(password),
        }
        users.append(new_user)
        self._save_users(users)
        return new_user

    # -------------------------------------------------
    # LOGIN: cek email + password
    # -------------------------------------------------
    def login(self, email: str, password: str):
        users = self._load_users()
        pwd_hash = self._hash_password(password)

        for u in users:
            if u["email"].lower() == email.lower() and u["password_hash"] == pwd_hash:
                return u  # sukses: return dict user

        return None