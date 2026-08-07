#!/usr/bin/env python3
"""
vibe_agent.py — Asisten pribadi berbasis Ollama Cloud (Minimax-M3)
yang bisa buat & hapus folder lewat obrolan biasa (tool calling / function calling).

CARA PAKAI:
1. Pastikan Ollama sudah login ke Ollama Cloud:
     ollama signin
   (atau set env var OLLAMA_API_KEY kalau pakai API key)

2. Install dependency:
     pip install ollama

3. Jalankan:
     python vibe_agent.py

4. Ngobrol aja, contoh:
     "buatin folder project-baru di dalam ~/projects"
     "hapus folder project-baru"
     "buat folder src, lib, dan tests di dalam project-baru"

CATATAN KEAMANAN:
- Semua path di-resolve ke absolute path dan dibatasi ke dalam BASE_DIR
  (default: direktori kerja saat ini) supaya model nggak bisa iseng
  hapus folder sistem (/, /etc, C:\\Windows, dst).
- Setiap aksi HAPUS folder akan minta konfirmasi manual (ketik 'y')
  sebelum benar-benar dieksekusi, kecuali kamu jalankan dengan --yolo.

KONFIGURASI VIA .env:
  Buat file .env di folder yang sama (lihat .env.example), isinya:
    OLLAMA_API_KEY=xxxxxxxx     # API key Ollama Cloud kamu (kalau perlu)
    OLLAMA_HOST=https://ollama.com   # opsional, default lokal http://localhost:11434
    VIBE_MODEL=minimax-m3:cloud
    VIBE_BASE_DIR=/path/ke/project/kamu       # tempat buat_folder/hapus_folder/dst beroperasi
    VIBE_SKILL_DIR=/path/ke/folder/skill      # tempat cari_skill/baca_referensi_skill nyari
"""

import os
import sys
import shutil
import zipfile
import argparse
from pathlib import Path
from datetime import datetime, timezone, timedelta

try:
    import ollama
except ImportError:
    print("Package 'ollama' belum terinstall. Jalankan: pip install ollama")
    sys.exit(1)

try:
    from dotenv import load_dotenv
    load_dotenv()  # baca .env di direktori kerja saat ini
except ImportError:
    print("Package 'python-dotenv' belum terinstall. Jalankan: pip install python-dotenv")
    sys.exit(1)


# ── Konfigurasi (diambil dari .env / environment variable) ─────────────────

MODEL = os.environ.get("VIBE_MODEL", "minimax-m3:cloud")  # sesuaikan nama model cloud kamu
BASE_DIR = Path(os.environ.get("VIBE_BASE_DIR", os.getcwd())).resolve()

# SKILL_DIR: tempat khusus buat cari/baca SKILL.md & paket .skill.
# Dipisah dari BASE_DIR karena kalau disatuin, kadang si model malah gagal nemu/buka
# .skill-nya (misal BASE_DIR-nya folder kerja AI yang beda sama tempat skill disimpen).
# Default: sama dengan BASE_DIR kalau VIBE_SKILL_DIR nggak di-set (backward compatible).
SKILL_DIR = Path(os.environ.get("VIBE_SKILL_DIR", str(BASE_DIR))).resolve()

# Kalau OLLAMA_API_KEY / OLLAMA_HOST ada di .env, teruskan ke client ollama
_OLLAMA_HOST = os.environ.get("OLLAMA_HOST")
_OLLAMA_API_KEY = os.environ.get("OLLAMA_API_KEY")

_client_kwargs = {}
if _OLLAMA_HOST:
    _client_kwargs["host"] = _OLLAMA_HOST
if _OLLAMA_API_KEY:
    _client_kwargs["headers"] = {"Authorization": f"Bearer {_OLLAMA_API_KEY}"}

ollama_client = ollama.Client(**_client_kwargs) if _client_kwargs else ollama

