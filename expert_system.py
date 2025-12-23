import json
import os
from tabulate import tabulate

RULES_FILE = "rules.json"

# ===========================
# Load & Save Knowledge Base
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
# CRUD RULES
# ===========================
def add_rule():
    print("\n=== Tambah Rule Baru ===")
    minat = input("Minat (IT / Teknik): ").lower()
    ipa = int(input("Minimal Nilai IPA: "))
    mtk = int(input("Minimal Nilai Matematika: "))
    fisika = int(input("Minimal Nilai Fisika: "))
    jurusan = input("Rekomendasi Jurusan: ")

    rules = load_rules()
    rules.append({
        "minat": minat,
        "ipa": ipa,
        "mtk": mtk,
        "fisika": fisika,
        "then": jurusan
    })
    save_rules(rules)

    print("✔ Rule berhasil ditambahkan")


def view_rules():
    rules = load_rules()
    print("\n=== Basis Knowledge (Rules) ===")

    if not rules:
        print("Tidak ada rule")
        return

    table = []
    for i, r in enumerate(rules, start=1):
        table.append([
            i,
            r["minat"],
            r["ipa"],
            r["mtk"],
            r["fisika"],
            r["then"]
        ])

    print(tabulate(
        table,
        headers=[
            "No",
            "Minat",
            "Minimal Nilai IPA",
            "Minimal Nilai Matematika",
            "Minimal Nilai Fisika",
            "Rekomendasi Jurusan"
        ],
        tablefmt="grid"
    ))



def update_rule():
    rules = load_rules()
    if not rules:
        print("Tidak ada rule")
        return

    view_rules()
    idx = int(input("\nPilih nomor rule: ")) - 1

    if idx < 0 or idx >= len(rules):
        print("Nomor tidak valid")
        return

    minat = input("Minat baru: ").lower()
    ipa = int(input("Minimal Nilai IPA baru: "))
    mtk = int(input("Minimal Nilai Matematika baru: "))
    fisika = int(input("Minimal Nilai Fisika baru: "))
    jurusan = input("Rekomendasi Jurusan baru: ")

    rules[idx] = {
        "minat": minat,
        "ipa": ipa,
        "mtk": mtk,
        "fisika": fisika,
        "then": jurusan
    }
    save_rules(rules)

    print("✔ Rule berhasil diperbarui")


def delete_rule():
    rules = load_rules()
    if not rules:
        print("Tidak ada rule")
        return

    view_rules()
    idx = int(input("\nPilih nomor rule: ")) - 1

    if idx < 0 or idx >= len(rules):
        print("Nomor tidak valid")
        return

    rules.pop(idx)
    save_rules(rules)

    print("✔ Rule berhasil dihapus")


# ===========================
# Forward Chaining (Dominan)
# ===========================
def forward_chaining():
    print("\n=== Input Data Siswa ===")
    nama = input("Nama: ")
    minat = input("Minat (IT / Teknik): ").lower()
    ipa = int(input("Nilai IPA: "))
    mtk = int(input("Nilai Matematika: "))
    fisika = int(input("Nilai Fisika: "))

    rules = load_rules()
    hasil = []

    for r in rules:
        if minat != r["minat"]:
            continue

        # JURUSAN IT → dominan IPA & MTK
        if r["then"] in ["Teknik Informatika", "Sistem Informasi"]:
            if ipa >= r["ipa"] and mtk >= r["mtk"]:
                hasil.append(r["then"])

        # JURUSAN TEKNIK → dominan FISIKA & MTK
        else:
            if fisika >= r["fisika"] and mtk >= r["mtk"]:
                hasil.append(r["then"])

    print("\n=== Hasil Rekomendasi ===")
    if hasil:
        for h in hasil:
            print(f"- {nama} direkomendasikan ke jurusan {h}")
    else:
        print("Tidak ada jurusan yang sesuai")


# ===========================
# Main Menu
# ===========================
def main_menu():
    while True:
        print("\n====== SISTEM PAKAR PENENTUAN JURUSAN ======")
        print("1. Tambah Rule")
        print("2. Lihat Basis Knowledge")
        print("3. Update Rule")
        print("4. Hapus Rule")
        print("5. Jalankan Forward Chaining")
        print("6. Keluar")

        pilih = input("Pilih menu: ")

        if pilih == "1":
            add_rule()
        elif pilih == "2":
            view_rules()
        elif pilih == "3":
            update_rule()
        elif pilih == "4":
            delete_rule()
        elif pilih == "5":
            forward_chaining()
        elif pilih == "6":
            print("Keluar...")
            break
        else:
            print("Pilihan tidak valid")


if __name__ == "__main__":
    main_menu()
