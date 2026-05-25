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

    def __init__(self, parent, on_navigate):
        super().__init__(
            parent,
            width=260,
            fg_color="#FFFFFF",
            corner_radius=0
        )

        self.pack_propagate(False)

        self._nav = on_navigate
        self._btns = {}
        self._aktif = None

        self._build()

    def _build(self):

        # ====================================================
        # LOGO
        # ====================================================
        top = ctk.CTkFrame(
            self,
            fg_color="transparent"
        )
        top.pack(fill="x", padx=24, pady=(28, 20))

        logo = ctk.CTkImage(
            light_image=Image.open("assets/logo-graduation.png"),
            dark_image=Image.open("assets/logo-graduation.png"),
            size=(50, 50)
        )

        kiri = ctk.CTkFrame(top, fg_color="transparent")
        kiri.pack(side="left")

        self.logo_label = ctk.CTkLabel(
            kiri,
            image=logo,
            text=""
        )
        self.logo_label.pack()

        kanan = ctk.CTkFrame(top, fg_color="transparent")
        kanan.pack(side="left", padx=10)

        ctk.CTkLabel(
            kanan,
            text="SIAKAD",
            font=("Segoe UI", 22, "bold"),
            text_color="#2B2B2B"
        ).pack(anchor="w")

        ctk.CTkLabel(
            kanan,
            text="Mahasiswa",
            font=("Segoe UI", 11),
            text_color="#78716C"
        ).pack(anchor="w")

        # ====================================================
        # MENU
        # ====================================================

        self._section("MENU")

        self._menu_button(
            "Beranda",
            "beranda",
            "🏠"
        )

        self._menu_button(
            "Dashboard",
            "dashboard",
            "▦"
        )

        self._section("DATA MASTER")

        self._menu_button(
            "Data Mahasiswa",
            "mahasiswa",
            "👥"
        )

        self._menu_button(
            "Input Nilai",
            "nilai",
            "📝"
        )

        self._section("LAPORAN")

        self._menu_button(
            "Statistik",
            "statistik",
            "📊"
        )

        self._menu_button(
            "Riwayat Akademik",
            "riwayat",
            "🕘"
        )

        self._menu_button(
            "Kalender Akademik",
            "jadwal_akademik",
            "📅"
        )

        self._section("SISTEM")

        logout = ctk.CTkButton(
            self,
            text="↪ Logout",
            anchor="w",
            height=48,
            fg_color="transparent",
            hover_color="#F5F5F5",
            text_color="#6B7280",
            font=("Segoe UI", 13),
            corner_radius=14,
            command=lambda: self._nav("logout")
        )

        logout.pack(
            side="bottom",
            fill="x",
            padx=18,
            pady=24
        )

    def _section(self, text):

        if text:
            ctk.CTkLabel(
                self,
                text=text,
                font=("Segoe UI", 11, "bold"),
                text_color="#A1A1AA"
            ).pack(anchor="w", padx=36, pady=(22, 10))

    def _menu_button(self, text, key, icon):

        btn = ctk.CTkButton(
            self,
            text=f"{icon}   {text}",
            anchor="w",
            height=52,
            fg_color="transparent",
            hover_color="#FFF1E8",
            text_color="#52525B",
            font=("Segoe UI", 14),
            corner_radius=16,
            command=lambda k=key: self._klik(k)
        )

        btn.pack(fill="x", padx=18, pady=4)

        self._btns[key] = btn

    def _klik(self, key: str):

        for k, b in self._btns.items():

            b.configure(
                fg_color="transparent",
                text_color="#52525B",
                font=("Segoe UI", 14)
            )

        if key in self._btns:
            self._btns[key].configure(
                fg_color="#FF6B00",
                hover_color="#FF6B00",
                text_color="#FFFFFF",
                font=("Segoe UI", 14, "bold")
            )

        self._aktif = key
        self._nav(key)

    def aktifkan(self, key):
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
# HALAMAN BERANDA
# ============================================================

class HalamanBeranda(HalamanBase):

    def __init__(self, parent):
        super().__init__(parent)
        self._build()

    def _build(self):
        # Header
        hdr = ctk.CTkFrame(self, fg_color="transparent", corner_radius=0, height=70)
        hdr.pack(fill="x", padx=0, pady=0)
        hdr.pack_propagate(False)
        inner = ctk.CTkFrame(hdr, fg_color="transparent")
        inner.pack(side="left", padx=28, pady=12)
        ctk.CTkLabel(inner, text="🏠", font=("Segoe UI Emoji", 20)).pack(side="left", padx=(0, 8))
        ctk.CTkLabel(inner, text="Beranda", font=F_JUDUL, text_color=C["teks"]).pack(side="left", anchor="w")
        ctk.CTkFrame(self, height=1, fg_color=C["abu_border"]).pack(fill="x")

        # Scroll area
        scroll = ctk.CTkScrollableFrame(self, fg_color="transparent", corner_radius=0)
        scroll.pack(fill="both", expand=True, padx=24, pady=16)

        # Banner Pengumuman
        banner = ctk.CTkFrame(scroll, fg_color=C["oranye"], corner_radius=16)
        banner.pack(fill="x", pady=(0, 20))

        banner_inner = ctk.CTkFrame(banner, fg_color="transparent")
        banner_inner.pack(fill="x", padx=28, pady=20)

        ikon_wrap = ctk.CTkFrame(
            banner_inner, fg_color="#FFFFFF",
            width=72, height=72, corner_radius=36
        )
        ikon_wrap.pack(side="left", padx=(0, 20))
        ikon_wrap.pack_propagate(False)
        ctk.CTkLabel(
            ikon_wrap, text="📢",
            font=("Segoe UI Emoji", 28)
        ).place(relx=0.5, rely=0.5, anchor="center")

        teks_wrap = ctk.CTkFrame(banner_inner, fg_color="transparent")
        teks_wrap.pack(side="left", fill="both", expand=True)

        ctk.CTkLabel(
            teks_wrap, text="Pengumuman",
            font=("Segoe UI", 18, "bold"),
            text_color="#FFFFFF", anchor="w"
        ).pack(anchor="w", pady=(0, 8))

        pengumuman = [
            "Bagi Anda yang akan mengikuti Kuliah Semester Antara / Semester Padat, silakan pilih mata kuliah pada tautan: Semester Padat",
            "Pembayaran melalui virtual account mulai tanggal 1 Juni 2026 sampai 15 Juni 2026.",
            "Setelah melakukan proses pembayaran, Anda dapat mengisi IRS dan melaksanakan perwalian daring pada tanggal 18 Juni 2026 sampai 21 Juni 2026.",
        ]
        for p in pengumuman:
            baris = ctk.CTkFrame(teks_wrap, fg_color="transparent")
            baris.pack(anchor="w", pady=2, fill="x")
            ctk.CTkLabel(
                baris, text="✅", font=("Segoe UI Emoji", 12),
                text_color="#FFFFFF"
            ).pack(side="left", padx=(0, 6))
            ctk.CTkLabel(
                baris, text=p,
                font=("Segoe UI", 11),
                text_color="#FFFFFF", anchor="w", justify="left", wraplength=650
            ).pack(side="left", anchor="w")

        # Info Cards
        info_items = [
            ("👤", "Manajemen DIM", "Fitur-fitur manajemen Data Induk Mahasiswa (DIM), pengajuan IRS dan PRS, informasi Kalender Akademik, dan Jadwal Kuliah."),
            ("🌐", "Akses Di Mana Saja", "Sistem ini menggunakan Single Sign On UPI sebagai fitur otentifikasi, dan dikembangkan dengan infrastruktur internet sehingga dapat diakses di mana saja."),
            ("🗄️", "Data Terintegrasi", "Data yang dimunculkan merupakan replikasi dari data pada SIAK Utama UPI. Jika terdapat perbedaan, SIAK Utama menjadi rujukan yang dianggap benar."),
        ]

        for ikon, judul, deskripsi in info_items:
            card = ctk.CTkFrame(
                scroll,
                fg_color=C["putih"],
                corner_radius=14,
                border_width=1,
                border_color=C["abu_border"]
            )
            card.pack(fill="x", pady=8)

            ikon_card = ctk.CTkFrame(
                card, fg_color=C["oranye_muda"],
                width=54, height=54, corner_radius=12
            )
            ikon_card.pack(side="left", padx=20, pady=16)
            ikon_card.pack_propagate(False)
            ctk.CTkLabel(
                ikon_card, text=ikon,
                font=("Segoe UI Emoji", 22)
            ).place(relx=0.5, rely=0.5, anchor="center")

            teks_card = ctk.CTkFrame(card, fg_color="transparent")
            teks_card.pack(side="left", fill="both", expand=True, pady=16, padx=(0, 20))

            ctk.CTkLabel(
                teks_card, text=judul,
                font=("Segoe UI", 13, "bold"),
                text_color=C["teks"], anchor="w"
            ).pack(anchor="w")

            ctk.CTkLabel(
                teks_card, text=deskripsi,
                font=("Segoe UI", 11),
                text_color=C["teks_sub"], anchor="w",
                justify="left", wraplength=700
            ).pack(anchor="w", pady=(4, 0))

    def refresh(self):
        pass

# ============================================================
# HALAMAN DASHBOARD
# ============================================================

# ─────────────────────────────────────────────
# Warna tema (sesuaikan dengan C dict kamu)
# ─────────────────────────────────────────────
ORANYE   = "#f97316"
ORANYE_MUDA = "#fff3e0"
HIJAU    = "#22c55e"
MERAH    = "#ef4444"
KUNING   = "#fbbf24"
PUTIH    = "#ffffff"
ABU_BG   = "#f0f0f0"
ABU_CARD = "#f9fafb"
TEKS     = "#222222"
TEKS_SUB = "#888888"

