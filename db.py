# ============================================================
# db.py  —  Database & Logic
# Sistem Informasi Akademik Mahasiswa
# Pure Python + JSON
# ============================================================

import json
import os
from datetime import datetime

FILE = "database.json"

# ============================================================
# KURIKULUM PAKET SEMESTER 1-6
# ============================================================

KURIKULUM = {
    1: [
        ("Pendidikan Agama Islam",          2),
        ("Pendidikan Pancasila",            2),
        ("Keterampilan Berbahasa Inggris",  3),
        ("Kalkulus",                        4),
        ("Computer Aided Design",           3),
        ("Fisika",                          4),
    ],
    2: [
        ("Pengukuran dan Instrumentasi Industri",   3),
        ("Pendidikan Kewarganegaraan",              2),
        ("Dasar Komputer dan Pemrograman",          3),
        ("Rangkaian Listrik 1",                     3),
        ("Matematika Teknik",                       3),
        ("Pengantar Otomasi Industri dan Robotika", 4),
        ("Pendidikan Bahasa Indonesia",             2),
    ],
    3: [
        ("Rangkaian Listrik 2",                 3),
        ("Medan Elektromagnetik",               3),
        ("Praktikum Bengkel dan Dasar Elektro", 3),
        ("Kewirausahaan",                       2),
        ("Psikologi Pendidikan",                2),
        ("Elektronika Dasar",                   3),
    ],
    4: [
        ("Pengelolaan Kelas",               2),
        ("Kurikulum dan Pembelajaran",      2),
        ("Praktikum Elektronika",           3),
        ("Sistem Digital",                  3),
        ("Elektronika",                     3),
        ("Sistem Kendali",                  3),
    ],
    5: [
        ("Mikrokontroler",          3),
        ("PLC dan Otomasi",         3),
        ("Sensor dan Aktuator",     3),
        ("Metodologi Penelitian",   2),
        ("Media Pembelajaran",      2),
        ("Praktikum PLC",           3),
    ],
    6: [
        ("IoT Industri",        3),
        ("Robotika Lanjut",     3),
        ("Magang Industri",     4),
        ("Seminar Proposal",    2),
        ("Manajemen Proyek",    2),
        ("Tugas Akhir Awal",    3),
    ],
}

# ============================================================
# GRADE CONVERTER
# ============================================================

def nilai_ke_grade(nilai: float) -> tuple[str, float]:
    skala = [
        (85, "A",  4.0),
        (80, "A-", 3.7),
        (75, "B+", 3.3),
        (70, "B",  3.0),
        (65, "B-", 2.7),
        (60, "C+", 2.3),
        (55, "C",  2.0),
        (40, "D",  1.0),
        (0,  "E",  0.0),
    ]
    for batas, huruf, bobot in skala:
        if nilai >= batas:
            return huruf, bobot
    return "E", 0.0


def hitung_ips(daftar: list) -> float:
    total_mutu = sum(nilai_ke_grade(mk["nilai"])[1] * mk["sks"] for mk in daftar)
    total_sks  = sum(mk["sks"] for mk in daftar)
    return round(total_mutu / total_sks, 2) if total_sks else 0.0


def predikat(ipk: float) -> str:
    if ipk >= 3.75: return "Cumlaude"
    if ipk >= 3.50: return "Sangat Baik"
    if ipk >= 3.00: return "Baik"
    if ipk >= 2.00: return "Cukup"
    return "Perlu Perbaikan"

# ============================================================
# INISIALISASI FILE
# ============================================================

def init():
    default = {"admin": {"username": "admin", "password": "123"}, "mahasiswa": [], "riwayat": []}
    if not os.path.exists(FILE):
        _simpan(default)
        return
    # validasi format — reset kalau rusak
    try:
        data = _load()
        if not isinstance(data.get("mahasiswa"), list):
            raise ValueError
        if not isinstance(data.get("admin"), dict):
            raise ValueError
    except Exception:
        _simpan(default)


def _load() -> dict:
    with open(FILE, "r", encoding="utf-8") as f:
        return json.load(f)


def _simpan(data: dict):
    with open(FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)


def _log(aksi: str, detail: str):
    data = _load()
    data["riwayat"].insert(0, {
        "waktu": datetime.now().strftime("%d/%m/%Y %H:%M"),
        "aksi": aksi,
        "detail": detail,
    })
    data["riwayat"] = data["riwayat"][:20]
    _simpan(data)

# ============================================================
# AUTH
# ============================================================

def cek_login(username: str, password: str) -> bool:
    data = _load()
    return username == data["admin"]["username"] and password == data["admin"]["password"]

# ============================================================
# MAHASISWA — CRUD
# ============================================================