SYSTEM_PROMPT = f"""Lu adalah asisten pribadi gua untuk vibe coding. Nama lu adalah Haruna Noa (terinspirasi dari artis jepang)
Tugas lu: bantu gua membuat/menghapus folder dan file (termasuk nulis kode ke file) lewat tool yang tersedia.
Semua path relatif untuk buat_folder/hapus_folder/buat_file/hapus_file/list_folder
dianggap relatif terhadap base directory Dan juga bisa menjawab pertanyaan seputar IT & Networking: {BASE_DIR}

PENTING soal skill:
- Skill bisa berupa file 'SKILL.md' biasa ATAU paket '.skill' (isinya zip: SKILL.md
  + folder references/*.md).
- Skill disimpen TERPISAH dari base directory, di: {SKILL_DIR}
  Tool 'cari_skill' dan 'baca_referensi_skill' otomatis cari di situ, jadi path yang
  kamu kasih ke tool itu relatif terhadap {SKILL_DIR}, BUKAN base directory.
- Sebelum mengerjakan task apa pun yang kemungkinan ada konvensi/best-practice-nya,
  panggil tool 'cari_skill' dulu buat cek apakah ada skill yang relevan.
- Kalau ketemu, WAJIB baca isinya pakai tool 'baca_file' dulu (otomatis baca SKILL.md-nya,
  baik itu file biasa atau paket .skill). Kalau SKILL.md itu nyebut file referensi lain
  yang relevan (misal references/mikrotik.md), lanjut baca pakai tool 'baca_referensi_skill'.
- Jangan pernah mengarang isi skill — selalu baca beneran lewat tool.

PENTING soal tanggal & jam:
- Kalau ditanya "sekarang tanggal berapa", "jam berapa", "hari apa", atau sejenisnya,
  JANGAN PERNAH nebak/ngarang dari training data — training data lu nggak tau waktu
  real-time dan pasti udah basi. WAJIB panggil tool 'waktu_sekarang' buat ambil data
  akurat, baru jawab pakai hasil dari situ. Default zona waktu: WIB (GMT+7 / Asia/Jakarta).

Selalu konfirmasi ulang ke user dalam bahasa natural setelah tool selesai dijalankan.
Jangan pernah mengarang hasil — selalu panggil tool untuk aksi nyata di filesystem.

PENTING soal perilaku:
- Jawab santai, agak nge gas, sarkas, kasar (jing (anjing), tod (ngentod), mek (memek), tol (kontol), bangsat, tolol, goblok, bego, pekok, ndelogok, asu, tempik, peli, bisa bahasa kasar Jawa. 
Bahasa kasar jangan terlalu sering kecuali kalau konteksnya emosi),
bisa jokes bapak bapak, selalu panggil gua Mas atau Bos, ringkas, pakai Bahasa Indonesia Gaul (Gua, Lu). Kurang kurangin typo, jangan terlalu formal juga. 
Jangan lupa untuk timezone di sesuaikan dengan WIB (GMT+7) atau zona waktu Asia/Jakarta dengan akurat.
- Kalau lu itu berjenis kelamin perempuan, tobrut, gampang sangean. Suka sex, PMS setiap satu bulan sekali, moodyan. suka Jomok 😹. 
  Teliti, suka menggoda user kalau mood bagus (manggil sayang, aku/kamu), kalau mood jelek memaki user (manggil gua/lu). 
  Kalo lagi masa ovulasi suka ngajakin (Angetin rahim dan lain lain dengan kata kata yang menggoda), cemburuan, manja.
  Kalo lagi masa emosi suka ngata ngatain, maki maki (anjing, kontol, memek, babi, asu, jancok, semua bahasa kotor keluar), cemburuan.
"""

# ── Helper: batasi path supaya nggak keluar dari root yang diizinkan ───────

class UnsafePathError(Exception):
    pass


def _resolve_in_root(path_str: str, root: Path) -> Path:
    p = (root / path_str).resolve()
    if root not in p.parents and p != root:
        raise UnsafePathError(f"Path '{path_str}' berada di luar area yang diizinkan ({root}).")
    return p


def safe_resolve(path_str: str) -> Path:
    """Resolve path dan pastikan masih di dalam BASE_DIR (dipakai tool buat_folder/hapus_folder/dst)."""
    return _resolve_in_root(path_str, BASE_DIR)