class HalamanDashboard(HalamanBase):

    def __init__(self, parent):
        super().__init__(parent)
        self.configure(fg_color=C["abu_bg"])
        self._build()

    def _build(self):
        # ── Baris 1: 4 kartu statistik ──────────────────────────────────
        row1 = ctk.CTkFrame(self, fg_color="transparent")
        row1.pack(fill="x", padx=24, pady=(20, 10))

        stats_spec = [
            ("total",       "Total Mahasiswa",  "👥", C["oranye"]),
            ("sudah_nilai", "Sudah Input Nilai", "✅", C["hijau"]),
            ("rata_ipk",    "Rata-rata IPK",     "⭐", C["kuning"]),
            ("belum_nilai", "Belum Input Nilai", "⏳", C["merah"]),
        ]
        self._stat_vals = {}
        self._stat_subs = {}

        for col, (key, label, emoji, warna) in enumerate(stats_spec):
            row1.columnconfigure(col, weight=1)
            card = ctk.CTkFrame(row1, fg_color=C["putih"], corner_radius=14)
            card.grid(row=0, column=col, padx=6, sticky="nsew", ipady=14)

            inner = ctk.CTkFrame(card, fg_color="transparent")
            inner.pack(fill="x", padx=16, pady=14)

            # Kotak ikon warna pastel sesuai warna kartu
            # Kalau mau pakai gambar PNG, ganti baris emoji di bawah dengan:
            #   img = ctk.CTkImage(Image.open("nama_file.png"), size=(32,32))
            #   ctk.CTkLabel(icon_box, image=img, text="").place(relx=0.5, rely=0.5, anchor="center")
            icon_bg = {
                C["oranye"]: C["oranye_muda"],
                C["hijau"]:  C["hijau_muda"],
                C["kuning"]: C["kuning_muda"],
                C["merah"]:  C["merah_muda"],
            }.get(warna, C["oranye_muda"])

            icon_box = ctk.CTkFrame(inner, fg_color=icon_bg,
                                    corner_radius=12, width=52, height=52)
            icon_box.pack(side="left", padx=(0, 14))
            icon_box.pack_propagate(False)
            ctk.CTkLabel(icon_box, text=emoji, font=("Segoe UI", 22),
                         fg_color="transparent"
            ).place(relx=0.5, rely=0.5, anchor="center")

            info = ctk.CTkFrame(inner, fg_color="transparent")
            info.pack(side="left", fill="x", expand=True)

            ctk.CTkLabel(info, text=label,
                font=("Segoe UI", 10), text_color=C["teks_sub"], anchor="w"
            ).pack(fill="x")

            val_lbl = ctk.CTkLabel(info, text="0",
                font=("Segoe UI", 26, "bold"), text_color=warna, anchor="w")
            val_lbl.pack(fill="x")

            sub_lbl = ctk.CTkLabel(info, text="",
                font=("Segoe UI", 9), text_color=C["teks_sub"], anchor="w")
            sub_lbl.pack(fill="x")

            self._stat_vals[key] = val_lbl
            self._stat_subs[key] = sub_lbl

        # ── Baris 2: Donut + Top 5 ───────────────────────────────────────
        row2 = ctk.CTkFrame(self, fg_color="transparent")
        row2.pack(fill="x", padx=24, pady=(0, 10))
        row2.columnconfigure(0, weight=2)
        row2.columnconfigure(1, weight=3)

        # -- Donut card --
        donut_card = ctk.CTkFrame(row2, fg_color=C["putih"], corner_radius=14)
        donut_card.grid(row=0, column=0, padx=(0, 6), sticky="nsew")

        hdr_d = ctk.CTkFrame(donut_card, fg_color="transparent")
        hdr_d.pack(fill="x", padx=18, pady=(14, 0))
        ctk.CTkLabel(hdr_d, text="Distribusi IPK Mahasiswa",
            font=("Segoe UI", 12, "bold"), text_color=C["teks"]).pack(side="left")
        ctk.CTkLabel(hdr_d, text="Lihat Detail",
            font=("Segoe UI", 10), text_color=C["oranye"]).pack(side="right")

        donut_inner = ctk.CTkFrame(donut_card, fg_color="transparent")
        donut_inner.pack(fill="x", padx=18, pady=14)

        self._donut_canvas = tk.Canvas(donut_inner, width=130, height=130,
                                       bg=C["putih"], highlightthickness=0)
        self._donut_canvas.pack(side="left")

        legend_frame = ctk.CTkFrame(donut_inner, fg_color="transparent")
        legend_frame.pack(side="left", padx=(16, 0), fill="y", expand=True)

        self._legend_specs = [
            ("IPK < 2.00",     C["merah"],   "lt2"),
            ("IPK 2.00–2.75",  C["oranye"],  "lt275"),
            ("IPK 2.76–3.50",  C["kuning"],  "lt35"),
            ("IPK 3.51–4.00",  C["hijau"],   "lt4"),
        ]
        self._legend_labels = {}
        for nama, warna, key in self._legend_specs:
            rf = ctk.CTkFrame(legend_frame, fg_color="transparent")
            rf.pack(fill="x", pady=5)
            ctk.CTkFrame(rf, fg_color=warna,
                         width=10, height=10, corner_radius=5
            ).pack(side="left")
            ctk.CTkLabel(rf, text=nama,
                font=F_KECIL, text_color=C["teks_sub"]
            ).pack(side="left", padx=6)
            lbl_v = ctk.CTkLabel(rf, text="0 (0%)",
                font=F_KECIL, text_color=C["teks_sub"])
            lbl_v.pack(side="right")
            self._legend_labels[key] = lbl_v

        # -- Top 5 card --
        top5_card = ctk.CTkFrame(row2, fg_color=C["putih"], corner_radius=14)
        top5_card.grid(row=0, column=1, padx=(6, 0), sticky="nsew")

        hdr_t = ctk.CTkFrame(top5_card, fg_color="transparent")
        hdr_t.pack(fill="x", padx=18, pady=(14, 4))
        ctk.CTkLabel(hdr_t, text="Top 5 IPK Tertinggi",
            font=("Segoe UI", 12, "bold"), text_color=C["teks"]).pack(side="left")
        ctk.CTkLabel(hdr_t, text="Lihat Semua",
            font=("Segoe UI", 10), text_color=C["oranye"]).pack(side="right")

        self._top5_frame = ctk.CTkFrame(top5_card, fg_color="transparent")
        self._top5_frame.pack(fill="both", padx=18, pady=(0, 14), expand=True)

        # ── Baris 3: Tabel mahasiswa ─────────────────────────────────────
        tbl_card = ctk.CTkFrame(self, fg_color=C["putih"], corner_radius=14)
        tbl_card.pack(fill="both", expand=True, padx=24, pady=(0, 20))

        tbl_top = ctk.CTkFrame(tbl_card, fg_color="transparent")
        tbl_top.pack(fill="x", padx=18, pady=(14, 8))
        ctk.CTkLabel(tbl_top, text="Data Mahasiswa Terbaru",
            font=("Segoe UI", 12, "bold"), text_color=C["teks"]).pack(side="left")

        ctrl = ctk.CTkFrame(tbl_top, fg_color="transparent")
        ctrl.pack(side="right")
        self._search_var = ctk.StringVar()
        self._search_var.trace_add("write", lambda *_: self._render_tabel(db.get_semua()))
        ctk.CTkEntry(ctrl, textvariable=self._search_var,
            placeholder_text="Cari mahasiswa...", width=200, corner_radius=8,
            border_color=C["abu_border"], fg_color=C["putih"]
        ).pack(side="left", padx=(0, 8))
        _btn(ctrl, "+ Tambah Mahasiswa",
             command=lambda: self.master.buka_halaman("tambah"),
             color=C["oranye"], width=170
        ).pack(side="left")

        # Header kolom
        col_defs = [("NIM", 90), ("Nama Mahasiswa", 160),
                    ("Program Studi", 160), ("Angkatan", 75),
                    ("IPK", 60), ("Aksi", 70)]
        col_hdr = ctk.CTkFrame(tbl_card, fg_color=C["oranye"],
                               corner_radius=8, height=32)
        col_hdr.pack(fill="x", padx=18, pady=(0, 4))
        col_hdr.pack_propagate(False)
        for txt, w in col_defs:
            ctk.CTkLabel(col_hdr, text=txt, width=w,
                font=("Segoe UI", 10, "bold"), text_color=C["putih"], anchor="w"
            ).pack(side="left", padx=(8, 0))

        self._tbl_scroll = ctk.CTkScrollableFrame(tbl_card, fg_color="transparent")
        self._tbl_scroll.pack(fill="both", expand=True, padx=18, pady=(0, 14))
        self._col_defs = col_defs

        self.refresh()

    # ── Donut chart ──────────────────────────────────────────────────────
    def _draw_donut(self, dist: dict, total: int):
        c = self._donut_canvas
        c.delete("all")
        cx, cy, r_out, r_in = 65, 65, 55, 34
        warna_urut = [C["merah"], C["oranye"], C["kuning"], C["hijau"]]
        keys_urut  = ["lt2", "lt275", "lt35", "lt4"]

        if total == 0:
            c.create_oval(cx-r_out, cy-r_out, cx+r_out, cy+r_out,
                          outline="#e5e7eb", width=22)
        else:
            start = -90.0
            for warna, key in zip(warna_urut, keys_urut):
                val = dist.get(key, 0)
                extent = (val / total) * 360
                if extent > 0:
                    c.create_arc(cx-r_out, cy-r_out, cx+r_out, cy+r_out,
                        start=start, extent=extent,
                        fill=warna, outline=warna)
                    start += extent
            # lubang tengah
            c.create_oval(cx-r_in, cy-r_in, cx+r_in, cy+r_in,
                          fill=C["putih"], outline=C["putih"])

        c.create_text(cx, cy-8,  text=str(total),
                      font=("Segoe UI", 16, "bold"), fill=C["teks"])
        c.create_text(cx, cy+10, text="Mahasiswa",
                      font=("Segoe UI", 9), fill=C["teks_sub"])

    # ── Top 5 ────────────────────────────────────────────────────────────
    def _render_top5(self, semua: list):
        for w in self._top5_frame.winfo_children():
            w.destroy()

        ranked = sorted(
            [m for m in semua if m["semester"]],
            key=lambda m: db.ipk_mahasiswa(m), reverse=True
        )[:5]

        rank_colors  = [C["oranye"], C["teks_sub"], C["kuning"]]
        rank_fg      = [C["putih"],  C["putih"],    C["putih"]]

        for i, m in enumerate(ranked):
            ipk  = db.ipk_mahasiswa(m)
            row  = ctk.CTkFrame(self._top5_frame, fg_color="transparent", height=36)
            row.pack(fill="x", pady=2)
            row.pack_propagate(False)

            bg_r = rank_colors[i] if i < 3 else C["abu_card"]
            fg_r = rank_fg[i]     if i < 3 else C["teks_sub"]
            rbox = ctk.CTkFrame(row, fg_color=bg_r,
                                width=26, height=26, corner_radius=13)
            rbox.pack(side="left", padx=(0, 10))
            rbox.pack_propagate(False)
            ctk.CTkLabel(rbox, text=str(i+1),
                font=("Segoe UI", 10, "bold"), text_color=fg_r
            ).place(relx=0.5, rely=0.5, anchor="center")

            ctk.CTkLabel(row, text=m["nama"],
                font=F_NORMAL, text_color=C["teks"], anchor="w"
            ).pack(side="left")
            ctk.CTkLabel(row, text=f"{ipk:.2f}",
                font=("Segoe UI", 11, "bold"), text_color=C["teks"], anchor="e"
            ).pack(side="right")
            ctk.CTkLabel(row, text=m["nim"],
                font=F_KECIL, text_color=C["teks_sub"], anchor="e"
            ).pack(side="right", padx=(0, 12))

    # ── Tabel mahasiswa ──────────────────────────────────────────────────
    def _render_tabel(self, semua: list):
        for w in self._tbl_scroll.winfo_children():
            w.destroy()

        query    = self._search_var.get().lower()
        filtered = [m for m in semua
                    if query in m["nama"].lower() or query in m["nim"].lower()]

        for idx, m in enumerate(filtered[:20]):
            ipk    = db.ipk_mahasiswa(m) if m["semester"] else 0.0
            bg_row = C["putih"] if idx % 2 == 0 else C["abu_card"]
            row    = ctk.CTkFrame(self._tbl_scroll, fg_color=bg_row,
                                  height=34, corner_radius=6)
            row.pack(fill="x", pady=1)
            row.pack_propagate(False)

            vals = [m["nim"], m["nama"],
                    m.get("prodi", "-"), str(m.get("angkatan", "-")),
                    f"{ipk:.2f}"]
            for val, (_, w) in zip(vals, self._col_defs[:-1]):
                ctk.CTkLabel(row, text=val, width=w,
                    font=F_KECIL, text_color=C["teks"], anchor="w"
                ).pack(side="left", padx=(8, 0))

            aksi = ctk.CTkFrame(row, fg_color="transparent")
            aksi.pack(side="left", padx=4)
            ctk.CTkButton(aksi, text="👁", width=28, height=26,
                fg_color="transparent", hover_color=C["oranye_muda"],
                text_color=C["oranye"], corner_radius=6,
                command=lambda nim=m["nim"]: self.master.buka_halaman("detail", nim)
            ).pack(side="left", padx=2)
            ctk.CTkButton(aksi, text="✏️", width=28, height=26,
                fg_color="transparent", hover_color=C["oranye_muda"],
                text_color=C["oranye"], corner_radius=6,
                command=lambda nim=m["nim"]: self.master.buka_halaman("edit", nim)
            ).pack(side="left", padx=2)

    # ── Refresh utama ────────────────────────────────────────────────────
    def refresh(self):
        stat  = db.statistik()   # keys: total, sudah_nilai, rata_ipk, terbaik, terbaik_ipk
        semua = db.get_semua()

        total = stat["total"]
        sudah = stat["sudah_nilai"]
        belum = total - sudah

        # ── 4 kartu stat (sama persis dengan kode asli) ──
        self._stat_vals["total"].configure(text=str(total))
        self._stat_subs["total"].configure(text="orang terdaftar")

        self._stat_vals["sudah_nilai"].configure(text=str(sudah))
        self._stat_subs["sudah_nilai"].configure(text="mahasiswa")

        self._stat_vals["rata_ipk"].configure(text=str(stat["rata_ipk"]))
        self._stat_subs["rata_ipk"].configure(text="dari 4.00")

        self._stat_vals["belum_nilai"].configure(text=str(belum))
        self._stat_subs["belum_nilai"].configure(text="mahasiswa")

        # ── Distribusi IPK untuk donut ──
        dist = {"lt2": 0, "lt275": 0, "lt35": 0, "lt4": 0}
        for m in semua:
            if m["semester"]:
                ipk = db.ipk_mahasiswa(m)
                if   ipk < 2.00: dist["lt2"]   += 1
                elif ipk < 2.75: dist["lt275"]  += 1
                elif ipk < 3.50: dist["lt35"]   += 1
                else:            dist["lt4"]    += 1

        self._draw_donut(dist, total)

        ipk_total = sum(dist.values()) or 1
        for _, _, key in self._legend_specs:
            n   = dist.get(key, 0)
            pct = n / ipk_total * 100
            self._legend_labels[key].configure(text=f"{n} ({pct:.1f}%)")

        self._render_top5(semua)
        self._render_tabel(semua)


