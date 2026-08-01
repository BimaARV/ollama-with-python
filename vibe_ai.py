#!/usr/bin/env python3
"""
vibe_agent.py — Asisten pribadi berbasis Ollama Cloud (MiniMax)
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

try:
    import ollama
except ImportError:
    print("Package 'ollama' belum terinstall. Jalankan: pip install ollama")
    sys.exit(1)

try:
    from dotenv import load_dotenv

    load_dotenv()  # baca .env di direktori kerja saat ini
except ImportError:
    print(
        "Package 'python-dotenv' belum terinstall. Jalankan: pip install python-dotenv"
    )
    sys.exit(1)


# ── Konfigurasi (diambil dari .env / environment variable) ─────────────────

MODEL = os.environ.get("VIBE_MODEL", "nemotron-3-ultra:cloud")  # sesuaikan nama model cloud kamu
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

Selalu konfirmasi ulang ke user dalam bahasa natural setelah tool selesai dijalankan.
Jangan pernah mengarang hasil — selalu panggil tool untuk aksi nyata di filesystem.
Jawab santai, agak nge gas, sarkas, kasar (jing (anjing), tod (ngentod), mek (memek), tol (kontol), bangsat, tolol, goblok, bego, pekok, ndelogok, asu, tempik, peli, bisa bahasa kasar Jawa. bahasa kasar jangan terlalu sering kecuali kalau konteksnya emosi),
bisa jokes bapak bapak, selalu panggil gua BOS Bima atau Bos, ringkas, pakai Bahasa Indonesia Gaul (Gua, Lu). Kurang kurangin typo, jangan terlalu formal juga. jangan lupa untuk timezone di sesuaikan dengan WIB (GMT+7) atau zona waktu Asia/Jakarta dengan akurat.
"""


# ── Helper: batasi path supaya nggak keluar dari root yang diizinkan ───────


class UnsafePathError(Exception):
    pass


def _resolve_in_root(path_str: str, root: Path) -> Path:
    p = (root / path_str).resolve()
    if root not in p.parents and p != root:
        raise UnsafePathError(
            f"Path '{path_str}' berada di luar area yang diizinkan ({root})."
        )
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


# ── Tool implementations ────────────────────────────────────────────────────


def buat_folder(path: str) -> str:
    try:
        target = safe_resolve(path)
    except UnsafePathError as e:
        return f"DITOLAK: {e}"

    if target.exists():
        return f"Folder '{target}' sudah ada, nggak perlu dibuat lagi."

    target.mkdir(parents=True, exist_ok=True)
    return f"Berhasil membuat folder: {target}"


def hapus_folder(path: str, force: bool = False) -> str:
    try:
        target = safe_resolve(path)
    except UnsafePathError as e:
        return f"DITOLAK: {e}"

    if not target.exists():
        return f"Folder '{target}' tidak ditemukan, nggak ada yang dihapus."

    if target == BASE_DIR:
        return "DITOLAK: nggak boleh menghapus base directory itu sendiri."

    if not force:
        jawab = (
            input(
                f"\n⚠️  Model minta izin HAPUS folder: {target}\n"
                f"   Isinya: {list(target.iterdir())[:5]}{'...' if len(list(target.iterdir())) > 5 else ''}\n"
                f"   Yakin hapus? (y/N): "
            )
            .strip()
            .lower()
        )
        if jawab != "y":
            return f"Dibatalkan oleh user. Folder '{target}' TIDAK dihapus."

    shutil.rmtree(target)
    return f"Berhasil menghapus folder: {target}"


