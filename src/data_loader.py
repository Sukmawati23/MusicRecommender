import pandas as pd
import os

def load_all_data():
    songs_path = os.path.join("data", "songs.csv")
    try:
        songs = pd.read_csv(songs_path, sep=';', encoding='utf-8-sig')
    except UnicodeDecodeError:
        # fallback jika UTF-8-SIG gagal
        songs = pd.read_csv(songs_path, sep=';', encoding='latin1')
    except Exception as e:
        raise RuntimeError(f"Gagal memuat songs.csv: {e}")

    ratings_path = os.path.join("data", "ratings.csv")
    if os.path.exists(ratings_path):
        ratings = pd.read_csv(ratings_path)
    else:
        ratings = pd.DataFrame(columns=['user_id', 'song_id', 'rating'])
        ratings.to_csv(ratings_path, index=False)
    
    return songs, ratings

def create_user_item_matrix(ratings_df, songs_df):
    # Bersihkan song_id → buang NaN & konversi ke integer
    songs_df = songs_df.dropna(subset=['song_id']).copy()
    songs_df['song_id'] = pd.to_numeric(songs_df['song_id'], errors='coerce').astype('Int64')
    
    if ratings_df.empty:
        # Jika belum ada rating, buat matriks kosong
        all_ids = songs_df['song_id'].dropna().astype(int).tolist()
        return pd.DataFrame(columns=all_ids)
    
    # Bersihkan ratings_df juga
    ratings_df = ratings_df.dropna(subset=['song_id', 'user_id']).copy()
    ratings_df['song_id'] = pd.to_numeric(ratings_df['song_id'], errors='coerce').astype('Int64')
    ratings_df['user_id'] = pd.to_numeric(ratings_df['user_id'], errors='coerce').astype('Int64')
    
    # Hapus baris dengan NaN di song_id/user_id
    ratings_df = ratings_df.dropna(subset=['song_id', 'user_id'])
    
    matrix = ratings_df.pivot_table(
        index='user_id',
        columns='song_id',
        values='rating',
        fill_value=0
    )
    
    all_song_ids = songs_df['song_id'].dropna().astype(int).tolist()
    matrix = matrix.reindex(columns=all_song_ids, fill_value=0)
    return matrix