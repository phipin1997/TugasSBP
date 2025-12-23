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
        syarat_str = ""
        # Loop untuk menampilkan syarat dengan rapi
        for k, v in r["syarat"].items():
            if k == "minat":
                syarat_str += f"Minat: {v}\n"
            else:
                # Format nama mapel biar bagus (mtk -> Mtk)
                syarat_str += f"{k.upper() if len(k) < 4 else k.capitalize()} >= {v}\n"
        
        table.append([i, r["jurusan"], syarat_str.strip()])

    print(tabulate(table, headers=["No", "Rekomendasi Jurusan", "Syarat Kelulusan"], tablefmt="grid"))

# ===========================
# 3. Fitur Tambah Rule
# ===========================
def add_rule():
    print("\n=== TAMBAH RULE BARU ===")
    jurusan = input("Nama Jurusan: ")
    
    print("--- Masukkan Syarat (Tekan Enter jika tidak ada syarat utk mapel tsb) ---")
    syarat = {}
    
    # Input Minat
    minat = input("Minat Spesifik (misal: komputer/teknik/manajemen): ").lower()
    if minat: syarat["minat"] = minat
        
    # Input Nilai (Flexible)
    def input_nilai(label, key):
        val = input(f"Minimal Nilai {label}: ")
        if val: return int(val)
        return None

    try:
        mtk = input_nilai("Matematika", "mtk")
        if mtk: syarat["mtk"] = mtk
        
        ing = input_nilai("B.Inggris", "b_inggris")
        if ing: syarat["b_inggris"] = ing
        
        fis = input_nilai("Fisika", "fisika")
        if fis: syarat["fisika"] = fis
        
    except ValueError:
        print("❌ Error: Nilai harus angka!")
        return

    rules = load_rules()
    rules.append({"jurusan": jurusan, "syarat": syarat})
    save_rules(rules)
    print(f"✔ Rule {jurusan} berhasil disimpan!")

# ===========================
# 4. Fitur Hapus Rule
# ===========================
def delete_rule():
    view_rules()
    rules = load_rules()
    if not rules: return

    try:
        idx = int(input("\nMasukkan Nomor Rule yang akan dihapus: ")) - 1
        if 0 <= idx < len(rules):
            deleted = rules.pop(idx)
            save_rules(rules)
            print(f"✔ Rule '{deleted['jurusan']}' berhasil dihapus.")
        else:
            print("❌ Nomor tidak valid.")
    except ValueError:
        print("❌ Input harus angka.")

# ===========================
# 5. Fitur Update Rule
# ===========================
def update_rule():
    view_rules()
    rules = load_rules()
    if not rules: return

    try:
        idx = int(input("\nPilih Nomor Rule untuk diedit: ")) - 1
        if not (0 <= idx < len(rules)):
            print("❌ Nomor tidak valid.")
            return
            
        rule_lama = rules[idx]
        print(f"\n--- Mengedit Rule: {rule_lama['jurusan']} ---")
        print("(Tekan Enter jika tidak ingin mengubah data)")

        # Edit Nama Jurusan
        new_jurusan = input(f"Nama Jurusan [{rule_lama['jurusan']}]: ")
        if new_jurusan:
            rule_lama['jurusan'] = new_jurusan

        # Edit Syarat?
        edit_syarat = input("Apakah ingin mengubah syarat-syaratnya? (y/n): ").lower()
        if edit_syarat == 'y':
            syarat_baru = {}
            
            # Helper untuk input update
            def get_input(label, key, old_dict):
                old_val = old_dict.get(key, "")
                val = input(f"{label} [{old_val}]: ")
                if val: return val # Jika user ketik baru
                return old_val     # Jika user enter doang

            # Update Minat
            minat = get_input("Minat", "minat", rule_lama['syarat'])
            if minat: syarat_baru["minat"] = minat

            # Update Nilai
            try:
                # MTK
                mtk_old = rule_lama['syarat'].get('mtk', '')
                mtk_new = input(f"Min. Matematika [{mtk_old}]: ")
                if mtk_new: syarat_baru['mtk'] = int(mtk_new)
                elif mtk_old: syarat_baru['mtk'] = mtk_old # Keep old if exists

                # B.Inggris
                ing_old = rule_lama['syarat'].get('b_inggris', '')
                ing_new = input(f"Min. B.Inggris [{ing_old}]: ")
                if ing_new: syarat_baru['b_inggris'] = int(ing_new)
                elif ing_old: syarat_baru['b_inggris'] = ing_old

                # Fisika
                fis_old = rule_lama['syarat'].get('fisika', '')
                fis_new = input(f"Min. Fisika [{fis_old}]: ")
                if fis_new: syarat_baru['fisika'] = int(fis_new)
                elif fis_old: syarat_baru['fisika'] = fis_old

            except ValueError:
                print("❌ Error: Input nilai harus angka. Batal update.")
                return
            
            rule_lama['syarat'] = syarat_baru

        save_rules(rules)
        print("✔ Rule berhasil diperbarui!")

    except ValueError:
        print("❌ Input error.")

