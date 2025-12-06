# src/data_loader.py
import pandas as pd
import os
import numpy as np

def load_all_data():
    # --- Load songs.csv ---
    songs_path = os.path.join("data", "songs.csv")
    try:
        songs = pd.read_csv(songs_path, sep=';', encoding='utf-8-sig')
    except UnicodeDecodeError:
        songs = pd.read_csv(songs_path, sep=';', encoding='latin1')
    except Exception as e:
        raise RuntimeError(f"Gagal memuat songs.csv: {e}")

    # --- Load ratings.csv (buat otomatis jika belum ada/kosong) ---
    ratings_path = os.path.join("data", "ratings.csv")
    if not os.path.exists(ratings_path) or os.path.getsize(ratings_path) == 0:
        # Buat file dengan header
        pd.DataFrame(columns=["user_id", "song_id", "rating"]).to_csv(
            ratings_path, index=False
        )
    
    try:
        ratings = pd.read_csv(ratings_path)
    except pd.errors.EmptyDataError:
        # Jika file ada tapi benar-benar kosong → buat ulang
        pd.DataFrame(columns=["user_id", "song_id", "rating"]).to_csv(
            ratings_path, index=False
        )
        ratings = pd.read_csv(ratings_path)

    # Pastikan kolom wajib ada
    required = {"user_id", "song_id", "rating"}
    if not required.issubset(set(ratings.columns)):
        missing = required - set(ratings.columns)
        raise ValueError(f"ratings.csv kehilangan kolom: {missing}")

    return songs, ratings


def create_user_item_matrix(ratings_df, songs_df):
    """
    Buat matriks user-item (user x song) berisi rating.
    - Kolom: semua song_id dari songs_df
    - Baris: user_id dari ratings_df
    - Nilai: rating (0 jika belum pernah di-rate)
    """
    # Bersihkan songs_df — pastikan song_id integer & valid
    songs_clean = songs_df.dropna(subset=['song_id']).copy()
    songs_clean['song_id'] = pd.to_numeric(songs_clean['song_id'], errors='coerce').astype('Int64')
    songs_clean = songs_clean.dropna(subset=['song_id'])
    all_song_ids = songs_clean['song_id'].astype(int).tolist()

    if ratings_df.empty:
        # Jika belum ada rating → buat matriks kosong (0 baris, banyak kolom)
        return pd.DataFrame(columns=all_song_ids, dtype=float)

    # Bersihkan ratings_df
    ratings_clean = ratings_df.dropna(subset=['user_id', 'song_id']).copy()
    ratings_clean['user_id'] = pd.to_numeric(ratings_clean['user_id'], errors='coerce').astype('Int64')
    ratings_clean['song_id'] = pd.to_numeric(ratings_clean['song_id'], errors='coerce').astype('Int64')
    ratings_clean = ratings_clean.dropna(subset=['user_id', 'song_id'])
    ratings_clean = ratings_clean[ratings_clean['song_id'].isin(all_song_ids)]

    if ratings_clean.empty:
        # Tidak ada rating yang valid → kembalikan matriks kosong
        return pd.DataFrame(columns=all_song_ids, dtype=float)

    # Buat pivot table
    matrix = ratings_clean.pivot_table(
        index='user_id',
        columns='song_id',
        values='rating',
        fill_value=0.0
    )

    # Pastikan semua lagu ada di kolom (bahkan yang belum pernah di-rate)
    matrix = matrix.reindex(columns=all_song_ids, fill_value=0.0)

    return matrix