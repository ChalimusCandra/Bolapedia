import os
import sys

# Tambahkan direktori scripts ke path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from convert_competitions import convert_competitions_to_documents
from convert_clubs import convert_clubs_to_documents
from convert_players import convert_players_to_documents
from convert_transfers import convert_transfers_to_documents
from convert_games import convert_games_to_documents

def main():
    print("=== Memulai Konversi Dataset BolaPedia ===")
    
    # Path Data Raw
    raw_players = "data/raw/players.csv"
    raw_clubs = "data/raw/clubs.csv"
    raw_competitions = "data/raw/competitions.csv"
    raw_transfers = "data/raw/transfers.csv"
    raw_games = "data/raw/games.csv"
    
    # Path Data Processed
    proc_players = "data/processed/players"
    proc_clubs = "data/processed/clubs"
    proc_competitions = "data/processed/competitions"
    proc_transfers = "data/processed/transfers"
    proc_games = "data/processed/matches"
    
    # 1. Konversi Kompetisi
    convert_competitions_to_documents(raw_competitions, proc_competitions)
    
    # 2. Konversi Klub
    convert_clubs_to_documents(raw_clubs, raw_competitions, proc_clubs)
    
    # 3. Konversi Pemain
    convert_players_to_documents(raw_players, raw_clubs, proc_players)
    
    # 4. Konversi Transfer
    convert_transfers_to_documents(raw_transfers, raw_players, raw_clubs, proc_transfers)
    
    # 5. Konversi Pertandingan
    convert_games_to_documents(raw_games, raw_clubs, raw_competitions, proc_games)
    
    print("=== Semua Konversi Selesai Sukses! ===")

if __name__ == "__main__":
    main()