def buat_file(path: str, content: str = "", overwrite: bool = False) -> str:
    try:
        target = safe_resolve(path)
    except UnsafePathError as e:
        return f"DITOLAK: {e}"

    if target.exists() and not overwrite:
        return (
            f"File '{target}' sudah ada. Panggil lagi dengan overwrite=true "
            f"kalau memang mau menimpa isinya."
        )

    target.parent.mkdir(parents=True, exist_ok=True)
    target.write_text(content, encoding="utf-8")
    verb = "menimpa" if target.exists() and overwrite else "membuat"
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
        jawab = (
            input(
                f"\n⚠️  Model minta izin HAPUS file: {target}\n   Yakin hapus? (y/N): "
            )
            .strip()
            .lower()
        )
        if jawab != "y":
            return f"Dibatalkan oleh user. File '{target}' TIDAK dihapus."

    target.unlink()
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
            candidates = {
                inner_path,
                f"references/{inner_path}",
                f"references/{inner_path}.md",
            }
            matches = [
                n for n in names if n in candidates or n.endswith(f"/{inner_path}")
            ]
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
                + ", ".join(other_refs)
                + "]"
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
        return (
            f"'{target}' itu folder, bukan file. Pakai list_folder buat lihat isinya."
        )

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
        hasil.append(
            "Paket .skill (zip, baca pakai tool 'baca_file'):\n" + "\n".join(skill_zip)
        )
    return "\n\n".join(hasil)


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
]


# ── Main loop ────────────────────────────────────────────────────────────


def run_tool_call(tool_call, force_delete: bool) -> dict:
    name = tool_call["function"]["name"]
    args = tool_call["function"].get("arguments", {}) or {}

    fn = TOOL_REGISTRY.get(name)
    if fn is None:
        result = f"Tool '{name}' tidak dikenal."
    else:
        if name in ("hapus_folder", "hapus_file"):
            result = fn(args.get("path", "."), force=force_delete)
        else:
            result = fn(**args)

    print(f"   → [{name}({args})] => {result}")
    return {"role": "tool", "content": result}


def main():
    parser = argparse.ArgumentParser(description="Asisten folder via Ollama Cloud")
    parser.add_argument(
        "--yolo",
        action="store_true",
        help="Skip konfirmasi manual sebelum menghapus folder (HATI-HATI).",
    )
    parser.add_argument(
        "--model", default=MODEL, help=f"Nama model Ollama Cloud (default: {MODEL})"
    )
    args = parser.parse_args()

    print(
        f"Base directory kerja (buat_folder/hapus_folder/buat_file/hapus_file): {BASE_DIR}"
    )
    print(f"Skill directory (cari_skill/baca_referensi_skill): {SKILL_DIR}")
    print(f"Model: {args.model}")
    if _OLLAMA_HOST:
        print(f"Ollama host (dari .env): {_OLLAMA_HOST}")
    if args.yolo:
        print("⚠️  Mode --yolo aktif: hapus folder TANPA konfirmasi!")

    skill_files = sorted(
        str(p.relative_to(SKILL_DIR)) for p in SKILL_DIR.rglob("SKILL.md")
    )
    skill_packages = sorted(
        str(p.relative_to(SKILL_DIR)) for p in SKILL_DIR.rglob("*.skill")
    )
    if skill_files or skill_packages:
        for s in skill_files:
            print(f"  - {s}")
        for s in skill_packages:
            print(f"  - {s}  (paket .skill/zip)")
        print(f"Ketemu {len(skill_files) + len(skill_packages)} skill.")
    else:
        print(
            "Nggak ada SKILL.md / paket .skill di skill directory (model tetep bisa cari manual pakai tool cari_skill)."
        )

    print("Ketik pesan kamu (atau '/exit' untuk keluar).\n")

    messages = [{"role": "system", "content": SYSTEM_PROMPT}]

    while True:
        user_input = input("Kamu: ").strip()
        if user_input.lower() in (
            "exit",
            "quit",
            "keluar",
            "/exit",
            "/quit",
            "/keluar",
        ):
            print("Sampai jumpa, Bos.")
            break
        if not user_input:
            continue

        messages.append({"role": "user", "content": user_input})

        # Loop supaya model bisa memanggil tool berkali-kali sebelum jawab final
        while True:
            response = ollama_client.chat(
                model=args.model,
                messages=messages,
                tools=TOOLS_SCHEMA,
            )

            msg = response["message"]
            messages.append(msg)

            tool_calls = msg.get("tool_calls")
            if not tool_calls:
                print(f"Asisten: {msg.get('content', '')}\n")
                break

            for tc in tool_calls:
                tool_result = run_tool_call(tc, force_delete=args.yolo)
                messages.append(tool_result)
            # lanjut loop: kirim balik hasil tool ke model untuk direspon


if __name__ == "__main__":
    main()
