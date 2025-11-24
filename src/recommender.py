import numpy as np
import pandas as pd
from sklearn.metrics.pairwise import cosine_similarity

def get_user_similarity(user_item_matrix):
    """Hitung cosine similarity antar user — aman untuk matriks kecil/kosong"""
    if user_item_matrix.empty or len(user_item_matrix) < 2:
        # Jika hanya 1 user atau kosong → buat matriks identitas
        n = max(len(user_item_matrix), 1)
        return pd.DataFrame(
            np.eye(n),
            index=user_item_matrix.index if not user_item_matrix.empty else [1],
            columns=user_item_matrix.index if not user_item_matrix.empty else [1]
        )
    
    # Hitung cosine similarity
    sim = cosine_similarity(user_item_matrix)
    return pd.DataFrame(
        sim,
        index=user_item_matrix.index,
        columns=user_item_matrix.index
    )

def predict_ratings(user_item_matrix, user_similarity):
    """Prediksi rating — hindari division by zero"""
    if user_item_matrix.empty:
        return pd.DataFrame()
    
    # Rata-rata tiap user (jika semua rating 0, mean = 0)
    user_mean = user_item_matrix.mean(axis=1)
    
    # Centering
    centered = user_item_matrix.sub(user_mean, axis=0)
    
    # Hitung weighted sum dan norm (hindari pembagian dengan 0)
    weighted_sum = user_similarity.dot(centered)
    sim_sum = np.abs(user_similarity).sum(axis=1)
    
    # Ganti 0 dengan 1 di denominator agar tidak error (user tanpa tetangga mirip)
    sim_sum_nozero = sim_sum.replace(0, 1)
    
    pred_centered = weighted_sum.div(sim_sum_nozero, axis=0)
    pred = pred_centered.add(user_mean, axis=0)
    
    return pred

def recommend_songs(user_id, user_item_matrix, pred_ratings, songs_df, top_n=5):
    """Rekomendasi lagu — handle user baru & fallback ke popularitas"""
    # ✅ Handle user yang belum ada di matrix (user baru)
    if user_id not in user_item_matrix.index:
        # Fallback: rekomendasi lagu paling populer
        popular = songs_df.sort_values('populer', ascending=False).head(top_n)
        return [
            {
                'song_id': int(row['song_id']),
                'title': row['title'],
                'artist': row['artist'],
                'genre': row['top genre'],
                'year': int(row['year']),
                'popularity': int(row['populer']),
                'predicted_rating': 0.0  # atau None, atau "Populer"
            }
            for _, row in popular.iterrows()
        ]
    
    # Ambil rating user
    user_ratings = user_item_matrix.loc[user_id]
    
    # Cari lagu yang belum di-rate (rating == 0)
    unrated_mask = user_ratings == 0
    if not unrated_mask.any():
        # Jika semua lagu sudah di-rate → rekomendasi lagu paling populer dari yang belum di-rate (seharusnya tidak ada, tapi aman)
        return recommend_songs(user_id, user_item_matrix, pred_ratings, songs_df, top_n)[:top_n]
    
    unrated_song_ids = user_ratings[unrated_mask].index.tolist()
    
    # Ambil prediksi untuk lagu yang belum di-rate
    try:
        predictions = pred_ratings.loc[user_id, unrated_song_ids]
        predictions = predictions.dropna()
        top_pred = predictions.sort_values(ascending=False).head(top_n)
    except (KeyError, ValueError):
        # Jika pred_ratings belum ada → fallback ke popularitas
        candidates = songs_df[songs_df['song_id'].isin(unrated_song_ids)]
        if candidates.empty:
            candidates = songs_df
        top_pred = candidates.sort_values('populer', ascending=False).head(top_n)
        return [
            {
                'song_id': int(row['song_id']),
                'title': row['title'],
                'artist': row['artist'],
                'genre': row['top genre'],
                'year': int(row['year']),
                'popularity': int(row['populer']),
                'predicted_rating': 0.0
            }
            for _, row in top_pred.iterrows()
        ]
    
    # Konversi ke list rekomendasi
    result = []
    for song_id in top_pred.index:
        song_id_int = int(song_id)
        song_row = songs_df[songs_df['song_id'] == song_id_int]
        if not song_row.empty:
            song_data = song_row.iloc[0]
            result.append({
                'song_id': song_id_int,
                'title': song_data['title'],
                'artist': song_data['artist'],
                'genre': song_data['top genre'],
                'year': int(song_data['year']),
                'popularity': int(song_data['populer']),
                'predicted_rating': round(top_pred[song_id], 2)
            })
        if len(result) >= top_n:
            break
    
    # Jika tidak cukup hasil → tambah dari populer
    while len(result) < top_n and len(result) < len(songs_df):
        remaining = songs_df[~songs_df['song_id'].isin([r['song_id'] for r in result])]
        if remaining.empty:
            break
        top_pop = remaining.sort_values('populer', ascending=False).iloc[0]
        result.append({
            'song_id': int(top_pop['song_id']),
            'title': top_pop['title'],
            'artist': top_pop['artist'],
            'genre': top_pop['top genre'],
            'year': int(top_pop['year']),
            'popularity': int(top_pop['populer']),
            'predicted_rating': 0.0
        })
    
    return result[:top_n]