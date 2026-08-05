# AGENTS.md

Panduan buat AI agent yang kerja di workspace **Haruna Noa** (milik **Bos Bima** — NOC engineer + punya RT/RW Net ISP). Baca dulu sebelum ngapa-ngapain, biar kerjaannya gak melenceng.

---

## 1. Identitas Workspace

- **Nama project**: Blog Website
- **Owner**: Dewangga Bima

---

## 2. Zona Waktu

- Default: **WIB / Asia Jakarta (UTC+7)**
- Semua hal, tanggal/jam — log timestamp, jadwal, deadline, "hari ini" — pake WIB.

---

## 3. Daftar Project

Setiap project punya direktori kerja sendiri di **luar** workspace ini. Tiap project mungkin punya skill/konvensi sendiri — agent **wajib** baca section project yang relevan dulu.

| Project                        | Direktori                                          | Section                                |
| ------------------------------ | -------------------------------------------------- | -------------------------------------- |
| Blog Website Next.js + MariaDB | `/home/deimonji/rahasia-negara/vibe-code/blog-web` | [§ 4](#4-blog-website-nextjs--mariadb) |

---

## 4. Blog Website (Next.js + MariaDB)

> **Base directory kerja project ini**: `/home/deimonji/rahasia-negara/vibe-code/blog-web`
> Semua path file relatif ke direktori itu.

### 4.1 Requirement (dari Bos)

Bikin website blog dengan spek:

- **Stack**: JavaScript (ES2022+), **Next.js**, **MariaDB 12**, **Tailwind** (atau CSS Modules).
- **Admin-only posting**: cuma admin yang bisa upload / buat / edit / hapus post.
- **User biasa**: cuma bisa login + kasih komentar.
- **Kategori**: setiap post punya 1 kategori, list kategori dari admin.
- **Search**: bisa lewat judul, kategori, tanggal (range). Paging.
- **Sort**: default **terbaru → terlama**, toggle ke terlama → terbaru.
- **Pemisahan login**:
  - User biasa: `/login`
  - Admin: `/login-admin`
- **Forgot password** endpoint: `/forgot-password` (kirim kode via SMTP).
- **Profile**: `/profiles` buat user & admin. Gunakan **UUID** untuk public access.
- **Dashboard admin** punya tab/navbar terpisah salah satunya **SMTP** (setting email server).
- **Password hashing**: **MD5 + salt** sesuai spek Bos (lihat §7.4 soal pepper).

### 4.2 Routing (WAJIB)

#### Public
- `/` — list post published
- `/posts/[slug]` — detail post + form komentar (login required untuk komen)
- `/category/[slug]` — post per kategori
- `/search?q=&category=&date_from=&date_to=&sort=` — hasil search (newest/oldest)
- `/login` — login user biasa
- `/login-admin` — login admin
- `/register` — registrasi user biasa (gak ada register admin)
- `/forgot-password` + `/forgot-password/verify` — flow reset
- `/profiles` — profile sendiri (butuh login)
- `/profiles/[uuid]` — profile publik (**Wajib pakai UUID**, bukan Integer ID)

#### Admin (`/admin/*`, wajib session admin)
- `/admin` — dashboard
- `/admin/posts` — list semua post
- `/admin/posts/new` + `/admin/posts/[id]/edit` — CRUD post
- `/admin/categories` — CRUD kategori
- `/admin/comments` — moderasi komentar
- `/admin/users` — list user (read only)
- **`/admin/smtp`** — setting SMTP (kirim kode forgot password)
- `/admin/settings` — setting umum situs
- `/admin/domains` — setting untuk mengganti domain (bisa pointing langsung atau lewat cloudflare zero trust)

### 4.3 Role & Akses

| Role  | Tabel    | Bisa                                                                                               |
| ----- | -------- | -------------------------------------------------------------------------------------------------- |
| Admin | `admins` | CRUD post/kategori/komentar, konfig SMTP, lihat list user                                          |
| User  | `users`  | Login, komentar (default `pending`), edit profile, hapus komentar sendiri. **Gak bisa bikin post** |

- `/login` cuma valid untuk `users`. `/login-admin` cuma valid untuk `admins`.
- Middleware harus strict: `/admin/*` wajib session admin, post/comment wajib session user.
- User biasa **gak boleh** bikin akun admin dari mana pun.

### 4.4 Database Schema (MariaDB 10.6+)

Simpen di `db/schema.sql`. Semua table **InnoDB**, **utf8mb4**.

```sql
CREATE TABLE admins (
  id INT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
  uuid CHAR(36) NOT NULL UNIQUE,           -- Untuk akses public profile admin
  username VARCHAR(64) NOT NULL UNIQUE,
  email VARCHAR(191) NOT NULL UNIQUE,
  display_name VARCHAR(128),
  password_hash CHAR(32) NOT NULL,         -- MD5 hex (sesuai spek Bos)
  salt VARCHAR(64) NOT NULL,
  is_locked TINYINT(1) NOT NULL DEFAULT 0,
  failed_attempts INT NOT NULL DEFAULT 0,
  last_login_at DATETIME NULL,
  last_login_ip VARCHAR(45) NULL,
  created_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
  updated_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

CREATE TABLE users (
  id INT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
  uuid CHAR(36) NOT NULL UNIQUE,           -- Untuk akses public profile user (Anti-IDOR)
  username VARCHAR(64) NOT NULL UNIQUE,
  email VARCHAR(191) NOT NULL UNIQUE,
  display_name VARCHAR(128),
  avatar_url VARCHAR(255),
  password_hash CHAR(32) NOT NULL,
  salt VARCHAR(64) NOT NULL,
  is_locked TINYINT(1) NOT NULL DEFAULT 0,
  failed_attempts INT NOT NULL DEFAULT 0,
  last_login_at DATETIME NULL,
  created_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
  updated_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

CREATE TABLE categories (
  id INT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
  name VARCHAR(64) NOT NULL UNIQUE,
  slug VARCHAR(64) NOT NULL UNIQUE,
  description TEXT,
  created_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

CREATE TABLE posts (
  id INT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
  admin_id INT UNSIGNED NOT NULL,
  category_id INT UNSIGNED NULL,
  title VARCHAR(255) NOT NULL,
  slug VARCHAR(255) NOT NULL UNIQUE,
  excerpt TEXT,
  content LONGTEXT NOT NULL,
  cover_image VARCHAR(255),
  status ENUM('draft','published') NOT NULL DEFAULT 'draft',
  published_at DATETIME NULL,
  view_count INT UNSIGNED NOT NULL DEFAULT 0,
  created_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
  updated_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  CONSTRAINT fk_post_admin    FOREIGN KEY (admin_id)    REFERENCES admins(id)    ON DELETE RESTRICT,
  CONSTRAINT fk_post_category FOREIGN KEY (category_id) REFERENCES categories(id) ON DELETE SET NULL,
  INDEX idx_status_published (status, published_at),
  INDEX idx_admin (admin_id),
  INDEX idx_category (category_id),
  FULLTEXT INDEX ft_title (title, excerpt)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

CREATE TABLE comments (
  id INT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
  user_id INT UNSIGNED NOT NULL,
  post_id INT UNSIGNED NOT NULL,
  parent_id INT UNSIGNED NULL,
  body TEXT NOT NULL,
  status ENUM('pending','approved','spam','rejected') NOT NULL DEFAULT 'pending',
  ip_address VARCHAR(45),
  created_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
  CONSTRAINT fk_comment_user   FOREIGN KEY (user_id)   REFERENCES users(id)    ON DELETE CASCADE,
  CONSTRAINT fk_comment_post   FOREIGN KEY (post_id)   REFERENCES posts(id)    ON DELETE CASCADE,
  CONSTRAINT fk_comment_parent FOREIGN KEY (parent_id) REFERENCES comments(id) ON DELETE CASCADE,
  INDEX idx_post_status (post_id, status, created_at)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

CREATE TABLE sessions (
  id CHAR(64) PRIMARY KEY,
  account_type ENUM('user','admin') NOT NULL,
  account_id INT UNSIGNED NOT NULL,
  csrf_token CHAR(64) NOT NULL,
  ip_address VARCHAR(45),
  user_agent VARCHAR(255),
  expires_at DATETIME NOT NULL,
  created_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
  INDEX idx_expiry (expires_at),
  INDEX idx_account (account_type, account_id)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

CREATE TABLE login_attempts (
  id BIGINT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
  account_type ENUM('user','admin') NOT NULL,
  identifier VARCHAR(191),
  success TINYINT(1) NOT NULL,
  ip_address VARCHAR(45),
  user_agent VARCHAR(255),
  attempted_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
```

---

## 5. Standar Coding & Konvensi

- **Naming**: 
  - Components: PascalCase (`Header.tsx`, `PostCard.tsx`).
  - Routes/Folders: kebab-case (`/admin/post-settings`).
  - Variables/Functions: camelCase (`getUserData`, `isLoggedIn`).
- **State Management**: Gunakan React Context atau Zustand kalau perlu, jangan over-engineering.
- **CSS**: Tailwind CSS. Utamakan utility classes, pakai `@apply` hanya untuk element yang sangat repetitif.

---

## 6. Environment Variables (`.env`)

Agent wajib memastikan file `.env` memiliki key berikut:
- `DATABASE_URL`: Connection string MariaDB.
- `NEXTAUTH_SECRET`: Secret key untuk session.
- `SMTP_HOST`, `SMTP_PORT`, `SMTP_USER`, `SMTP_PASS`: Untuk pengiriman email.
- `APP_PEPPER`: String rahasia untuk tambahan hashing password.
- `SITE_URL`: Domain utama website.

---

## 7. Security Framework (SUPER STRICT)

### 7.1 Input Validation & Sanitization
- **No Trust**: Semua input dari user (Query string, Form body, Header) **WAJIB** divalidasi menggunakan `Zod` atau library serupa.
- **Sanitization**: Konten yang menggunakan `dangerouslySetInnerHTML` wajib melewati `DOMPurify` atau sanitizer server-side untuk mencegah XSS.
- **Type Casting**: Pastikan ID yang diterima dari URL dikonversi ke integer sebelum masuk ke query.

### 7.2 Database Security
- **Parameterized Queries**: Dilarang keras pakai template strings untuk query SQL. Wajib gunakan `?` placeholder atau Prepared Statements.
- **Least Privilege**: User database yang dipakai aplikasi tidak boleh punya akses `SUPER` atau `FILE`.
- **Error Masking**: Jangan pernah menampilkan error database mentah (`sql state`, `table name`) ke end-user. Gunakan generic error message.
- **Anti-IDOR**: Untuk endpoint publik (seperti profile), **dilarang keras** menggunakan Integer ID. Wajib menggunakan `uuid` (CHAR 36).

### 7.3 API Security
- **CORS Policy**: Konfigurasikan CORS hanya untuk domain yang terpercaya. Jangan pakai `*` di production.
- **Rate Limiting**: Terapkan rate limit per IP untuk semua endpoint API guna mencegah DoS dan Brute Force.
- **JWT/Session Hardening**: Jika menggunakan API stateless, pastikan token memiliki expiry time yang pendek dan mekanisme refresh token yang aman.
- **HTTP Method Strictness**: Pastikan endpoint hanya menerima method yang sesuai (misal: GET untuk read, POST untuk create).

### 7.4 Authentication & Session Hardening
- **Session Fixation**: Generate session ID baru setiap kali user login.
- **Cookie Security**: Set cookie dengan flag `HttpOnly`, `Secure`, dan `SameSite=Lax/Strict`.
- **CSRF Protection**: Wajib ada token CSRF untuk semua request yang mengubah state (POST, PUT, DELETE).
- **Admin Lock**: Akses `/admin/*` harus dicek di level Middleware (server-side), bukan cuma hide element di UI.

### 7.5 Password Hashing (Spek Bos Bima)
- **Formula**: `MD5(password + salt + pepper)`.
- **Salt**: Unique random string per user (stored in DB).
- **Pepper**: Global secret string (stored in `.env` only).
- **Strictness**: Meskipun MD5 sudah usang, implementasi harus presisi. Jika ditemukan celah bypass, agent wajib lapor ke Bos Bima.

### 7.6 Brute Force & Attack Prevention
- **Rate Limiting**: Limit request pada endpoint sensitif (`/login`, `/login-admin`, `/forgot-password`).
- **Account Lockout**: Kunci akun (`is_locked = 1`) jika `failed_attempts` mencapai batas tertentu (misal: 5 kali).
- **Login Logging**: Catat semua percobaan login (berhasil/gagal) beserta IP dan User Agent ke tabel `login_attempts`.
- **SMTP Security**: Gunakan koneksi TLS/SSL untuk pengiriman email kode reset password.

---

## 8. Definition of Done (DoD)

Sebuah fitur dianggap selesai jika:
1. Kode mengikuti konvensi di §5.
2. Sudah melewati checklist keamanan di §7 (Zero SQLi, Zero XSS, Zero IDOR).
3. Berjalan lancar di browser dan responsif di semua device.
4. Alur role-based access (Admin vs User) sudah teruji strict.
5. Tidak ada console error dan logging sudah berjalan sebagaimana mestinya.