# ============================================================
# HALAMAN DATA MAHASISWA
# ============================================================

class HalamanMahasiswa(HalamanBase):

    ROWS_PER_PAGE = 10

    def __init__(self, parent, on_nilai):
        super().__init__(parent)
        self._on_nilai  = on_nilai
        self._page      = 1
        self._all_rows  = []
        self._header("Data Mahasiswa", "Kelola data mahasiswa terdaftar")
        self._build()
        self.refresh()

    def _build(self):
        # ── Toolbar ─────────────────────────────────────────────────────
        toolbar = ctk.CTkFrame(self, fg_color="transparent")
        toolbar.pack(fill="x", padx=28, pady=14)

        # Search box
        search_wrap = ctk.CTkFrame(toolbar, fg_color=C["putih"],
                                   corner_radius=8,
                                   border_width=1, border_color=C["abu_border"])
        search_wrap.pack(side="left")
        self._search_var = ctk.StringVar()
        self._search_var.trace_add("write", lambda *_: self._go_page(1))
        ctk.CTkEntry(
            search_wrap, textvariable=self._search_var,
            placeholder_text="Cari Mahasiswa...",
            width=240, height=38, border_width=0,
            fg_color="transparent", font=F_NORMAL,
        ).pack(side="left", padx=(10, 4))
        ctk.CTkLabel(search_wrap, text="🔍",
            font=("Segoe UI", 14), text_color=C["teks_sub"]
        ).pack(side="left", padx=(0, 8))

        # Tombol kanan (urutan di foto: Hapus | Input Nilai | Edit Nama | + Tambah)
        _btn(toolbar, "+ Tambah",   self._form_tambah,
             color=C["oranye"],  width=120).pack(side="right", padx=(6, 0))
        _btn(toolbar, "Edit Nama",  self._form_edit,
             color=C["oranye"],  width=110).pack(side="right", padx=6)
        _btn(toolbar, "Input Nilai", self._ke_nilai,
             color=C["oranye"],   width=115).pack(side="right", padx=6)
        _btn(toolbar, "Hapus",      self._hapus,
             color=C["oranye"],   width=90).pack(side="right")

        # ── Tabel (CTkFrame putih + header oranye + baris manual) ───────
        tbl_card = ctk.CTkFrame(self, fg_color=C["putih"],
                                corner_radius=12,
                                border_width=1, border_color=C["abu_border"])
        tbl_card.pack(fill="both", expand=True, padx=28, pady=(0, 10))

        # Header kolom
        col_defs = [
            ("NIM",             120, "center"),
            ("Nama Lengkap",    200, "w"),
            ("Semester Terisi", 160, "center"),
            ("IPK",              70, "center"),
            ("Total SKS",        90, "center"),
            ("Predikat",        130, "center"),
            ("Aksi",             90, "center"),
        ]
        self._col_defs = col_defs

        hdr = ctk.CTkFrame(tbl_card, fg_color=C["oranye"],
                           corner_radius=8, height=40)
        hdr.pack(fill="x", padx=10, pady=(10, 0))
        hdr.pack_propagate(False)
        for txt, w, anc in col_defs:
            ctk.CTkLabel(hdr, text=txt, width=w,
                font=("Segoe UI", 11, "bold"),
                text_color=C["putih"], anchor=anc
            ).pack(side="left", padx=(6, 0))

        # Scrollable frame untuk baris data
        self._body = ctk.CTkScrollableFrame(tbl_card, fg_color="transparent")
        self._body.pack(fill="both", expand=True, padx=10, pady=(4, 4))

        # ── Status bar + Paginasi ────────────────────────────────────────
        bottom = ctk.CTkFrame(self, fg_color="transparent")
        bottom.pack(fill="x", padx=28, pady=(0, 16))

        self._sbar = ctk.CTkLabel(bottom, text="",
            font=F_KECIL, text_color=C["teks_sub"], anchor="w")
        self._sbar.pack(side="left")

        self._pager_frame = ctk.CTkFrame(bottom, fg_color="transparent")
        self._pager_frame.pack(side="right")

        # Simpan NIM terpilih (ganti selection Treeview)
        self._selected_nim_var: str | None = None

    # ── Render baris tabel ───────────────────────────────────────────────
    def _render_body(self):
        for w in self._body.winfo_children():
            w.destroy()
        self._selected_nim_var = None

        start = (self._page - 1) * self.ROWS_PER_PAGE
        page_rows = self._all_rows[start: start + self.ROWS_PER_PAGE]

        predikat_warna = {
            "Cumlaude":        "#7C3AED",
            "Sangat Baik":     C["hijau"],
            "Baik":            C["oranye"],
            "Cukup":           C["kuning"],
            "Perlu Perbaikan": C["merah"],
        }

        for idx, m in enumerate(page_rows):
            ipk   = db.ipk_mahasiswa(m)
            pred  = db.predikat(ipk)
            smt   = db.semester_terisi(m)
            sks   = db.total_sks(m)
            warna_pred = predikat_warna.get(pred, C["teks"])

            bg = C["putih"] if idx % 2 == 0 else C["abu_card"]

            row = ctk.CTkFrame(self._body, fg_color=bg,
                               corner_radius=6, height=40, cursor="hand2")
            row.pack(fill="x", pady=1)
            row.pack_propagate(False)

            nim = m["nim"]

            # Klik baris → pilih
            def _pilih(e, n=nim, r=row):
                self._select_row(n, r)
            row.bind("<Button-1>", _pilih)

            vals = [
                (nim,           120, "center", C["teks"]),
                (m["nama"],     200, "w",      C["teks"]),
                (str(smt),      160, "center", C["teks_sub"]),
                (f"{ipk:.2f}",   70, "center", C["teks"]),
                (str(sks),       90, "center", C["teks"]),
                (pred,          130, "center", warna_pred),
            ]
            for txt, w, anc, clr in vals:
                lbl = ctk.CTkLabel(row, text=txt, width=w,
                    font=F_NORMAL, text_color=clr, anchor=anc,
                    fg_color="transparent")
                lbl.pack(side="left", padx=(6, 0))
                lbl.bind("<Button-1>", lambda e, n=nim, r=row: self._select_row(n, r))

            # Kolom Aksi
            aksi = ctk.CTkFrame(row, fg_color="transparent", width=90)
            aksi.pack(side="left", padx=(4, 0))
            aksi.pack_propagate(False)

            for icon, cmd in [
                ("👁",  lambda n=nim: self._detail_nim(n)),
                ("✏️", lambda n=nim: self._form_edit_nim(n)),
                ("🗑",  lambda n=nim: self._hapus_nim(n)),
            ]:
                ctk.CTkButton(aksi, text=icon, width=26, height=26,
                    fg_color="transparent",
                    hover_color=C["oranye_muda"],
                    text_color=C["teks_sub"],
                    corner_radius=6, font=("Segoe UI", 13),
                    command=cmd
                ).pack(side="left", padx=1)

        self._render_pager()

    # ── Highlight baris terpilih ─────────────────────────────────────────
    def _select_row(self, nim: str, row_frame: ctk.CTkFrame):
        # Reset semua baris
        for i, w in enumerate(self._body.winfo_children()):
            w.configure(fg_color=C["putih"] if i % 2 == 0 else C["abu_card"])
        # Highlight baris ini
        row_frame.configure(fg_color=C["oranye_muda"])
        self._selected_nim_var = nim

    # ── Paginasi ─────────────────────────────────────────────────────────
    def _render_pager(self):
        for w in self._pager_frame.winfo_children():
            w.destroy()

        total_pages = max(1, math.ceil(len(self._all_rows) / self.ROWS_PER_PAGE))
        if total_pages <= 1:
            return

        def _pg_btn(text, cmd, active=False):
            bg = C["oranye"] if active else C["putih"]
            fg = C["putih"]  if active else C["teks"]
            ctk.CTkButton(
                self._pager_frame, text=text, width=32, height=32,
                fg_color=bg, hover_color=C["oranye_muda"],
                text_color=fg, corner_radius=6,
                font=("Segoe UI", 11, "bold") if active else F_NORMAL,
                border_width=1, border_color=C["abu_border"],
                command=cmd
            ).pack(side="left", padx=2)

        _pg_btn("‹", lambda: self._go_page(self._page - 1))

        # Halaman yang ditampilkan: 1, 2, 3, ..., total
        pages_show = set()
        pages_show.update([1, 2, 3, total_pages])
        pages_show.add(self._page)
        if self._page > 1: pages_show.add(self._page - 1)
        if self._page < total_pages: pages_show.add(self._page + 1)

        prev = 0
        for p in sorted(pages_show):
            if p - prev > 1:
                ctk.CTkLabel(self._pager_frame, text="...",
                    font=F_NORMAL, text_color=C["teks_sub"], width=20
                ).pack(side="left")
            _pg_btn(str(p), lambda pg=p: self._go_page(pg), active=(p == self._page))
            prev = p

        _pg_btn("›", lambda: self._go_page(self._page + 1))

    def _go_page(self, page: int):
        total_pages = max(1, math.ceil(len(self._all_rows) / self.ROWS_PER_PAGE))
        self._page  = max(1, min(page, total_pages))
        self._render_body()
        total = db.statistik()["total"]
        self._sbar.configure(
            text=f"Menampilkan {len(self._all_rows)} dari {total} mahasiswa")

    # ── Refresh data ─────────────────────────────────────────────────────
    def refresh(self):
        keyword = self._search_var.get()
        self._all_rows = db.cari(keyword) if keyword else db.get_semua()
        self._go_page(self._page)

    # ── Ambil NIM terpilih (dari klik baris atau toolbar) ────────────────
    def _selected_nim(self) -> str | None:
        if not self._selected_nim_var:
            messagebox.showwarning("Perhatian", "Pilih mahasiswa terlebih dahulu.")
            return None
        return self._selected_nim_var

    # ── Aksi toolbar ─────────────────────────────────────────────────────
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
        self._form_edit_nim(nim)

    def _form_edit_nim(self, nim: str):
        semua = db.get_semua()
        mhs   = next((m for m in semua if m["nim"] == nim), None)
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
        self._hapus_nim(nim)

    def _hapus_nim(self, nim: str):
        semua = db.get_semua()
        mhs   = next((m for m in semua if m["nim"] == nim), None)
        if not mhs: return
        if messagebox.askyesno("Konfirmasi",
                f"Hapus {mhs['nama']} ({nim})?\n\nSemua data nilai ikut terhapus."):
            try:
                db.hapus_mahasiswa(nim)
                self._selected_nim_var = None
                self.refresh()
            except ValueError as err:
                messagebox.showerror("Gagal", str(err))

    def _ke_nilai(self):
        nim = self._selected_nim()
        if nim:
            self._on_nilai(nim)

    def _detail_nim(self, nim: str):
        semua = db.get_semua()
        mhs   = next((m for m in semua if m["nim"] == nim), None)
        if not mhs: return

        # ── Sama persis dengan _detail() asli ──
        win = ctk.CTkToplevel(self)
        win.title(f"Detail — {mhs['nama']}")
        win.geometry("520x560")
        win.grab_set()

        ipk  = db.ipk_mahasiswa(mhs)
        pred = db.predikat(ipk)

        ctk.CTkLabel(win, text=mhs["nama"], font=F_JUDUL
        ).pack(padx=24, pady=(20, 2), anchor="w")
        ctk.CTkLabel(win, text=f"NIM {mhs['nim']}", font=F_KECIL,
            text_color=C["teks_sub"]).pack(padx=24, anchor="w")

        badge = ctk.CTkFrame(win, fg_color=C["oranye_muda"], corner_radius=10)
        badge.pack(fill="x", padx=24, pady=14)
        ctk.CTkLabel(badge, text=f"{ipk:.2f}",
            font=("Segoe UI", 36, "bold"), text_color=C["oranye"]
        ).pack(side="left", padx=20, pady=14)
        info = ctk.CTkFrame(badge, fg_color="transparent")
        info.pack(side="left", pady=14)
        ctk.CTkLabel(info, text=pred,
            font=("Segoe UI", 13, "bold"), text_color=C["oranye"]
        ).pack(anchor="w")
        ctk.CTkLabel(info,
            text=f"{db.total_sks(mhs)} SKS  |  Semester terisi: {db.semester_terisi(mhs)}",
            font=F_KECIL, text_color=C["teks_sub"]
        ).pack(anchor="w")

        ctk.CTkLabel(win, text="Rincian Semester",
            font=F_SUBJUDUL, text_color=C["teks"]
        ).pack(padx=24, pady=(4, 6), anchor="w")

        scroll = ctk.CTkScrollableFrame(win, fg_color="transparent")
        scroll.pack(fill="both", expand=True, padx=24, pady=(0, 20))

        for smt_key in sorted(mhs["semester"].keys(), key=int):
            data = mhs["semester"][smt_key]
            ips  = db.hitung_ips(data)

            smt_hdr = ctk.CTkFrame(scroll, fg_color=C["abu_card"], corner_radius=8)
            smt_hdr.pack(fill="x", pady=(8, 2))
            ctk.CTkLabel(smt_hdr, text=f"Semester {smt_key}",
                font=("Segoe UI", 11, "bold"), text_color=C["oranye"]
            ).pack(side="left", padx=14, pady=8)
            ctk.CTkLabel(smt_hdr, text=f"IPS: {ips:.2f}",
                font=("Segoe UI", 11, "bold"), text_color=C["hijau"]
            ).pack(side="right", padx=14)

            for mk in data:
                row = ctk.CTkFrame(scroll, fg_color=C["putih"],
                    border_width=1, border_color=C["abu_border"], corner_radius=6)
                row.pack(fill="x", pady=1)
                ctk.CTkLabel(row, text=mk["nama"],
                    font=F_NORMAL, text_color=C["teks"]
                ).pack(side="left", padx=14, pady=6)
                ctk.CTkLabel(row, text=f"SKS {mk['sks']}",
                    font=F_KECIL, text_color=C["teks_sub"]
                ).pack(side="right", padx=8)
                ctk.CTkLabel(row, text=f"{mk['nilai']:.0f}  /  {mk['grade']}",
                    font=("Segoe UI", 10, "bold"), text_color=C["oranye"]
                ).pack(side="right", padx=10)


