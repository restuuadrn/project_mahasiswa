"""
SISTEM MANAJEMEN DATA MAHASISWA (ULTIMATE EDITION)
--------------------------------------------------
Created by  : Restu
NIM         : 241011400106
Version     : 5.0 (Masterpiece)
Framework   : Streamlit
Language    : Python 3.10+
Features    :
    - CRUD Operations (Create, Read, Update, Delete)
    - File Persistence (CSV)
    - Sorting Algorithms (Manual Implementation):
        1. Bubble Sort
        2. Selection Sort (New!)
        3. Insertion Sort
        4. Merge Sort
    - Searching Algorithms:
        1. Linear Search
        2. Binary Search
    - Authentication System
    - Real-time Stopwatch (JavaScript)
    - Enter Key Navigation (JavaScript)
    - Glassmorphism UI Design
    - System Activity Logging
    - Toast Notifications
"""

import streamlit as st
import pandas as pd
import csv
import os
import re
import time
import streamlit.components.v1 as components
from datetime import datetime
from abc import ABC, abstractmethod
from typing import List, Dict, Any, Optional

# ==============================================================================
# 1. PAGE CONFIGURATION & GLOBAL SETTINGS
# ==============================================================================
st.set_page_config(
    page_title="Sistem Akademik",
    page_icon="🎓",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ==============================================================================
# 2. ADVANCED CSS & JAVASCRIPT INJECTION
# ==============================================================================
# ==============================================================================
# 2. ADVANCED CSS & JAVASCRIPT INJECTION (DIPERBAIKI)
# ==============================================================================
def inject_resources():
    """
    Menyuntikkan Custom CSS dan JavaScript ke dalam aplikasi Streamlit.
    Mengatur tema Glassmorphism, Animasi, dan Logika Frontend.
    """
    
    # --- JAVASCRIPT LOGIC ---
    js_code = """
    <script>
    // 1. ENTER KEY NAVIGATION LOGIC (UPDATED)
    // Sekarang mendukung Text -> Password -> Submit
    document.addEventListener('DOMContentLoaded', function() {
        // PERBAIKAN DISINI: Menambahkan input[type="password"] agar kolom password terdeteksi
        const inputs = Array.from(document.querySelectorAll('input[type="text"], input[type="password"], input[type="number"]'));
        
        inputs.forEach((input, index) => {
            input.addEventListener('keydown', function(event) {
                if (event.key === 'Enter') {
                    // Cek apakah ini kolom terakhir (biasanya password di login)
                    // Jika iya, jangan preventDefault agar form bisa tersubmit (atau trigger tombol)
                    // Jika bukan, pindah ke kolom bawahnya
                    
                    if (index < inputs.length - 1) {
                        event.preventDefault();
                        const nextInput = inputs[index + 1];
                        if (nextInput) {
                            nextInput.focus();
                        }
                    }
                }
            });
        });
    });

    // 2. REAL-TIME STOPWATCH LOGIC
    let startTime = sessionStorage.getItem('startTime');
    if (!startTime) {
        startTime = Date.now();
        sessionStorage.setItem('startTime', startTime);
    }

    function updateTimer() {
        const now = Date.now();
        const diff = now - startTime;
        
        const hrs = Math.floor(diff / 3600000);
        const mins = Math.floor((diff % 3600000) / 60000);
        const secs = Math.floor((diff % 60000) / 1000);
        
        const formatted = 
            (hrs < 10 ? "0" + hrs : hrs) + ":" + 
            (mins < 10 ? "0" + mins : mins) + ":" + 
            (secs < 10 ? "0" + secs : secs);
        
        const timerElement = document.getElementById('timer_display');
        if (timerElement) {
            timerElement.innerText = formatted;
        }
    }
    
    setInterval(updateTimer, 1000);
    </script>
    
    <style>
        .stopwatch-container {
            background: rgba(255, 255, 255, 0.1); 
            padding: 15px; 
            border-radius: 12px; 
            text-align: center; 
            border: 1px solid rgba(255, 255, 255, 0.2);
            color: white;
            font-family: 'Segoe UI', sans-serif;
            margin-bottom: 25px;
            box-shadow: 0 4px 6px rgba(0,0,0,0.1);
        }
        .stopwatch-label {
            margin: 0; 
            font-size: 10px; 
            color: #ddd; 
            text-transform: uppercase; 
            letter-spacing: 2px;
        }
        .stopwatch-time {
            margin: 5px 0 0 0; 
            font-family: 'Courier New', monospace; 
            font-size: 26px; 
            font-weight: bold;
            text-shadow: 0 0 10px rgba(255,255,255,0.5);
        }
    </style>
    
    <div class="stopwatch-container">
        <p class="stopwatch-label">Durasi Sesi Admin</p>
        <h2 id="timer_display" class="stopwatch-time">00:00:00</h2>
    </div>
    """
    
    # --- CSS STYLING (AESTHETIC & ANIMATIONS) ---
    css_code = """
    <style>
        /* IMPORT GOOGLE FONTS */
        @import url('https://fonts.googleapis.com/css2?family=Poppins:wght@300;400;600;700&display=swap');

        /* GLOBAL THEME */
        .stApp {
            background: linear-gradient(135deg, #0F2027 0%, #203A43 50%, #2C5364 100%);
            font-family: 'Poppins', sans-serif;
            color: #ffffff;
        }

        /* ANIMASI FADE IN UNTUK KONTEN */
        @keyframes fadeIn {
            0% { opacity: 0; transform: translateY(20px); }
            100% { opacity: 1; transform: translateY(0); }
        }

        .glass-card {
            background: rgba(255, 255, 255, 0.05);
            backdrop-filter: blur(16px);
            -webkit-backdrop-filter: blur(16px);
            border-radius: 20px;
            border: 1px solid rgba(255, 255, 255, 0.15);
            padding: 30px;
            box-shadow: 0 8px 32px 0 rgba(0, 0, 0, 0.3);
            margin-bottom: 25px;
            animation: fadeIn 0.6s ease-out forwards;
        }

        /* CUSTOM SIDEBAR */
        [data-testid="stSidebar"] {
            background-color: rgba(0, 0, 0, 0.2);
            border-right: 1px solid rgba(255, 255, 255, 0.1);
        }

        /* INPUT FIELDS CUSTOMIZATION */
        .stTextInput > div > div > input, 
        .stSelectbox > div > div > div, 
        .stNumberInput > div > div > input {
            background-color: rgba(0, 0, 0, 0.3) !important;
            color: #ffffff !important;
            border: 1px solid rgba(255, 255, 255, 0.2) !important;
            border-radius: 10px !important;
            transition: all 0.3s ease;
        }

        .stTextInput > div > div > input:focus, 
        .stNumberInput > div > div > input:focus {
            border-color: #00d2ff !important;
            box-shadow: 0 0 10px rgba(0, 210, 255, 0.3) !important;
        }

        /* GRADIENT BUTTONS */
        div.stButton > button {
            background: linear-gradient(90deg, #00d2ff 0%, #3a7bd5 100%);
            color: white;
            border: none;
            padding: 12px 28px;
            border-radius: 10px;
            font-weight: 600;
            letter-spacing: 0.5px;
            transition: all 0.3s cubic-bezier(0.25, 0.8, 0.25, 1);
            width: 100%;
            text-transform: uppercase;
        }

        div.stButton > button:hover {
            transform: translateY(-3px) scale(1.02);
            box-shadow: 0 10px 20px rgba(0, 210, 255, 0.4);
            background: linear-gradient(90deg, #3a7bd5 0%, #00d2ff 100%);
        }

        /* TOAST NOTIFICATION STYLING */
        div[data-testid="stToast"] {
            background-color: #ffffff !important;
            color: #1a1a1a !important;
            font-weight: 500;
            border-radius: 12px;
            border-left: 6px solid #00d2ff;
            box-shadow: 0 5px 15px rgba(0,0,0,0.2);
            padding: 15px;
        }

        /* TYPOGRAPHY OVERRIDES */
        h1, h2, h3, h4, h5, h6 { color: #ffffff !important; text-shadow: 0 2px 4px rgba(0,0,0,0.3); }
        p, label, span, div.stMarkdown { color: #e0e0e0 !important; }
        .stCaption { color: #a0a0a0 !important; }
        
        /* SCROLLBAR */
        ::-webkit-scrollbar { width: 10px; }
        ::-webkit-scrollbar-track { background: #0F2027; }
        ::-webkit-scrollbar-thumb { background: #3a7bd5; border-radius: 5px; }
    </style>
    """
    
    st.markdown(css_code, unsafe_allow_html=True)
    
    # Render JS di Sidebar agar tidak mengganggu layout utama
    with st.sidebar:
        st.markdown("### ⏳ Status Sistem")
        components.html(js_code, height=130)

# ==============================================================================
# 3. OOP DATA MODELS (DATA STRUCTURES)
# ==============================================================================

class Person(ABC):
    """
    Abstract Base Class yang merepresentasikan entitas manusia dasar.
    Menerapkan konsep Enkapsulasi dan Abstraksi.
    """
    def __init__(self, nama: str, email: str):
        self._nama = nama
        self._email = email

    @abstractmethod
    def get_role(self):
        pass

class Student(Person):
    """
    Class Student turunan dari Person.
    Menyimpan data spesifik mahasiswa seperti NIM, Jurusan, dan IPK.
    """
    def __init__(self, nim: str, nama: str, email: str, jurusan: str, ipk: float):
        super().__init__(nama, email)
        self._nim = str(nim)
        self._jurusan = jurusan
        self._ipk = float(ipk)
        self._created_at = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    # --- Property Getters (Encapsulation) ---
    @property
    def nim(self) -> str: return self._nim
    @property
    def nama(self) -> str: return self._nama
    @property
    def email(self) -> str: return self._email
    @property
    def jurusan(self) -> str: return self._jurusan
    @property
    def ipk(self) -> float: return self._ipk
    @property
    def created_at(self) -> str: return self._created_at

    def get_role(self) -> str:
        return "Mahasiswa"

    def to_dict(self) -> Dict[str, Any]:
        """Konversi objek ke dictionary untuk penyimpanan CSV."""
        return {
            "NIM": self._nim,
            "Nama": self._nama,
            "Email": self._email,
            "Jurusan": self._jurusan,
            "IPK": self._ipk,
            "Waktu Input": self._created_at
        }

# ==============================================================================
# 4. SYSTEM LOGGER (SIMULASI LOG)
# ==============================================================================
class SystemLogger:
    """Class sederhana untuk menyimpan log aktivitas sistem secara runtime."""
    def __init__(self):
        if 'system_logs' not in st.session_state:
            st.session_state.system_logs = []

    def log(self, activity: str, level: str = "INFO"):
        timestamp = datetime.now().strftime("%H:%M:%S")
        entry = f"[{timestamp}] [{level}] {activity}"
        st.session_state.system_logs.insert(0, entry) # Insert di awal (terbaru diatas)

    def get_logs(self):
        return st.session_state.system_logs

# ==============================================================================
# 5. ALGORITMA SEARCHING & SORTING (LOGIC CORE)
# ==============================================================================
class AlgorithmEngine:
    """
    Kumpulan method statis untuk operasi Sorting dan Searching.
    Semua algoritma diimplementasikan secara MANUAL untuk tujuan edukasi.
    """

    @staticmethod
    def _get_val(student: Student, key: str):
        """Helper untuk mengambil nilai atribut berdasarkan key kolom."""
        if key == "NIM": return student.nim
        elif key == "IPK": return student.ipk
        else: return student.nama.lower()

    # --------------------------------------------------------------------------
    # ALGORITMA SORTING
    # --------------------------------------------------------------------------
    
    @staticmethod
    def bubble_sort(data: List[Student], key: str, descending: bool) -> List[Student]:
        """
        Bubble Sort: Membandingkan elemen bersebelahan dan menukarnya.
        Time Complexity: O(n^2)
        """
        arr = data.copy()
        n = len(arr)
        for i in range(n):
            swapped = False
            for j in range(0, n - i - 1):
                val_a = AlgorithmEngine._get_val(arr[j], key)
                val_b = AlgorithmEngine._get_val(arr[j+1], key)
                
                condition = (val_a < val_b) if descending else (val_a > val_b)
                
                if condition:
                    arr[j], arr[j+1] = arr[j+1], arr[j]
                    swapped = True
            if not swapped:
                break
        return arr

    @staticmethod
    def selection_sort(data: List[Student], key: str, descending: bool) -> List[Student]:
        """
        Selection Sort: Mencari elemen minimum/maksimum dari unsorted part
        dan menaruhnya di posisi yang benar.
        Time Complexity: O(n^2)
        """
        arr = data.copy()
        n = len(arr)
        for i in range(n):
            idx_target = i
            for j in range(i + 1, n):
                val_j = AlgorithmEngine._get_val(arr[j], key)
                val_target = AlgorithmEngine._get_val(arr[idx_target], key)
                
                # Logic: Jika descending, cari yang terbesar. Jika ascending, cari terkecil.
                condition = (val_j > val_target) if descending else (val_j < val_target)
                
                if condition:
                    idx_target = j
            
            # Swap elemen ditemukan dengan elemen di posisi i
            arr[i], arr[idx_target] = arr[idx_target], arr[i]
        return arr

    @staticmethod
    def insertion_sort(data: List[Student], key: str, descending: bool) -> List[Student]:
        """
        Insertion Sort: Membangun array yang disortir satu per satu.
        Time Complexity: O(n^2)
        """
        arr = data.copy()
        for i in range(1, len(arr)):
            key_item = arr[i]
            val_key = AlgorithmEngine._get_val(key_item, key)
            j = i - 1
            
            while j >= 0:
                val_j = AlgorithmEngine._get_val(arr[j], key)
                condition = (val_j < val_key) if descending else (val_j > val_key)
                
                if condition:
                    arr[j + 1] = arr[j]
                    j -= 1
                else:
                    break
            arr[j + 1] = key_item
        return arr

    @staticmethod
    def merge_sort(data: List[Student], key: str, descending: bool) -> List[Student]:
        """
        Merge Sort: Divide and Conquer algorithm.
        Time Complexity: O(n log n)
        """
        arr = data.copy()
        return AlgorithmEngine._merge_sort_recursive(arr, key, descending)

    @staticmethod
    def _merge_sort_recursive(arr, key, descending):
        if len(arr) <= 1: return arr
        
        mid = len(arr) // 2
        left = AlgorithmEngine._merge_sort_recursive(arr[:mid], key, descending)
        right = AlgorithmEngine._merge_sort_recursive(arr[mid:], key, descending)
        
        return AlgorithmEngine._merge(left, right, key, descending)

    @staticmethod
    def _merge(left, right, key, descending):
        result = []
        i = j = 0
        while i < len(left) and j < len(right):
            val_l = AlgorithmEngine._get_val(left[i], key)
            val_r = AlgorithmEngine._get_val(right[j], key)
            
            condition = (val_l >= val_r) if descending else (val_l <= val_r)
            
            if condition:
                result.append(left[i])
                i += 1
            else:
                result.append(right[j])
                j += 1
        
        result.extend(left[i:])
        result.extend(right[j:])
        return result

# ==============================================================================
# 6. DATA MANAGER (BACKEND)
# ==============================================================================
class DataManager:
    """Class untuk mengelola persistensi data (CSV) dan operasi CRUD."""
    
    CSV_PATH = 'database_mahasiswa_v5.csv'

    def __init__(self):
        self.students: List[Student] = []
        self.logger = SystemLogger()
        self.load_data()

    def load_data(self):
        """Membaca data dari file CSV saat inisialisasi."""
        self.students = []
        if os.path.exists(self.CSV_PATH):
            try:
                with open(self.CSV_PATH, mode='r', newline='', encoding='utf-8') as f:
                    reader = csv.DictReader(f)
                    for row in reader:
                        # Handle potential missing keys if CSV format changes
                        if 'NIM' in row:
                            self.students.append(Student(
                                row['NIM'], row['Nama'], row['Email'], 
                                row['Jurusan'], row['IPK']
                            ))
                self.logger.log(f"Database dimuat: {len(self.students)} records.", "SYSTEM")
            except Exception as e:
                self.logger.log(f"Error loading data: {e}", "ERROR")

    def save_data(self):
        """Menyimpan seluruh list students ke CSV (Overwrite)."""
        try:
            with open(self.CSV_PATH, mode='w', newline='', encoding='utf-8') as f:
                fieldnames = ['NIM', 'Nama', 'Email', 'Jurusan', 'IPK', 'Waktu Input']
                writer = csv.DictWriter(f, fieldnames=fieldnames)
                writer.writeheader()
                for s in self.students:
                    writer.writerow(s.to_dict())
        except Exception as e:
            self.logger.log(f"Gagal menyimpan data: {e}", "ERROR")

    def add_student(self, nim, nama, email, jurusan, ipk):
        """Menambahkan data mahasiswa baru dengan validasi."""
        # Validasi Input
        if not re.match(r"^\d+$", nim): 
            raise ValueError("Format NIM salah! Harus berupa angka.")
        if len(nama) < 3: 
            raise ValueError("Nama terlalu pendek! Minimal 3 karakter.")
        if not re.match(r"[^@]+@[^@]+\.[^@]+", email): 
            raise ValueError("Format Email tidak valid!")
        if any(s.nim == nim for s in self.students): 
            raise KeyError(f"NIM {nim} sudah terdaftar dalam sistem!")

        new_student = Student(nim, nama, email, jurusan, ipk)
        self.students.append(new_student)
        self.save_data()
        self.logger.log(f"Input Data Baru: {nama} ({nim})", "SUCCESS")

    def delete_student(self, nim):
        """Menghapus data mahasiswa berdasarkan NIM."""
        initial_count = len(self.students)
        self.students = [s for s in self.students if s.nim != nim]
        
        if len(self.students) == initial_count:
            raise ValueError("NIM tidak ditemukan untuk dihapus.")
        
        self.save_data()
        self.logger.log(f"Hapus Data NIM: {nim}", "WARNING")

    def search_students(self, keyword):
        """Melakukan pencarian Linear sederhana berdasarkan Nama atau NIM."""
        keyword = keyword.lower()
        return [s for s in self.students if keyword in s.nama.lower() or keyword in s.nim]

# ==============================================================================
# 7. UI PAGES (VIEW LAYER)
# ==============================================================================

def render_login():
    """Menampilkan Halaman Login."""
    c1, c2, c3 = st.columns([1, 1.2, 1])
    with c2:
        st.markdown("<br><br><br>", unsafe_allow_html=True)
        st.markdown('<div class="glass-card" style="text-align:center;">', unsafe_allow_html=True)
        st.image("https://cdn-icons-png.flaticon.com/512/295/295128.png", width=80)
        st.markdown("<h2 style='margin-bottom: 20px;'>Admin Portal</h2>", unsafe_allow_html=True)
        
        with st.form("login_form"):
            username = st.text_input("Username", placeholder="Masukkan username")
            password = st.text_input("Password", type="password", placeholder="Masukkan password")
            submit = st.form_submit_button("MASUK🔐")
            
            if submit:
                if username == "admin" and password == "admin":
                    st.success("Login Berhasil! Mengalihkan...") # Muncul di dalam form
                    st.session_state.logged_in = True
                    time.sleep(1.5) # Beri waktu user membaca
                    st.rerun()
                    st.error("Akses Ditolak: Username/Password Salah.")
        
        st.caption("Default Credentials: admin / admin")
        st.markdown('</div>', unsafe_allow_html=True)

def render_dashboard(manager: DataManager):
    """Menampilkan Dashboard Statistik & Log Sistem."""
    st.markdown("## 📊 Dashboard Overview")
    
    # Statistik Utama
    total_mhs = len(manager.students)
    avg_ipk = sum(s.ipk for s in manager.students) / total_mhs if total_mhs > 0 else 0.0
    
    c1, c2, c3 = st.columns(3)
    with c1:
        st.markdown('<div class="glass-card" style="text-align:center">', unsafe_allow_html=True)
        st.metric("Total Mahasiswa", f"{total_mhs} Orang", delta="Active Data")
        st.markdown('</div>', unsafe_allow_html=True)
    with c2:
        st.markdown('<div class="glass-card" style="text-align:center">', unsafe_allow_html=True)
        st.metric("Rata-Rata IPK", f"{avg_ipk:.2f}", delta="Indeks Prestasi")
        st.markdown('</div>', unsafe_allow_html=True)
    with c3:
        st.markdown('<div class="glass-card" style="text-align:center">', unsafe_allow_html=True)
        # Menghitung jurusan terbanyak
        jurusan_list = [s.jurusan for s in manager.students]
        top_jurusan = max(set(jurusan_list), key=jurusan_list.count) if jurusan_list else "-"
        st.metric("Jurusan Terpopuler", top_jurusan)
        st.markdown('</div>', unsafe_allow_html=True)

    # Grafik & Log
    col_chart, col_log = st.columns([2, 1])
    
    with col_chart:
        st.markdown('<div class="glass-card">', unsafe_allow_html=True)
        st.subheader("🏆 Top Academic Achievers")
        if manager.students:
            # Menggunakan Selection Sort untuk Top 5
            top_students = AlgorithmEngine.selection_sort(manager.students, "IPK", True)[:5]
            for i, s in enumerate(top_students):
                st.write(f"#{i+1} **{s.nama}** ({s.jurusan}) - IPK: {s.ipk}")
                st.progress(int(s.ipk / 4.0 * 100))
        else:
            st.info("Belum ada data untuk ditampilkan.")
        st.markdown('</div>', unsafe_allow_html=True)

    with col_log:
        st.markdown('<div class="glass-card">', unsafe_allow_html=True)
        st.subheader("📜 System Logs")
        logs = manager.logger.get_logs()
        if logs:
            log_text = "\n".join(logs[:8]) # Ambil 8 log terakhir
            st.code(log_text, language="log")
        else:
            st.caption("Tidak ada aktivitas terbaru.")
        st.markdown('</div>', unsafe_allow_html=True)

def render_input_data(manager: DataManager):
    """Halaman gabungan Input Data & Table View dengan Sorting."""
    col_left, col_right = st.columns([1, 2.2])
    
    # --- FORM INPUT (KIRI) ---
    with col_left:
        st.markdown('<div class="glass-card">', unsafe_allow_html=True)
        st.subheader("📝 Input Data Baru")
        
        with st.form("data_entry_form", clear_on_submit=True):
            nim_input = st.text_input("NIM Mahasiswa", help="Harus angka unik")
            nama_input = st.text_input("Nama Lengkap")
            email_input = st.text_input("Email")
            jurusan_input = st.selectbox("Program Studi", ["Teknik Informatika", "Sistem Informasi", "Akuntansi", "Manajemen", "Sastra Inggris"])
            ipk_input = st.number_input("IPK Terakhir", min_value=0.0, max_value=4.0, step=0.01, value=3.0)
            
            submitted = st.form_submit_button("SIMPAN DATA KE DATABASE 💾")
            
            if submitted:
                try:
                    manager.add_student(nim_input, nama_input, email_input, jurusan_input, ipk_input)
                    st.toast(f"Sukses! Data {nama_input} berhasil disimpan.", icon="✅")
                    # Delay sedikit agar user melihat toast sebelum refresh
                    time.sleep(1.2)
                    st.rerun()
                except Exception as e:
                    st.toast(f"Gagal Menyimpan: {str(e)}", icon="❌")
        
        st.markdown('</div>', unsafe_allow_html=True)

    # --- TABEL DATA & SORTING (KANAN) ---
    with col_right:
        st.markdown('<div class="glass-card">', unsafe_allow_html=True)
        st.subheader("📂 Direktori Mahasiswa")
        
        # Toolbar Filter & Sort
        row_tool1, row_tool2, row_tool3 = st.columns([2, 1.5, 1])
        with row_tool1:
            search_keyword = st.text_input("🔍 Pencarian (Nama/NIM)", placeholder="Ketik keyword...")
        with row_tool2:
            sort_algorithm = st.selectbox("Algoritma Pengurutan", 
                                          ["Selection Sort", "Bubble Sort", "Insertion Sort", "Merge Sort"])
        with row_tool3:
            sort_direction = st.selectbox("Arah", ["Ascending", "Descending"])
        
        # Logic Processing
        # 1. Searching
        if search_keyword:
            display_data = manager.search_students(search_keyword)
        else:
            display_data = manager.students

        # 2. Sorting
        is_descending = (sort_direction == "Descending")
        sort_key = st.radio("Urutkan Berdasarkan:", ["NIM", "Nama", "IPK"], horizontal=True)

        # Eksekusi Sorting + Benchmark Waktu
        start_time = time.perf_counter()
        
        if sort_algorithm == "Bubble Sort":
            display_data = AlgorithmEngine.bubble_sort(display_data, sort_key, is_descending)
        elif sort_algorithm == "Selection Sort":
            display_data = AlgorithmEngine.selection_sort(display_data, sort_key, is_descending)
        elif sort_algorithm == "Insertion Sort":
            display_data = AlgorithmEngine.insertion_sort(display_data, sort_key, is_descending)
        elif sort_algorithm == "Merge Sort":
            display_data = AlgorithmEngine.merge_sort(display_data, sort_key, is_descending)
            
        end_time = time.perf_counter()
        execution_time = end_time - start_time

        # 3. Menampilkan Tabel
        if display_data:
            # Konversi objek Student ke Dict untuk DataFrame
            table_data = [s.to_dict() for s in display_data]
            df = pd.DataFrame(table_data)
            
            # Tampilan Tabel Interaktif
            st.dataframe(
                df, 
                use_container_width=True,
                hide_index=True,
                column_config={
                    "IPK": st.column_config.ProgressColumn(
                        "Indeks Prestasi",
                        format="%.2f",
                        min_value=0,
                        max_value=4,
                    ),
                    "Email": st.column_config.LinkColumn("Kontak Email")
                }
            )
            
            # Footer Tabel (Statistik & Delete)
            col_info, col_del = st.columns([3, 1])
            with col_info:
                st.caption(f"ℹ️ Total: {len(display_data)} Data | Algo: {sort_algorithm} | Time: {execution_time:.6f} detik")
            with col_del:
                with st.popover("🗑️ Hapus Data"):
                    nim_to_del = st.selectbox("Pilih NIM", [s.nim for s in display_data])
                    if st.button("Konfirmasi Hapus", type="primary"):
                        try:
                            manager.delete_student(nim_to_del)
                            st.toast("Data berhasil dihapus dari sistem!", icon="🗑️")
                            time.sleep(1)
                            st.rerun()
                        except Exception as e:
                            st.error(str(e))
        else:
            st.warning("Data tidak ditemukan atau database kosong.")
            
        st.markdown('</div>', unsafe_allow_html=True)
def render_profile():
    """Menampilkan Profil Pengembang (User Request: Restu)."""
    st.markdown('<div class="glass-card">', unsafe_allow_html=True)
    
    col_img, col_desc = st.columns([1, 3])
    
    with col_img:
        # --- UPDATE: MENDUKUNG FORMAT JPEG ---
        # Nama file harus persis sama dengan yang ada di komputer Anda
        foto_nama = "restu.jpeg" 
        
        # Cek apakah file ada di folder
        if os.path.exists(foto_nama):
            st.image(foto_nama, width=180)
            st.caption("Administrator - Online 🟢")
        else:
            # Fallback jika file masih tidak terbaca
            st.image("https://cdn-icons-png.flaticon.com/512/3135/3135715.png", width=180)
            # Pesan error agar kita tahu apa yang salah
            st.error(f"⚠️ Gagal: File '{foto_nama}' tidak ditemukan.")
            st.caption("Pastikan nama file dan ekstensinya benar!")
        
        st.markdown("---")
        st.write("**Social Links:**")
        st.markdown("[GitHub](https://github.com/) | [Instagram](https://www.instagram.com/restuuadrn_?igsh=aHoyZjZwZW81Mjhh)")

    with col_desc:
        st.title("Profile Administrator")
        st.markdown("### Restu")
        st.markdown("##### *Lead Developer & System Architect*")
        
        st.markdown("---")
        
        # Informasi Detail
        info_data = {
            "Nomor Induk Mahasiswa": "241011400106",
            "Program Studi": "Teknik Informatika",
            "Universitas": "Universitas Pamulang",
            "Usia": "21 Tahun",
            "Alamat Domisili": "Kp. Baru, Jl. H. Daud, Kebon Jeruk",
            "Minat Utama": "Software Engineering, Algorithm Analysis, Python Development"
        }
        
        for key, value in info_data.items():
            st.text_input(key, value, disabled=True)
            
        st.info("💡 *Aplikasi ini dikembangkan untuk memenuhi project Algoritma Pemrograman II*")

    st.markdown('</div>', unsafe_allow_html=True)

def render_help():
    """Halaman Dokumentasi Algoritma (Bonus Content)."""
    st.markdown("## 📚 Dokumentasi Algoritma")
    st.markdown('<div class="glass-card">', unsafe_allow_html=True)
    
    tabs = st.tabs(["Bubble Sort", "Selection Sort", "Insertion Sort", "Merge Sort"])
    
    with tabs[0]:
        st.markdown("""
        ### Bubble Sort
        Algoritma pengurutan sederhana yang berulang kali melangkah melalui daftar, membandingkan elemen yang berdekatan dan menukarnya jika urutannya salah.
        - **Best Case:** O(n)
        - **Average Case:** O(n²)
        - **Worst Case:** O(n²)
        """)
    
    with tabs[1]:
        st.markdown("""
        ### Selection Sort
        Algoritma yang membagi daftar input menjadi dua bagian: sublist item yang sudah disortir dan sublist item yang belum disortir. Ia mencari elemen terkecil/terbesar dari sublist yang belum disortir dan menukarnya.
        - **Time Complexity:** O(n²) untuk semua kasus.
        - **Kelebihan:** Melakukan jumlah penukaran memori minimum.
        """)
        
    with tabs[2]:
        st.markdown("""
        ### Insertion Sort
        Algoritma yang membangun array yang disortir final satu item pada satu waktu. Ini jauh lebih kurang efisien pada daftar besar daripada algoritma yang lebih canggih.
        - **Best Case:** O(n)
        - **Worst Case:** O(n²)
        """)
        
    with tabs[3]:
        st.markdown("""
        ### Merge Sort
        Algoritma Divide and Conquer yang efisien, tujuan umum, dan berbasis perbandingan.
        - **Time Complexity:** O(n log n)
        - **Kestabilan:** Stabil
        """)
        
    st.markdown('</div>', unsafe_allow_html=True)

# ==============================================================================
# 8. MAIN APP CONTROLLER
# ==============================================================================
def main():
    """Fungsi Utama (Main Entry Point)."""
    
    # 1. Inject Resources (CSS/JS)
    inject_resources()
    
    # 2. Initialize Session State
    if 'logged_in' not in st.session_state:
        st.session_state.logged_in = False
    
    # 3. Initialize Data Manager
    if 'data_manager' not in st.session_state:
        st.session_state.data_manager = DataManager()
    
    manager = st.session_state.data_manager

    # 4. Routing Logic
    if not st.session_state.logged_in:
        render_login()
    else:
        # --- SIDEBAR NAVIGATION ---
        with st.sidebar:
            st.image("https://cdn-icons-png.flaticon.com/512/906/906343.png", width=60)
            st.title("Admin Menu")
            st.markdown(f"User: **Restu** (Admin)")
            
            st.markdown("---")
            
            selected_menu = st.radio(
                "Navigasi Halaman:", 
                ["📊 Dashboard", "📝 Input & Data", "👤 Profile", "📚 Bantuan Algoritma"],
                index=0
            )
            
            st.markdown("---")
            if st.button("LOGOUT / KELUAR 🚪"):
                st.session_state.logged_in = False
                st.toast("Berhasil Logout!", icon="👋")
                time.sleep(1)
                st.rerun()

        # --- PAGE RENDERING ---
        if selected_menu == "📊 Dashboard":
            render_dashboard(manager)
        elif selected_menu == "📝 Input & Data":
            render_input_data(manager)
        elif selected_menu == "👤 Profile":
            render_profile()
        elif selected_menu == "📚 Bantuan Algoritma":
            render_help()

if __name__ == "__main__":
    main()