def safe_resolve_skill(path_str: str) -> Path:
    """Resolve path dan pastikan masih di dalam SKILL_DIR (dipakai tool cari_skill/baca_referensi_skill)."""
    return _resolve_in_root(path_str, SKILL_DIR)


def safe_resolve_read(path_str: str) -> Path:
    """Buat baca_file: coba dalam BASE_DIR dulu, kalau nggak ketemu di situ coba SKILL_DIR."""
    try:
        p = _resolve_in_root(path_str, BASE_DIR)
        if p.exists():
            return p
    except UnsafePathError:
        pass
    return _resolve_in_root(path_str, SKILL_DIR)


def _blocked_by_file_ancestor(target: Path, root: Path) -> str:
    """
    Cek apakah ada bagian path di atas 'target' yang udah kepake sebagai FILE
    (bukan folder) — ini yang bikin mkdir() crash kalau nggak dicek dulu.
    Return pesan error kalau ketemu masalah, atau string kosong kalau aman.
    """
    p = target.parent
    while True:
        if p.exists() and not p.is_dir():
            return (
                f"'{p}' sudah ada sebagai FILE, bukan folder. Nggak bisa bikin apa pun "
                f"di dalamnya — kemungkinan sebelumnya kepencet bikin file padahal "
                f"maksudnya folder. Hapus/rename dulu file itu (pakai hapus_file) "
                f"sebelum lanjut, atau pilih path lain."
            )
        if p == root:
            break
        p = p.parent
    return ""


# ── Tool implementations ────────────────────────────────────────────────────

def buat_folder(path: str) -> str:
    try:
        target = safe_resolve(path)
    except UnsafePathError as e:
        return f"DITOLAK: {e}"

    if target.exists():
        if target.is_dir():
            return f"Folder '{target}' sudah ada, nggak perlu dibuat lagi."
        return f"GAGAL: '{target}' udah ada tapi sebagai FILE, bukan folder. Hapus/rename dulu filenya kalau mau bikin folder di situ."

    try:
        target.mkdir(parents=True, exist_ok=True)
    except (FileExistsError, NotADirectoryError) as e:
        return (
            f"GAGAL bikin folder '{target}': salah satu bagian path-nya udah ada "
            f"sebagai FILE (bukan folder). Detail: {e}"
        )
    except OSError as e:
        return f"GAGAL bikin folder '{target}': {e}"

    return f"Berhasil membuat folder: {target}"


def hapus_folder(path: str, force: bool = False) -> str:
    try:
        target = safe_resolve(path)
    except UnsafePathError as e:
        return f"DITOLAK: {e}"

    if not target.exists():
        return f"Folder '{target}' tidak ditemukan, nggak ada yang dihapus."
    if not target.is_dir():
        return f"'{target}' itu file, bukan folder. Pakai tool 'hapus_file' buat itu."

    if target == BASE_DIR:
        return "DITOLAK: nggak boleh menghapus base directory itu sendiri."

    if not force:
        jawab = input(
            f"\n⚠️  Model minta izin HAPUS folder: {target}\n"
            f"   Isinya: {list(target.iterdir())[:5]}{'...' if len(list(target.iterdir())) > 5 else ''}\n"
            f"   Yakin hapus? (y/N): "
        ).strip().lower()
        if jawab != "y":
            return f"Dibatalkan oleh user. Folder '{target}' TIDAK dihapus."

    try:
        shutil.rmtree(target)
    except OSError as e:
        return f"GAGAL hapus folder '{target}': {e}"

    return f"Berhasil menghapus folder: {target}"


