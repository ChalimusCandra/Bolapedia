import pandas as pd
import os

def convert_competitions_to_documents(competitions_csv_path: str, output_dir: str) -> int:
    """Konversi competitions.csv menjadi dokumen teks deskriptif per kompetisi."""
    print(f"Membaca {competitions_csv_path}...")
    df_comp = pd.read_csv(competitions_csv_path)
    
    os.makedirs(output_dir, exist_ok=True)
    
    count = 0
    for _, row in df_comp.iterrows():
        comp_type = row.get('type', 'Tidak diketahui')
        if comp_type == 'domestic_league':
            type_id = 'Liga Domestik'
        elif comp_type == 'domestic_cup':
            type_id = 'Piala Domestik'
        elif comp_type == 'international_cup':
            type_id = 'Kompetisi Internasional'
        else:
            type_id = comp_type
            
        doc = f"""Profil Kompetisi: {row['name']}
Nama Kompetisi: {row['name']}
Tipe Kompetisi: {type_id}
Negara Penyelenggara: {row.get('country_name', 'Internasional')}
Konfederasi: {row.get('confederation', 'Tidak diketahui')}
Kode Kompetisi: {row['competition_id']}
"""
        filename = f"competition_{row['competition_id']}.txt"
        with open(os.path.join(output_dir, filename), "w", encoding="utf-8") as f:
            f.write(doc)
        count += 1
        
    print(f"[SUKSES] {count} dokumen kompetisi berhasil dibuat di {output_dir}")
    return count

if __name__ == "__main__":
    convert_competitions_to_documents(
        "data/raw/competitions.csv",
        "data/processed/competitions"
    )