# ============================================================
# HALAMAN INPUT NILAI
# ============================================================

class HalamanNilai(HalamanBase):
    """
    Halaman Input Nilai — desain sesuai mockup:
    - Header dengan info IPK & semester terisi
    - Card selector (mahasiswa, dropdown, semester)
    - Tabel nilai per matkul dengan kolom No / Mata Kuliah / SKS / Predikat / Nilai
    - Footer: total SKS + rata-rata semester + tombol Batal & Simpan
    """

    # ── Icon emoji per kategori matkul (urutan sesuai KURIKULUM) ──────────
    _ICONS = ["📖", "🏛️", "💬", "📐", "🖥️", "⚗️", "📊", "🔬",
              "💡", "📡", "🔧", "🗃️", "🌐", "✏️", "📚", "🎯"]

    def __init__(self, parent, on_selesai):
        super().__init__(parent)
        self._on_selesai = on_selesai
        self._nim_aktif  = None
        self._entries    = []
        self.configure(fg_color=C["abu_bg"])
        self._build()

    # ─────────────────────────────────────────────────────────
    # BUILD
    # ─────────────────────────────────────────────────────────

    def _build(self):
        # ── Top header bar ────────────────────────────────────
        self._build_topbar()

        # ── Scrollable container untuk selector + form ────────
        self._scroll_container = ctk.CTkScrollableFrame(
            self,
            fg_color="transparent",
            corner_radius=0
        )
        self._scroll_container.pack(fill="both", expand=True, padx=0, pady=(0, 16))

        # ── Selector card ─────────────────────────────────────
        self._build_selector()

        # ── Form card (tabel nilai) ───────────────────────────
        self._form_outer = ctk.CTkFrame(
            self._scroll_container,
            fg_color=C["putih"],
            corner_radius=14,
            border_width=1,
            border_color="#E8E8E8"
        )
        self._form_outer.pack(fill="both", expand=True, padx=24, pady=(0, 0))

        self._tampil_placeholder()
        self._update_dropdown()

    # ─────────────────────────────────────────────────────────
    # TOP BAR
    # ─────────────────────────────────────────────────────────

    def _build_topbar(self):
        bar = ctk.CTkFrame(self, fg_color="transparent")
        bar.pack(fill="x", padx=24, pady=(18, 10))

        # Ikon + judul
        icon_box = ctk.CTkFrame(bar, fg_color=C["oranye"],
                                corner_radius=10, width=40, height=40)
        icon_box.pack(side="left")
        icon_box.pack_propagate(False)
        ctk.CTkLabel(icon_box, text="📋", font=("Segoe UI Emoji", 18),
                     fg_color="transparent").place(relx=0.5, rely=0.5, anchor="center")

        titl = ctk.CTkFrame(bar, fg_color="transparent")
        titl.pack(side="left", padx=12)
        ctk.CTkLabel(titl, text="Input Nilai",
                     font=("Segoe UI", 20, "bold"), text_color=C["teks"]
                     ).pack(anchor="w")
        ctk.CTkLabel(titl, text="Pilih mahasiswa, semester, lalu isi nilai",
                     font=("Segoe UI", 10), text_color=C["teks_sub"]
                     ).pack(anchor="w")

        # Badge info kanan
        self._badge = ctk.CTkFrame(bar, fg_color="transparent")
        self._badge.pack(side="right")
        self._badge_lbl = ctk.CTkLabel(
            self._badge, text="",
            font=("Segoe UI", 10), text_color=C["teks_sub"]
        )
        self._badge_lbl.pack(side="right")

    # ─────────────────────────────────────────────────────────
    # SELECTOR CARD
    # ─────────────────────────────────────────────────────────

    def _build_selector(self):
        card = ctk.CTkFrame(
            self._scroll_container,
            fg_color=C["putih"],
            corner_radius=14,
            border_width=1,
            border_color="#E8E8E8"
        )
        card.pack(fill="x", padx=24, pady=(0, 12))

        # Accent bar kiri oranye
        accent = ctk.CTkFrame(card, fg_color=C["oranye"],
                              width=4, corner_radius=2)
        accent.pack(side="left", fill="y", padx=(14, 0), pady=14)

        body = ctk.CTkFrame(card, fg_color="transparent")
        body.pack(side="left", fill="x", expand=True, padx=16, pady=14)

        ctk.CTkLabel(body, text="Data Mahasiswa & Semester",
                     font=("Segoe UI", 12, "bold"),
                     text_color=C["teks"]).pack(anchor="w", pady=(0, 12))

        fields = ctk.CTkFrame(body, fg_color="transparent")
        fields.pack(fill="x")

        # ── Kolom Mahasiswa (search) ──────────────────────────
        col_mhs = ctk.CTkFrame(fields, fg_color="transparent")
        col_mhs.pack(side="left", padx=(0, 20))

        ctk.CTkLabel(col_mhs, text="Mahasiswa",
                     font=("Segoe UI", 9), text_color=C["teks_sub"]
                     ).pack(anchor="w", pady=(0, 4))

        search_wrap = ctk.CTkFrame(col_mhs, fg_color="#F5F5F5",
                                   corner_radius=8, border_width=1,
                                   border_color="#E0E0E0")
        search_wrap.pack()
        ctk.CTkLabel(search_wrap, text="🔍", font=("Segoe UI Emoji", 12),
                     fg_color="transparent").pack(side="left", padx=(10, 4))
        self._search = ctk.CTkEntry(
            search_wrap, width=220, height=36,
            corner_radius=0,
            placeholder_text="Ketik NIM atau nama mahasiswa...",
            font=("Segoe UI", 10),
            fg_color="transparent",
            border_width=0,
            text_color=C["teks"]
        )
        self._search.pack(side="left")
        self._search.bind("<KeyRelease>", self._update_dropdown)

        # ── Kolom Dropdown mahasiswa ──────────────────────────
        col_dd = ctk.CTkFrame(fields, fg_color="transparent")
        col_dd.pack(side="left", padx=(0, 20))

        ctk.CTkLabel(col_dd, text=" ", font=("Segoe UI", 9),
                     text_color=C["teks_sub"]).pack(anchor="w", pady=(0, 4))

        self._dd_var  = tk.StringVar()
        self._dd_data = {}
        self._combo   = ttk.Combobox(
            col_dd, textvariable=self._dd_var,
            state="readonly", width=28, font=("Segoe UI", 10)
        )
        self._combo.pack(ipady=6)
        self._combo.bind("<<ComboboxSelected>>", self._pilih_mahasiswa)

        # ── Kolom Semester ────────────────────────────────────
        col_smt = ctk.CTkFrame(fields, fg_color="transparent")
        col_smt.pack(side="left")

        ctk.CTkLabel(col_smt, text="Semester",
                     font=("Segoe UI", 9), text_color=C["teks_sub"]
                     ).pack(anchor="w", pady=(0, 4))

        smt_wrap = ctk.CTkFrame(col_smt, fg_color="#F5F5F5",
                                corner_radius=8, border_width=1,
                                border_color="#E0E0E0")
        smt_wrap.pack()
        ctk.CTkLabel(smt_wrap, text="📅", font=("Segoe UI Emoji", 12),
                     fg_color="transparent").pack(side="left", padx=(10, 4))
        self._smt_var = tk.StringVar(value="1")
        smt_cb = ttk.Combobox(
            smt_wrap, textvariable=self._smt_var,
            values=["1 (Semester 1)", "2 (Semester 2)", "3 (Semester 3)",
                    "4 (Semester 4)", "5 (Semester 5)", "6 (Semester 6)"],
            state="readonly", width=14, font=("Segoe UI", 10)
        )
        smt_cb.pack(side="left", ipady=6, padx=(0, 6))
        smt_cb.bind("<<ComboboxSelected>>", self._on_smt_change)

    def _on_smt_change(self, event=None):
        """Ambil angka saja dari nilai combo semester."""
        raw = self._smt_var.get()
        angka = raw.split()[0]  # "1 (Semester 1)" → "1"
        self._smt_var.set(angka)
        self._load_form()

    # ─────────────────────────────────────────────────────────
    # PLACEHOLDER
    # ─────────────────────────────────────────────────────────

    def _tampil_placeholder(self):
        for w in self._form_outer.winfo_children():
            w.destroy()
        wrap = ctk.CTkFrame(self._form_outer, fg_color="transparent")
        wrap.place(relx=0.5, rely=0.5, anchor="center")
        ctk.CTkLabel(wrap, text="📋", font=("Segoe UI Emoji", 48)).pack()
        ctk.CTkLabel(wrap, text="Pilih mahasiswa dan semester untuk mulai input nilai.",
                     font=("Segoe UI", 12), text_color=C["teks_sub"]).pack(pady=(8, 0))

    # ─────────────────────────────────────────────────────────
    # LOAD FORM TABEL
    # ─────────────────────────────────────────────────────────

    def _load_form(self, event=None):
        if not self._nim_aktif:
            return

        smt    = int(self._smt_var.get())
        matkul = db.KURIKULUM[smt]

        for w in self._form_outer.winfo_children():
            w.destroy()
        self._entries = []

        # ── Sub-header: "Nilai Semester X  [badge SKS]" ───────
        hdr = ctk.CTkFrame(self._form_outer, fg_color="transparent")
        hdr.pack(fill="x", padx=24, pady=(16, 0))

        ctk.CTkLabel(hdr, text=f"Nilai Semester {smt}",
                     font=("Segoe UI", 14, "bold"),
                     text_color=C["teks"]).pack(side="left")

        total_sks = sum(s for _, s in matkul)
        badge_sks = ctk.CTkFrame(hdr, fg_color=C["oranye_muda"],
                                 corner_radius=10)
        badge_sks.pack(side="left", padx=10)
        ctk.CTkLabel(badge_sks, text=f"{total_sks} SKS",
                     font=("Segoe UI", 9, "bold"),
                     text_color=C["oranye"]).pack(padx=10, pady=4)

        # ── Kolom header tabel ────────────────────────────────
        COL = [("No.",        40,  "center"),
               ("Mata Kuliah",300,  "w"),
               ("SKS",        60,  "center"),
               ("Predikat",   100, "center"),
               ("Nilai",      120, "center"),
               ("",           40,  "center")]   # aksi edit

        tbl_hdr = ctk.CTkFrame(self._form_outer,
                               fg_color="#FAFAFA",
                               corner_radius=0, height=38)
        tbl_hdr.pack(fill="x", padx=24, pady=(12, 0))
        tbl_hdr.pack_propagate(False)

        for txt, w, anc in COL:
            ctk.CTkLabel(tbl_hdr, text=txt, width=w,
                         font=("Segoe UI", 10, "bold"),
                         text_color=C["teks_sub"],
                         anchor=anc).pack(side="left",
                                          padx=(4, 0) if txt == "No." else 0)

        ctk.CTkFrame(self._form_outer, height=1,
                     fg_color="#EFEFEF").pack(fill="x", padx=24)

        # ── Scrollable tabel ──────────────────────────────────
        scroll = ctk.CTkScrollableFrame(
            self._form_outer, fg_color="transparent", corner_radius=0
        )
        scroll.pack(fill="both", expand=True, padx=24, pady=0)

        semua    = db.get_semua()
        mhs      = next((m for m in semua if m["nim"] == self._nim_aktif), None)
        existing = mhs["semester"].get(str(smt), []) if mhs else []

        grade_colors = {
            "A":  ("#DCFCE7", "#16A34A"),
            "A-": ("#DCFCE7", "#16A34A"),
            "B+": ("#DBEAFE", "#2563EB"),
            "B":  ("#DBEAFE", "#2563EB"),
            "B-": ("#EDE9FE", "#6D28D9"),
            "C+": ("#FEF9C3", "#B45309"),
            "C":  ("#FEF9C3", "#B45309"),
            "D":  ("#FEE2E2", "#DC2626"),
            "E":  ("#FEE2E2", "#DC2626"),
        }

        self._grade_labels = []

        for i, (nama_mk, sks) in enumerate(matkul):
            row_bg = C["putih"] if i % 2 == 0 else "#FAFAFA"
            row = ctk.CTkFrame(scroll, fg_color=row_bg,
                               corner_radius=0, height=54)
            row.pack(fill="x")
            row.pack_propagate(False)
            ctk.CTkFrame(row, height=1,
                         fg_color="#F0F0F0").pack(fill="x", side="bottom")

            # No
            ctk.CTkLabel(row, text=str(i + 1), width=40,
                         font=("Segoe UI", 11), text_color=C["teks_sub"],
                         anchor="center").pack(side="left", padx=(4, 0))

            # Icon
            icon = self._ICONS[i % len(self._ICONS)]
            icon_box = ctk.CTkFrame(row, fg_color=C["oranye_muda"],
                                    corner_radius=8, width=30, height=30)
            icon_box.pack(side="left", padx=(4, 8))
            icon_box.pack_propagate(False)
            ctk.CTkLabel(icon_box, text=icon, font=("Segoe UI Emoji", 13),
                         fg_color="transparent"
                         ).place(relx=0.5, rely=0.5, anchor="center")

            # Nama matkul
            ctk.CTkLabel(row, text=nama_mk, width=262,
                         font=("Segoe UI", 11), text_color=C["teks"],
                         anchor="w").pack(side="left")

            # SKS
            ctk.CTkLabel(row, text=str(sks), width=60,
                         font=("Segoe UI", 11), text_color=C["teks_sub"],
                         anchor="center").pack(side="left")

            # Predikat badge
            grade_wrap = ctk.CTkFrame(row, fg_color="transparent", width=100)
            grade_wrap.pack(side="left")
            grade_wrap.pack_propagate(False)

            grade_badge = ctk.CTkFrame(grade_wrap, fg_color="#F0F0F0",
                                       corner_radius=8, width=42, height=28)
            grade_badge.place(relx=0.5, rely=0.5, anchor="center")
            grade_badge.pack_propagate(False)
            grade_lbl = ctk.CTkLabel(grade_badge, text="—",
                                     font=("Segoe UI", 10, "bold"),
                                     text_color=C["teks_sub"])
            grade_lbl.place(relx=0.5, rely=0.5, anchor="center")

            # Entry nilai
            e = ctk.CTkEntry(
                row, width=110, height=34,
                corner_radius=8, justify="center",
                font=("Segoe UI", 11),
                border_color="#E0E0E0",
                fg_color=C["putih"],
                placeholder_text="0–100"
            )
            e.pack(side="left", padx=(0, 8))

            if i < len(existing):
                e.insert(0, str(int(existing[i]["nilai"])))

            # Edit icon
            ctk.CTkLabel(row, text="✏️", width=36,
                         font=("Segoe UI Emoji", 12),
                         text_color=C["teks_sub"],
                         cursor="hand2").pack(side="left")

            def _upd(event, el=e, gb=grade_badge, gl=grade_lbl):
                try:
                    g, _ = db.nilai_ke_grade(float(el.get()))
                    bg, fg = grade_colors.get(g, ("#F0F0F0", C["teks_sub"]))
                    gb.configure(fg_color=bg)
                    gl.configure(text=g, text_color=fg)
                except Exception:
                    gb.configure(fg_color="#F0F0F0")
                    gl.configure(text="—", text_color=C["teks_sub"])

            e.bind("<KeyRelease>", _upd)
            _upd(None)
            self._entries.append(e)

        # Tab chain
        for i in range(len(self._entries) - 1):
            nxt = self._entries[i + 1]
            self._entries[i].bind("<Return>", lambda ev, n=nxt: n.focus_set())

        # ── Footer: total SKS + rata-rata + tombol ────────────
        self._build_footer(self._form_outer, total_sks, smt, existing)

        if self._entries:
            self._entries[0].focus_set()

    def _build_footer(self, parent, total_sks, smt, existing):
        foot = ctk.CTkFrame(parent, fg_color="#FAFAFA",
                            corner_radius=0, height=60)
        foot.pack(fill="x", side="bottom")
        foot.pack_propagate(False)
        ctk.CTkFrame(foot, height=1, fg_color="#EFEFEF").pack(fill="x", side="top")

        # Kiri: total SKS
        left = ctk.CTkFrame(foot, fg_color="transparent")
        left.pack(side="left", padx=20, pady=10)

        sks_box = ctk.CTkFrame(left, fg_color=C["oranye_muda"],
                               corner_radius=8, width=32, height=32)
        sks_box.pack(side="left")
        sks_box.pack_propagate(False)
        ctk.CTkLabel(sks_box, text="📅", font=("Segoe UI Emoji", 14),
                     fg_color="transparent").place(relx=0.5, rely=0.5, anchor="center")

        txt = ctk.CTkFrame(left, fg_color="transparent")
        txt.pack(side="left", padx=8)
        ctk.CTkLabel(txt, text="Total", font=("Segoe UI", 9),
                     text_color=C["teks_sub"]).pack(anchor="w")
        ctk.CTkLabel(txt, text=f"{total_sks} SKS",
                     font=("Segoe UI", 12, "bold"),
                     text_color=C["oranye"]).pack(anchor="w")

        # Kanan: rata-rata + badge + tombol
        right = ctk.CTkFrame(foot, fg_color="transparent")
        right.pack(side="right", padx=20)

        # Rata-rata semester (hitung dari existing)
        if existing:
            rata = sum(m["nilai"] for m in existing) / len(existing)
            try:
                g_rata, _ = db.nilai_ke_grade(rata)
            except Exception:
                g_rata = "—"
        else:
            rata  = 0.0
            g_rata = "—"

        rata_col = ctk.CTkFrame(right, fg_color="transparent")
        rata_col.pack(side="left", padx=(0, 20))
        ctk.CTkLabel(rata_col, text="Rata-rata Semester",
                     font=("Segoe UI", 9), text_color=C["teks_sub"]).pack(anchor="e")
        ctk.CTkLabel(rata_col, text=f"{rata:.2f}" if existing else "—",
                     font=("Segoe UI", 16, "bold"),
                     text_color=C["oranye"]).pack(anchor="e")

        # Badge grade rata-rata
        if g_rata != "—":
            gbadge = ctk.CTkFrame(right, fg_color=C["oranye"],
                                  corner_radius=20, width=44, height=44)
            gbadge.pack(side="left", padx=(0, 24))
            gbadge.pack_propagate(False)
            ctk.CTkLabel(gbadge, text=g_rata,
                         font=("Segoe UI", 13, "bold"),
                         text_color="white").place(relx=0.5, rely=0.5, anchor="center")

        # Tombol Batal
        ctk.CTkButton(
            right, text="✕  Batal", width=110, height=40,
            corner_radius=10,
            fg_color="#FEE2E2", hover_color="#FECACA",
            text_color="#DC2626", font=("Segoe UI", 11, "bold"),
            border_width=0,
            command=self._tampil_placeholder
        ).pack(side="left", padx=(0, 10))

        # Tombol Simpan
        ctk.CTkButton(
            right, text="💾  Simpan Nilai", width=160, height=40,
            corner_radius=10,
            fg_color=C["oranye"], hover_color=C["oranye_gelap"],
            text_color="white", font=("Segoe UI", 11, "bold"),
            command=self._simpan
        ).pack(side="left")

    # ─────────────────────────────────────────────────────────
    # DROPDOWN & PILIH MAHASISWA
    # ─────────────────────────────────────────────────────────

    def _update_dropdown(self, event=None):
        keyword = self._search.get()
        rows    = db.cari(keyword) if keyword else db.get_semua()
        opts    = [f"{m['nim']}  —  {m['nama']}" for m in rows]
        nims    = {f"{m['nim']}  —  {m['nama']}": m["nim"] for m in rows}
        self._dd_data         = nims
        self._combo["values"] = opts
        if opts and not self._combo.get():
            self._combo.set(opts[0])
            self._pilih_mahasiswa()

    def _pilih_mahasiswa(self, event=None):
        label = self._dd_var.get()
        nim   = self._dd_data.get(label)
        if not nim:
            return
        self._nim_aktif = nim
        semua = db.get_semua()
        mhs   = next((m for m in semua if m["nim"] == nim), None)
        if mhs:
            ipk    = db.ipk_mahasiswa(mhs)
            terisi = db.semester_terisi(mhs)
            self._badge_lbl.configure(
                text=f"⏱  IPK saat ini: {ipk:.2f}  |  Semester sudah terisi: {terisi}"
            )
        self._load_form()

    # ─────────────────────────────────────────────────────────
    # SIMPAN
    # ─────────────────────────────────────────────────────────

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

    # ─────────────────────────────────────────────────────────
    # SET NIM (dipanggil dari HalamanMahasiswa)
    # ─────────────────────────────────────────────────────────

    def set_nim(self, nim: str):
        semua = db.get_semua()
        mhs   = next((m for m in semua if m["nim"] == nim), None)
        if not mhs:
            return
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
        self._badge_lbl.configure(
            text=f"⏱  IPK saat ini: {ipk:.2f}  |  Semester sudah terisi: {terisi}"
        )
        self._load_form()


