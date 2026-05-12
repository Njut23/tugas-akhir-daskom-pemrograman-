

import json
import random

FILE = "database.json"

NAMA = [
    "Andi", "Budi", "Citra", "Dewi", "Eka",
    "Fajar", "Gita", "Hadi", "Intan", "Joko"
]

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

    for i, nama in enumerate(NAMA, start=1):
        nim = f"20240{i:03}"

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

    print("✅ Data mahasiswa + nilai berhasil dibuat!")

if __name__ == "__main__":
    generate()