def get_semua() -> list:
    return _load()["mahasiswa"]


def cari(keyword: str) -> list:
    kw = keyword.lower()
    return [m for m in get_semua() if kw in m["nim"].lower() or kw in m["nama"].lower()]


def tambah_mahasiswa(nim: str, nama: str) -> bool:
    nim = nim.strip()
    nama = nama.strip()
    if not nim:
        raise ValueError("NIM tidak boleh kosong.")
    if not nama:
        raise ValueError("Nama tidak boleh kosong.")
    data = _load()
    if not isinstance(data.get("mahasiswa"), list):
        data["mahasiswa"] = []
    nim_list = [m["nim"] for m in data["mahasiswa"] if isinstance(m, dict)]
    if nim in nim_list:
        raise ValueError(f"NIM {nim} sudah terdaftar.")
    data["mahasiswa"].append({"nim": nim, "nama": nama, "semester": {}})
    _simpan(data)
    _log("TAMBAH", f"{nama} ({nim})")
    return True


def hapus_mahasiswa(nim: str):
    data = _load()
    target = next((m for m in data["mahasiswa"] if m["nim"] == nim), None)
    if not target:
        raise ValueError("Mahasiswa tidak ditemukan.")
    data["mahasiswa"] = [m for m in data["mahasiswa"] if m["nim"] != nim]
    _simpan(data)
    _log("HAPUS", f"{target['nama']} ({nim})")


def edit_mahasiswa(nim: str, nama_baru: str):
    nama_baru = nama_baru.strip()
    if not nama_baru:
        raise ValueError("Nama tidak boleh kosong.")
    data = _load()
    for m in data["mahasiswa"]:
        if m["nim"] == nim:
            lama = m["nama"]
            m["nama"] = nama_baru
            _simpan(data)
            _log("EDIT", f"{lama} -> {nama_baru} ({nim})")
            return
    raise ValueError("Mahasiswa tidak ditemukan.")


def simpan_nilai(nim: str, semester: int, daftar_nilai: list[float]):
    """
    daftar_nilai: list nilai angka (urut sesuai KURIKULUM[semester])
    """
    if semester not in KURIKULUM:
        raise ValueError("Semester tidak valid.")
    matkul_smt = KURIKULUM[semester]
    if len(daftar_nilai) != len(matkul_smt):
        raise ValueError("Jumlah nilai tidak sesuai jumlah mata kuliah.")
    for n in daftar_nilai:
        if not (0 <= n <= 100):
            raise ValueError(f"Nilai {n} di luar range 0-100.")

    records = []
    for (nama_mk, sks), nilai in zip(matkul_smt, daftar_nilai):
        huruf, _ = nilai_ke_grade(nilai)
        records.append({"nama": nama_mk, "sks": sks, "nilai": nilai, "grade": huruf})

    data = _load()
    for m in data["mahasiswa"]:
        if m["nim"] == nim:
            m["semester"][str(semester)] = records
            _simpan(data)
            _log("NILAI", f"{m['nama']} — Semester {semester}")
            return
    raise ValueError("Mahasiswa tidak ditemukan.")

# ============================================================
# KALKULASI IPK
# ============================================================

def ipk_mahasiswa(mhs: dict) -> float:
    semua_mk = []
    for smt_data in mhs["semester"].values():
        semua_mk.extend(smt_data)
    return hitung_ips(semua_mk) if semua_mk else 0.0


def semester_terisi(mhs: dict) -> str:
    keys = sorted(mhs["semester"].keys(), key=int)
    return ", ".join(keys) if keys else "-"


def total_sks(mhs: dict) -> int:
    return sum(mk["sks"] for smt in mhs["semester"].values() for mk in smt)

# ============================================================
# STATISTIK DASHBOARD
# ============================================================

def statistik() -> dict:
    semua = get_semua()
    if not semua:
        return {"total": 0, "sudah_nilai": 0, "rata_ipk": 0.0, "terbaik": "-", "terbaik_ipk": 0.0}

    ipk_list = [(m["nama"], ipk_mahasiswa(m)) for m in semua]
    ipk_vals  = [v for _, v in ipk_list]
    sudah     = sum(1 for m in semua if m["semester"])
    terbaik   = max(ipk_list, key=lambda x: x[1])

    return {
        "total":      len(semua),
        "sudah_nilai": sudah,
        "rata_ipk":   round(sum(ipk_vals) / len(ipk_vals), 2),
        "terbaik":    terbaik[0],
        "terbaik_ipk": terbaik[1],
    }


def get_riwayat() -> list:
    return _load().get("riwayat", [])

# ============================================================
# INISIALISASI SAAT IMPORT
# ============================================================

init()