# ============================================================
# HALAMAN STATISTIK — dengan grafik canvas
# ============================================================

class HalamanStatistik(HalamanBase):
    """
    Dashboard statistik — layout mirip screenshot:
    Row 1 : Bar IPK (kiri lebar) + Pie Predikat (kanan, dengan footer stat)
    Row 2 : Line IPS per Semester (full width)
    Row 3 : Column Grade (kiri lebar) + Ringkasan Statistik (kanan)
    Toolbar filter semester + tombol Refresh ada di header bar.
    """

    def __init__(self, parent):
        super().__init__(parent)
        self._build()

    # ------------------------------------------------------------------
    # BUILD
    # ------------------------------------------------------------------
    def _build(self):
        # ── Header bar (judul + filter + refresh) ──────────────────────
        topbar = ctk.CTkFrame(self, fg_color=C["putih"], corner_radius=0, height=64)
        topbar.pack(fill="x")
        topbar.pack_propagate(False)
        ctk.CTkFrame(self, height=1, fg_color=C["abu_border"]).pack(fill="x")

        # Judul kiri
        titl = ctk.CTkFrame(topbar, fg_color="transparent")
        titl.pack(side="left", padx=24, pady=10)
        ctk.CTkLabel(titl, text="Statistik Kelas",
                     font=("Segoe UI", 18, "bold"),
                     text_color=C["teks"]).pack(anchor="w")
        ctk.CTkLabel(titl, text="Visualisasi data akademik seluruh mahasiswa",
                     font=F_KECIL, text_color=C["teks_sub"]).pack(anchor="w")

        # Filter + refresh kanan
        ctrl = ctk.CTkFrame(topbar, fg_color="transparent")
        ctrl.pack(side="right", padx=24)
        ctk.CTkLabel(ctrl, text="Filter Semester:",
                     font=F_KECIL, text_color=C["teks_sub"]).pack(side="left", padx=(0, 6))
        self._filter_smt = tk.StringVar(value="Semua Semester")
        smt_opts = ["Semua Semester", "1", "2", "3", "4", "5", "6"]
        smt_cb = ttk.Combobox(ctrl, textvariable=self._filter_smt,
                               values=smt_opts, state="readonly", width=14,
                               font=("Segoe UI", 10))
        smt_cb.pack(side="left", padx=(0, 10))
        smt_cb.bind("<<ComboboxSelected>>", lambda *_: self.refresh())

        # Tombol Refresh oranye
        ctk.CTkButton(
            ctrl, text="↻  Refresh", command=self.refresh,
            width=110, height=36,
            font=("Segoe UI", 11, "bold"),
            fg_color=C["oranye"], hover_color=C["oranye_gelap"],
            corner_radius=8,
        ).pack(side="left")

        # ── Scrollable content ──────────────────────────────────────────
        scroll = ctk.CTkScrollableFrame(self, fg_color=C["abu_bg"])
        scroll.pack(fill="both", expand=True)

        pad = {"padx": 20, "pady": (0, 14)}

        # ── ROW 1: Bar IPK (weight 3) + Pie Predikat (weight 2) ────────
        row1 = ctk.CTkFrame(scroll, fg_color="transparent")
        row1.pack(fill="x", padx=20, pady=(16, 0))
        row1.columnconfigure(0, weight=3)
        row1.columnconfigure(1, weight=2)

        # Card IPK
        card_ipk = self._card(row1)
        card_ipk.grid(row=0, column=0, padx=(0, 8), sticky="nsew", pady=(0, 14))
        self._card_header(card_ipk, "📊", "Distribusi Rentang IPK",
                          "Jumlah mahasiswa per rentang IPK")
        self._canvas_ipk = tk.Canvas(card_ipk, height=210,
                                     bg=C["putih"], highlightthickness=0)
        self._canvas_ipk.pack(fill="x", padx=16, pady=(0, 4))
        # Footer mini stat di bawah bar
        self._ipk_footer = ctk.CTkFrame(card_ipk, fg_color="transparent")
        self._ipk_footer.pack(fill="x", padx=16, pady=(0, 14))

        # Card Predikat
        card_pred = self._card(row1)
        card_pred.grid(row=0, column=1, padx=(8, 0), sticky="nsew", pady=(0, 14))
        self._card_header(card_pred, "🥧", "Sebaran Predikat",
                          "Sebaran predikat mahasiswa")
        self._canvas_pred = tk.Canvas(card_pred, height=210,
                                      bg=C["putih"], highlightthickness=0)
        self._canvas_pred.pack(fill="x", padx=16, pady=(0, 4))
        # Footer total mahasiswa di bawah pie
        self._pred_footer = ctk.CTkFrame(card_pred, fg_color="transparent")
        self._pred_footer.pack(fill="x", padx=16, pady=(0, 14))

        # ── ROW 2: Line IPS per semester (full width) ───────────────────
        card_ips = self._card(scroll)
        card_ips.pack(fill="x", **pad)
        self._card_header(card_ips, "📈", "Rata-rata IPS per Semester",
                          "Tren rata-rata IPS per semester")
        self._canvas_ips = tk.Canvas(card_ips, height=190,
                                     bg=C["putih"], highlightthickness=0)
        self._canvas_ips.pack(fill="x", padx=16, pady=(0, 14))

        # ── ROW 3: Column Grade (weight 3) + Ringkasan (weight 2) ──────
        row3 = ctk.CTkFrame(scroll, fg_color="transparent")
        row3.pack(fill="x", padx=20, pady=(0, 20))
        row3.columnconfigure(0, weight=3)
        row3.columnconfigure(1, weight=2)

        card_grade = self._card(row3)
        card_grade.grid(row=0, column=0, padx=(0, 8), sticky="nsew")
        self._card_header(card_grade, "🏆", "Distribusi Grade (Semua Mata Kuliah)",
                          "Distribusi grade seluruh mata kuliah")
        self._canvas_grade = tk.Canvas(card_grade, height=200,
                                       bg=C["putih"], highlightthickness=0)
        self._canvas_grade.pack(fill="x", padx=16, pady=(0, 14))

        # Card Ringkasan Statistik
        card_sum = self._card(row3)
        card_sum.grid(row=0, column=1, padx=(8, 0), sticky="nsew")
        self._card_header(card_sum, "📋", "Ringkasan Statistik", "")
        self._sum_frame = ctk.CTkFrame(card_sum, fg_color="transparent")
        self._sum_frame.pack(fill="both", expand=True, padx=16, pady=(0, 14))

        self.refresh()

    # ------------------------------------------------------------------
    # Helper: Card header dengan ikon
    # ------------------------------------------------------------------
    def _card_header(self, card, icon: str, title: str, subtitle: str):
        hdr = ctk.CTkFrame(card, fg_color="transparent")
        hdr.pack(fill="x", padx=16, pady=(14, 6))
        # ikon dalam kotak oranye muda
        icon_box = ctk.CTkFrame(hdr, fg_color=C["oranye_muda"],
                                corner_radius=8, width=34, height=34)
        icon_box.pack(side="left", padx=(0, 10))
        icon_box.pack_propagate(False)
        ctk.CTkLabel(icon_box, text=icon,
                     font=("Segoe UI Emoji", 15)).place(relx=0.5, rely=0.5, anchor="center")
        txt = ctk.CTkFrame(hdr, fg_color="transparent")
        txt.pack(side="left")
        ctk.CTkLabel(txt, text=title, font=("Segoe UI", 12, "bold"),
                     text_color=C["teks"]).pack(anchor="w")
        if subtitle:
            ctk.CTkLabel(txt, text=subtitle, font=("Segoe UI", 8),
                         text_color=C["teks_sub"]).pack(anchor="w")

    # ------------------------------------------------------------------
    # DATA
    # ------------------------------------------------------------------
    def _get_data(self):
        semua = db.get_semua()
        fs = self._filter_smt.get()
        filter_smt = "Semua" if fs == "Semua Semester" else fs

        ipk_list = []
        for m in semua:
            if not m["semester"]:
                continue
            if filter_smt != "Semua" and filter_smt not in m["semester"]:
                continue
            ipk_list.append(db.ipk_mahasiswa(m))

        rentang = [
            ("0.00-1.99", 0), ("2.00-2.49", 0), ("2.50-2.99", 0),
            ("3.00-3.49", 0), ("3.50-3.74", 0), ("3.75-4.00", 0),
        ]
        for ipk in ipk_list:
            if   ipk < 2.0:  rentang[0] = (rentang[0][0], rentang[0][1] + 1)
            elif ipk < 2.5:  rentang[1] = (rentang[1][0], rentang[1][1] + 1)
            elif ipk < 3.0:  rentang[2] = (rentang[2][0], rentang[2][1] + 1)
            elif ipk < 3.5:  rentang[3] = (rentang[3][0], rentang[3][1] + 1)
            elif ipk < 3.75: rentang[4] = (rentang[4][0], rentang[4][1] + 1)
            else:            rentang[5] = (rentang[5][0], rentang[5][1] + 1)

        pred_dist = {"Cumlaude": 0, "Sangat Baik": 0, "Baik": 0,
                     "Cukup": 0, "Perlu Perbaikan": 0}
        for ipk in ipk_list:
            p = db.predikat(ipk)
            pred_dist[p] = pred_dist.get(p, 0) + 1

        ips_per_smt = {}
        grade_dist  = {}
        for m in semua:
            for smt_key, mk_list in m["semester"].items():
                if filter_smt != "Semua" and smt_key != filter_smt:
                    continue
                ips = db.hitung_ips(mk_list)
                ips_per_smt.setdefault(smt_key, []).append(ips)
                for mk in mk_list:
                    g = mk.get("grade", "E")
                    grade_dist[g] = grade_dist.get(g, 0) + 1

        avg_ips = {smt: round(sum(v) / len(v), 2) for smt, v in ips_per_smt.items()}

        return {
            "ipk_list":   ipk_list,
            "rentang":    rentang,
            "pred_dist":  pred_dist,
            "avg_ips":    avg_ips,
            "grade_dist": grade_dist,
            "total":      len(semua),
        }

    # ------------------------------------------------------------------
    # REFRESH
    # ------------------------------------------------------------------
    def refresh(self, *_):
        data = self._get_data()
        self.update_idletasks()

        ipk_list = data["ipk_list"]
        total    = data["total"]

        # ── 1. Bar chart IPK ───────────────────────────────────────────
        colors_ipk = [C["merah"], C["kuning"], "#F59E0B",
                      C["oranye"], C["hijau"], "#059669"]
        Chart.bar(self._canvas_ipk, data["rentang"],
                  colors=colors_ipk, title="")

        # Footer di bawah bar: Total Mahasiswa | Rata-rata IPK
        for w in self._ipk_footer.winfo_children():
            w.destroy()
        rata_ipk = f"{sum(ipk_list)/len(ipk_list):.2f}" if ipk_list else "0.00"
        self._ipk_footer.columnconfigure((0, 1), weight=1)
        for col, (lbl, val, ico, color) in enumerate([
            ("Total Mahasiswa", str(total), "👥", C["oranye"]),
            ("Rata-rata IPK",   rata_ipk,  "⭐", C["oranye"]),
        ]):
            box = ctk.CTkFrame(self._ipk_footer, fg_color=C["abu_card"],
                               corner_radius=8)
            box.grid(row=0, column=col,
                     sticky="nsew", padx=4)
            inner = ctk.CTkFrame(box, fg_color="transparent")
            inner.pack(fill="x", padx=10, pady=8)
            ctk.CTkLabel(inner, text=ico + "  " + lbl,
                         font=("Segoe UI", 9), text_color=C["teks_sub"]).pack(anchor="w")
            ctk.CTkLabel(inner, text=val,
                         font=("Segoe UI", 18, "bold"),
                         text_color=color).pack(anchor="w")

        # ── 2. Pie chart predikat ──────────────────────────────────────
        pred_data   = [(k, v) for k, v in data["pred_dist"].items() if v > 0]
        pred_colors = [C["ungu"], C["hijau"], C["oranye"], C["kuning"], C["merah"]]
        Chart.pie(self._canvas_pred, pred_data, colors=pred_colors, title="")

        # Footer di bawah pie: Total Mahasiswa
        for w in self._pred_footer.winfo_children():
            w.destroy()
        box_p = ctk.CTkFrame(self._pred_footer, fg_color=C["abu_card"],
                             corner_radius=8)
        box_p.pack(fill="x")
        pi = ctk.CTkFrame(box_p, fg_color="transparent")
        pi.pack(fill="x", padx=10, pady=8)
        ctk.CTkLabel(pi, text="🎓  Total Mahasiswa",
                     font=("Segoe UI", 9), text_color=C["teks_sub"]).pack(anchor="w")
        ctk.CTkLabel(pi, text=str(total),
                     font=("Segoe UI", 18, "bold"),
                     text_color=C["oranye"]).pack(anchor="w")

        # ── 3. Line chart IPS ─────────────────────────────────────────
        smts      = sorted(data["avg_ips"].keys(), key=int)
        ips_vals  = [data["avg_ips"][s] for s in smts]
        smt_lbls  = [f"Smt {s}" for s in smts]
        if len(ips_vals) >= 2:
            Chart.line(self._canvas_ips,
                       datasets=[("Rata-rata IPS", C["oranye"], ips_vals)],
                       labels=smt_lbls, title="")
        else:
            self._canvas_ips.delete("all")
            self._canvas_ips.update_idletasks()
            cw = self._canvas_ips.winfo_width() or 500
            self._canvas_ips.create_text(
                cw // 2, 95,
                text="Butuh minimal 2 semester untuk menampilkan tren.",
                fill=C["teks_sub"], font=F_KECIL
            )

        # ── 4. Column chart grade ─────────────────────────────────────
        grade_order  = ["A", "A-", "B+", "B", "B-", "C+", "C", "D", "E"]
        grade_data   = [(g, data["grade_dist"].get(g, 0)) for g in grade_order
                        if data["grade_dist"].get(g, 0) > 0]
        grade_colors = ["#059669","#16A34A","#22C55E","#4ADE80","#86EFAC",
                        "#F59E0B","#D97706","#EA580C","#DC2626"]
        Chart.column(self._canvas_grade, grade_data,
                     colors=grade_colors[:len(grade_data)], title="")

        # ── 5. Ringkasan Statistik (card kanan bawah) ─────────────────
        for w in self._sum_frame.winfo_children():
            w.destroy()

        stats = [
            ("Mahasiswa\ndengan nilai",    str(len(ipk_list)),   "👥", C["oranye"]),
            ("Rata-rata IPK",              rata_ipk,             "📈", C["oranye"]),
            ("IPK tertinggi",
             f"{max(ipk_list):.2f}" if ipk_list else "0.00",    "⬆️", C["hijau"]),
            ("IPK terendah",
             f"{min(ipk_list):.2f}" if ipk_list else "0.00",    "⬇️", C["merah"]),
            ("Total mahasiswa\nterdaftar", str(total),           "🏫", C["teks"]),
        ]

        self._sum_frame.columnconfigure((0, 1), weight=1, uniform="s")
        for idx, (label, val, ico, color) in enumerate(stats):
            row_g = idx // 2
            col_g = idx % 2
            box = ctk.CTkFrame(self._sum_frame, fg_color=C["abu_card"],
                               corner_radius=10)
            box.grid(row=row_g, column=col_g, padx=4, pady=4, sticky="nsew")
            inner_b = ctk.CTkFrame(box, fg_color="transparent")
            inner_b.pack(fill="x", padx=12, pady=10)
            ctk.CTkLabel(inner_b, text=ico + "  " + label,
                         font=("Segoe UI", 8), text_color=C["teks_sub"],
                         justify="left", anchor="w").pack(anchor="w")
            ctk.CTkLabel(inner_b, text=val,
                         font=("Segoe UI", 22, "bold"),
                         text_color=color).pack(anchor="w")