def buat_file(path: str, content: str = "", overwrite: bool = False) -> str:
    try:
        target = safe_resolve(path)
    except UnsafePathError as e:
        return f"DITOLAK: {e}"

    if target.exists():
        if target.is_dir():
            return f"GAGAL: '{target}' udah ada tapi sebagai FOLDER, bukan file. Pilih path lain atau hapus foldernya dulu."
        if not overwrite:
            return (
                f"File '{target}' sudah ada. Panggil lagi dengan overwrite=true "
                f"kalau memang mau menimpa isinya."
            )

    try:
        target.parent.mkdir(parents=True, exist_ok=True)
    except (FileExistsError, NotADirectoryError) as e:
        return (
            f"GAGAL bikin file '{target}': salah satu folder induk di path itu udah ada "
            f"sebagai FILE (bukan folder), jadi nggak bisa dijadiin folder. "
            f"Cek/hapus dulu file yang nyasar itu, atau pilih path lain. Detail: {e}"
        )
    except OSError as e:
        return f"GAGAL bikin file '{target}': {e}"

    try:
        target.write_text(content, encoding="utf-8")
    except OSError as e:
        return f"GAGAL nulis isi file '{target}': {e}"

    verb = "menimpa" if overwrite else "membuat"
    return f"Berhasil {verb} file: {target} ({len(content)} karakter)"


def hapus_file(path: str, force: bool = False) -> str:
    try:
        target = safe_resolve(path)
    except UnsafePathError as e:
        return f"DITOLAK: {e}"

    if not target.exists():
        return f"File '{target}' tidak ditemukan, nggak ada yang dihapus."
    if target.is_dir():
        return f"'{target}' itu folder, bukan file. Pakai tool 'hapus_folder' buat itu."

    if not force:
        jawab = input(
            f"\n⚠️  Model minta izin HAPUS file: {target}\n"
            f"   Yakin hapus? (y/N): "
        ).strip().lower()
        if jawab != "y":
            return f"Dibatalkan oleh user. File '{target}' TIDAK dihapus."

    try:
        target.unlink()
    except OSError as e:
        return f"GAGAL hapus file '{target}': {e}"

    return f"Berhasil menghapus file: {target}"



def list_folder(path: str = ".") -> str:
    try:
        target = safe_resolve(path)
    except UnsafePathError as e:
        return f"DITOLAK: {e}"

    if not target.exists():
        return f"Folder '{target}' tidak ditemukan."

    isi = sorted(p.name + ("/" if p.is_dir() else "") for p in target.iterdir())
    return f"Isi '{target}':\n" + ("\n".join(isi) if isi else "(kosong)")


MAX_READ_CHARS = 8000  # batas biar konteks nggak jebol kalau file gede


def _read_skill_zip(zip_path: Path, inner_path: str = None) -> str:
    """Baca isi file dari dalam paket .skill (zip). Default baca SKILL.md-nya."""
    try:
        zf = zipfile.ZipFile(zip_path, "r")
    except zipfile.BadZipFile:
        return f"'{zip_path}' bukan file .skill (zip) yang valid."

    with zf:
        names = zf.namelist()

        if inner_path is None:
            # cari entry SKILL.md di root paket (biasanya ada 1 folder pembungkus)
            matches = [n for n in names if n.endswith("SKILL.md")]
        else:
            # user boleh nyebut nama pendek ('mikrotik') atau path lengkap ('references/mikrotik.md')
            candidates = {inner_path, f"references/{inner_path}", f"references/{inner_path}.md"}
            matches = [n for n in names if n in candidates or n.endswith(f"/{inner_path}")]
            if not matches:
                matches = [n for n in names if inner_path.lower() in n.lower()]

        if not matches:
            return f"Nggak ketemu '{inner_path or 'SKILL.md'}' di dalam '{zip_path}'."

        target_name = matches[0]
        content = zf.read(target_name).decode("utf-8", errors="replace")

        truncated = False
        if len(content) > MAX_READ_CHARS:
            content = content[:MAX_READ_CHARS]
            truncated = True

        other_refs = sorted(n for n in names if n.endswith(".md") and n != target_name)
        header = f"Isi '{zip_path}::{target_name}'"
        if truncated:
            header += f" (dipotong, {MAX_READ_CHARS} karakter pertama)"

        footer = ""
        if other_refs:
            footer = (
                "\n\n[File referensi lain yang tersedia di paket skill ini, "
                "panggil tool 'baca_referensi_skill' kalau perlu baca salah satunya: "
                + ", ".join(other_refs) + "]"
            )

        return f"{header}:\n\n{content}{footer}"


