import pandas as pd
import os

def convert_games_to_documents(games_csv_path: str, clubs_csv_path: str, competitions_csv_path: str, output_dir: str) -> int:
    """Konversi games.csv menjadi dokumen teks deskriptif per pertandingan."""
    print(f"Membaca {games_csv_path}...")
    df_games = pd.read_csv(games_csv_path)
    
    # Resolusi ID ke nama
    club_dict = {}
    if os.path.exists(clubs_csv_path):
        print(f"Membaca {clubs_csv_path} untuk nama klub...")
        df_clubs = pd.read_csv(clubs_csv_path)
        for _, row in df_clubs.iterrows():
            club_dict[row['club_id']] = row['name']
            
    comp_dict = {}
    if os.path.exists(competitions_csv_path):
        print(f"Membaca {competitions_csv_path} untuk nama liga...")
        df_comp = pd.read_csv(competitions_csv_path)
        for _, row in df_comp.iterrows():
            comp_dict[row['competition_id']] = row['name']
            
    os.makedirs(output_dir, exist_ok=True)
    
    count = 0
    # Batasi data pertandingan ke 10000 pertandingan terbaru agar database tidak terlalu bengkak dan relevan
    # Urutkan berdasarkan tanggal jika kolom 'date' ada
    if 'date' in df_games.columns:
        df_games = df_games.sort_values(by='date', ascending=False)
    
    df_games_subset = df_games.head(10000) # Batasi ke 10.000 pertandingan terbaru
    
    for _, row in df_games_subset.iterrows():
        home_club = club_dict.get(row.get('home_club_id'), "Klub Tuan Rumah")
        away_club = club_dict.get(row.get('away_club_id'), "Klub Tamu")
        comp_name = comp_dict.get(row.get('competition_id'), "Kompetisi")
        
        home_goals = row.get('home_club_goals', 0)
        away_goals = row.get('away_club_goals', 0)
        
        # Tentukan pemenang
        if home_goals > away_goals:
            hasil = f"Pertandingan dimenangkan oleh {home_club} sebagai tuan rumah."
        elif away_goals > home_goals:
            hasil = f"Pertandingan dimenangkan oleh {away_club} sebagai tim tamu."
        else:
            hasil = "Pertandingan berakhir imbang (seri)."
            
        att_val = row.get('attendance')
        att_str = f"{att_val:,.0f}" if pd.notna(att_val) else "Tidak diketahui"
            
        doc = f"""Laporan Pertandingan: {home_club} vs {away_club}
Pertandingan: {home_club} melawan {away_club}
Skor Akhir: {home_club} {home_goals} - {away_goals} {away_club}
Tanggal Pertandingan: {row.get('date', 'Tidak diketahui')}
Kompetisi/Liga: {comp_name}
Lokasi / Stadion: {row.get('stadium', 'Tidak diketahui')}
Jumlah Penonton: {att_str}
Wasit (Referee): {row.get('referee', 'Tidak diketahui')}
Hasil Akhir: {hasil}
"""
        filename = f"game_{row['game_id']}.txt"
        with open(os.path.join(output_dir, filename), "w", encoding="utf-8") as f:
            f.write(doc)
        count += 1
        
    print(f"[SUKSES] {count} dokumen pertandingan berhasil dibuat di {output_dir}")
    return count

if __name__ == "__main__":
    convert_games_to_documents(
        "data/raw/games.csv",
        "data/raw/clubs.csv",
        "data/raw/competitions.csv",
        "data/processed/matches"
    )
