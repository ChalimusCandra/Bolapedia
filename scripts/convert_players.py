import pandas as pd
import os

def convert_players_to_documents(players_csv_path: str, clubs_csv_path: str, output_dir: str) -> int:
    """Konversi players.csv menjadi dokumen teks deskriptif per pemain."""
    print(f"Membaca {players_csv_path}...")
    df_players = pd.read_csv(players_csv_path)
    
    # Buat kamus klub untuk resolusi nama klub
    club_dict = {}
    if os.path.exists(clubs_csv_path):
        print(f"Membaca {clubs_csv_path} untuk nama klub...")
        df_clubs = pd.read_csv(clubs_csv_path)
        for _, row in df_clubs.iterrows():
            club_dict[row['club_id']] = row['name']
            
    os.makedirs(output_dir, exist_ok=True)
    
    count = 0
    for _, row in df_players.iterrows():
        # Dapatkan nama klub saat ini
        club_id = row.get('current_club_id')
        club_name = club_dict.get(club_id, "Tidak diketahui") if pd.notna(club_id) else "Tidak diketahui"
        
        # Format market value ke jutaan/ribuan euro jika ada
        mv = row.get('market_value_in_eur')
        mv_str = "Tidak diketahui"
        if pd.notna(mv):
            mv_str = f"€{mv:,.0f}"
            
        doc = f"""Profil Pemain: {row['name']}
Nama Lengkap: {row['name']}
Posisi: {row.get('position', 'Tidak diketahui')}
Tanggal Lahir: {row.get('date_of_birth', 'Tidak diketahui')}
Negara Asal: {row.get('country_of_citizenship', 'Tidak diketahui')}
Klub Saat Ini: {club_name}
Tinggi Badan: {f"{row['height_in_cm']} cm" if pd.notna(row.get('height_in_cm')) else 'Tidak diketahui'}
Kaki Dominan: {row.get('foot', 'Tidak diketahui')}
Nilai Pasar (Market Value): {mv_str}
"""
        filename = f"player_{row['player_id']}.txt"
        with open(os.path.join(output_dir, filename), "w", encoding="utf-8") as f:
            f.write(doc)
        count += 1
        
    print(f"[SUKSES] {count} dokumen profil pemain berhasil dibuat di {output_dir}")
    return count

if __name__ == "__main__":
    convert_players_to_documents(
        "data/raw/players.csv",
        "data/raw/clubs.csv",
        "data/processed/players"
    )