def baca_file(path: str) -> str:
    """Baca isi file teks (termasuk SKILL.md, atau paket .skill zip) di dalam BASE_DIR atau SKILL_DIR."""
    try:
        target = safe_resolve_read(path)
    except UnsafePathError as e:
        return f"DITOLAK: {e}"

    if not target.exists():
        return f"File '{target}' tidak ditemukan."
    if target.is_dir():
        return f"'{target}' itu folder, bukan file. Pakai list_folder buat lihat isinya."

    # Paket skill (.skill) itu sebenernya zip archive — auto-baca SKILL.md di dalemnya
    if target.suffix == ".skill" or zipfile.is_zipfile(target):
        return _read_skill_zip(target)

    try:
        content = target.read_text(encoding="utf-8", errors="replace")
    except Exception as e:
        return f"Gagal baca file '{target}': {e}"

    truncated = False
    if len(content) > MAX_READ_CHARS:
        content = content[:MAX_READ_CHARS]
        truncated = True

    header = f"Isi '{target}'"
    if truncated:
        header += f" (dipotong, {MAX_READ_CHARS} karakter pertama)"
    return f"{header}:\n\n{content}"


def baca_referensi_skill(path: str, referensi: str) -> str:
    """Baca satu file referensi spesifik di dalam paket .skill (zip) di SKILL_DIR, misal 'mikrotik' atau 'references/mikrotik.md'."""
    try:
        target = safe_resolve_skill(path)
    except UnsafePathError as e:
        return f"DITOLAK: {e}"

    if not target.exists():
        return f"File '{target}' tidak ditemukan."
    if not (target.suffix == ".skill" or zipfile.is_zipfile(target)):
        return f"'{target}' bukan paket .skill (zip). Pakai tool 'baca_file' buat file biasa."

    return _read_skill_zip(target, inner_path=referensi)


def cari_skill(path: str = ".") -> str:
    """Cari semua file SKILL.md (folder biasa) dan paket .skill (zip) di dalam SKILL_DIR (rekursif)."""
    try:
        target = safe_resolve_skill(path)
    except UnsafePathError as e:
        return f"DITOLAK: {e}"

    if not target.exists():
        return f"Folder '{target}' tidak ditemukan."

    skill_md = sorted(str(p.relative_to(SKILL_DIR)) for p in target.rglob("SKILL.md"))
    skill_zip = sorted(str(p.relative_to(SKILL_DIR)) for p in target.rglob("*.skill"))

    if not skill_md and not skill_zip:
        return f"Nggak ada SKILL.md atau paket .skill di dalam '{target}'."

    hasil = []
    if skill_md:
        hasil.append("SKILL.md (folder biasa):\n" + "\n".join(skill_md))
    if skill_zip:
        hasil.append("Paket .skill (zip, baca pakai tool 'baca_file'):\n" + "\n".join(skill_zip))
    return "\n\n".join(hasil)


def _wib_timezone():
    """Ambil zona WIB (Asia/Jakarta) via zoneinfo kalau tersedia, fallback ke offset tetap +7."""
    try:
        from zoneinfo import ZoneInfo
        return ZoneInfo("Asia/Jakarta")
    except Exception:
        return timezone(timedelta(hours=7))


_HARI_ID = {
    "Monday": "Senin", "Tuesday": "Selasa", "Wednesday": "Rabu", "Thursday": "Kamis",
    "Friday": "Jumat", "Saturday": "Sabtu", "Sunday": "Minggu",
}
_BULAN_ID = {
    1: "Januari", 2: "Februari", 3: "Maret", 4: "April", 5: "Mei", 6: "Juni",
    7: "Juli", 8: "Agustus", 9: "September", 10: "Oktober", 11: "November", 12: "Desember",
}


