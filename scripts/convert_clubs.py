import pandas as pd
import os

def convert_clubs_to_documents(clubs_csv_path: str, competitions_csv_path: str, output_dir: str) -> int:
    """Konversi clubs.csv menjadi dokumen teks deskriptif per klub."""
    print(f"Membaca {clubs_csv_path}...")
    df_clubs = pd.read_csv(clubs_csv_path)
    
    # Buat kamus kompetisi untuk resolusi nama kompetisi
    comp_dict = {}
    if os.path.exists(competitions_csv_path):
        print(f"Membaca {competitions_csv_path} untuk nama liga...")
        df_comp = pd.read_csv(competitions_csv_path)
        for _, row in df_comp.iterrows():
            comp_dict[row['competition_id']] = row['name']
            
    os.makedirs(output_dir, exist_ok=True)
    
    count = 0
    for _, row in df_clubs.iterrows():
        comp_id = row.get('domestic_competition_id')
        comp_name = comp_dict.get(comp_id, "Tidak diketahui") if pd.notna(comp_id) else "Tidak diketahui"
        
        doc = f"""Profil Klub: {row['name']}
Nama Klub: {row['name']}
Liga Domestik: {comp_name}
Jumlah Anggota Skuad (Squad Size): {row.get('squad_size', 'Tidak diketahui')}
Nama Stadion: {row.get('stadium_name', 'Tidak diketahui')}
Kapasitas Stadion: {f"{row['stadium_seats']:,} kursi" if pd.notna(row.get('stadium_seats')) else 'Tidak diketahui'}
Pelatih (Coach): {row.get('coach_name', 'Tidak diketahui')}
"""
        filename = f"club_{row['club_id']}.txt"
        with open(os.path.join(output_dir, filename), "w", encoding="utf-8") as f:
            f.write(doc)
        count += 1
        
    print(f"[SUKSES] {count} dokumen profil klub berhasil dibuat di {output_dir}")
    return count

if __name__ == "__main__":
    convert_clubs_to_documents(
        "data/raw/clubs.csv",
        "data/raw/competitions.csv",
        "data/processed/clubs"
    )
