# ============================================================
# ui.py  —  GUI Utama
# Sistem Informasi Akademik Mahasiswa
# CustomTkinter — Tema Putih Clean + Oranye
# ============================================================

import customtkinter as ctk
from tkinter import messagebox, ttk
import tkinter as tk
import db
import math
from PIL import Image, ImageTk

# ============================================================
# TEMA
# ============================================================

ctk.set_appearance_mode("light")
ctk.set_default_color_theme("blue")

C = {
    "oranye":       "#EA580C",
    "oranye_gelap": "#C2410C",
    "oranye_muda":  "#FFEDD5",
    "oranye_aksen": "#F97316",
    "putih":        "#FFFFFF",
    "abu_bg":       "#FFFBF7",
    "abu_card":     "#FFF7ED",
    "abu_border":   "#FED7AA",
    "teks":         "#1C1917",
    "teks_sub":     "#78716C",
    "hijau":        "#16A34A",
    "hijau_muda":   "#DCFCE7",
    "merah":        "#DC2626",
    "merah_muda":   "#FEE2E2",
    "kuning":       "#D97706",
    "kuning_muda":  "#FEF3C7",
    "ungu":         "#7C3AED",
    "ungu_muda":    "#F5F3FF",
}

F_JUDUL   = ("Segoe UI", 22, "bold")
F_SUBJUDUL= ("Segoe UI", 14, "bold")
F_NORMAL  = ("Segoe UI", 11)
F_KECIL   = ("Segoe UI", 9)
F_MONO    = ("Consolas", 10)

# ============================================================
# HELPER
# ============================================================

def _entry(parent, placeholder="", show="", width=280, height=40):
    return ctk.CTkEntry(
        parent, width=width, height=height,  # <-- Parameter height ditambahkan di sini
        placeholder_text=placeholder,
        show=show,
        font=F_NORMAL,
        corner_radius=8,
        border_color=C["abu_border"],
        fg_color=C["putih"],
        text_color=C["teks"],
    )


def _btn(parent, text, command, color=None, width=160, height=38):
    color = color or C["oranye"]
    return ctk.CTkButton(
        parent, text=text, command=command,
        width=width, height=height,
        font=("Segoe UI", 11, "bold"),
        fg_color=color,
        hover_color=_gelap(color),
        corner_radius=8,
    )


def _gelap(hex_color: str) -> str:
    try:
        r = max(0, int(hex_color[1:3], 16) - 25)
        g = max(0, int(hex_color[3:5], 16) - 25)
        b = max(0, int(hex_color[5:7], 16) - 25)
        return f"#{r:02x}{g:02x}{b:02x}"
    except Exception:
        return hex_color


def _bind_enter_chain(entries: list):
    for i, e in enumerate(entries):
        if i < len(entries) - 1:
            nxt = entries[i + 1]
            e.bind("<Return>", lambda ev, n=nxt: n.focus_set())


def _label(parent, text, font=None, color=None, bg=None, anchor="w"):
    return ctk.CTkLabel(
        parent, text=text,
        font=font or F_NORMAL,
        text_color=color or C["teks"],
        anchor=anchor,
    )


# ============================================================
# TREEVIEW STYLE
# ============================================================

def _style_tree():
    s = ttk.Style()
    s.theme_use("clam")
    s.configure("App.Treeview",
        background=C["putih"],
        foreground=C["teks"],
        fieldbackground=C["putih"],
        rowheight=42,
        font=("Segoe UI", 11),
        borderwidth=0,
    )
    s.configure("App.Treeview.Heading",
        background=C["oranye"],
        foreground=C["putih"],
        font=("Segoe UI", 11, "bold"),
        borderwidth=0,
        relief="flat",
        padding=(0, 10),
    )
    s.map("App.Treeview",
        background=[("selected", C["oranye_muda"])],
        foreground=[("selected", C["oranye_gelap"])]
    )


# ============================================================
# GRAFIK CANVAS — helper fungsi untuk menggambar chart
# ============================================================

