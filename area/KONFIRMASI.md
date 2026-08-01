# Konfirmasi Sebelum Bikin Project

Bos, sebelum gue bikin semua filenya, ini yang perlu loe konfirmasi:

## A. Skala & Target
1. [ ] Single Bahasa (Indonesia aja) atau Multi-bahasa?
2. [ ] User publik boleh daftar & ikut ujian, atau cuma staff/admin yang ngisi?
3. [ ] Ujian ada timer count-down & auto-submit kalo waktu habis?
4. [ ] Hasil ujian langsung keluar (skor) atau di-review admin dulu?

## B. Tipe Soal Ujian
- [ ] Pilihan Ganda (single answer)
- [ ] Pilihan Ganda Kompleks (multiple answer)
- [ ] Benar/Salah
- [ ] Esai (manual grading)
- [ ] Matching/pasangan (opsional)
- [ ] Angka/isian (koreksi otomatis)

## C. Baileys / WA Gateway
- [ ] Loe udah punya service baileys-server jalan di mana? (URL endpoint?)
- [ ] Format request API-nya gimana? (default: POST /send-message)
- [ ] Butuh fitur apa aja? (kirim pesan / receive webhook / reconnect QR display di admin?)

## D. Frontend Style
- [ ] Minimalis / Academia / Tech / Custom tema?
- [ ] Butuh dark mode?
- [ ] Bahasa Indonesia aja?

## E. Database
- [ ] MySQL 8.x (recommended)
- [ ] MariaDB 10.x (juga oke)
- [ ] PostgreSQL (kalo loe prefer ini)

## F. Deployment
- [ ] Deploy ke VPS langsung (Ubuntu, Nginx, PHP-FPM)?
- [ ] Pakai Docker?
- [ ] Pakai Laravel Forge/Ploi?
- [ ] Shared hosting (Lumens / Niagahoster / dll) — bakal tricky buat Filament tapi possible

## G. Feature Tambahan
- [ ] Komentar di blog? (butuh moderasi)
- [ ] Newsletter / Subscribe email?
- [ ] Search fitur?
- [ ] RSS feed?
- [ ] Sitemap.xml auto-generated?
- [ ] Quiz random / shuffle soal & jawaban?
