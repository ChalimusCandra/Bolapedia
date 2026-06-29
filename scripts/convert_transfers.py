import pandas as pd
import os

def convert_transfers_to_documents(transfers_csv_path: str, players_csv_path: str, clubs_csv_path: str, output_dir: str) -> int:
    """Konversi transfers.csv menjadi dokumen teks deskriptif per transfer pemain."""
    print(f"Membaca {transfers_csv_path}...")
    df_transfers = pd.read_csv(transfers_csv_path)
    
    # Resolusi ID ke nama
    player_dict = {}
    if os.path.exists(players_csv_path):
        print(f"Membaca {players_csv_path} untuk nama pemain...")
        df_players = pd.read_csv(players_csv_path)
        for _, row in df_players.iterrows():
            player_dict[row['player_id']] = row['name']
            
    club_dict = {}
    if os.path.exists(clubs_csv_path):
        print(f"Membaca {clubs_csv_path} untuk nama klub...")
        df_clubs = pd.read_csv(clubs_csv_path)
        for _, row in df_clubs.iterrows():
            club_dict[row['club_id']] = row['name']
            
    os.makedirs(output_dir, exist_ok=True)
    
    count = 0
    # Kita hanya mengolah transfer yang memiliki nama pemain untuk menghemat space dan menjaga kualitas
    for _, row in df_transfers.iterrows():
        player_id = row['player_id']
        player_name = player_dict.get(player_id)
        if not player_name:
            continue  # Lewati jika profil pemain tidak ditemukan di players.csv
            
        from_club = club_dict.get(row.get('from_club_id'), "Tidak diketahui")
        to_club = club_dict.get(row.get('to_club_id'), "Tidak diketahui")
        
        fee = row.get('transfer_fee')
        fee_str = f"€{fee:,.0f}" if pd.notna(fee) else "Tidak diketahui / Bebas Transfer"
        
        mv = row.get('market_value_in_eur')
        mv_str = f"€{mv:,.0f}" if pd.notna(mv) else "Tidak diketahui"
        
        doc = f"""Informasi Transfer Pemain: {player_name}
Nama Pemain: {player_name}
Tanggal Transfer: {row.get('transfer_date', 'Tidak diketahui')}
Pindah Dari Klub: {from_club}
Pindah Ke Klub: {to_club}
Biaya Transfer (Transfer Fee): {fee_str}
Nilai Pasar Saat Transfer (Market Value): {mv_str}
"""
        # Nama file menggunakan player_id dan tanggal transfer untuk menjamin keunikan
        filename = f"transfer_{player_id}_{row.get('transfer_date', 'date')}.txt"
        # Ganti karakter ilegal untuk nama file jika ada
        filename = filename.replace("-", "_")
        with open(os.path.join(output_dir, filename), "w", encoding="utf-8") as f:
            f.write(doc)
        count += 1
        
    print(f"[SUKSES] {count} dokumen data transfer pemain berhasil dibuat di {output_dir}")
    return count

if __name__ == "__main__":
    convert_transfers_to_documents(
        "data/raw/transfers.csv",
        "data/raw/players.csv",
        "data/raw/clubs.csv",
        "data/processed/transfers"
    )
