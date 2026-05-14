

import json
import random

FILE = "database.json"

NAMA = [
    "Andi", "Budi", "Citra", "Dewi", "Eka",
    "Fajar", "Gita", "Hadi", "Intan", "Joko",
    "Kartika", "Lestari", "Muhammad", "Nadia", "Opik",
    "Putri", "Qori", "Rudi", "Siti", "Tono",
    "Umar", "Vina", "Wawan", "Xena", "Yusuf",
    "Zahra", "Ahmad", "Bayu", "Caca", "Dimas",
    "Erna", "Farhan", "Gusti", "Hana", "Indra",
    "Jamil", "Kiki", "Lina", "Mamat", "Nina",
    "Oki", "Pipit", "Rina", "Syahrul", "Tari",
    "Usman", "Vivi", "Windi", "Yanti", "Zainal"
]

JUMLAH_MAHASISWA = 1000

KURIKULUM = {
    1: [
        ("Pendidikan Agama Islam", 2),
        ("Pendidikan Pancasila", 2),
        ("Bahasa Inggris", 3),
        ("Kalkulus", 4),
    ],
    2: [
        ("Pemrograman", 3),
        ("Basis Data", 3),
        ("Jaringan", 3),
    ]
}

def random_nilai():
    return random.randint(60, 95)

def generate():
    data = {
        "admin": {"username": "admin", "password": "123"},
        "mahasiswa": [],
        "riwayat": []
    }

    for i in range(1, JUMLAH_MAHASISWA + 1):
        nama = NAMA[(i - 1) % len(NAMA)]
        nim = f"2024{i:05}"

        mhs = {
            "nim": nim,
            "nama": nama,
            "semester": {}
        }

        # isi semester
        for smt, matkul in KURIKULUM.items():
            records = []
            for mk, sks in matkul:
                nilai = random_nilai()
                records.append({
                    "nama": mk,
                    "sks": sks,
                    "nilai": nilai,
                    "grade": "A"  # simple dulu
                })
            mhs["semester"][str(smt)] = records

        data["mahasiswa"].append(mhs)

    with open(FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)

    print(f"✅ {JUMLAH_MAHASISWA} data mahasiswa + nilai berhasil dibuat!")

if __name__ == "__main__":
    generate()