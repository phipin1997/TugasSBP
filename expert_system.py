import json
import os
from tabulate import tabulate

RULES_FILE = "rules.json"

# ===========================
# 1. Load & Save Data
# ===========================
def load_rules():
    if not os.path.exists(RULES_FILE):
        return []
    with open(RULES_FILE, "r") as f:
        return json.load(f)

def save_rules(rules):
    with open(RULES_FILE, "w") as f:
        json.dump(rules, f, indent=4)

# ===========================
# 2. Fitur Tampilan (View)
# ===========================
def view_rules():
    rules = load_rules()
    print("\n=== BASIS PENGETAHUAN (RULES) ===")
    
    if not rules:
        print("Belum ada rule tersimpan.")
        return

    table = []
    for i, r in enumerate(rules, start=1):
        # Memformat syarat agar terlihat rapi di tabel
        syarat_str = ""
        for k, v in r["syarat"].items():
            if isinstance(v, str):
                syarat_str += f"{k.capitalize()}: {v}\n"
            else:
                syarat_str += f"{k.capitalize()} >= {v}\n"
        
        table.append([i, r["jurusan"], syarat_str.strip()])

    print(tabulate(table, headers=["No", "Rekomendasi Jurusan", "Syarat Kelulusan"], tablefmt="grid"))

# ===========================
# 3. Fitur Tambah Rule (Dinamis)
# ===========================
def add_rule():
    print("\n=== TAMBAH RULE BARU ===")
    jurusan = input("Nama Jurusan: ")
    
    print("--- Masukkan Syarat (Tekan Enter jika tidak ingin memberi syarat pada mapel tersebut) ---")
    
    syarat = {}
    
    # Input Minat
    minat = input("Minat Spesifik (misal: komputer/teknik/manajemen): ").lower()
    if minat:
        syarat["minat"] = minat
        
    # Input Nilai-nilai (Bisa ditambah mapel lain disini)
    try:
        mtk = input("Minimal Nilai Matematika: ")
        if mtk: syarat["mtk"] = int(mtk)
        
        inggris = input("Minimal Nilai B.Inggris: ")
        if inggris: syarat["b_inggris"] = int(inggris)
        
        fisika = input("Minimal Nilai Fisika: ")
        if fisika: syarat["fisika"] = int(fisika)
        
    except ValueError:
        print("Error: Nilai harus berupa angka!")
        return

    rules = load_rules()
    rules.append({
        "jurusan": jurusan,
        "syarat": syarat
    })
    save_rules(rules)
    print(f"✔ Rule untuk {jurusan} berhasil disimpan!")

# ===========================
# 4. CORE ENGINE: Forward Chaining
# ===========================
def forward_chaining():
    print("\n========================================")
    print("   SISTEM PAKAR PENENTUAN JURUSAN v2.0")
    print("========================================")
    
    # --- FASE 1: PENGUMPULAN FAKTA (FACT GATHERING) ---
    nama = input("Nama Siswa: ")
    
    print("\n--- Masukkan Data Akademik ---")
    user_data = {}
    
    # Kita ambil semua kemungkinan input yang diperlukan
    user_data["minat"] = input("Minat (komputer/teknik/manajemen): ").lower()
    
    try:
        user_data["mtk"] = int(input("Nilai Matematika: "))
        user_data["b_inggris"] = int(input("Nilai Bahasa Inggris: "))
        user_data["fisika"] = int(input("Nilai Fisika: "))
    except ValueError:
        print("❌ Error: Input nilai harus angka!")
        return

    # --- FASE 2: INFERENCE ENGINE (PENCOCOKAN RULE) ---
    print("\nSedang menganalisis kecocokan...")
    rules = load_rules()
    rekomendasi = []

    for rule in rules:
        syarat_jurusan = rule["syarat"]
        match = True # Asumsi awal cocok, kita cari celah gagalnya
        
        # Cek setiap syarat di dalam rule tersebut
        for kriteria, nilai_syarat in syarat_jurusan.items():
            
            # Jika kriteria (misal: fisika) ada di syarat, tapi user gak punya nilainya (misal user IPS)
            if kriteria not in user_data:
                match = False
                break
            
            nilai_user = user_data[kriteria]
            
            # Logika Pengecekan:
            # 1. Jika data berupa String (Text), harus SAMA PERSIS (misal: minat)
            if isinstance(nilai_syarat, str):
                if nilai_user != nilai_syarat:
                    match = False
                    break
            
            # 2. Jika data berupa Angka, user harus LEBIH BESAR ATAU SAMA DENGAN syarat
            elif isinstance(nilai_syarat, int):
                if nilai_user < nilai_syarat:
                    match = False
                    break
        
        # Jika lolos semua cek di atas, berarti cocok
        if match:
            rekomendasi.append(rule["jurusan"])

    # --- FASE 3: KESIMPULAN ---
    print(f"\n=== HASIL ANALISIS UNTUK {nama.upper()} ===")
    if rekomendasi:
        print(f"Berdasarkan nilai dan minat, Anda disarankan masuk ke:")
        for rek in rekomendasi:
            print(f"⭐ {rek}")
    else:
        print("⚠️ Tidak ada jurusan yang sesuai dengan kualifikasi saat ini.")
        print("Saran: Tingkatkan nilai akademik atau sesuaikan minat.")

# ===========================
# MAIN MENU
# ===========================
def main_menu():
    while True:
        print("\n\n[ MENU UTAMA ]")
        print("1. Jalankan Konsultasi (Forward Chaining)")
        print("2. Lihat Knowledge Base")
        print("3. Tambah Rule Baru")
        print("4. Keluar")
        
        pilih = input(">> Pilih: ")
        
        if pilih == "1":
            forward_chaining()
        elif pilih == "2":
            view_rules()
        elif pilih == "3":
            add_rule()
        elif pilih == "4":
            print("Terima kasih.")
            break
        else:
            print("Pilihan salah.")

if __name__ == "__main__":
    main_menu()
