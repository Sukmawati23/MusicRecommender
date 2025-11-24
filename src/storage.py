import pandas as pd
import os

def add_rating(user_id, song_id, rating=5):
    path = os.path.join("data", "ratings.csv")
    
    # Baca existing data
    if os.path.exists(path):
        df = pd.read_csv(path)
    else:
        df = pd.DataFrame(columns=['user_id', 'song_id', 'rating'])
    
    # Cek duplikat (user + song)
    mask = (df['user_id'] == user_id) & (df['song_id'] == song_id)
    if mask.any():
        # Update rating jika sudah ada
        df.loc[mask, 'rating'] = rating
    else:
        # Tambah baris baru
        new_row = pd.DataFrame([{
            'user_id': user_id,
            'song_id': song_id,
            'rating': rating
        }])
        df = pd.concat([df, new_row], ignore_index=True)
    
    # Simpan kembali ke file
    df.to_csv(path, index=False)