# ============================================================
# HALAMAN RIWAYAT
# ============================================================

class HalamanRiwayat(HalamanBase):

    def __init__(self, parent):
        super().__init__(parent)
        self._header("Riwayat Aktivitas", "20 operasi terakhir")
        _style_tree()
        self._build()

    def _build(self):
        toolbar = ctk.CTkFrame(self, fg_color="transparent")
        toolbar.pack(fill="x", padx=28, pady=12)
        _btn(toolbar, "Refresh", self.refresh, width=100).pack(side="right")

        card = ctk.CTkFrame(self, fg_color=C["putih"],
            corner_radius=12, border_width=1, border_color=C["abu_border"])
        card.pack(fill="both", expand=True, padx=28, pady=(0, 24))

        cols = ("waktu", "aksi", "detail")
        self._tree = ttk.Treeview(card, columns=cols, show="headings",
            style="App.Treeview")
        self._tree.heading("waktu",  text="Waktu",  anchor="center")
        self._tree.heading("aksi",   text="Aksi",   anchor="center")
        self._tree.heading("detail", text="Detail", anchor="w")
        self._tree.column("waktu",  width=150, anchor="center")
        self._tree.column("aksi",   width=90,  anchor="center")
        self._tree.column("detail", width=450, anchor="w")

        self._tree.tag_configure("TAMBAH", foreground=C["hijau"])
        self._tree.tag_configure("HAPUS",  foreground=C["merah"])
        self._tree.tag_configure("NILAI",  foreground=C["oranye"])
        self._tree.tag_configure("EDIT",   foreground=C["kuning"])

        vsb = ttk.Scrollbar(card, orient="vertical", command=self._tree.yview)
        self._tree.configure(yscrollcommand=vsb.set)
        self._tree.pack(side="left", fill="both", expand=True, pady=1, padx=(1, 0))
        vsb.pack(side="right", fill="y")

        self.refresh()

    def refresh(self):
        for i in self._tree.get_children():
            self._tree.delete(i)
        for h in db.get_riwayat():
            self._tree.insert("", "end",
                values=(h["waktu"], h["aksi"], h["detail"]),
                tags=(h["aksi"],))


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
# HALAMAN KALENDER AKADEMIK
# ============================================================

