import json
import random
from db import nilai_ke_grade  # Import fungsi grade converter dari db.py

FILE = "database.json"

NAMA = [
    "Andi", "Budi", "Citra", "Dewi", "Eka",
    "Fajar", "Gita", "Hadi", "Intan", "Joko",
    "Kartika", "Lestari", "Maya", "Nanda", "Opik",
    "Putri", "Qori", "Rudi", "Siti", "Tono"
]

JUMLAH_MAHASISWA = 1000  # Target 1000 mahasiswa

KURIKULUM = {
    1: [
        ("Pendidikan Agama Islam", 2),
        ("Pendidikan Pancasila", 2),
        ("Bahasa Inggris", 3),
        ("Kalkulus", 4),
        ("Computer Aided Design", 3),
        ("Fisika", 4),
    ],
    2: [
        ("Pengukuran dan Instrumentasi Industri", 3),
        ("Pendidikan Kewarganegaraan", 2),
        ("Dasar Komputer dan Pemrograman", 3),
        ("Rangkaian Listrik 1", 3),
        ("Matematika Teknik", 3),
        ("Pengantar Otomasi Industri dan Robotika", 4),
        ("Pendidikan Bahasa Indonesia", 2),
    ],
    3: [
        ("Rangkaian Listrik 2", 3),
        ("Medan Elektromagnetik", 3),
        ("Praktikum Bengkel dan Dasar Elektro", 3),
        ("Kewirausahaan", 2),
        ("Psikologi Pendidikan", 2),
        ("Elektronika Dasar", 3),
    ],
    4: [
        ("Pengelolaan Kelas", 2),
        ("Kurikulum dan Pembelajaran", 2),
        ("Praktikum Elektronika", 3),
        ("Sistem Digital", 3),
        ("Elektronika", 3),
        ("Sistem Kendali", 3),
    ],
    5: [
        ("Mikrokontroler", 3),
        ("PLC dan Otomasi", 3),
        ("Sensor dan Aktuator", 3),
        ("Metodologi Penelitian", 2),
        ("Media Pembelajaran", 2),
        ("Praktikum PLC", 3),
    ],
    6: [
        ("IoT Industri", 3),
        ("Robotika Lanjut", 3),
        ("Magang Industri", 4),
        ("Seminar Proposal", 2),
        ("Manajemen Proyek", 2),
        ("Tugas Akhir Awal", 3),
    ],
}

def random_nilai():
    """Generate nilai dengan distribusi realistis (lebih banyak di range 70-90)"""
    # 10% kemungkinan nilai rendah (40-65)
    # 60% kemungkinan nilai sedang (70-85)
    # 30% kemungkinan nilai tinggi (86-98)
    roll = random.random()
    if roll < 0.10:
        return random.randint(40, 65)
    elif roll < 0.70:
        return random.randint(70, 85)
    else:
        return random.randint(86, 98)

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

        # isi semester - setiap mahasiswa punya 2-6 semester terisi
        max_semester = random.randint(2, 6)
        for smt in range(1, max_semester + 1):
            if smt not in KURIKULUM:
                continue
            matkul = KURIKULUM[smt]
            records = []
            for mk, sks in matkul:
                nilai = random_nilai()
                grade, _ = nilai_ke_grade(nilai)  # Hitung grade otomatis
                records.append({
                    "nama": mk,
                    "sks": sks,
                    "nilai": nilai,
                    "grade": grade
                })
            mhs["semester"][str(smt)] = records

        data["mahasiswa"].append(mhs)

    with open(FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)

    print("✅ Data mahasiswa + nilai berhasil dibuat!")
    print(f"📊 Total mahasiswa: {JUMLAH_MAHASISWA}")
    print(f"📚 Semester terisi: 2-6 semester per mahasiswa")
    print("🎯 Nilai bervariasi: 40-98 dengan distribusi realistis")

if __name__ == "__main__":
    generate()