class Chart:
    """
    Kumpulan fungsi statis untuk menggambar chart di Canvas tkinter.
    Tidak perlu matplotlib — murni Canvas drawing.
    """

    @staticmethod
    def bar(canvas, data: list[tuple], colors: list[str] = None,
            title: str = "", x_label: str = "", y_label: str = ""):
        """
        Bar chart horizontal.
        data: [(label, value), ...]
        """
        canvas.delete("all")
        canvas.update_idletasks()
        W = canvas.winfo_width() or 400
        H = canvas.winfo_height() or 300

        if not data:
            canvas.create_text(W // 2, H // 2, text="Belum ada data",
                               fill=C["teks_sub"], font=F_KECIL)
            return

        PAD_L, PAD_R, PAD_T, PAD_B = 70, 24, 36, 48
        chart_w = W - PAD_L - PAD_R
        chart_h = H - PAD_T - PAD_B

        max_val = max(v for _, v in data) or 1
        n = len(data)
        gap = 6
        bar_h = max(10, (chart_h - gap * (n + 1)) // n)

        default_colors = [C["oranye"], C["hijau"], C["kuning"], C["merah"],
                          C["ungu"], C["oranye_aksen"]] * 10
        colors = colors or default_colors

        # Title
        if title:
            canvas.create_text(PAD_L + chart_w // 2, 14, text=title,
                               font=("Segoe UI", 9, "bold"),
                               fill=C["teks"], anchor="center")

        # Grid lines vertikal
        grid_steps = 5
        for i in range(grid_steps + 1):
            gx = PAD_L + int(chart_w * i / grid_steps)
            gy1, gy2 = PAD_T, PAD_T + chart_h
            canvas.create_line(gx, gy1, gx, gy2,
                               fill="#E2E8F0", width=1, dash=(3, 3))
            val_label = int(max_val * i / grid_steps)
            canvas.create_text(gx, PAD_T + chart_h + 10,
                               text=str(val_label),
                               font=("Segoe UI", 7), fill=C["teks_sub"])

        # Bar-bar
        for i, ((label, val), color) in enumerate(zip(data, colors)):
            y1 = PAD_T + gap + i * (bar_h + gap)
            y2 = y1 + bar_h
            bar_len = int(chart_w * val / max_val)

            # Background track
            canvas.create_rectangle(PAD_L, y1, PAD_L + chart_w, y2,
                                    fill="#F1F5F9", outline="")
            # Bar
            if bar_len > 0:
                canvas.create_rectangle(PAD_L, y1, PAD_L + bar_len, y2,
                                        fill=color, outline="")
                # Rounded cap (simulasi)
                canvas.create_oval(PAD_L + bar_len - 4, y1,
                                   PAD_L + bar_len + 4, y2,
                                   fill=color, outline="")

            # Label kiri
            canvas.create_text(PAD_L - 6, (y1 + y2) // 2,
                               text=label, font=("Segoe UI", 8),
                               fill=C["teks"], anchor="e")

            # Nilai di ujung bar
            if val > 0:
                canvas.create_text(PAD_L + bar_len + 8, (y1 + y2) // 2,
                                   text=str(val), font=("Segoe UI", 8, "bold"),
                                   fill=color, anchor="w")

    @staticmethod
    def column(canvas, data: list[tuple], colors: list[str] = None,
               title: str = ""):
        """
        Column chart (bar vertikal).
        data: [(label, value), ...]
        """
        canvas.delete("all")
        canvas.update_idletasks()
        W = canvas.winfo_width() or 400
        H = canvas.winfo_height() or 300

        if not data:
            canvas.create_text(W // 2, H // 2, text="Belum ada data",
                               fill=C["teks_sub"], font=F_KECIL)
            return

        PAD_L, PAD_R, PAD_T, PAD_B = 40, 16, 36, 48
        chart_w = W - PAD_L - PAD_R
        chart_h = H - PAD_T - PAD_B

        max_val = max(v for _, v in data) or 1
        n = len(data)
        gap = 8
        bar_w = max(12, (chart_w - gap * (n + 1)) // n)

        default_colors = [C["oranye"], C["hijau"], C["kuning"], C["merah"],
                          C["ungu"], C["oranye_aksen"]] * 10
        colors = colors or default_colors

        # Title
        if title:
            canvas.create_text(PAD_L + chart_w // 2, 14, text=title,
                               font=("Segoe UI", 9, "bold"),
                               fill=C["teks"], anchor="center")

        # Grid lines horizontal
        grid_steps = 4
        for i in range(grid_steps + 1):
            gy = PAD_T + chart_h - int(chart_h * i / grid_steps)
            canvas.create_line(PAD_L, gy, PAD_L + chart_w, gy,
                               fill="#E2E8F0", width=1, dash=(3, 3))
            val_label = int(max_val * i / grid_steps)
            canvas.create_text(PAD_L - 6, gy,
                               text=str(val_label),
                               font=("Segoe UI", 7), fill=C["teks_sub"],
                               anchor="e")

        # Sumbu X
        canvas.create_line(PAD_L, PAD_T + chart_h,
                           PAD_L + chart_w, PAD_T + chart_h,
                           fill=C["abu_border"], width=1)

        for i, ((label, val), color) in enumerate(zip(data, colors)):
            x1 = PAD_L + gap + i * (bar_w + gap)
            x2 = x1 + bar_w
            bar_h_px = int(chart_h * val / max_val)
            y1 = PAD_T + chart_h - bar_h_px
            y2 = PAD_T + chart_h

            # Bar
            if bar_h_px > 0:
                canvas.create_rectangle(x1, y1, x2, y2,
                                        fill=color, outline="")

            # Label bawah
            canvas.create_text((x1 + x2) // 2, PAD_T + chart_h + 12,
                               text=label, font=("Segoe UI", 8),
                               fill=C["teks"], anchor="n")

            # Nilai di atas bar
            if val > 0:
                canvas.create_text((x1 + x2) // 2, y1 - 8,
                                   text=str(val),
                                   font=("Segoe UI", 8, "bold"),
                                   fill=color, anchor="s")

    @staticmethod
    def pie(canvas, data: list[tuple], colors: list[str] = None,
            title: str = ""):
        """
        Pie chart.
        data: [(label, value), ...]
        """
        canvas.delete("all")
        canvas.update_idletasks()
        W = canvas.winfo_width() or 400
        H = canvas.winfo_height() or 300

        total = sum(v for _, v in data if v > 0)
        if total == 0:
            canvas.create_text(W // 2, H // 2, text="Belum ada data",
                               fill=C["teks_sub"], font=F_KECIL)
            return

        default_colors = [C["oranye"], C["hijau"], C["kuning"],
                          C["merah"], C["ungu"], C["oranye_aksen"]] * 10
        colors = colors or default_colors

        cx = W * 0.38
        cy = H // 2
        r  = min(cx - 20, H // 2 - 30)

        if title:
            canvas.create_text(W // 2, 14, text=title,
                               font=("Segoe UI", 9, "bold"),
                               fill=C["teks"], anchor="center")

        start = 0.0
        slices = [(label, val, color)
                  for (label, val), color in zip(data, colors)
                  if val > 0]

        for label, val, color in slices:
            extent = (val / total) * 360
            canvas.create_arc(cx - r, cy - r, cx + r, cy + r,
                              start=start, extent=extent,
                              fill=color, outline=C["putih"], width=2)
            start += extent

        # Legend kanan
        lx = cx * 2 + 16
        ly = H // 2 - len(slices) * 18
        for label, val, color in slices:
            pct = val / total * 100
            canvas.create_rectangle(lx, ly, lx + 12, ly + 12,
                                    fill=color, outline="")
            canvas.create_text(lx + 18, ly + 6,
                               text=f"{label}  {val} ({pct:.1f}%)",
                               font=("Segoe UI", 8), fill=C["teks"],
                               anchor="w")
            ly += 22

    @staticmethod
    def line(canvas, datasets: list[tuple], labels: list[str],
             title: str = ""):
        """
        Line chart multi-series.
        datasets: [(series_label, color, [values]), ...]
        labels: label sumbu X
        """
        canvas.delete("all")
        canvas.update_idletasks()
        W = canvas.winfo_width() or 400
        H = canvas.winfo_height() or 300

        all_vals = [v for _, _, vals in datasets for v in vals]
        if not all_vals:
            canvas.create_text(W // 2, H // 2, text="Belum ada data",
                               fill=C["teks_sub"], font=F_KECIL)
            return

        PAD_L, PAD_R, PAD_T, PAD_B = 50, 20, 36, 48
        chart_w = W - PAD_L - PAD_R
        chart_h = H - PAD_T - PAD_B

        max_val = max(all_vals) or 1
        min_val = 0
        n = len(labels)

        if title:
            canvas.create_text(PAD_L + chart_w // 2, 14, text=title,
                               font=("Segoe UI", 9, "bold"),
                               fill=C["teks"], anchor="center")

        # Grid
        grid_steps = 4
        for i in range(grid_steps + 1):
            gy = PAD_T + chart_h - int(chart_h * i / grid_steps)
            gval = min_val + (max_val - min_val) * i / grid_steps
            canvas.create_line(PAD_L, gy, PAD_L + chart_w, gy,
                               fill="#E2E8F0", width=1, dash=(3, 3))
            canvas.create_text(PAD_L - 6, gy,
                               text=f"{gval:.2f}",
                               font=("Segoe UI", 7), fill=C["teks_sub"],
                               anchor="e")

        # X labels
        if n > 1:
            for i, lbl in enumerate(labels):
                gx = PAD_L + int(chart_w * i / (n - 1))
                canvas.create_text(gx, PAD_T + chart_h + 12,
                                   text=lbl, font=("Segoe UI", 8),
                                   fill=C["teks_sub"])

        # Lines & dots
        for s_label, color, vals in datasets:
            if len(vals) < 2:
                continue
            points = []
            for i, v in enumerate(vals):
                gx = PAD_L + int(chart_w * i / (n - 1))
                gy = PAD_T + chart_h - int(chart_h * (v - min_val) / (max_val - min_val))
                points.append((gx, gy))

            # Line
            for i in range(len(points) - 1):
                x1, y1 = points[i]
                x2, y2 = points[i + 1]
                canvas.create_line(x1, y1, x2, y2, fill=color, width=2, smooth=True)

            # Dots
            for gx, gy in points:
                canvas.create_oval(gx - 4, gy - 4, gx + 4, gy + 4,
                                   fill=color, outline=C["putih"], width=2)

        # Legend
        lx = PAD_L + chart_w - 10
        ly = PAD_T + 6
        for s_label, color, _ in datasets:
            canvas.create_rectangle(lx - 90, ly, lx - 78, ly + 8,
                                    fill=color, outline="")
            canvas.create_text(lx - 72, ly + 4,
                               text=s_label, font=("Segoe UI", 8),
                               fill=C["teks"], anchor="w")
            ly += 16


# ============================================================
# KOMPONEN SIDEBAR
# ============================================================

class Sidebar(ctk.CTkFrame):

    MENU = [
        ("Dashboard",       "dashboard"),
        ("Data Mahasiswa",  "mahasiswa"),
        ("Input Nilai",     "nilai"),
        ("Statistik",       "statistik"),
        ("Riwayat",         "riwayat"),
    ]

    def __init__(self, parent, on_navigate):
        super().__init__(parent,
            width=220, corner_radius=0,
            fg_color=C["oranye_gelap"],
        )
        self.pack_propagate(False)
        self._nav = on_navigate
        self._btns = {}
        self._aktif = None
        self._build()

    def _build(self):
        logo_frame = ctk.CTkFrame(self, fg_color="transparent")
        logo_frame.pack(fill="x", padx=20, pady=(28, 24))

        ctk.CTkLabel(logo_frame,
            text="ARION",
            font=("Segoe UI", 20, "bold"),
            text_color="#FFFFFF",
        ).pack(anchor="w")
        ctk.CTkLabel(logo_frame,
            text="Automation Robotics Information Online Network\nPendidikan Teknik Otomasi Industri dan Robotika",
            font=("Segoe UI", 8),
            text_color="#FED7AA",
            wraplength=180,
        ).pack(anchor="w")

        ctk.CTkFrame(self, height=1, fg_color="#C2410C").pack(fill="x", padx=16)

        menu_frame = ctk.CTkFrame(self, fg_color="transparent")
        menu_frame.pack(fill="x", padx=12, pady=16)

        for label, key in self.MENU:
            b = ctk.CTkButton(
                menu_frame,
                text=label,
                anchor="w",
                width=196,
                height=40,
                font=("Segoe UI", 11),
                fg_color="transparent",
                hover_color="#C2410C",
                text_color="#FFEDD5",
                corner_radius=8,
                command=lambda k=key: self._klik(k),
            )
            b.pack(fill="x", pady=2)
            self._btns[key] = b

        ctk.CTkButton(
            self,
            text="Logout",
            anchor="w",
            width=196,
            height=40,
            font=("Segoe UI", 11),
            fg_color="transparent",
            hover_color="#7F1D1D",
            text_color="#FCA5A5",
            corner_radius=8,
            command=lambda: self._nav("logout"),
        ).pack(side="bottom", padx=12, pady=20, fill="x")

    def _klik(self, key: str):
        for k, b in self._btns.items():
            b.configure(fg_color="transparent", text_color="#FFEDD5", font=("Segoe UI", 11))
        if key in self._btns:
            self._btns[key].configure(
                fg_color=C["oranye_aksen"],
                text_color="#FFFFFF",
                font=("Segoe UI", 11, "bold"),
            )
        self._aktif = key
        self._nav(key)

    def aktifkan(self, key: str):
        self._klik(key)


# ============================================================
# HALAMAN DASAR
# ============================================================

class HalamanBase(ctk.CTkFrame):

    def __init__(self, parent):
        super().__init__(parent, corner_radius=0, fg_color=C["abu_bg"])

    def _header(self, judul: str, subjudul: str = ""):
        hdr = ctk.CTkFrame(self, fg_color=C["putih"], corner_radius=0, height=70)
        hdr.pack(fill="x")
        hdr.pack_propagate(False)
        inner = ctk.CTkFrame(hdr, fg_color="transparent")
        inner.pack(side="left", padx=28, pady=12)
        ctk.CTkLabel(inner, text=judul, font=F_JUDUL, text_color=C["teks"]).pack(anchor="w")
        if subjudul:
            ctk.CTkLabel(inner, text=subjudul, font=F_KECIL, text_color=C["teks_sub"]).pack(anchor="w")
        ctk.CTkFrame(self, height=1, fg_color=C["abu_border"]).pack(fill="x")

    def _card(self, parent, **kw):
        return ctk.CTkFrame(parent,
            fg_color=C["putih"],
            corner_radius=12,
            border_width=1,
            border_color=C["abu_border"],
            **kw
        )


# ============================================================
# HALAMAN DASHBOARD
# ============================================================

class HalamanDashboard(HalamanBase):

    def __init__(self, parent):
        super().__init__(parent)
        self._header("Dashboard", "Selamat datang, Admin")
        self._build()

    def _build(self):
        row1 = ctk.CTkFrame(self, fg_color="transparent")
        row1.pack(fill="x", padx=28, pady=(20, 10))

        self._cards = {}
        specs = [
            ("total",       "Total Mahasiswa",  C["oranye"],   "orang terdaftar"),
            ("sudah_nilai", "Sudah Input Nilai", C["hijau"],  "mahasiswa"),
            ("rata_ipk",    "Rata-rata IPK",     C["kuning"], "dari 4.00"),
            ("belum_nilai", "Belum Input Nilai", C["merah"],  "mahasiswa"),
        ]
        for col, (key, label, warna, satuan) in enumerate(specs):
            card = self._card(row1, height=130)
            card.grid(row=0, column=col, padx=6, sticky="nsew")
            card.grid_propagate(False)
            row1.columnconfigure(col, weight=1)

            ctk.CTkFrame(card, width=5, fg_color=warna, corner_radius=0
                ).place(x=0, y=0, relheight=1)

            ctk.CTkLabel(card, text=label,
                font=("Segoe UI", 9), text_color=C["teks_sub"]
            ).place(x=22, y=16)

            val_lbl = ctk.CTkLabel(card, text="0",
                font=("Segoe UI", 34, "bold"), text_color=warna)
            val_lbl.place(x=22, y=38)

            ctk.CTkLabel(card, text=satuan,
                font=("Segoe UI", 8), text_color=C["teks_sub"]
            ).place(x=24, y=100)

            self._cards[key] = val_lbl

        row2 = ctk.CTkFrame(self, fg_color="transparent")
        row2.pack(fill="x", padx=28, pady=(0, 10))
        row2.columnconfigure(0, weight=2)
        row2.columnconfigure(1, weight=3)

        info_card = self._card(row2, height=110)
        info_card.grid(row=0, column=0, padx=(0, 6), sticky="nsew")
        info_card.grid_propagate(False)

        ctk.CTkLabel(info_card, text="MAHASISWA TERBAIK",
            font=("Segoe UI", 8, "bold"), text_color=C["teks_sub"]
        ).place(x=18, y=14)
        self._lbl_best = ctk.CTkLabel(info_card, text="belum ada data",
            font=("Segoe UI", 13, "bold"), text_color=C["oranye"])
        self._lbl_best.place(x=18, y=34)
        self._lbl_best_ipk = ctk.CTkLabel(info_card, text="",
            font=("Segoe UI", 10), text_color=C["teks_sub"])
        self._lbl_best_ipk.place(x=18, y=60)

        ctk.CTkFrame(info_card, width=1, fg_color=C["abu_border"]
            ).place(relx=0.56, y=10, relheight=0.75)

        ctk.CTkLabel(info_card, text="IPK TERTINGGI",
            font=("Segoe UI", 8), text_color=C["teks_sub"]
        ).place(relx=0.59, y=14)
        self._lbl_ipk_max = ctk.CTkLabel(info_card, text="0.00",
            font=("Segoe UI", 20, "bold"), text_color=C["hijau"])
        self._lbl_ipk_max.place(relx=0.59, y=34)

        ctk.CTkLabel(info_card, text="IPK TERENDAH",
            font=("Segoe UI", 8), text_color=C["teks_sub"]
        ).place(relx=0.59, y=66)
        self._lbl_ipk_min = ctk.CTkLabel(info_card, text="0.00",
            font=("Segoe UI", 20, "bold"), text_color=C["merah"])
        self._lbl_ipk_min.place(relx=0.59, y=84)

        dist_card = self._card(row2, height=110)
        dist_card.grid(row=0, column=1, padx=(6, 0), sticky="nsew")
        dist_card.grid_propagate(False)

        ctk.CTkLabel(dist_card, text="DISTRIBUSI PREDIKAT",
            font=("Segoe UI", 8, "bold"), text_color=C["teks_sub"]
        ).place(x=18, y=14)

        self._dist_labels = {}
        predikat_specs = [
            ("Cumlaude",        "#7C3AED"),
            ("Sangat Baik",     C["hijau"]),
            ("Baik",            C["oranye"]),
            ("Cukup",           C["kuning"]),
            ("Perlu Perbaikan", C["merah"]),
        ]
        for idx, (nama, warna) in enumerate(predikat_specs):
            ctk.CTkLabel(dist_card, text=nama,
                font=("Segoe UI", 8), text_color=C["teks_sub"]
            ).place(x=18 + idx * 145, y=36)
            lbl_val = ctk.CTkLabel(dist_card, text="0",
                font=("Segoe UI", 24, "bold"), text_color=warna)
            lbl_val.place(x=18 + idx * 145, y=58)
            self._dist_labels[nama] = lbl_val

        riwayat_card = self._card(self)
        riwayat_card.pack(fill="both", expand=True, padx=28, pady=(0, 24))

        hdr_row = ctk.CTkFrame(riwayat_card, fg_color="transparent")
        hdr_row.pack(fill="x", padx=20, pady=(14, 0))
        ctk.CTkLabel(hdr_row, text="Aktivitas Terbaru",
            font=F_SUBJUDUL, text_color=C["teks"]).pack(side="left")
        ctk.CTkLabel(hdr_row, text="10 operasi terakhir",
            font=F_KECIL, text_color=C["teks_sub"]).pack(side="right")

        col_hdr = ctk.CTkFrame(riwayat_card, fg_color=C["abu_card"], height=28)
        col_hdr.pack(fill="x", padx=20, pady=(8, 0))
        col_hdr.pack_propagate(False)
        for txt, w in [("Waktu", 150), ("Aksi", 80), ("Detail", 0)]:
            ctk.CTkLabel(col_hdr, text=txt, width=w,
                font=("Segoe UI", 9, "bold"), text_color=C["teks_sub"],
                anchor="w").pack(side="left", padx=(10, 0))

        self._riwayat_frame = ctk.CTkScrollableFrame(
            riwayat_card, fg_color="transparent")
        self._riwayat_frame.pack(fill="both", expand=True, padx=20, pady=(4, 14))

        self.refresh()

    def refresh(self):
        stat  = db.statistik()
        semua = db.get_semua()

        total = stat["total"]
        sudah = stat["sudah_nilai"]

        self._cards["total"].configure(text=str(total))
        self._cards["sudah_nilai"].configure(text=str(sudah))
        self._cards["rata_ipk"].configure(text=str(stat["rata_ipk"]))
        self._cards["belum_nilai"].configure(text=str(total - sudah))

        if stat["terbaik"] != "-":
            self._lbl_best.configure(text=stat["terbaik"])
            self._lbl_best_ipk.configure(text=f"IPK {stat['terbaik_ipk']:.2f}")
        else:
            self._lbl_best.configure(text="belum ada data")
            self._lbl_best_ipk.configure(text="")

        ipk_vals = [db.ipk_mahasiswa(m) for m in semua if m["semester"]]
        if ipk_vals:
            self._lbl_ipk_max.configure(text=f"{max(ipk_vals):.2f}")
            self._lbl_ipk_min.configure(text=f"{min(ipk_vals):.2f}")
        else:
            self._lbl_ipk_max.configure(text="0.00")
            self._lbl_ipk_min.configure(text="0.00")

        dist = {"Cumlaude": 0, "Sangat Baik": 0, "Baik": 0,
                "Cukup": 0, "Perlu Perbaikan": 0}
        for m in semua:
            if m["semester"]:
                p = db.predikat(db.ipk_mahasiswa(m))
                if p in dist:
                    dist[p] += 1
        for nama, lbl in self._dist_labels.items():
            lbl.configure(text=str(dist.get(nama, 0)))

        aksi_warna = {
            "TAMBAH": C["hijau"], "HAPUS": C["merah"],
            "NILAI":  C["oranye"],  "EDIT":  C["kuning"],
        }
        for w in self._riwayat_frame.winfo_children():
            w.destroy()
        for h in db.get_riwayat()[:10]:
            row = ctk.CTkFrame(self._riwayat_frame, fg_color="transparent", height=30)
            row.pack(fill="x", pady=1)
            row.pack_propagate(False)
            warna_aksi = aksi_warna.get(h["aksi"], C["teks_sub"])
            ctk.CTkLabel(row, text=h["waktu"], width=150,
                font=F_KECIL, text_color=C["teks_sub"], anchor="w"
            ).pack(side="left", padx=(4, 0))
            ctk.CTkLabel(row, text=h["aksi"], width=72,
                font=("Segoe UI", 9, "bold"),
                text_color=warna_aksi, anchor="w"
            ).pack(side="left")
            ctk.CTkLabel(row, text=h["detail"],
                font=F_KECIL, text_color=C["teks"], anchor="w"
            ).pack(side="left", padx=(4, 0))


# ============================================================
# HALAMAN DATA MAHASISWA
# ============================================================

class HalamanMahasiswa(HalamanBase):

    def __init__(self, parent, on_nilai):
        super().__init__(parent)
        self._on_nilai = on_nilai
        self._header("Data Mahasiswa", "Kelola data mahasiswa terdaftar")
        _style_tree()
        self._build()
        self.refresh()

    def _build(self):
        toolbar = ctk.CTkFrame(self, fg_color="transparent")
        toolbar.pack(fill="x", padx=28, pady=14)

        self._search_var = ctk.StringVar()
        self._search_var.trace_add("write", lambda *_: self.refresh())
        search = ctk.CTkEntry(
            toolbar, width=260, height=38,
            placeholder_text="Cari NIM atau nama...",
            textvariable=self._search_var,
            font=F_NORMAL,
            corner_radius=8,
        )
        search.pack(side="left")

        _btn(toolbar, "+ Tambah", self._form_tambah, width=130).pack(side="right", padx=(6, 0))
        _btn(toolbar, "Edit Nama", self._form_edit, color=C["kuning"], width=110).pack(side="right", padx=6)
        _btn(toolbar, "Input Nilai", self._ke_nilai, color=C["hijau"], width=110).pack(side="right", padx=6)
        _btn(toolbar, "Hapus", self._hapus, color=C["merah"], width=90).pack(side="right")

        tbl_frame = ctk.CTkFrame(self, fg_color=C["putih"],
            corner_radius=12, border_width=1, border_color=C["abu_border"])
        tbl_frame.pack(fill="both", expand=True, padx=28, pady=(0, 24))

        cols = ("nim", "nama", "semester_terisi", "ipk", "total_sks", "predikat")
        self._tree = ttk.Treeview(tbl_frame, columns=cols, show="headings",
            style="App.Treeview", selectmode="browse")

        hdrs = {
            "nim":             ("NIM",             140),
            "nama":            ("Nama Lengkap",    260),
            "semester_terisi": ("Semester Terisi", 160),
            "ipk":             ("IPK",              90),
            "total_sks":       ("Total SKS",       110),
            "predikat":        ("Predikat",        160),
        }
        for col, (head, w) in hdrs.items():
            self._tree.heading(col, text=head, anchor="center")
            anc = "center" if col not in ("nama",) else "w"
            self._tree.column(col, width=w, anchor=anc, minwidth=80)

        vsb = ttk.Scrollbar(tbl_frame, orient="vertical", command=self._tree.yview)
        self._tree.configure(yscrollcommand=vsb.set)
        self._tree.pack(side="left", fill="both", expand=True, padx=(1, 0), pady=1)
        vsb.pack(side="right", fill="y")

        self._tree.tag_configure("cumlaude",  foreground="#7C3AED")
        self._tree.tag_configure("sangat",    foreground=C["hijau"])
        self._tree.tag_configure("baik",      foreground=C["oranye"])
        self._tree.tag_configure("cukup",     foreground=C["kuning"])
        self._tree.tag_configure("perlu",     foreground=C["merah"])

        self._tree.bind("<Double-1>", lambda e: self._detail())

        self._sbar = ctk.CTkLabel(self, text="", font=F_KECIL, text_color=C["teks_sub"])
        self._sbar.pack(anchor="w", padx=28, pady=(0, 8))

    def refresh(self):
        for i in self._tree.get_children():
            self._tree.delete(i)

        keyword = self._search_var.get()
        rows = db.cari(keyword) if keyword else db.get_semua()

        tag_map = {
            "Cumlaude":        "cumlaude",
            "Sangat Baik":     "sangat",
            "Baik":            "baik",
            "Cukup":           "cukup",
            "Perlu Perbaikan": "perlu",
        }

        for m in rows:
            ipk  = db.ipk_mahasiswa(m)
            pred = db.predikat(ipk)
            self._tree.insert("", "end", iid=m["nim"], values=(
                m["nim"],
                m["nama"],
                db.semester_terisi(m),
                f"{ipk:.2f}",
                db.total_sks(m),
                pred,
            ), tags=(tag_map.get(pred, ""),))

        self._sbar.configure(
            text=f"Menampilkan {len(rows)} dari {db.statistik()['total']} mahasiswa")

    def _selected_nim(self) -> str | None:
        sel = self._tree.selection()
        if not sel:
            messagebox.showwarning("Perhatian", "Pilih mahasiswa terlebih dahulu.")
            return None
        return sel[0]

    def _form_tambah(self):
        win = ctk.CTkToplevel(self)
        win.title("Tambah Mahasiswa")
        win.geometry("420x300")
        win.resizable(False, False)
        win.grab_set()

        ctk.CTkLabel(win, text="Tambah Mahasiswa Baru",
            font=F_SUBJUDUL).pack(pady=(24, 16))

        e_nim  = _entry(win, placeholder="NIM (angka)")
        e_nim.pack(pady=6)
        e_nama = _entry(win, placeholder="Nama lengkap")
        e_nama.pack(pady=6)

        _bind_enter_chain([e_nim, e_nama])

        def simpan(*_):
            try:
                db.tambah_mahasiswa(e_nim.get(), e_nama.get())
                self.refresh()
                win.destroy()
                messagebox.showinfo("Berhasil", "Mahasiswa berhasil ditambahkan.")
            except ValueError as err:
                messagebox.showerror("Gagal", str(err))

        e_nama.bind("<Return>", simpan)
        _btn(win, "Simpan", simpan, width=280).pack(pady=18)
        e_nim.focus_set()

    def _form_edit(self):
        nim = self._selected_nim()
        if not nim: return
        semua = db.get_semua()
        mhs = next((m for m in semua if m["nim"] == nim), None)
        if not mhs: return

        win = ctk.CTkToplevel(self)
        win.title("Edit Nama")
        win.geometry("420x240")
        win.resizable(False, False)
        win.grab_set()

        ctk.CTkLabel(win, text=f"Edit Nama  —  NIM {nim}",
            font=F_SUBJUDUL).pack(pady=(24, 16))

        e_nama = _entry(win, placeholder="Nama baru")
        e_nama.insert(0, mhs["nama"])
        e_nama.pack(pady=6)

        def simpan(*_):
            try:
                db.edit_mahasiswa(nim, e_nama.get())
                self.refresh()
                win.destroy()
            except ValueError as err:
                messagebox.showerror("Gagal", str(err))

        e_nama.bind("<Return>", simpan)
        _btn(win, "Simpan", simpan, width=280).pack(pady=18)
        e_nama.focus_set()

    def _hapus(self):
        nim = self._selected_nim()
        if not nim: return
        semua = db.get_semua()
        mhs = next((m for m in semua if m["nim"] == nim), None)
        if not mhs: return
        if messagebox.askyesno("Konfirmasi",
                f"Hapus {mhs['nama']} ({nim})?\n\nSemua data nilai ikut terhapus."):
            try:
                db.hapus_mahasiswa(nim)
                self.refresh()
            except ValueError as err:
                messagebox.showerror("Gagal", str(err))

    def _ke_nilai(self):
        nim = self._selected_nim()
        if nim:
            self._on_nilai(nim)

    def _detail(self):
        nim = self._selected_nim()
        if not nim: return
        semua = db.get_semua()
        mhs = next((m for m in semua if m["nim"] == nim), None)
        if not mhs: return

        win = ctk.CTkToplevel(self)
        win.title(f"Detail — {mhs['nama']}")
        win.geometry("520x560")
        win.grab_set()

        ipk  = db.ipk_mahasiswa(mhs)
        pred = db.predikat(ipk)

        ctk.CTkLabel(win, text=mhs["nama"], font=F_JUDUL).pack(padx=24, pady=(20, 2), anchor="w")
        ctk.CTkLabel(win, text=f"NIM {mhs['nim']}", font=F_KECIL,
            text_color=C["teks_sub"]).pack(padx=24, anchor="w")

        badge = ctk.CTkFrame(win, fg_color=C["oranye_muda"], corner_radius=10)
        badge.pack(fill="x", padx=24, pady=14)
        ctk.CTkLabel(badge, text=f"{ipk:.2f}",
            font=("Segoe UI", 36, "bold"), text_color=C["oranye"]).pack(side="left", padx=20, pady=14)
        info = ctk.CTkFrame(badge, fg_color="transparent")
        info.pack(side="left", pady=14)
        ctk.CTkLabel(info, text=pred, font=("Segoe UI", 13, "bold"),
            text_color=C["oranye"]).pack(anchor="w")
        ctk.CTkLabel(info, text=f"{db.total_sks(mhs)} SKS  |  Semester terisi: {db.semester_terisi(mhs)}",
            font=F_KECIL, text_color=C["teks_sub"]).pack(anchor="w")

        ctk.CTkLabel(win, text="Rincian Semester",
            font=F_SUBJUDUL, text_color=C["teks"]).pack(padx=24, pady=(4, 6), anchor="w")

        scroll = ctk.CTkScrollableFrame(win, fg_color="transparent")
        scroll.pack(fill="both", expand=True, padx=24, pady=(0, 20))

        for smt_key in sorted(mhs["semester"].keys(), key=int):
            data = mhs["semester"][smt_key]
            ips  = db.hitung_ips(data)

            smt_hdr = ctk.CTkFrame(scroll, fg_color=C["abu_card"], corner_radius=8)
            smt_hdr.pack(fill="x", pady=(8, 2))
            ctk.CTkLabel(smt_hdr, text=f"Semester {smt_key}",
                font=("Segoe UI", 11, "bold"), text_color=C["oranye"]).pack(side="left", padx=14, pady=8)
            ctk.CTkLabel(smt_hdr, text=f"IPS: {ips:.2f}",
                font=("Segoe UI", 11, "bold"), text_color=C["hijau"]).pack(side="right", padx=14)

            for mk in data:
                row = ctk.CTkFrame(scroll, fg_color=C["putih"],
                    border_width=1, border_color=C["abu_border"], corner_radius=6)
                row.pack(fill="x", pady=1)
                ctk.CTkLabel(row, text=mk["nama"], font=F_NORMAL,
                    text_color=C["teks"]).pack(side="left", padx=14, pady=6)
                ctk.CTkLabel(row, text=f"SKS {mk['sks']}",
                    font=F_KECIL, text_color=C["teks_sub"]).pack(side="right", padx=8)
                ctk.CTkLabel(row, text=f"{mk['nilai']:.0f}  /  {mk['grade']}",
                    font=("Segoe UI", 10, "bold"), text_color=C["oranye"]).pack(side="right", padx=10)


# ============================================================
# HALAMAN INPUT NILAI
# ============================================================

class HalamanNilai(HalamanBase):

    def __init__(self, parent, on_selesai):
        super().__init__(parent)
        self._on_selesai = on_selesai
        self._nim_aktif  = None
        self._entries    = []
        self._header("Input Nilai", "Pilih mahasiswa dan semester, lalu isi nilai")
        self._build()

    def _build(self):
        top = ctk.CTkFrame(self, fg_color=C["putih"],
            corner_radius=12, border_width=1, border_color=C["abu_border"])
        top.pack(fill="x", padx=28, pady=16)

        row1 = ctk.CTkFrame(top, fg_color="transparent")
        row1.pack(fill="x", padx=20, pady=14)

        ctk.CTkLabel(row1, text="Mahasiswa", font=F_KECIL,
            text_color=C["teks_sub"]).grid(row=0, column=0, sticky="w")
        self._search = ctk.CTkEntry(row1, width=260, height=38,
            placeholder_text="Ketik NIM atau nama...", font=F_NORMAL, corner_radius=8)
        self._search.grid(row=1, column=0, padx=(0, 16))
        self._search.bind("<KeyRelease>", self._update_dropdown)

        self._dd_var  = tk.StringVar()
        self._dd_data = {}
        self._combo   = ttk.Combobox(row1, textvariable=self._dd_var,
            state="readonly", width=30, font=("Segoe UI", 10))
        self._combo.grid(row=1, column=1, padx=(0, 16))
        self._combo.bind("<<ComboboxSelected>>", self._pilih_mahasiswa)

        ctk.CTkLabel(row1, text="Semester", font=F_KECIL,
            text_color=C["teks_sub"]).grid(row=0, column=2, sticky="w")
        self._smt_var = tk.StringVar(value="1")
        smt_cb = ttk.Combobox(row1, textvariable=self._smt_var,
            values=["1", "2", "3", "4", "5", "6"],
            state="readonly", width=8, font=("Segoe UI", 10))
        smt_cb.grid(row=1, column=2)
        smt_cb.bind("<<ComboboxSelected>>", self._load_form)

        row1.columnconfigure((0, 1, 2), pad=8)

        self._lbl_info = ctk.CTkLabel(top, text="",
            font=F_KECIL, text_color=C["teks_sub"])
        self._lbl_info.pack(anchor="w", padx=20, pady=(0, 10))

        self._form_card = ctk.CTkFrame(self, fg_color=C["putih"],
            corner_radius=12, border_width=1, border_color=C["abu_border"])
        self._form_card.pack(fill="both", expand=True, padx=28, pady=(0, 24))

        self._placeholder()
        self._update_dropdown()

    def _placeholder(self):
        for w in self._form_card.winfo_children():
            w.destroy()
        ctk.CTkLabel(self._form_card,
            text="Pilih mahasiswa dan semester untuk mulai input nilai.",
            font=F_NORMAL, text_color=C["teks_sub"]
        ).pack(expand=True)

    def _update_dropdown(self, event=None):
        keyword = self._search.get()
        rows = db.cari(keyword) if keyword else db.get_semua()
        opts = [f"{m['nim']}  —  {m['nama']}" for m in rows]
        nims = {f"{m['nim']}  —  {m['nama']}": m["nim"] for m in rows}
        self._dd_data = nims
        self._combo["values"] = opts
        if opts and not self._combo.get():
            self._combo.set(opts[0])
            self._pilih_mahasiswa()

    def _pilih_mahasiswa(self, event=None):
        label = self._dd_var.get()
        nim   = self._dd_data.get(label)
        if not nim: return
        self._nim_aktif = nim
        semua = db.get_semua()
        mhs   = next((m for m in semua if m["nim"] == nim), None)
        if mhs:
            ipk    = db.ipk_mahasiswa(mhs)
            terisi = db.semester_terisi(mhs)
            self._lbl_info.configure(
                text=f"IPK saat ini: {ipk:.2f}  |  Semester sudah terisi: {terisi}")
        self._load_form()

    def _load_form(self, event=None):
        if not self._nim_aktif:
            return

        smt    = int(self._smt_var.get())
        matkul = db.KURIKULUM[smt]

        for w in self._form_card.winfo_children():
            w.destroy()

        self._entries = []

        header = ctk.CTkFrame(self._form_card, fg_color="transparent")
        header.pack(fill="x", padx=20, pady=(14, 8))
        ctk.CTkLabel(header, text=f"Nilai Semester {smt}",
            font=F_SUBJUDUL, text_color=C["teks"]).pack(side="left")

        semua    = db.get_semua()
        mhs      = next((m for m in semua if m["nim"] == self._nim_aktif), None)
        existing = mhs["semester"].get(str(smt), []) if mhs else []

        scroll = ctk.CTkScrollableFrame(self._form_card, fg_color="transparent")
        scroll.pack(fill="both", expand=True, padx=20, pady=(0, 8))

        for i, (nama_mk, sks) in enumerate(matkul):
            row = ctk.CTkFrame(scroll, fg_color=C["abu_card"], corner_radius=8)
            row.pack(fill="x", pady=4)

            ctk.CTkLabel(row,
                text=f"{nama_mk}",
                font=F_NORMAL, text_color=C["teks"], anchor="w", width=320
            ).pack(side="left", padx=14, pady=10)

            ctk.CTkLabel(row, text=f"{sks} SKS",
                font=F_KECIL, text_color=C["teks_sub"]).pack(side="left", padx=8)

            e = ctk.CTkEntry(row, width=80, height=34,
                font=F_NORMAL, corner_radius=6,
                justify="center",
                placeholder_text="0-100")
            e.pack(side="right", padx=14)

            if i < len(existing):
                e.insert(0, str(int(existing[i]["nilai"])))

            grade_lbl = ctk.CTkLabel(row, text="", width=36,
                font=("Segoe UI", 10, "bold"), text_color=C["oranye"])
            grade_lbl.pack(side="right")

            def update_grade(event, el=e, gl=grade_lbl):
                try:
                    g, _ = db.nilai_ke_grade(float(el.get()))
                    colors = {
                        "A": C["hijau"], "A-": C["hijau"],
                        "B+": "#16A34A", "B": C["oranye"], "B-": C["oranye"],
                        "C+": C["kuning"], "C": C["kuning"],
                        "D": C["merah"], "E": C["merah"],
                    }
                    gl.configure(text=g, text_color=colors.get(g, C["teks_sub"]))
                except Exception:
                    gl.configure(text="", text_color=C["teks_sub"])

            e.bind("<KeyRelease>", update_grade)
            update_grade(None, e, grade_lbl)
            self._entries.append(e)

        for i in range(len(self._entries) - 1):
            nxt = self._entries[i + 1]
            self._entries[i].bind("<Return>", lambda ev, n=nxt: n.focus_set())

        foot = ctk.CTkFrame(self._form_card, fg_color="transparent")
        foot.pack(fill="x", padx=20, pady=12)
        _btn(foot, "Simpan Nilai", self._simpan, width=180).pack(side="right")
        _btn(foot, "Batal", self._placeholder, color=C["teks_sub"], width=100).pack(side="right", padx=(0, 8))

        if self._entries:
            self._entries[0].focus_set()

    def _simpan(self):
        if not self._nim_aktif:
            messagebox.showwarning("Perhatian", "Pilih mahasiswa terlebih dahulu.")
            return
        try:
            nilai_list = [float(e.get()) for e in self._entries]
            db.simpan_nilai(self._nim_aktif, int(self._smt_var.get()), nilai_list)
            messagebox.showinfo("Berhasil", "Nilai berhasil disimpan.")
            self._load_form()
            self._on_selesai()
        except ValueError as err:
            messagebox.showerror("Gagal", str(err))

    def set_nim(self, nim: str):
        semua = db.get_semua()
        mhs = next((m for m in semua if m["nim"] == nim), None)
        if not mhs: return
        label = f"{nim}  —  {mhs['nama']}"
        self._dd_data[label] = nim
        vals = list(self._combo["values"])
        if label not in vals:
            vals.insert(0, label)
        self._combo["values"] = vals
        self._combo.set(label)
        self._nim_aktif = nim
        ipk    = db.ipk_mahasiswa(mhs)
        terisi = db.semester_terisi(mhs)
        self._lbl_info.configure(
            text=f"IPK saat ini: {ipk:.2f}  |  Semester sudah terisi: {terisi}")
        self._load_form()


# ============================================================
# HALAMAN STATISTIK — dengan grafik canvas
# ============================================================

class HalamanStatistik(HalamanBase):
    """
    Dashboard statistik penuh dengan 4 grafik:
    1. Distribusi IPK (bar horizontal — rentang 0-4)
    2. Distribusi Predikat (pie chart)
    3. Rata-rata IPS per Semester (line chart)
    4. Distribusi Grade per Semester (column chart)
    """

    def __init__(self, parent):
        super().__init__(parent)
        self._header("Statistik Kelas", "Visualisasi data akademik seluruh mahasiswa")
        self._build()

    def _build(self):
        # Toolbar refresh
        bar = ctk.CTkFrame(self, fg_color="transparent")
        bar.pack(fill="x", padx=28, pady=(12, 4))
        self._filter_smt = tk.StringVar(value="Semua")
        ctk.CTkLabel(bar, text="Filter Semester:", font=F_KECIL,
                     text_color=C["teks_sub"]).pack(side="left", padx=(0, 8))
        smt_opts = ["Semua", "1", "2", "3", "4", "5", "6"]
        smt_cb = ttk.Combobox(bar, textvariable=self._filter_smt,
                              values=smt_opts, state="readonly", width=10,
                              font=("Segoe UI", 10))
        smt_cb.pack(side="left")
        smt_cb.bind("<<ComboboxSelected>>", lambda *_: self.refresh())
        _btn(bar, "Refresh", self.refresh, width=100).pack(side="right")

        # Scrollable area untuk semua grafik
        scroll = ctk.CTkScrollableFrame(self, fg_color="transparent")
        scroll.pack(fill="both", expand=True, padx=28, pady=(0, 20))

        # Row 1: distribusi IPK (gauge) + predikat (donut)
        row1 = ctk.CTkFrame(scroll, fg_color="transparent")
        row1.pack(fill="x", pady=(0, 12))
        row1.columnconfigure(0, weight=1)
        row1.columnconfigure(1, weight=1)

        card_ipk = self._card(row1)
        card_ipk.grid(row=0, column=0, padx=(0, 8), sticky="nsew")
        ctk.CTkLabel(card_ipk, text="Distribusi Rentang IPK",
                     font=F_SUBJUDUL, text_color=C["teks"]).pack(padx=16, pady=(14, 6), anchor="w")
        self._canvas_ipk = tk.Canvas(card_ipk, height=250,
                                     bg=C["putih"], highlightthickness=0)
        self._canvas_ipk.pack(fill="both", expand=True, padx=16, pady=(0, 14))

        card_pred = self._card(row1)
        card_pred.grid(row=0, column=1, padx=(8, 0), sticky="nsew")
        ctk.CTkLabel(card_pred, text="Sebaran Predikat",
                     font=F_SUBJUDUL, text_color=C["teks"]).pack(padx=16, pady=(14, 6), anchor="w")
        self._canvas_pred = tk.Canvas(card_pred, height=250,
                                      bg=C["putih"], highlightthickness=0)
        self._canvas_pred.pack(fill="both", expand=True, padx=16, pady=(0, 14))

        # Row 2: rata-rata IPS per semester (line) + distribusi grade (radial)
        row2 = ctk.CTkFrame(scroll, fg_color="transparent")
        row2.pack(fill="x", pady=(0, 12))
        row2.columnconfigure(0, weight=1)
        row2.columnconfigure(1, weight=1)

        card_ips = self._card(row2)
        card_ips.grid(row=0, column=0, padx=(0, 8), sticky="nsew")
        ctk.CTkLabel(card_ips, text="Rata-rata IPS per Semester",
                     font=F_SUBJUDUL, text_color=C["teks"]).pack(padx=16, pady=(14, 6), anchor="w")
        self._canvas_ips = tk.Canvas(card_ips, height=250,
                                     bg=C["putih"], highlightthickness=0)
        self._canvas_ips.pack(fill="both", expand=True, padx=16, pady=(0, 14))

        card_grade = self._card(row2)
        card_grade.grid(row=0, column=1, padx=(8, 0), sticky="nsew")
        ctk.CTkLabel(card_grade, text="Distribusi Grade",
                     font=F_SUBJUDUL, text_color=C["teks"]).pack(padx=16, pady=(14, 6), anchor="w")
        self._canvas_grade = tk.Canvas(card_grade, height=250,
                                       bg=C["putih"], highlightthickness=0)
        self._canvas_grade.pack(fill="both", expand=True, padx=16, pady=(0, 14))

        # Row 3: ringkasan teks
        card_sum = self._card(scroll)
        card_sum.pack(fill="x", pady=(0, 12))
        ctk.CTkLabel(card_sum, text="Ringkasan Statistik",
                     font=F_SUBJUDUL, text_color=C["teks"]).pack(padx=16, pady=(14, 6), anchor="w")
        self._sum_frame = ctk.CTkFrame(card_sum, fg_color="transparent")
        self._sum_frame.pack(fill="x", padx=16, pady=(0, 14))

        self.after(100, self.refresh)

    def _get_data(self):
        """Ambil dan hitung semua data statistik sekali jalan."""
        semua = db.get_semua()
        filter_smt = self._filter_smt.get()

        # Kumpulkan semua IPK
        ipk_list = []
        for m in semua:
            if not m["semester"]:
                continue
            if filter_smt != "Semua":
                if filter_smt not in m["semester"]:
                    continue
            ipk_list.append(db.ipk_mahasiswa(m))

        # Distribusi rentang IPK
        rentang = [
            ("0.00 - 1.99", 0),
            ("2.00 - 2.49", 0),
            ("2.50 - 2.99", 0),
            ("3.00 - 3.49", 0),
            ("3.50 - 3.74", 0),
            ("3.75 - 4.00", 0),
        ]
        for ipk in ipk_list:
            if ipk < 2.0:
                rentang[0] = (rentang[0][0], rentang[0][1] + 1)
            elif ipk < 2.5:
                rentang[1] = (rentang[1][0], rentang[1][1] + 1)
            elif ipk < 3.0:
                rentang[2] = (rentang[2][0], rentang[2][1] + 1)
            elif ipk < 3.5:
                rentang[3] = (rentang[3][0], rentang[3][1] + 1)
            elif ipk < 3.75:
                rentang[4] = (rentang[4][0], rentang[4][1] + 1)
            else:
                rentang[5] = (rentang[5][0], rentang[5][1] + 1)

        # Distribusi predikat
        pred_dist = {"Cumlaude": 0, "Sangat Baik": 0, "Baik": 0,
                     "Cukup": 0, "Perlu Perbaikan": 0}
        for ipk in ipk_list:
            p = db.predikat(ipk)
            pred_dist[p] = pred_dist.get(p, 0) + 1

        # Rata-rata IPS per semester
        ips_per_smt = {}  # {smt: [ips, ...]}
        grade_dist  = {}  # {grade: count}
        for m in semua:
            for smt_key, mk_list in m["semester"].items():
                if filter_smt != "Semua" and smt_key != filter_smt:
                    continue
                ips = db.hitung_ips(mk_list)
                ips_per_smt.setdefault(smt_key, []).append(ips)
                for mk in mk_list:
                    g = mk.get("grade", "E")
                    grade_dist[g] = grade_dist.get(g, 0) + 1

        avg_ips = {}
        for smt, vals in ips_per_smt.items():
            avg_ips[smt] = round(sum(vals) / len(vals), 2)

        return {
            "ipk_list":  ipk_list,
            "rentang":   rentang,
            "pred_dist": pred_dist,
            "avg_ips":   avg_ips,
            "grade_dist": grade_dist,
            "total":     len(semua),
        }

    def refresh(self, *_):
        data = self._get_data()

        # Tunggu canvas siap (width bisa 0 sebelum render)
        self.update_idletasks()

        # --- 1. GAUGE METER untuk Distribusi IPK ---
        self._draw_gauge_ipk(data["rentang"])

        # --- 2. DONUT CHART untuk Predikat ---
        pred_data = [(k, v) for k, v in data["pred_dist"].items() if v > 0]
        self._draw_donut_predikat(pred_data)

        # --- 3. RADIAL BARS untuk Distribusi Grade ---
        grade_order = ["A", "A-", "B+", "B", "B-", "C+", "C", "D", "E"]
        grade_data = [(g, data["grade_dist"].get(g, 0)) for g in grade_order
                      if data["grade_dist"].get(g, 0) > 0]
        self._draw_radial_grade(grade_data)

        # --- 4. SMOOTH LINE CHART untuk IPS ---
        smts = sorted(data["avg_ips"].keys(), key=int)
        ips_vals = [data["avg_ips"][s] for s in smts]
        if len(ips_vals) >= 2:
            self._draw_smooth_line(smts, ips_vals)
        else:
            self._canvas_ips.delete("all")
            self._canvas_ips.update_idletasks()
            w = self._canvas_ips.winfo_width() or 400
            self._canvas_ips.create_text(
                w // 2, 100,
                text="Butuh minimal 2 semester untuk menampilkan tren.",
                fill=C["teks_sub"], font=F_KECIL
            )

        # --- 5. Ringkasan teks ---
        for w in self._sum_frame.winfo_children():
            w.destroy()

        ipk_list = data["ipk_list"]
        stats = [
            ("Mahasiswa dengan nilai",    str(len(ipk_list)),                    C["oranye"]),
            ("Rata-rata IPK",             f"{sum(ipk_list)/len(ipk_list):.2f}" if ipk_list else "0.00", C["oranye"]),
            ("IPK tertinggi",             f"{max(ipk_list):.2f}" if ipk_list else "0.00", C["hijau"]),
            ("IPK terendah",              f"{min(ipk_list):.2f}" if ipk_list else "0.00", C["merah"]),
            ("Total mahasiswa terdaftar", str(data["total"]),                    C["teks"]),
        ]

        self._sum_frame.columnconfigure(tuple(range(len(stats))), weight=1, uniform="s")
        for col, (label, val, color) in enumerate(stats):
            box = ctk.CTkFrame(self._sum_frame, fg_color=C["abu_card"],
                               corner_radius=10)
            box.grid(row=0, column=col, padx=6, sticky="nsew")
            ctk.CTkLabel(box, text=label, font=("Segoe UI", 8),
                         text_color=C["teks_sub"]).pack(padx=12, pady=(10, 2), anchor="w")
            ctk.CTkLabel(box, text=val,
                         font=("Segoe UI", 20, "bold"),
                         text_color=color).pack(padx=12, pady=(0, 10), anchor="w")

    def _draw_gauge_ipk(self, rentang):
        """Gauge meter style untuk distribusi IPK"""
        canvas = self._canvas_ipk
        canvas.delete("all")
        w = canvas.winfo_width()
        h = canvas.winfo_height()

        # Fallback jika canvas belum ready
        if w is None or w < 10 or h is None or h < 10:
            canvas.after(50, lambda: self._draw_gauge_ipk(rentang))
            return

        cx, cy = w // 2, h // 2 + 20
        radius = min(w, h) // 2 - 60

        total = sum(r[1] for r in rentang)
        if total == 0:
            canvas.create_text(cx, cy, text="Tidak ada data", fill=C["teks_sub"], font=F_KECIL)
            return

        # Background arc (abu-abu)
        canvas.create_arc(cx-radius, cy-radius, cx+radius, cy+radius,
                         start=0, extent=180, style="arc",
                         outline=C["abu_border"], width=30)

        # Draw segments dengan warna berbeda - tema oranye
        start_angle = 0
        colors = [C["merah"], C["oranye_gelap"], C["kuning"], C["oranye_aksen"], "#FB923C", C["hijau"]]

        for i, (label, count) in enumerate(rentang):
            if count == 0:
                continue
            extent = (count / total) * 180
            color = colors[i % len(colors)]

            # Arc segment
            canvas.create_arc(cx-radius, cy-radius, cx+radius, cy+radius,
                             start=start_angle, extent=extent, style="arc",
                             outline=color, width=30)

            # Label di luar arc
            mid_angle = math.radians(start_angle + extent/2)
            label_x = cx + (radius + 40) * math.cos(mid_angle)
            label_y = cy - (radius + 40) * math.sin(mid_angle)

            canvas.create_text(label_x, label_y, text=f"{count}",
                              font=("Segoe UI", 11, "bold"), fill=color, anchor="center")

            start_angle += extent

        # Center text - Total
        canvas.create_text(cx, cy, text=f"{total}\nMHS",
                          font=("Segoe UI", 18, "bold"), fill=C["oranye_gelap"], justify="center")

        # Title
        canvas.create_text(cx, 25, text="Distribusi IPK",
                          font=("Segoe UI", 12, "bold"), fill=C["teks"])

    def _draw_donut_predikat(self, pred_data):
        """Donut chart modern untuk predikat"""
        canvas = self._canvas_pred
        canvas.delete("all")
        w = canvas.winfo_width()
        h = canvas.winfo_height()

        # Fallback jika canvas belum ready
        if w is None or w < 10 or h is None or h < 10:
            canvas.after(50, lambda: self._draw_donut_predikat(pred_data))
            return

        total = sum(v for _, v in pred_data)
        if total == 0:
            canvas.create_text(w//2, h//2, text="Tidak ada data", fill=C["teks_sub"], font=F_KECIL)
            return

        cx, cy = w // 2, h // 2
        outer_radius = min(w, h) // 2 - 40
        inner_radius = outer_radius * 0.6

        colors = ["#059669", "#16A34A", "#F59E0B", "#EA580C", "#DC2626"]
        labels_map = {
            "Cumlaude": "Cumlaude",
            "Sangat Baik": "Sangat\nMemuaskan",
            "Baik": "Memuaskan",
            "Cukup": "Cukup",
            "Perlu Perbaikan": "Perlu\nPerbaikan"
        }

        start_angle = 0
        legend_items = []

        for i, (label, count) in enumerate(pred_data):
            extent = (count / total) * 360
            color = colors[i % len(colors)]

            # Draw arc segment
            canvas.create_arc(cx-outer_radius, cy-outer_radius, cx+outer_radius, cy+outer_radius,
                             start=start_angle, extent=extent,
                             fill=color, outline="white", width=0)

            # Inner circle (untuk efek donut)
            canvas.create_oval(cx-inner_radius, cy-inner_radius, cx+inner_radius, cy+inner_radius,
                              fill=C["abu_bg"], outline="")

            # Calculate percentage position untuk label
            mid_angle = math.radians(start_angle + extent/2)
            label_radius = (outer_radius + inner_radius) / 2
            label_x = cx + label_radius * math.cos(mid_angle)
            label_y = cy + label_radius * math.sin(mid_angle)

            # Percentage text
            pct = (count / total) * 100
            if pct > 8:  # Hanya tampilkan jika cukup besar
                canvas.create_text(label_x, label_y, text=f"{pct:.0f}%",
                                  font=("Segoe UI", 11, "bold"), fill="white", anchor="center")

            legend_items.append((color, labels_map.get(label, label), count))
            start_angle += extent

        # Center text - Total
        canvas.create_text(cx, cy, text=f"{total}\nTotal",
                          font=("Segoe UI", 14, "bold"), fill=C["teks"], justify="center")

        # Legend horizontal di bawah
        legend_y = h - 35
        for i, (color, lbl, cnt) in enumerate(legend_items[:5]):
            x = 15 + (i % 3) * 75
            y = legend_y + (i // 3) * 20

            canvas.create_rectangle(x, y, x+10, y+10, fill=color, outline="", width=0)
            canvas.create_text(x+14, y+5, text=f"{lbl}",
                              font=("Segoe UI", 8), fill=C["teks"], anchor="w")

    def _draw_radial_grade(self, grade_data):
        """Radial bars concentric untuk distribusi grade"""
        canvas = self._canvas_grade
        canvas.delete("all")
        w = canvas.winfo_width()
        h = canvas.winfo_height()

        # Fallback jika canvas belum ready
        if w is None or w < 10 or h is None or h < 10:
            canvas.after(50, lambda: self._draw_radial_grade(grade_data))
            return

        total = sum(v for _, v in grade_data)
        if total == 0:
            canvas.create_text(w//2, h//2, text="Tidak ada data", fill=C["teks_sub"], font=F_KECIL)
            return

        cx, cy = w // 2, h // 2
        max_radius = min(w, h) // 2 - 30

        colors = ["#059669", "#16A34A", "#22C55E", "#4ADE80", "#86EFAC",
                  "#F59E0B", "#D97706", "#EA580C", "#DC2626"]

        # Sort by count descending
        sorted_grades = sorted(grade_data, key=lambda x: x[1], reverse=True)[:5]

        for i, (grade, count) in enumerate(sorted_grades):
            ratio = count / total
            radius = max_radius * (i + 1) / 5
            extent = ratio * 360

            color = colors[i % len(colors)]

            # Background circle
            canvas.create_oval(cx-radius, cy-radius, cx+radius, cy+radius,
                              outline=C["abu_border"], width=12)

            # Progress arc (start from top)
            canvas.create_arc(cx-radius, cy-radius, cx+radius, cy+radius,
                             start=-90, extent=extent,
                             style="arc", outline=color, width=12, capstyle="round")

            # Grade label
            angle_rad = math.radians(-90 + extent/2)
            label_x = cx + (radius - 20) * math.cos(angle_rad)
            label_y = cy + (radius - 20) * math.sin(angle_rad)

            canvas.create_text(label_x, label_y, text=f"{grade}\n{count}",
                              font=("Segoe UI", 10, "bold"), fill=C["teks"], justify="center")

        # Title
        canvas.create_text(cx, 20, text="Distribusi Nilai",
                          font=("Segoe UI", 12, "bold"), fill=C["teks"])

    def _draw_smooth_line(self, smts, ips_vals):
        """Smooth line chart dengan gradient effect"""
        canvas = self._canvas_ips
        canvas.delete("all")
        w = canvas.winfo_width()
        h = canvas.winfo_height()

        # Fallback jika canvas belum ready
        if w is None or w < 10 or h is None or h < 10:
            canvas.after(50, lambda: self._draw_smooth_line(smts, ips_vals))
            return

        margin_left = 50
        margin_right = 20
        margin_top = 30
        margin_bottom = 40

        chart_w = w - margin_left - margin_right
        chart_h = h - margin_top - margin_bottom

        if len(ips_vals) < 2:
            return

        max_val = max(ips_vals) if ips_vals else 4.0
        if max_val == 0:
            max_val = 4.0
        min_val = min(0, min(ips_vals))

        # Scale functions
        def scale_x(i):
            return margin_left + (i / (len(ips_vals) - 1)) * chart_w if len(ips_vals) > 1 else margin_left + chart_w/2

        def scale_y(val):
            return margin_top + chart_h - ((val - min_val) / (max_val - min_val)) * chart_h if max_val != min_val else margin_top + chart_h/2

        # Grid lines
        for i in range(5):
            y = margin_top + i * chart_h / 4
            val = max_val - i * (max_val - min_val) / 4
            canvas.create_line(margin_left, y, w - margin_right, y,
                              fill=C["abu_border"], dash=(2, 2), width=1)
            canvas.create_text(margin_left - 8, y, text=f"{val:.1f}",
                              font=("Segoe UI", 8), fill=C["teks_sub"], anchor="e")

        # Create points
        points = [(scale_x(i), scale_y(v)) for i, v in enumerate(ips_vals)]

        # Draw smooth line using Bezier curves approximation
        if len(points) >= 2:
            # Draw filled area under line (gradient effect simulation)
            area_points = [points[0]]
            for p in points[1:]:
                area_points.append(p)
            area_points.append((points[-1][0], margin_top + chart_h))
            area_points.append((points[0][0], margin_top + chart_h))

            # Simple polygon fill
            canvas.create_polygon(area_points, fill=C["oranye_muda"], outline="")

            # Draw main line
            line_coords = []
            for p in points:
                line_coords.extend(p)

            if len(points) > 2:
                # Smooth curve
                canvas.create_line(line_coords, fill=C["oranye_gelap"], width=4,
                                  smooth=True, capstyle="round", joinstyle="round")
            else:
                canvas.create_line(line_coords, fill=C["oranye_gelap"], width=4,
                                  capstyle="round")

            # Draw points with glow effect
            for i, (x, y) in enumerate(points):
                # Outer glow
                canvas.create_oval(x-8, y-8, x+8, y+8, fill=C["oranye_muda"], outline="")
                # Main point
                canvas.create_oval(x-5, y-5, x+5, y+5, fill="white",
                                  outline=C["oranye_gelap"], width=3)
                # Center dot
                canvas.create_oval(x-2, y-2, x+2, y+2, fill=C["oranye_gelap"], outline="")

                # X-axis labels
                canvas.create_text(x, h - 15, text=f"Smt {smts[i]}",
                                  font=("Segoe UI", 9), fill=C["teks_sub"], anchor="n")

        # Title
        canvas.create_text(w // 2, 15, text="Tren IPS per Semester",
                          font=("Segoe UI", 12, "bold"), fill=C["teks"])


# ============================================================
# HALAMAN RIWAYAT
# ============================================================

class HalamanLogin(ctk.CTkFrame):
    def __init__(self, parent, on_login):
        super().__init__(parent, corner_radius=0, fg_color=C["abu_bg"])
        self._on_login = on_login
        self._build()

    def _build(self):
        # === BAGIAN ATAS - ORANGE BANNER ===
        atas = ctk.CTkFrame(self, fg_color=C["oranye_gelap"], corner_radius=0, height=160)
        atas.pack(fill="x", side="top")
        atas.pack_propagate(False)

        # Teks ARION di tengah
        ctk.CTkLabel(atas, text="ARION",
            font=("Segoe UI", 36, "bold"), text_color="#FFFFFF"
        ).place(relx=0.5, rely=0.45, anchor="center")

        ctk.CTkLabel(atas,
            text="Automation Robotics Information Online Network\nPendidikan Teknik Otomasi Industri dan Robotika",
            font=("Segoe UI", 11), text_color="#FED7AA", justify="center"
        ).place(relx=0.5, rely=0.85, anchor="center")

        # === BAGIAN BAWAH - FORM LOGIN ===
        bawah = ctk.CTkFrame(self, fg_color=C["abu_bg"], corner_radius=0)
        bawah.pack(fill="both", expand=True, side="top")

        # Card Login (ditengah)
        card = ctk.CTkFrame(bawah, 
                           fg_color=C["putih"], 
                           corner_radius=20,
                           width=400,
                           height=420,
                           border_width=1,
                           border_color=C["abu_border"])
        card.place(relx=0.5, rely=0.35, anchor="center")

        # Icon User Circle
        icon_bg = ctk.CTkFrame(card, fg_color=C["oranye_muda"],
                              corner_radius=40, width=80, height=80)
        icon_bg.place(relx=0.5, rely=0.08, anchor="center")
        
        ctk.CTkLabel(icon_bg, text="👤", 
                    font=("Segoe UI", 40), text_color=C["oranye"]
        ).place(relx=0.5, rely=0.5, anchor="center")

        # Welcome Text
        ctk.CTkLabel(card, text="Selamat Datang Kembali 👋", 
                    font=("Segoe UI", 20, "bold"), text_color=C["teks"]
        ).place(relx=0.5, rely=0.22, anchor="center")
        
        ctk.CTkLabel(card, text="Silakan masuk untuk melanjutkan", 
                    font=("Segoe UI", 10), text_color=C["teks_sub"]
        ).place(relx=0.5, rely=0.28, anchor="center")

        # Username Field
        user_frame = ctk.CTkFrame(card, fg_color=C["abu_bg"],
                                 corner_radius=10, width=320, height=45)
        user_frame.place(relx=0.5, rely=0.38, anchor="center")
        
        ctk.CTkLabel(user_frame, text="👤", 
                    font=("Segoe UI", 14), text_color=C["oranye"]
        ).place(x=12, y=12)
        
        self._e_user = ctk.CTkEntry(user_frame, width=270, height=45,
            placeholder_text="Username",
            font=F_NORMAL, border_width=0, fg_color="transparent",
            text_color=C["teks"]
        )
        self._e_user.place(x=40, y=0)

        # Password Field
        pass_frame = ctk.CTkFrame(card, fg_color=C["abu_bg"],
                                 corner_radius=10, width=320, height=45)
        pass_frame.place(relx=0.5, rely=0.49, anchor="center")
        
        ctk.CTkLabel(pass_frame, text="🔒", 
                    font=("Segoe UI", 14), text_color=C["oranye"]
        ).place(x=12, y=12)
        
        self._e_pass = ctk.CTkEntry(pass_frame, width=270, height=45,
            placeholder_text="Password", show="*",
            font=F_NORMAL, border_width=0, fg_color="transparent",
            text_color=C["teks"]
        )
        self._e_pass.place(x=40, y=0)

        # Remember & Forgot
        chk_frame = ctk.CTkFrame(card, fg_color="transparent")
        chk_frame.place(relx=0.5, rely=0.59, anchor="center")
        
        self._chk_ingat = ctk.CTkCheckBox(chk_frame, text="Ingat saya",
            font=("Segoe UI", 9), text_color=C["teks_sub"],
            checkbox_width=16, checkbox_height=16,
            fg_color=C["oranye"], border_color=C["abu_border"]
        )
        self._chk_ingat.pack(side="left")
        
        btn_lupa = ctk.CTkLabel(chk_frame, text="Lupa password?",
            font=("Segoe UI", 9, "underline"), text_color=C["oranye"],
            cursor="hand2")
        btn_lupa.pack(side="right")

        # Login Button
        btn_masuk = ctk.CTkButton(card, text="→ MASUK", 
            command=self._login, width=320, height=45,
            font=("Segoe UI", 13, "bold"),
            fg_color=C["oranye"],
            hover_color=C["oranye_gelap"],
            corner_radius=12
        )
        btn_masuk.place(relx=0.5, rely=0.68, anchor="center")

        # Security Footer
        sec_frame = ctk.CTkFrame(card, fg_color="transparent")
        sec_frame.place(relx=0.5, rely=0.85, anchor="center")
        
        ctk.CTkLabel(sec_frame, text="", 
                    font=("Segoe UI", 12), text_color=C["hijau"]
        ).pack(side="left", padx=(0, 4))
        
        ctk.CTkLabel(sec_frame, text="Sistem aman & terpercaya", 
                    font=("Segoe UI", 9), text_color=C["teks_sub"]
        ).pack(side="left")

        # Error Label
        self._lbl_err = ctk.CTkLabel(card, text=" ", 
            font=("Segoe UI", 9), text_color=C["merah"])
        self._lbl_err.place(relx=0.5, rely=0.92, anchor="center")

        _bind_enter_chain([self._e_user, self._e_pass])
        self._e_pass.bind("<Return>", lambda e: self._login())
        self._e_user.focus_set()

    def _login(self):
        u = self._e_user.get().strip()
        p = self._e_pass.get()
        if db.cek_login(u, p):
            self._on_login()
        else:
            self._lbl_err.configure(text="Username atau password salah.")

#============================================================
#HALAMAN LOGIN - UPDATED UI
#============================================================
    

class HalamanLogin(ctk.CTkFrame):

    def __init__(self, parent, on_login):
        super().__init__(parent, corner_radius=0, fg_color="#FFF8F3")
        self._on_login = on_login
        self._build()

    def _build(self):

        # =========================================================
        # BACKGROUND UTAMA
        # =========================================================
        bg = ctk.CTkFrame(self, fg_color="#FFF8F3", corner_radius=0)
        bg.pack(fill="both", expand=True)

        # =========================================================
        # PANEL KIRI — HERO SECTION
        # =========================================================
        kiri = ctk.CTkFrame(
            bg,
            fg_color="#EA580C",
            corner_radius=0
        )
        kiri.place(relx=0, rely=0, relwidth=0.48, relheight=1)

        # Decorative circle
        lingkar1 = ctk.CTkFrame(
            kiri,
            fg_color="#FB923C",
            width=260,
            height=260,
            corner_radius=130
        )
        lingkar1.place(relx=0.78, rely=0.01)

        lingkar2 = ctk.CTkFrame(
            kiri,
            fg_color="#FDBA74",
            width=180,
            height=180,
            corner_radius=90
        )
        lingkar2.place(relx=-0.10, rely=0.72)

        # Logo / branding
        # =========================================================
        # LOGO GAMBAR
        # =========================================================
        logo_img = ctk.CTkImage(
            light_image=Image.open("assets/logo-graduation.png"),
            dark_image=Image.open("assets/logo-graduation.png"),
            size=(90, 90)   # ubah ukuran di sini
        )

        self.logo_label = ctk.CTkLabel(
            kiri,
            image=logo_img,
            text=""
        )
        self.logo_label.place(relx=0.07, rely=0.13)

        ctk.CTkLabel(
            kiri,
            text="SISTEM INFORMASI",
            font=("Segoe UI", 40, "bold"),
            text_color="white"
        ).place(relx=0.07, rely=0.23)

        ctk.CTkLabel(
            kiri,
            text="AKADEMIK MAHASISWA",
            font=("Segoe UI", 40, "bold"),
            text_color="white"
        ).place(relx=0.07, rely=0.30)

        ctk.CTkLabel(
            kiri,
            text="Kelola data akademik dengan\ncepat dan terintegrasi",
            font=("Segoe UI", 15),
            justify="left",
            text_color="#FFEDD5"
        ).place(relx=0.07, rely=0.40)


        # Quote Card
        quote = ctk.CTkFrame(
            kiri,
            fg_color="#FB923C",
            corner_radius=20,
            width=300,
            height=120,
            border_width=1,
            border_color="#FDBA74"
        )
        quote.place(relx=0.19, rely=0.74)

        ctk.CTkLabel(
            quote,
            text='"Pendidikan adalah senjata\npaling ampuh untuk mengubah dunia."',
            font=("Segoe UI", 12, "italic"),
            justify="left",
            text_color="white"
        ).place(relx=0.15, rely=0.28)

        ctk.CTkLabel(
            quote,
            text="— Nelson Mandela",
            font=("Segoe UI", 10),
            text_color="#FFEDD5"
        ).place(relx=0.08, rely=0.72)

        # =========================================================
        # PANEL KANAN
        # =========================================================
        kanan = ctk.CTkFrame(
            bg,
            fg_color="#FFF8F3",
            corner_radius=0
        )
        kanan.place(relx=0.48, rely=0, relwidth=0.52, relheight=1)

        # =========================================================
        # LOGIN CARD
        # =========================================================
        card = ctk.CTkFrame(
            kanan,
            fg_color="#FFFFFF",
            width=430,
            height=520,
            corner_radius=28,
            border_width=1,
            border_color="#FED7AA"
        )
        card.place(relx=0.5, rely=0.5, anchor="center")

        # Icon user
        icon_bg = ctk.CTkFrame(
            card,
            fg_color="#FFF1E8",
            width=90,
            height=90,
            corner_radius=45
        )
        icon_bg.place(relx=0.5, rely=0.12, anchor="center")

        ctk.CTkLabel(
            icon_bg,
            text="👤",
            font=("Segoe UI Emoji", 42),
            text_color="#EA580C"
        ).place(relx=0.5, rely=0.5, anchor="center")

        # Heading
        ctk.CTkLabel(
            card,
            text="Selamat Datang Kembali 👋",
            font=("Segoe UI", 24, "bold"),
            text_color="#2B2B2B"
        ).place(relx=0.5, rely=0.24, anchor="center")

        ctk.CTkLabel(
            card,
            text="Silakan masuk untuk melanjutkan",
            font=("Segoe UI", 11),
            text_color="#78716C"
        ).place(relx=0.5, rely=0.30, anchor="center")

        # =========================================================
        # USERNAME
        # =========================================================
        ctk.CTkLabel(
            card,
            text="Username",
            font=("Segoe UI", 10, "bold"),
            text_color="#78716C"
        ).place(relx=0.12, rely=0.39)

        self._e_user = ctk.CTkEntry(
            card,
            width=320,
            height=48,
            corner_radius=14,
            border_width=1,
            border_color="#FED7AA",
            fg_color="#FFF7ED",
            text_color="#2B2B2B",
            placeholder_text="Masukkan username",
            placeholder_text_color="#A8A29E",
            font=("Segoe UI", 12)
        )
        self._e_user.place(relx=0.5, rely=0.46, anchor="center")

        # =========================================================
        # PASSWORD
        # =========================================================
        ctk.CTkLabel(
            card,
            text="Password",
            font=("Segoe UI", 10, "bold"),
            text_color="#78716C"
        ).place(relx=0.12, rely=0.54)

        self._e_pass = ctk.CTkEntry(
            card,
            width=320,
            height=48,
            show="*",
            corner_radius=14,
            border_width=1,
            border_color="#FED7AA",
            fg_color="#FFF7ED",
            text_color="#2B2B2B",
            placeholder_text="Masukkan password",
            placeholder_text_color="#A8A29E",
            font=("Segoe UI", 12)
        )
        self._e_pass.place(relx=0.5, rely=0.61, anchor="center")

        # =========================================================
        # REMEMBER
        # =========================================================
        self._chk_ingat = ctk.CTkCheckBox(
            card,
            text="Ingat saya",
            font=("Segoe UI", 10),
            text_color="#78716C",
            fg_color="#EA580C",
            hover_color="#C2410C",
            border_color="#FED7AA"
        )
        self._chk_ingat.place(relx=0.12, rely=0.70)

        ctk.CTkLabel(
            card,
            text="Lupa password?",
            font=("Segoe UI", 10, "underline"),
            text_color="#EA580C",
            cursor="hand2"
        ).place(relx=0.68, rely=0.70)

        # =========================================================
        # BUTTON LOGIN
        # =========================================================
        btn_login = ctk.CTkButton(
            card,
            text="→  MASUK",
            command=self._login,
            width=320,
            height=50,
            corner_radius=14,
            fg_color="#F97316",
            hover_color="#C2410C",
            font=("Segoe UI", 14, "bold")
        )
        btn_login.place(relx=0.5, rely=0.80, anchor="center")

        # Footer
        ctk.CTkLabel(
            card,
            text="Sistem aman & terpercaya",
            font=("Segoe UI", 10),
            text_color="#A8A29E"
        ).place(relx=0.5, rely=0.90, anchor="center")

        # Error
        self._lbl_err = ctk.CTkLabel(
            card,
            text="",
            font=("Segoe UI", 10),
            text_color="#DC2626"
        )
        self._lbl_err.place(relx=0.5, rely=0.95, anchor="center")

        # Bind
        _bind_enter_chain([self._e_user, self._e_pass])
        self._e_pass.bind("<Return>", lambda e: self._login())
        self._e_user.focus_set()

    def _login(self):
        u = self._e_user.get().strip()
        p = self._e_pass.get()

        if db.cek_login(u, p):
            self._on_login()
        else:
            self._lbl_err.configure(
                text="Username atau password salah."
            )

# ============================================================
# APLIKASI UTAMA
# ============================================================

class App(ctk.CTk):

    def __init__(self):
        super().__init__()
        self.title("Sistem Informasi Akademik Mahasiswa")
        self.geometry("1280x740")
        self.minsize(1024, 640)
        self.configure(fg_color=C["abu_bg"])
        _style_tree()
        self._tampil_login()

    def _tampil_login(self):
        self._bersih()
        HalamanLogin(self, self._setelah_login).pack(fill="both", expand=True)

    def _setelah_login(self):
        self._bersih()
        self._bangun_shell()
        self._sidebar.aktifkan("dashboard")

    def _bangun_shell(self):
        self._sidebar = Sidebar(self, self._navigasi)
        self._sidebar.pack(side="left", fill="y")

        self._area = ctk.CTkFrame(self, corner_radius=0, fg_color=C["abu_bg"])
        self._area.pack(side="left", fill="both", expand=True)

        self._dash      = HalamanDashboard(self._area)
        self._mhs       = HalamanMahasiswa(self._area, on_nilai=self._buka_nilai)
        self._nilai     = HalamanNilai(self._area, on_selesai=self._selesai_nilai)
        self._statistik = HalamanStatistik(self._area)
        self._riwayat   = HalamanRiwayat(self._area)

        self._halaman_aktif = None

    def _navigasi(self, key: str):
        if key == "logout":
            if messagebox.askyesno("Logout", "Yakin ingin keluar?"):
                self._tampil_login()
            return

        mapping = {
            "dashboard":  self._dash,
            "mahasiswa":  self._mhs,
            "nilai":      self._nilai,
            "statistik":  self._statistik,
            "riwayat":    self._riwayat,
        }

        target = mapping.get(key)
        if not target or target is self._halaman_aktif:
            return

        if self._halaman_aktif:
            self._halaman_aktif.pack_forget()

        target.pack(fill="both", expand=True)
        self._halaman_aktif = target

        if key == "dashboard":   self._dash.refresh()
        if key == "mahasiswa":   self._mhs.refresh()
        if key == "statistik":   self._statistik.refresh()
        if key == "riwayat":     self._riwayat.refresh()

    def _buka_nilai(self, nim: str):
        self._sidebar.aktifkan("nilai")
        self._nilai.set_nim(nim)

    def _selesai_nilai(self):
        self._dash.refresh()
        self._mhs.refresh()

    def _bersih(self):
        for w in self.winfo_children():
            w.destroy()