# ===========================
# 6. CORE ENGINE: Forward Chaining
# ===========================
def forward_chaining():
    print("\n========================================")
    print("   SISTEM PAKAR PENENTUAN JURUSAN")
    print("========================================")
    
    nama = input("Nama Siswa: ")
    print("\n--- Masukkan Data Akademik ---")
    
    # Input Data User
    user_data = {}
    user_data["minat"] = input("Minat (komputer/teknik/manajemen): ").lower()
    
    try:
        user_data["mtk"] = int(input("Nilai Matematika: "))
        user_data["b_inggris"] = int(input("Nilai Bahasa Inggris: "))
        user_data["fisika"] = int(input("Nilai Fisika: "))
    except ValueError:
        print("❌ Error: Input nilai harus angka!")
        return

    # Logika Pencocokan (Inference Engine)
    print("\nSedang menganalisis...")
    rules = load_rules()
    rekomendasi = []

    for rule in rules:
        syarat_jurusan = rule["syarat"]
        match = True
        
        for kriteria, nilai_syarat in syarat_jurusan.items():
            # Jika user tidak punya data utk kriteria yg diminta rule (misal: kimia)
            if kriteria not in user_data:
                match = False
                break
            
            nilai_user = user_data[kriteria]
            
            # Cek String (Minat)
            if isinstance(nilai_syarat, str):
                if nilai_user != nilai_syarat:
                    match = False
                    break
            # Cek Angka (Nilai)
            elif isinstance(nilai_syarat, int):
                if nilai_user < nilai_syarat:
                    match = False
                    break
        
        if match:
            rekomendasi.append(rule["jurusan"])

    # Hasil
    print(f"\n=== HASIL REKOMENDASI: {nama.upper()} ===")
    if rekomendasi:
        print("Jurusan yang cocok:")
        for rek in rekomendasi:
            print(f"✅ {rek}")
    else:
        print("⚠️ Tidak ada jurusan yang memenuhi kriteria.")

# ===========================
# MAIN MENU
# ===========================
def main_menu():
    while True:
        print("\n\n[ MENU UTAMA ]")
        print("1. Konsultasi (Forward Chaining)")
        print("2. Lihat Rules")
        print("3. Tambah Rule")
        print("4. Update Rule")
        print("5. Hapus Rule")
        print("6. Keluar")
        
        pilih = input(">> Pilih: ")
        
        if pilih == "1": forward_chaining()
        elif pilih == "2": view_rules()
        elif pilih == "3": add_rule()
        elif pilih == "4": update_rule()
        elif pilih == "5": delete_rule()
        elif pilih == "6": break
        else: print("Pilihan salah.")

if __name__ == "__main__":
    main_menu()