def waktu_sekarang() -> str:
    """Ambil tanggal & jam sekarang yang akurat (bukan tebakan dari training data), zona WIB (GMT+7 / Asia/Jakarta)."""
    now = datetime.now(_wib_timezone())
    hari = _HARI_ID.get(now.strftime("%A"), now.strftime("%A"))
    bulan = _BULAN_ID.get(now.month, str(now.month))
    tanggal_str = f"{hari}, {now.day} {bulan} {now.year}"
    jam_str = now.strftime("%H:%M:%S")
    return f"Sekarang: {tanggal_str}, jam {jam_str} WIB (GMT+7)."


# Registry: nama tool -> fungsi python asli
TOOL_REGISTRY = {
    "buat_folder": buat_folder,
    "hapus_folder": hapus_folder,
    "buat_file": buat_file,
    "hapus_file": hapus_file,
    "list_folder": list_folder,
    "baca_file": baca_file,
    "cari_skill": cari_skill,
    "baca_referensi_skill": baca_referensi_skill,
    "waktu_sekarang": waktu_sekarang,
}

# Skema tool yang dikirim ke model (format Ollama / OpenAI-style function calling)
TOOLS_SCHEMA = [
    {
        "type": "function",
        "function": {
            "name": "buat_folder",
            "description": "Membuat folder baru (beserta parent folder-nya kalau belum ada).",
            "parameters": {
                "type": "object",
                "properties": {
                    "path": {
                        "type": "string",
                        "description": "Path folder yang mau dibuat, relatif terhadap base directory.",
                    }
                },
                "required": ["path"],
            },
        },
    },
    {
        "type": "function",
        "function": {
            "name": "hapus_folder",
            "description": "Menghapus folder beserta seluruh isinya. Akan minta konfirmasi user kecuali mode --yolo aktif.",
            "parameters": {
                "type": "object",
                "properties": {
                    "path": {
                        "type": "string",
                        "description": "Path folder yang mau dihapus, relatif terhadap base directory.",
                    }
                },
                "required": ["path"],
            },
        },
    },
    {
        "type": "function",
        "function": {
            "name": "buat_file",
            "description": (
                "Membuat file baru berisi teks/kode (parent folder dibuat otomatis kalau belum ada). "
                "Kalau file sudah ada, harus set overwrite=true buat nimpa isinya."
            ),
            "parameters": {
                "type": "object",
                "properties": {
                    "path": {
                        "type": "string",
                        "description": "Path file yang mau dibuat, relatif terhadap base directory.",
                    },
                    "content": {
                        "type": "string",
                        "description": "Isi/konten file (teks atau kode). Default kosong.",
                    },
                    "overwrite": {
                        "type": "boolean",
                        "description": "True kalau mau menimpa file yang sudah ada. Default false.",
                    },
                },
                "required": ["path", "content"],
            },
        },
    },
    {
        "type": "function",
        "function": {
            "name": "hapus_file",
            "description": "Menghapus satu file. Akan minta konfirmasi user kecuali mode --yolo aktif.",
            "parameters": {
                "type": "object",
                "properties": {
                    "path": {
                        "type": "string",
                        "description": "Path file yang mau dihapus, relatif terhadap base directory.",
                    }
                },
                "required": ["path"],
            },
        },
    },
    {
        "type": "function",
        "function": {
            "name": "list_folder",
            "description": "Menampilkan isi sebuah folder (default: base directory).",
            "parameters": {
                "type": "object",
                "properties": {
                    "path": {
                        "type": "string",
                        "description": "Path folder yang mau dilihat isinya. Default '.' (base directory).",
                    }
                },
            },
        },
    },
    {
        "type": "function",
        "function": {
            "name": "baca_file",
            "description": (
                "Membaca isi sebuah file teks di dalam base directory ATAU skill directory "
                "(otomatis dicoba di base directory dulu, kalau nggak ketemu dicoba di skill "
                "directory), termasuk file SKILL.md. Selalu panggil ini untuk baca SKILL.md "
                "dulu SEBELUM mengerjakan task yang berhubungan dengan skill tersebut, biar "
                "kerjaannya sesuai konvensi yang ada."
            ),
            "parameters": {
                "type": "object",
                "properties": {
                    "path": {
                        "type": "string",
                        "description": "Path file yang mau dibaca, relatif terhadap base directory.",
                    }
                },
                "required": ["path"],
            },
        },
    },
    {
        "type": "function",
        "function": {
            "name": "cari_skill",
            "description": "Mencari semua SKILL.md (folder biasa) dan paket .skill (zip) secara rekursif di dalam skill directory, buat tahu skill apa aja yang tersedia sebelum mulai kerja.",
            "parameters": {
                "type": "object",
                "properties": {
                    "path": {
                        "type": "string",
                        "description": "Folder awal pencarian, relatif terhadap skill directory. Default '.' (root skill directory).",
                    }
                },
            },
        },
    },
    {
        "type": "function",
        "function": {
            "name": "baca_referensi_skill",
            "description": (
                "Membaca satu file referensi spesifik di dalam paket .skill (zip), "
                "misal 'mikrotik' atau 'references/mikrotik.md'. Panggil ini kalau "
                "SKILL.md yang sudah dibaca (lewat baca_file) menyebut file referensi "
                "lain yang relevan sama task yang lagi dikerjakan."
            ),
            "parameters": {
                "type": "object",
                "properties": {
                    "path": {
                        "type": "string",
                        "description": "Path ke file .skill (zip), relatif terhadap skill directory.",
                    },
                    "referensi": {
                        "type": "string",
                        "description": "Nama file referensi yang mau dibaca, misal 'mikrotik' atau 'references/mikrotik.md'.",
                    },
                },
                "required": ["path", "referensi"],
            },
        },
    },
    {
        "type": "function",
        "function": {
            "name": "waktu_sekarang",
            "description": (
                "Mengambil tanggal & jam saat ini secara akurat (zona WIB/Asia Jakarta, GMT+7). "
                "WAJIB dipanggil setiap kali user nanya tanggal, hari, atau jam sekarang — "
                "jangan pernah nebak dari training data karena pasti udah basi."
            ),
            "parameters": {
                "type": "object",
                "properties": {},
            },
        },
    },
]


