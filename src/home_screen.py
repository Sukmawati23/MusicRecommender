# src/home_screen.py
import tkinter as tk
from tkinter import ttk


def start_home_screen(user):
    root = tk.Toplevel()  # buka window baru, bukan root
    root.title("Music Recommender - Home")
    root.geometry("820x480")
    root.configure(bg="#f4f7fb")

    header = tk.Frame(root, bg="#2d6cdf")
    header.pack(fill="x")

    title = tk.Label(
        header,
        text="Sonova Music Recommender",
        font=("Segoe UI", 16, "bold"),
        fg="white",
        bg="#2d6cdf",
        pady=10,
    )
    title.pack(side="left", padx=16)

    user_label = tk.Label(
        header,
        text=f"👤 {user.email}",
        font=("Segoe UI", 10),
        fg="#e5f3ff",
        bg="#2d6cdf",
    )
    user_label.pack(side="right", padx=16)

    body = tk.Frame(root, bg="#f4f7fb", padx=20, pady=20)
    body.pack(fill="both", expand=True)

    tk.Label(
        body,
        text="Daftar Lagu (dummy dulu)",
        font=("Segoe UI", 12, "bold"),
        bg="#f4f7fb",
    ).grid(row=0, column=0, sticky="w")

    tk.Label(
        body,
        text="Rekomendasi Untuk Kamu (dummy)",
        font=("Segoe UI", 12, "bold"),
        bg="#f4f7fb",
    ).grid(row=0, column=1, sticky="w", padx=(40, 0))

    songs = tk.Listbox(body, height=12)
    songs.grid(row=1, column=0, sticky="nsew", pady=(8, 0))

    for s in ["Cinta Dilema", "Lagu Bergema", "Senja Tenang", "Malam Biru"]:
        songs.insert(tk.END, s)

    recs = tk.Listbox(body, height=12)
    recs.grid(row=1, column=1, sticky="nsew", padx=(40, 0), pady=(8, 0))

    for r in ["Rek: Melofi Beat", "Rek: Midnight Chill", "Rek: Echo Room"]:
        recs.insert(tk.END, r)

    body.columnconfigure(0, weight=1)
    body.columnconfigure(1, weight=1)

    root.transient()  # biar di atas window login
    root.grab_set()   # fokus ke window ini