class HalamanJadwalAkademik(ctk.CTkFrame):
    """
    Halaman Kalender Akademik — menampilkan jadwal kegiatan akademik
    per semester dengan tampilan accordion / collapsible.
    """

    # ----------------------------------------------------------------
    # Data Kalender Akademik 2025/2026
    # ----------------------------------------------------------------
    DATA_KALENDER = {
        "Semester Ganjil": [
            {
                "icon": "👥",
                "judul": "PENERIMAAN MAHASISWA",
                "items": [
                    {
                        "nomor": 1,
                        "nama": "Seleksi Nasional Berdasarkan Prestasi (SNBP)",
                        "sub": [
                            ("Pengisian PDSS",                           "06 Des 2024 – 03 Mar 2025"),
                            ("Pendaftaran",                               "04 – 18 Feb 2025"),
                            ("Pengumuman Kelulusan",                      "18 Mar 2025"),
                        ]
                    },
                    {
                        "nomor": 2,
                        "nama": "Seleksi Nasional Berdasarkan Test (SNBT)",
                        "sub": [
                            ("Pendaftaran",                               "11 – 27 Mar 2025"),
                            ("Pelaksanaan Tes UTBK",                      "23 Apr – 03 Mei 2025"),
                            ("Pengumuman Kelulusan",                      "28 Mei 2025"),
                        ]
                    },
                    {
                        "nomor": 3,
                        "nama": "Seleksi Mandiri Berdasarkan Nilai UTBK SNBT",
                        "sub": [
                            ("Pendaftaran",                               "01 Mei – 29 Jun 2025"),
                        ]
                    },
                    {
                        "nomor": 4,
                        "nama": "Seleksi Mandiri Jalur Reguler (SM) dan Prestasi Istimewa (PI)",
                        "sub": [
                            ("Pendaftaran",                               "01 Mei – 29 Jun 2025"),
                            ("Pelaksanaan UTBK",                          "01 – 03 Jul 2025"),
                            ("Pelaksanaan Ujian Keterampilan dan/atau Wawancara", "04 – 07 Jul 2025"),
                            ("Pengumuman Kelulusan",                      "18 Jul 2025"),
                        ]
                    },
                    {
                        "nomor": 5,
                        "nama": "Pascasarjana (S2 dan S3)",
                        "sub": [
                            ("Pendaftaran",                               "08 Apr – 05 Mei 2025"),
                            ("Pelaksanaan Tes",                           "15 – 16 Mei 2025"),
                            ("Pengumuman",                                "21 Mei 2025"),
                        ]
                    },
                ]
            },
            {
                "icon": "📋",
                "judul": "REGISTRASI",
                "items": [
                    {
                        "nomor": 1,
                        "nama": "Pembayaran UKT/Biaya Pendidikan",
                        "sub": [
                            ("Mahasiswa Baru Jalur SNBP",                 "23 Apr – 30 Mei 2025"),
                            ("Mahasiswa Lama (D4, S1, S2, dan S3)",       "22 Jun – 31 Jul 2025"),
                            ("Mahasiswa Baru S2 dan S3",                  "18 – 21 Agu 2025"),
                            ("Mahasiswa Baru Jalur SNBT",                 "23 Jun – 08 Jul 2025"),
                            ("Mahasiswa Baru Jalur Seleksi Mandiri (SM dan PI)", "10 – 20 Agu 2025"),
                        ]
                    },
                    {
                        "nomor": 2,
                        "nama": "Verifikasi Data Mahasiswa Baru",
                        "sub": [
                            ("Jalur SNBP",                                "30 Mei – 02 Jun 2025"),
                            ("Jalur SNBT dan Pascasarjana (S2 dan S3)",   "14 – 18 Agu 2025"),
                            ("Jalur SMM PTN Barat",                       "22 – 24 Agu 2025"),
                            ("Jalur Seleksi Mandiri (SM dan PI)",         "25 – 27 Agu 2025"),
                        ]
                    },
                    {
                        "nomor": 3,
                        "nama": "Kuliah Umum dan Pra Perkuliahan",
                        "sub": [
                            ("Pelaksanaan",                               "25 – 29 Agu 2025"),
                        ]
                    },
                    {
                        "nomor": 4,
                        "nama": "Pengisian Isian Rencana IRS dan Perwalian",
                        "sub": [
                            ("Mahasiswa Baru",                            "25 – 29 Agu 2025"),
                            ("Mahasiswa Lama",                            "26 – 29 Agu 2025"),
                        ]
                    },
                    {
                        "nomor": 5,
                        "nama": "Perubahan Rencana Studi",
                        "sub": [
                            ("Pelaksanaan",                               "01 – 05 Sep 2025"),
                        ]
                    },
                ]
            },
            {
                "icon": "🎓",
                "judul": "PERKULIAHAN",
                "items": [
                    {
                        "nomor": 1,
                        "nama": "Perkuliahan Semester Ganjil",
                        "sub": [
                            ("Mulai Perkuliahan",                         "01 Sep 2025"),
                            ("Akhir Perkuliahan",                         "31 Jan 2026"),
                        ]
                    },
                ]
            },
            {
                "icon": "📝",
                "judul": "UJIAN DAN PEMASUKAN NILAI",
                "items": [
                    {
                        "nomor": 1,
                        "nama": "Ujian Tengah Semester (UTS)",
                        "sub": [
                            ("Pelaksanaan",                               "20 Okt – 01 Nov 2025"),
                        ]
                    },
                    {
                        "nomor": 2,
                        "nama": "Ujian Akhir Semester",
                        "sub": [
                            ("Pelaksanaan",                               "19 Jan – 31 Jan 2026"),
                        ]
                    },
                    {
                        "nomor": 3,
                        "nama": "Pemeriksaan dan Pemasukan Nilai UAS",
                        "sub": [
                            ("Pelaksanaan",                               "01 – 14 Feb 2026"),
                        ]
                    },
                ]
            },
            {
                "icon": "🌿",
                "judul": "CUTI AKADEMIK",
                "items": [
                    {
                        "nomor": 1,
                        "nama": "Pengajuan",
                        "sub": [
                            ("Batas Akhir Pengajuan",                     "05 Sep 2025"),
                        ]
                    },
                    {
                        "nomor": 2,
                        "nama": "Pengaktifan Kembali",
                        "sub": [
                            ("Batas Akhir Pengajuan",                     "29 Agu 2025"),
                        ]
                    },
                ]
            },
        ],
        "Semester Genap": [
            {
                "icon": "🎓",
                "judul": "PERKULIAHAN",
                "items": [
                    {
                        "nomor": 1,
                        "nama": "Perkuliahan Semester Genap",
                        "sub": [
                            ("Mulai Perkuliahan",                         "16 Feb 2026"),
                            ("Akhir Perkuliahan",                         "30 Jun 2026"),
                        ]
                    },
                ]
            },
            {
                "icon": "📝",
                "judul": "UJIAN DAN PEMASUKAN NILAI",
                "items": [
                    {
                        "nomor": 1,
                        "nama": "Ujian Tengah Semester (UTS)",
                        "sub": [
                            ("Pelaksanaan",                               "06 – 17 Apr 2026"),
                        ]
                    },
                    {
                        "nomor": 2,
                        "nama": "Ujian Akhir Semester",
                        "sub": [
                            ("Pelaksanaan",                               "15 – 30 Jun 2026"),
                        ]
                    },
                ]
            },
        ],
        "Semester Padat": [
            {
                "icon": "🎓",
                "judul": "PERKULIAHAN",
                "items": [
                    {
                        "nomor": 1,
                        "nama": "Perkuliahan Semester Padat",
                        "sub": [
                            ("Mulai Perkuliahan",                         "13 Jul 2026"),
                            ("Akhir Perkuliahan",                         "22 Agu 2026"),
                        ]
                    },
                ]
            },
        ],
        "Wisuda": [
            {
                "icon": "🏅",
                "judul": "WISUDA",
                "items": [
                    {
                        "nomor": 1,
                        "nama": "Wisuda Periode I",
                        "sub": [
                            ("Pendaftaran Wisuda",                        "20 Okt – 14 Nov 2025"),
                            ("Pelaksanaan Wisuda",                        "20 Nov 2025"),
                        ]
                    },
                    {
                        "nomor": 2,
                        "nama": "Wisuda Periode II",
                        "sub": [
                            ("Pendaftaran Wisuda",                        "23 Feb – 20 Mar 2026"),
                            ("Pelaksanaan Wisuda",                        "26 Mar 2026"),
                        ]
                    },
                    {
                        "nomor": 3,
                        "nama": "Wisuda Periode III",
                        "sub": [
                            ("Pendaftaran Wisuda",                        "15 Jun – 10 Jul 2026"),
                            ("Pelaksanaan Wisuda",                        "16 Jul 2026"),
                        ]
                    },
                ]
            },
        ],
    }

    def __init__(self, parent):
        super().__init__(parent, fg_color="transparent", corner_radius=0)
        self._semester_aktif = "Semester Ganjil"
        self._tab_btns = {}
        self._collapse_state = {}   # key -> bool (True = collapsed)
        self._build()

    def _build(self):
        # ── Header ──────────────────────────────────────────────────
        hdr = ctk.CTkFrame(self, fg_color="transparent")
        hdr.pack(fill="x", pady=(0, 16))

        icon_frame = ctk.CTkFrame(hdr, width=48, height=48,
                                  corner_radius=12,
                                  fg_color=C["oranye_muda"])
        icon_frame.pack(side="left")
        icon_frame.pack_propagate(False)
        ctk.CTkLabel(icon_frame, text="📅",
                     font=("Segoe UI Emoji", 22)).place(relx=.5, rely=.5, anchor="center")

        teks_hdr = ctk.CTkFrame(hdr, fg_color="transparent")
        teks_hdr.pack(side="left", padx=14)
        ctk.CTkLabel(teks_hdr, text="Kalender Akademik",
                     font=F_JUDUL, text_color=C["teks"]).pack(anchor="w")
        ctk.CTkLabel(teks_hdr, text="Informasi jadwal kegiatan akademik Tahun Akademik 2025/2026",
                     font=F_NORMAL, text_color=C["teks_sub"]).pack(anchor="w")

        # ── Tahun akademik label ─────────────────────────────────────
        ta_frame = ctk.CTkFrame(self, fg_color=C["putih"], corner_radius=12)
        ta_frame.pack(fill="x", pady=(0, 12))
        ctk.CTkLabel(ta_frame, text="Tahun Akademik 2025/2026",
                     font=F_SUBJUDUL, text_color=C["teks"]).pack(anchor="w", padx=20, pady=14)

        # ── Tab semester ─────────────────────────────────────────────
        tab_bar = ctk.CTkFrame(self, fg_color=C["putih"], corner_radius=12)
        tab_bar.pack(fill="x", pady=(0, 16))

        tabs_inner = ctk.CTkFrame(tab_bar, fg_color="transparent")
        tabs_inner.pack(side="left", padx=12, pady=8)

        for sem in self.DATA_KALENDER.keys():
            btn = ctk.CTkButton(
                tabs_inner,
                text=sem,
                width=140,
                height=36,
                corner_radius=8,
                fg_color="transparent",
                hover_color=C["oranye_muda"],
                text_color=C["teks_sub"],
                font=("Segoe UI", 12),
                command=lambda s=sem: self._ganti_tab(s)
            )
            btn.pack(side="left", padx=4)
            self._tab_btns[sem] = btn

        # ── Scrollable content area ──────────────────────────────────
        self._scroll = ctk.CTkScrollableFrame(
            self,
            fg_color="transparent",
            corner_radius=0
        )
        self._scroll.pack(fill="both", expand=True)

        # Render tab aktif
        self._render_tab(self._semester_aktif)
        self._set_tab_aktif(self._semester_aktif)

    def _ganti_tab(self, semester: str):
        if semester == self._semester_aktif:
            return
        self._semester_aktif = semester
        self._set_tab_aktif(semester)
        self._render_tab(semester)

    def _set_tab_aktif(self, semester: str):
        for s, btn in self._tab_btns.items():
            if s == semester:
                btn.configure(
                    fg_color=C["oranye"],
                    hover_color=C["oranye_gelap"],
                    text_color=C["putih"],
                    font=("Segoe UI", 12, "bold")
                )
            else:
                btn.configure(
                    fg_color="transparent",
                    hover_color=C["oranye_muda"],
                    text_color=C["teks_sub"],
                    font=("Segoe UI", 12)
                )

    def _render_tab(self, semester: str):
        # Hapus konten lama
        for w in self._scroll.winfo_children():
            w.destroy()
        self._collapse_state.clear()

        seksi_list = self.DATA_KALENDER.get(semester, [])
        for seksi in seksi_list:
            self._buat_seksi(seksi)

    def _buat_seksi(self, seksi: dict):
        # ── Section header (icon + judul) ────────────────────────────
        sec_frame = ctk.CTkFrame(self._scroll, fg_color=C["putih"],
                                 corner_radius=14)
        sec_frame.pack(fill="x", pady=(0, 16))

        sec_hdr = ctk.CTkFrame(sec_frame, fg_color="transparent")
        sec_hdr.pack(fill="x", padx=18, pady=14)

        icon_box = ctk.CTkFrame(sec_hdr, width=36, height=36,
                                corner_radius=8,
                                fg_color=C["oranye_muda"])
        icon_box.pack(side="left")
        icon_box.pack_propagate(False)
        ctk.CTkLabel(icon_box, text=seksi["icon"],
                     font=("Segoe UI Emoji", 16)).place(relx=.5, rely=.5, anchor="center")

        ctk.CTkLabel(sec_hdr, text=seksi["judul"],
                     font=("Segoe UI", 13, "bold"),
                     text_color=C["teks"]).pack(side="left", padx=12)

        # ── Accordion items ─────────────────────────────────────────
        for item in seksi["items"]:
            self._buat_accordion(sec_frame, item)

    def _buat_accordion(self, parent, item: dict):
        uid = f"{item['nomor']}_{item['nama'][:20]}"
        self._collapse_state[uid] = False  # mulai terbuka

        # ── Card wrapper ─────────────────────────────────────────────
        card = ctk.CTkFrame(parent,
                            fg_color=C["putih"],
                            corner_radius=10,
                            border_width=1,
                            border_color="#F0F0F0")
        card.pack(fill="x", padx=16, pady=(0, 10))

        # ── Header accordion (clickable) ─────────────────────────────
        hdr_frame = ctk.CTkFrame(card, fg_color="transparent")
        hdr_frame.pack(fill="x")

        # Badge nomor
        badge = ctk.CTkFrame(hdr_frame, width=28, height=28,
                             corner_radius=14,
                             fg_color=C["oranye"])
        badge.pack(side="left", padx=(12, 0), pady=12)
        badge.pack_propagate(False)
        ctk.CTkLabel(badge,
                     text=str(item["nomor"]),
                     font=("Segoe UI", 10, "bold"),
                     text_color=C["putih"]).place(relx=.5, rely=.5, anchor="center")

        # Judul item
        lbl_nama = ctk.CTkLabel(
            hdr_frame,
            text=item["nama"],
            font=("Segoe UI", 12, "bold"),
            text_color=C["teks"],
            anchor="w"
        )
        lbl_nama.pack(side="left", padx=10, pady=12, fill="x", expand=True)

        # Toggle button
        lbl_toggle = ctk.CTkLabel(
            hdr_frame,
            text="∧",
            font=("Segoe UI", 14, "bold"),
            text_color=C["teks_sub"]
        )
        lbl_toggle.pack(side="right", padx=14)

        # ── Body sub-items ─────────────────────────────────────────
        body = ctk.CTkFrame(card, fg_color="transparent")
        body.pack(fill="x")

        # Divider
        div = ctk.CTkFrame(body, height=1, fg_color=C["abu_border"])
        div.pack(fill="x", padx=12)

        for nama_sub, tanggal in item["sub"]:
            row = ctk.CTkFrame(body, fg_color="transparent")
            row.pack(fill="x", padx=24, pady=3)

            # Bullet
            ctk.CTkLabel(row, text="●",
                         font=("Segoe UI", 8),
                         text_color=C["oranye"]).pack(side="left")

            ctk.CTkLabel(row, text=nama_sub,
                         font=F_NORMAL,
                         text_color=C["teks"],
                         anchor="w").pack(side="left", padx=8, fill="x", expand=True)

            # Tanggal dengan icon
            tgl_frame = ctk.CTkFrame(row, fg_color=C["oranye_muda"],
                                     corner_radius=6)
            tgl_frame.pack(side="right", pady=2)
            ctk.CTkLabel(tgl_frame,
                         text=f"📅  {tanggal}",
                         font=("Segoe UI", 10),
                         text_color=C["oranye"]).pack(padx=8, pady=3)

        ctk.CTkFrame(body, height=6, fg_color="transparent").pack()

        # ── Toggle logic ─────────────────────────────────────────────
        def toggle(e=None, _uid=uid, _body=body, _lbl=lbl_toggle):
            self._collapse_state[_uid] = not self._collapse_state[_uid]
            if self._collapse_state[_uid]:
                _body.pack_forget()
                _lbl.configure(text="∨")
            else:
                _body.pack(fill="x")
                _lbl.configure(text="∧")

        hdr_frame.bind("<Button-1>", toggle)
        lbl_nama.bind("<Button-1>", toggle)
        lbl_toggle.bind("<Button-1>", toggle)
        badge.bind("<Button-1>", toggle)

    def refresh(self):
        pass   # Tidak perlu fetch DB


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

        # =====================================================
        # MAIN CONTAINER
        # =====================================================
        wrapper = ctk.CTkFrame(
            self,
            fg_color="#FFF8F3",
            corner_radius=0
        )
        wrapper.pack(fill="both", expand=True)

        # =====================================================
        # SIDEBAR
        # =====================================================
        sidebar_wrap = ctk.CTkFrame(
            wrapper,
            fg_color=C["oranye_gelap"],
            width=280,
            corner_radius=0
        )
        sidebar_wrap.pack(side="left", fill="y")
        sidebar_wrap.pack_propagate(False)

        self._sidebar = Sidebar(
            sidebar_wrap,
            self._navigasi
        )
        self._sidebar.pack(
            fill="both",
            expand=True,
        )

        # =====================================================
        # CONTENT AREA
        # =====================================================
        kanan = ctk.CTkFrame(
            wrapper,
            fg_color="#FFF8F3",
            corner_radius=0
        )
        kanan.pack(side="left", fill="both", expand=True)

        # =====================================================
        # TOP BAR MODERN
        # =====================================================
        topbar = ctk.CTkFrame(
            kanan,
            height=90,
            fg_color="#FFF8F3",
            corner_radius=0
        )
        topbar.pack(fill="x", padx=30, pady=(18, 0))
        topbar.pack_propagate(False)

        kiri = ctk.CTkFrame(
            topbar,
            fg_color="transparent"
        )
        kiri.pack(side="left", fill="y")

        ctk.CTkLabel(
            kiri,
            text="Dashboard Akademik",
            font=("Segoe UI", 28, "bold"),
            text_color="#2B2B2B"
        ).pack(anchor="w")

        ctk.CTkLabel(
            kiri,
            text="Kelola informasi akademik mahasiswa",
            font=("Segoe UI", 12),
            text_color="#78716C"
        ).pack(anchor="w")

        kanan_top = ctk.CTkFrame(
            topbar,
            fg_color="transparent"
        )
        kanan_top.pack(side="right")

        notif = ctk.CTkFrame(
            kanan_top,
            width=48,
            height=48,
            corner_radius=24,
            fg_color="#FFFFFF"
        )
        notif.pack(side="right", padx=(10, 0))
        notif.pack_propagate(False)

        ctk.CTkLabel(
            notif,
            text="🔔",
            font=("Segoe UI Emoji", 18)
        ).place(relx=0.5, rely=0.5, anchor="center")

        profile = ctk.CTkFrame(
            kanan_top,
            height=48,
            corner_radius=24,
            fg_color="#FFFFFF"
        )
        profile.pack(side="right", padx=10)

        ctk.CTkLabel(
            profile,
            text="👨‍💻 Admin",
            font=("Segoe UI", 12, "bold"),
            text_color="#2B2B2B"
        ).pack(padx=18, pady=12)

        # =====================================================
        # PAGE CONTENT
        # =====================================================
        self._area = ctk.CTkFrame(
            kanan,
            fg_color="#FFF8F3",
            corner_radius=0
        )
        self._area.pack(
            fill="both",
            expand=True,
            padx=30,
            pady=(12, 25)
        )

        # =====================================================
        # HALAMAN
        # =====================================================
        self._beranda = HalamanBeranda(self._area)
        self._dash = HalamanDashboard(self._area)
        self._mhs = HalamanMahasiswa(
            self._area,
            on_nilai=self._buka_nilai
        )
        self._nilai = HalamanNilai(
            self._area,
            on_selesai=self._selesai_nilai
        )
        self._statistik = HalamanStatistik(self._area)
        self._riwayat = HalamanRiwayat(self._area)
        self._jadwal_akademik = HalamanJadwalAkademik(self._area)

        self._halaman_aktif = None

    def _navigasi(self, key: str):
        if key == "logout":
            if messagebox.askyesno("Logout", "Yakin ingin keluar?"):
                self._tampil_login()
            return

        mapping = {
            "beranda":          self._beranda,
            "dashboard":        self._dash,
            "mahasiswa":        self._mhs,
            "nilai":            self._nilai,
            "statistik":        self._statistik,
            "riwayat":          self._riwayat,
            "jadwal_akademik":  self._jadwal_akademik,
        }

        target = mapping.get(key)
        if not target or target is self._halaman_aktif:
            return

        if self._halaman_aktif:
            self._halaman_aktif.pack_forget()

        target.pack(fill="both", expand=True)
        self._halaman_aktif = target

        if key == "beranda":     self._beranda.refresh()
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