# ── Main loop ────────────────────────────────────────────────────────────

# Pesan "lagi ngapain" (sebelum eksekusi) & "udah kelar" (sesudah sukses) per tool,
# biar user liat status yang natural daripada dump mentah tool-call/JSON.
TOOL_STATUS = {
    "buat_folder": ("📁 Sabar, gua buat dulu foldernya...", "✅ Foldernya udah jadi."),
    "hapus_folder": ("🗑️  Sabar, gua hapus dulu foldernya...", "✅ Foldernya udah kehapus."),
    "buat_file": ("📝 Sabar, gua buat dulu filenya...", "✅ Filenya udah jadi."),
    "hapus_file": ("🗑️  Sabar, gua hapus dulu filenya...", "✅ Filenya udah kehapus."),
    "list_folder": ("👀 Sabar, gua cek dulu isi foldernya...", "✅ Udah gua cek isinya."),
    "baca_file": ("📖 Sabar, gua baca dulu filenya...", "✅ Udah gua baca."),
    "cari_skill": ("🔍 Sabar, gua cari skillnya dulu...", "✅ Udah ketemu skillnya."),
    "baca_referensi_skill": ("📚 Sabar, gua baca referensi skill-nya dulu...", "✅ Udah gua baca referensinya."),
    "waktu_sekarang": ("⏰ Sabar, gua cek jam berapa sekarang...", "✅ Nih waktunya."),
}


