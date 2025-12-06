# MusicRecommender.py
import tkinter as tk
from tkinter import ttk, messagebox
from pathlib import Path

from src.auth import Auth as AuthManager
from src.home_screen import start_home_screen


class AuthApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Sonova - Music Recommender")
        self.geometry("900x520")
        self.configure(bg="#e7f1ff")
        self.resizable(False, False)

        self.auth = AuthManager()

        self._build_ui()

    def _build_ui(self):
        wrapper = tk.Frame(self, bg="#e7f1ff", padx=24, pady=24)
        wrapper.pack(fill="both", expand=True)

        card = tk.Frame(
            wrapper,
            bg="white",
            bd=0,
            relief="solid",
        )
        card.pack(fill="both", expand=True)
        card.grid_rowconfigure(0, weight=1)
        card.grid_columnconfigure(1, weight=1)

        # KIRI: logo + tagline
        left = tk.Frame(card, bg="#2d6cdf", padx=28, pady=28)
        left.grid(row=0, column=0, sticky="nsew")

        # logo
        logo_path = Path(__file__).parent / "assets" / "logo-musik.png"
        try:
            self.logo_img = tk.PhotoImage(file=str(logo_path))
            logo_label = tk.Label(left, image=self.logo_img, bg="#2d6cdf")
            logo_label.pack(anchor="w")
        except Exception:
            tk.Label(left, text="♪", font=("Segoe UI", 38), bg="#2d6cdf", fg="white").pack(
                anchor="w"
            )

        tk.Label(
            left,
            text="Sonova",
            font=("Segoe UI", 22, "bold"),
            fg="white",
            bg="#2d6cdf",
        ).pack(anchor="w", pady=(12, 0))

        tk.Label(
            left,
            text="Smart Music Recommender\nberbasis Collaborative Filtering (User-Based).",
            font=("Segoe UI", 10),
            fg="#e5f3ff",
            bg="#2d6cdf",
            justify="left",
        ).pack(anchor="w", pady=(8, 0))

        tk.Label(
            left,
            text="Semakin banyak lagu yang kamu nilai,\n"
                 "semakin akurat rekomendasi yang kami berikan.",
            font=("Segoe UI", 9),
            fg="#cfe4ff",
            bg="#2d6cdf",
            justify="left",
        ).pack(anchor="w", pady=(20, 0))

        # KANAN: tab login & daftar
        right = tk.Frame(card, bg="white", padx=32, pady=28)
        right.grid(row=0, column=1, sticky="nsew")

        title = tk.Label(
            right,
            text="Selamat datang 👋",
            font=("Segoe UI", 16, "bold"),
            fg="#111827",
            bg="white",
        )
        title.pack(anchor="w")

        subtitle = tk.Label(
            right,
            text="Masuk atau buat akun baru untuk mulai mendapatkan rekomendasi musik pribadi.",
            font=("Segoe UI", 9),
            fg="#6b7280",
            bg="white",
            wraplength=380,
            justify="left",
        )
        subtitle.pack(anchor="w", pady=(4, 16))

        notebook = ttk.Notebook(right)
        notebook.pack(fill="both", expand=True)

        self.login_frame = tk.Frame(notebook, bg="white")
        self.register_frame = tk.Frame(notebook, bg="white")
        notebook.add(self.login_frame, text="Masuk")
        notebook.add(self.register_frame, text="Daftar")

        self._build_login_tab()
        self._build_register_tab()

    # ---------------- LOGIN TAB ----------------
    def _build_login_tab(self):
        f = self.login_frame

        tk.Label(
            f,
            text="Email",
            font=("Segoe UI", 10),
            bg="white",
        ).pack(anchor="w", pady=(16, 4))
        self.login_email = tk.Entry(f, font=("Segoe UI", 10))
        self.login_email.pack(fill="x")

        tk.Label(
            f,
            text="Kata Sandi",
            font=("Segoe UI", 10),
            bg="white",
        ).pack(anchor="w", pady=(12, 4))
        self.login_password = tk.Entry(f, font=("Segoe UI", 10), show="•")
        self.login_password.pack(fill="x")

        btn = tk.Button(
            f,
            text="Masuk",
            font=("Segoe UI", 10, "bold"),
            bg="#2d6cdf",
            fg="white",
            activebackground="#1f4fad",
            activeforeground="white",
            bd=0,
            padx=12,
            pady=6,
            command=self.handle_login,
        )
        btn.pack(anchor="e", pady=(18, 4))

        helper = tk.Label(
            f,
            text="Untuk demo, jika lupa password bisa daftar ulang dengan email lain.",
            font=("Segoe UI", 8),
            fg="#9ca3af",
            bg="white",
            wraplength=360,
            justify="left",
        )
        helper.pack(anchor="w", pady=(4, 0))

    # ---------------- REGISTER TAB ----------------
    def _build_register_tab(self):
        f = self.register_frame

        tk.Label(
            f,
            text="Email",
            font=("Segoe UI", 10),
            bg="white",
        ).pack(anchor="w", pady=(16, 4))
        self.reg_email = tk.Entry(f, font=("Segoe UI", 10))
        self.reg_email.pack(fill="x")

        tk.Label(
            f,
            text="Kata Sandi",
            font=("Segoe UI", 10),
            bg="white",
        ).pack(anchor="w", pady=(12, 4))
        self.reg_password = tk.Entry(f, font=("Segoe UI", 10), show="•")
        self.reg_password.pack(fill="x")

        btn = tk.Button(
            f,
            text="Daftar",
            font=("Segoe UI", 10, "bold"),
            bg="#10b981",
            fg="white",
            activebackground="#059669",
            activeforeground="white",
            bd=0,
            padx=12,
            pady=6,
            command=self.handle_register,
        )
        btn.pack(anchor="e", pady=(18, 4))

        helper = tk.Label(
            f,
            text="Gunakan email aktif. Password minimal 6 karakter "
                 "(disimpan dalam bentuk hash).",
            font=("Segoe UI", 8),
            fg="#9ca3af",
            bg="white",
            wraplength=360,
            justify="left",
        )
        helper.pack(anchor="w", pady=(4, 0))

    # ---------------- HANDLER ----------------
    def handle_register(self):
        email = self.reg_email.get().strip()
        password = self.reg_password.get().strip()

        if len(password) < 6:
            messagebox.showerror("Gagal", "Password minimal 6 karakter.")
            return

        try:
            user = self.auth.register(email, password)
            messagebox.showinfo("Berhasil", f"Akun {user.email} berhasil dibuat. Silakan login.")
        except ValueError as e:
            messagebox.showerror("Gagal", str(e))

    def handle_login(self):
        email = self.login_email.get().strip()
        password = self.login_password.get().strip()

        user = self.auth.login(email, password)
        if user is None:
            messagebox.showerror("Gagal", "Email atau password salah.")
            return

        messagebox.showinfo("Berhasil", f"Selamat datang, {user.email}!")
        start_home_screen(user)


if __name__ == "__main__":
    app = AuthApp()
    app.mainloop()