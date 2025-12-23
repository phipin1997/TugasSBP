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
                syarat_str += f"{k.capitalize()} >= {v}\n"
        
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
    
    minat = input("Minat Spesifik (komputer/teknik/manajemen): ").lower()
    if minat: syarat["minat"] = minat
        
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

    mtk = input_syarat_nilai("Matematika", "mtk")
    if mtk is not None: syarat["mtk"] = mtk
    
    ing = input_syarat_nilai("B.Inggris", "b_inggris")
    if ing is not None: syarat["b_inggris"] = ing
    
    fis = input_syarat_nilai("Fisika", "fisika")
    if fis is not None: syarat["fisika"] = fis

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
            rules.pop(idx)
            save_rules(rules)
            print("✔ Terhapus.")
        else: print("❌ Tidak valid.")
    except ValueError: print("❌ Harus angka.")

# ===========================
# 5. Fitur Update Rule
# ===========================
def update_rule():
    view_rules()
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
            # Logic update sederhana, reset syarat lama biar bersih
            print("Silakan input syarat baru:")
            syarat = {}
            minat = input("Minat: ").lower()
            if minat: syarat["minat"] = minat
            
            # Re-use logic input manual agar cepat (bisa dikembangkan lagi)
            mtk = input("Min MTK: ")
            if mtk: syarat["mtk"] = int(mtk)
            ing = input("Min B.Inggris: ")
            if ing: syarat["b_inggris"] = int(ing)
            fis = input("Min Fisika: ")
            if fis: syarat["fisika"] = int(fis)
            
            r['syarat'] = syarat

        save_rules(rules)
        print("✔ Update sukses.")
    except ValueError: print("❌ Error.")

# ===========================
# 6. CORE ENGINE: Forward Chaining
# ===========================
def forward_chaining():
    print("\n========================================")
    print("   SISTEM PAKAR PENENTUAN JURUSAN")
    print("========================================")
    
    nama = input("Nama Siswa: ")
    
    # --- VALIDASI INPUT NILAI (ANTI DOSEN ISENG) ---
    def get_valid_score(mapel):
        while True:
            try:
                val = int(input(f"Nilai {mapel}: "))
                if 0 <= val <= 100: return val
                print("⚠️ Nilai tidak masuk akal (harus 0-100).")
            except ValueError:
                print("❌ Input harus angka.")

    user_data = {}
    user_data["minat"] = input("Minat (komputer/teknik/manajemen): ").lower()
    user_data["mtk"] = get_valid_score("Matematika")
    user_data["b_inggris"] = get_valid_score("Bahasa Inggris")
    user_data["fisika"] = get_valid_score("Fisika")

    print("\nSedang menganalisis...")
    rules = load_rules()
    rekomendasi = []

    # Logic Pencocokan + PENJELASAN
    for rule in rules:
        syarat = rule["syarat"]
        match = True
        alasan = [] # Menyimpan alasan kenapa cocok
        
        for kriteria, butuh in syarat.items():
            punya = user_data.get(kriteria)
            
            if kriteria == "minat":
                if punya != butuh:
                    match = False; break
                alasan.append(f"Minat sesuai ({butuh})")
            else: # Nilai Angka
                if punya < butuh:
                    match = False; break
                alasan.append(f"Nilai {kriteria.upper()} {punya} (Min: {butuh})")
        
        if match:
            rekomendasi.append({
                "jurusan": rule["jurusan"],
                "detail": ", ".join(alasan)
            })

    # Output & Laporan
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    print(f"\n=== HASIL ANALISIS: {nama.upper()} ===")
    if rekomendasi:
        print(f"Berdasarkan analisis pada {timestamp}:")
        for rek in rekomendasi:
            print(f"\n✅ {rek['jurusan']}")
            print(f"   Alasan: {rek['detail']}")
        
        # Simpan ke File (Bukti Fisik)
        with open("hasil_konsultasi.txt", "a") as f:
            f.write(f"\n[{timestamp}] {nama}: {', '.join([r['jurusan'] for r in rekomendasi])}")
            print("\n(Hasil telah disimpan ke hasil_konsultasi.txt)")
    else:
        print("⚠️ Mohon maaf, kualifikasi belum memenuhi syarat jurusan manapun.")
        print("Saran: Coba tingkatkan nilai akademik atau eksplorasi minat lain.")

# ===========================
# MAIN MENU
# ===========================
def main_menu():
    while True:
        print("\n[ MENU UTAMA ]")
        print("1. Konsultasi")
        print("2. Database Rules")
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
