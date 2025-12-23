import json
import os
from datetime import datetime
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
        syarat_str = ""
        for k, v in r["syarat"].items():
            if k == "minat":
                syarat_str += f"Minat: {v}\n"
            else:
                # Mempercantik tampilan nama mata pelajaran
                nama_mapel = k.replace("_", " ").title()
                syarat_str += f"{nama_mapel} >= {v}\n"
        
        table.append([i, r["jurusan"], syarat_str.strip()])

    print(tabulate(table, headers=["No", "Rekomendasi Jurusan", "Syarat Kelulusan"], tablefmt="grid"))

# ===========================
# 3. Fitur Tambah Rule
# ===========================
def add_rule():
    print("\n=== TAMBAH RULE BARU ===")
    jurusan = input("Nama Jurusan: ")
    print("--- Masukkan Syarat (Tekan Enter jika kosong) ---")
    syarat = {}
    
    minat = input("Minat Spesifik (contoh: komputer/teknik/kesehatan): ").lower()
    if minat: syarat["minat"] = minat
        
    # Helper function untuk input nilai
    def input_syarat_nilai(label, key):
        while True:
            val = input(f"Minimal Nilai {label}: ")
            if not val: return None
            try:
                angka = int(val)
                if 0 <= angka <= 100: return angka
                print("⚠️ Nilai harus 0 - 100.")
            except ValueError:
                print("❌ Harus angka!")

    # Daftar Mapel yang bisa dijadikan syarat
    mapel_list = [
        ("Matematika", "mtk"),
        ("B.Inggris", "b_inggris"),
        ("B.Indonesia", "b_indonesia"),
        ("Fisika", "fisika"),
        ("Kimia", "kimia"),
        ("Biologi", "biologi"),
        ("Ekonomi", "ekonomi")
    ]

    for label, key in mapel_list:
        nilai = input_syarat_nilai(label, key)
        if nilai is not None:
            syarat[key] = nilai

    rules = load_rules()
    rules.append({"jurusan": jurusan, "syarat": syarat})
    save_rules(rules)
    print("✔ Rule tersimpan.")

# ===========================
# 4. Fitur Hapus Rule
# ===========================
def delete_rule():
    view_rules()
    rules = load_rules()
    if not rules: return
    try:
        idx = int(input("\nHapus Nomor: ")) - 1
        if 0 <= idx < len(rules):
            deleted = rules.pop(idx)
            save_rules(rules)
            print(f"✔ Rule '{deleted['jurusan']}' terhapus.")
        else: print("❌ Tidak valid.")
    except ValueError: print("❌ Harus angka.")

# ===========================
# 5. Fitur Update Rule
# ===========================
def update_rule():
    view_rules() # Tampilkan dulu biar user tau nomornya
    rules = load_rules()
    if not rules: return
    try:
        idx = int(input("\nEdit Nomor: ")) - 1
        if not (0 <= idx < len(rules)): return
        
        r = rules[idx]
        print(f"Edit {r['jurusan']} (Enter utk skip)")
        
        baru = input(f"Nama Jurusan [{r['jurusan']}]: ")
        if baru: r['jurusan'] = baru
        
        ubah_syarat = input("Ubah syarat? (y/n): ").lower()
        if ubah_syarat == 'y':
            print("Silakan input syarat baru (kosongkan jika tidak perlu):")
            syarat = {}
            minat = input("Minat: ").lower()
            if minat: syarat["minat"] = minat
            
            # Input ulang nilai-nilai
            mapel_list = [("Matematika", "mtk"), ("B.Inggris", "b_inggris"), 
                          ("B.Indonesia", "b_indonesia"), ("Fisika", "fisika"), 
                          ("Kimia", "kimia"), ("Biologi", "biologi"), ("Ekonomi", "ekonomi")]
            
            for label, key in mapel_list:
                val = input(f"Min {label}: ")
                if val: syarat[key] = int(val)
            
            r['syarat'] = syarat

        save_rules(rules)
        print("✔ Update sukses.")
    except ValueError: print("❌ Error input.")