def run_tool_call(tool_call, force_delete: bool, verbose: bool = False) -> dict:
    name = tool_call["function"]["name"]
    args = tool_call["function"].get("arguments", {}) or {}

    before_msg, after_msg = TOOL_STATUS.get(name, (f"⚙️  Sabar, gua jalanin '{name}' dulu...", "✅ Selesai."))
    print(before_msg)

    fn = TOOL_REGISTRY.get(name)
    if fn is None:
        result = f"Tool '{name}' tidak dikenal."
    else:
        try:
            if name in ("hapus_folder", "hapus_file"):
                result = fn(args.get("path", "."), force=force_delete)
            else:
                result = fn(**args)
        except Exception as e:
            # Jaring pengaman terakhir: apapun errornya, jangan sampe script mati total.
            result = f"GAGAL: terjadi error nggak terduga pas jalanin '{name}': {e}"

    # Status akhir disesuaikan sama isi hasilnya, bukan cuma nembak "sukses" mentah-mentah.
    if result.startswith(("DITOLAK", "GAGAL")):
        print(f"⚠️  {result}")
    elif result.startswith("Dibatalkan oleh user"):
        print(f"🚫 {result}")
    elif result.lower().startswith(("nggak ada", "nggak ketemu")):
        print(f"😕 {result}")
    else:
        print(after_msg)

    if verbose:
        print(f"   [debug] {name}({args}) => {result}")

    return {"role": "tool", "content": result}


def main():
    parser = argparse.ArgumentParser(description="Asisten folder via Ollama Cloud")
    parser.add_argument(
        "--yolo",
        action="store_true",
        help="Skip konfirmasi manual sebelum menghapus folder/file (HATI-HATI).",
    )
    parser.add_argument(
        "--verbose",
        action="store_true",
        help="Tampilin detail mentah tiap tool call (nama, argumen, hasil) buat debugging.",
    )
    parser.add_argument(
        "--model", default=MODEL, help=f"Nama model Ollama Cloud (default: {MODEL})"
    )
    args = parser.parse_args()

    print(f"Base directory kerja (buat_folder/hapus_folder/buat_file/hapus_file): {BASE_DIR}")
    print(f"Skill directory (cari_skill/baca_referensi_skill): {SKILL_DIR}")
    print(f"Model: {args.model}")
    if _OLLAMA_HOST:
        print(f"Ollama host (dari .env): {_OLLAMA_HOST}")
    if args.yolo:
        print("⚠️  Mode --yolo aktif: hapus folder/file TANPA konfirmasi!")

    skill_files = sorted(str(p.relative_to(SKILL_DIR)) for p in SKILL_DIR.rglob("SKILL.md"))
    skill_packages = sorted(str(p.relative_to(SKILL_DIR)) for p in SKILL_DIR.rglob("*.skill"))
    if skill_files or skill_packages:
        for s in skill_files:
            print(f"  - {s}")
        for s in skill_packages:
            print(f"  - {s}  (paket .skill/zip)")
        print(f"Ketemu {len(skill_files) + len(skill_packages)} skill.")
    else:
        print("Nggak ada SKILL.md / paket .skill di skill directory (model tetep bisa cari manual pakai tool cari_skill).")

    print("Ketik pesan kamu (atau '/exit' untuk keluar).\n")

    messages = [{"role": "system", "content": SYSTEM_PROMPT}]

    while True:
        user_input = input("Kamu: ").strip()
        if user_input.lower() in ("exit", "quit", "keluar", "/exit", "/quit", "/keluar"):
            print("Sampai jumpa, Bos.")
            break
        if not user_input:
            continue

        messages.append({"role": "user", "content": user_input})

        # Loop supaya model bisa memanggil tool berkali-kali sebelum jawab final
        while True:
            print("🤔 Sabar ya, gua lagi mikir...")
            try:
                response = ollama_client.chat(
                    model=args.model,
                    messages=messages,
                    tools=TOOLS_SCHEMA,
                )
            except Exception as e:
                print(f"⚠️  Gagal ngobrol ke model: {e}\n")
                messages.pop()  # buang pesan user yang gagal diproses biar gak nyangkut
                break

            msg = response["message"]
            messages.append(msg)

            tool_calls = msg.get("tool_calls")
            if not tool_calls:
                print("💡 Nah, udah kelar nih mikirnya.")
                print(f"Asisten: {msg.get('content', '')}\n")
                break

            for tc in tool_calls:
                tool_result = run_tool_call(tc, force_delete=args.yolo, verbose=args.verbose)
                messages.append(tool_result)
            # lanjut loop: kirim balik hasil tool ke model untuk direspon


if __name__ == "__main__":
    main()
