import pandas as pd
import os

if __name__ == "__main__":
    print("Memvalidasi dataset songs.csv...\n")
    
    try:
        df = pd.read_csv("data/songs.csv", sep=';', encoding='utf-8-sig')
        print("Jumlah lagu:", len(df))
        print("Kolom:", list(df.columns))
        print("Sample lagu:", df.iloc[0]['title'])
        print("Song_id tipe data:", df['song_id'].dtype)
        print("populer range:", int(df['populer'].min()), "-", int(df['populer'].max()))
        print("\nDataset siap digunakan!")
    except Exception as e:
        print("Error:", e)
        print("Tips: Pastikan file songs.csv ada di folder data/ dan format delimiter ';'")