# ===========================
# 6. CORE ENGINE: Forward Chaining
# ===========================
def forward_chaining():
    print("\n========================================")
    print("   SISTEM PAKAR PENENTUAN JURUSAN")
    print("========================================")
    
    nama = input("Nama Siswa: ")
    
    # --- VALIDASI INPUT NILAI ---
    def get_valid_score(label):
        while True:
            try:
                val = input(f"Nilai {label}: ")
                # Jika user kosongkan (Enter), anggap 0 (User tidak ambil mapel itu/Anak IPS/IPA)
                if not val: return 0 
                angka = int(val)
                if 0 <= angka <= 100: return angka
                print("⚠️ Nilai harus 0-100.")
            except ValueError:
                print("❌ Input harus angka.")

    user_data = {}
    print("\n--- Masukkan Minat & Nilai Rapor ---")
    print("(Tips: Ketik salah satu: komputer, manajemen, teknik, kesehatan, eksperimen, hitungan, bahasa)")
    user_data["minat"] = input("Minat Dominan: ").lower()
    
    # Meminta input semua mata pelajaran yang ada di Rule
    user_data["mtk"] = get_valid_score("Matematika")
    user_data["b_inggris"] = get_valid_score("Bahasa Inggris")
    user_data["b_indonesia"] = get_valid_score("Bahasa Indonesia")
    
    print("\n-- Kelompok IPA --")
    user_data["fisika"] = get_valid_score("Fisika")
    user_data["kimia"] = get_valid_score("Kimia")
    user_data["biologi"] = get_valid_score("Biologi")
    
    print("\n-- Kelompok IPS --")
    user_data["ekonomi"] = get_valid_score("Ekonomi")

    print("\nSedang menganalisis...")
    rules = load_rules()
    rekomendasi = []

    # Logic Pencocokan + PENJELASAN
    for rule in rules:
        syarat = rule["syarat"]
        match = True
        alasan = [] 
        
        for kriteria, butuh in syarat.items():
            punya = user_data.get(kriteria, 0) # Default 0 jika data tidak ada
            
            if kriteria == "minat":
                # Partial match: misal syarat 'komputer', user ketik 'suka komputer' -> Tetap Match
                if butuh not in punya: 
                    match = False; break
                alasan.append(f"Minat sesuai ({butuh})")
            else: # Nilai Angka
                if punya < butuh:
                    match = False; break
                # Format nama mapel biar bagus
                nama_mapel = kriteria.replace("_", " ").title()
                alasan.append(f"{nama_mapel}: {punya} (Min: {butuh})")
        
        if match:
            rekomendasi.append({
                "jurusan": rule["jurusan"],
                "detail": ", ".join(alasan)
            })

    # Output & Laporan
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    print(f"\n=== HASIL REKOMENDASI: {nama.upper()} ===")
    if rekomendasi:
        print(f"Berdasarkan analisis sistem:")
        for rek in rekomendasi:
            print(f"\n✅ {rek['jurusan']}")
            print(f"   Alasan Kuat: {rek['detail']}")
        
        # Simpan ke File
        with open("hasil_konsultasi.txt", "a") as f:
            jurusan_str = ", ".join([r['jurusan'] for r in rekomendasi])
            f.write(f"[{timestamp}] {nama}: {jurusan_str}\n")
            print("\n(Data tersimpan di hasil_konsultasi.txt)")
    else:
        print("⚠️ Tidak ada jurusan yang cocok.")
        print("Saran: Coba cek kembali input nilai atau minat Anda.")

# ===========================
# MAIN MENU
# ===========================
def main_menu():
    while True:
        print("\n[ MENU UTAMA ]")
        print("1. Konsultasi Siswa")
        print("2. Lihat Knowledge Base")
        print("3. Tambah Rule")
        print("4. Update Rule")
        print("5. Hapus Rule")
        print("6. Keluar")
        
        p = input(">> Pilih: ")
        if p == "1": forward_chaining()
        elif p == "2": view_rules()
        elif p == "3": add_rule()
        elif p == "4": update_rule()
        elif p == "5": delete_rule()
        elif p == "6": break
        else: print("Salah pilih.")

if __name__ == "__main__":
    main_menu()
