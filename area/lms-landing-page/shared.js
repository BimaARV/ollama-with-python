// ============================================
// LMS Blog - Shared Mock Data & Utilities
// Simulasi Full-Stack di Frontend Only (localStorage)
// ============================================

const STORAGE_KEYS = {
  USERS: 'lms_users',
  COURSES: 'lms_courses',
  BLOG_POSTS: 'lms_blog_posts',
  ENROLLMENTS: 'lms_enrollments',
  CURRENT_USER: 'lms_current_user',
  SETTINGS: 'lms_settings'
};

// ---------- Default Seed Data ----------
const DEFAULT_COURSES = [
  {
    id: 1,
    slug: 'mastering-docker-k8s',
    title: 'Mastering Docker & Kubernetes',
    shortDesc: 'Belajar containerization sampai lu bisa deploy ribuan app tanpa nangis.',
    longDesc: `## Apa yang Akan Lu Dapatin?

**Module 1: Docker Fundamentals**
- Container vs VM: kenapa Docker lebih mantap
- Dockerfile, Image, Container lifecycle
- Multi-stage build biar image kecil
- Docker Compose buat local dev

**Module 2: Kubernetes Dasar**
- Arsitektur K8s: Master, Worker, etcd, kubelet
- Pod, Service, Deployment, ConfigMap, Secret
- Ingress Controller & TLS termination
- Helm Charts buat packaging

**Module 3: Production Ready**
- Rolling update & rollback strategy
- Resource limits, requests, HPA
- Monitoring pake Prometheus + Grafana
- Logging centralized pake ELK/Loki

**Module 4: Advanced & Troubleshooting**
- Network policies & CNI
- Persistent Volume & StorageClass
- Debugging crashloopbackoff, OOMKilled
- Cost optimization di cloud

**Bonus:** CI/CD pipeline pake GitHub Actions → deploy ke EKS/GKE/AKS.`,
    thumbnail: 'https://cdn-icons-png.flaticon.com/512/2862/2862910.png',
    category: 'DevOps',
    level: 'Advanced',
    price: 499000,
    originalPrice: 799000,
    rating: 4.9,
    totalReviews: 342,
    totalStudents: 2847,
    duration: '12 jam 30 menit',
    lessons: 48,
    instructor: { id: 1, name: 'Bima The Boss', avatar: 'https://i.pravatar.cc/100?u=bima' },
    tags: ['Docker', 'Kubernetes', 'DevOps', 'Cloud'],
    isPublished: true,
    createdAt: '2024-01-15T10:00:00Z',
    updatedAt: '2024-06-20T14:30:00Z'
  },
  {
    id: 2,
    slug: 'advanced-networking',
    title: 'Advanced Networking: Routing, Switching & Security',
    shortDesc: 'Bongkar rahasia routing, switching, dan security network tingkat tinggi.',
    longDesc: `## Kurikulum Lengkap

**Bagian 1: Routing Protocol Lanjutan**
- OSPF Multi-area, Route Summarization, Virtual Link
- BGP: eBGP vs iBGP, Path Attributes, Route Reflector
- Policy-Based Routing & VRF Lite
- Redistribution antar routing protocol

**Bagian 2: Switching Enterprise**
- VLAN, Trunk, VTP, DTP
- Spanning Tree: PVST+, Rapid PVST+, MST
- EtherChannel (LACP/PAgP), StackWise
- Private VLAN & Port Security

**Bagian 3: Network Security**
- AAA (RADIUS/TACACS+), 802.1X
- Firewall: ASA, Zone-Based Firewall
- VPN: Site-to-Site IPsec, SSL VPN, DMVPN
- Threat Defense: IPS/IDS, AMP

**Bagian 4: Automation & Programmability**
- NETCONF/RESTCONF, YANG Models
- Ansible untuk Network Automation
- Python + Netmiko/NAPALM
- GitOps untuk Network Config

**Labs:** Semua pakai Cisco CML / EVE-NG / GNS3. Bisa dijalankan di laptop biasa.`,
    thumbnail: 'https://cdn-icons-png.flaticon.com/512/2362/2362442.png',
    category: 'Networking',
    level: 'Expert',
    price: 749000,
    originalPrice: 1200000,
    rating: 4.8,
    totalReviews: 187,
    totalStudents: 1203,
    duration: '18 jam 45 menit',
    lessons: 62,
    instructor: { id: 2, name: 'Ahmad Networker', avatar: 'https://i.pravatar.cc/100?u=ahmad' },
    tags: ['CCIE', 'Routing', 'Switching', 'Security', 'Automation'],
    isPublished: true,
    createdAt: '2024-02-10T08:00:00Z',
    updatedAt: '2024-07-01T11:00:00Z'
  },
  {
    id: 3,
    slug: 'laravel-11-mastery',
    title: 'Laravel 11 Mastery: Dari Zero ke Enterprise',
    shortDesc: 'Bangun aplikasi enterprise dengan standar industri tanpa error bego.',
    longDesc: `## Kenapa Kursus Ini Beda?

Banyak kursus Laravel cuma ngajarin "cara bikin CRUD". Ini beda — gua ngajarin **pola pikir senior dev** biar code lu maintainable, scalable, & testable.

**Module 1: Foundation Solid**
- Laravel 11 Structure & Bootstrap Process
- Service Container & Service Provider (paham bener, bukan hafal)
- Facades vs Dependency Injection
- Config, Env, & Multiple Environment

**Module 2: Database & Eloquent Pro**
- Migration Best Practice (naming, index, foreign key)
- Eloquent Relationships: HasOne, HasMany, BelongsTo, ManyToMany, Polymorphic
- Query Optimization: Eager Loading, Chunk, Cursor
- Database Transactions & Locking

**Module 3: Architecture Patterns**
- Repository Pattern + Interface Binding
- Action/Service Classes (Single Responsibility)
- Form Request Validation & Custom Rules
- API Resources & Transformers

**Module 4: Advanced Features**
- Queue & Worker: Redis, Horizon, Retry Strategy
- Event Broadcasting: Laravel Reverb / Pusher
- Task Scheduling & Cron Jobs
- File Storage: S3, Local, Cloudflare R2

**Module 5: Testing & Quality**
- Pest PHP: Unit, Feature, Browser Testing
- TDD Workflow nyata
- Static Analysis: Larastan/PHPStan Level 8
- Code Style: Laravel Pint

**Module 6: Production Deployment**
- Octane (Swoole/RoadRunner) untuk performance
- Docker Multi-stage Build
- CI/CD: GitHub Actions → Deploy ke VPS/K8s
- Monitoring: Telescope, Pulse, Sentry

**Project Akhir:** Bangun **SaaS Multi-tenant** dengan Billing (Stripe/Midtrans), Team Management, Role/Permission (Spatie), API Versioning.`,
    thumbnail: 'https://cdn-icons-png.flaticon.com/512/1152/1152912.png',
    category: 'Backend',
    level: 'Intermediate',
    price: 399000,
    originalPrice: 599000,
    rating: 4.95,
    totalReviews: 521,
    totalStudents: 4156,
    duration: '22 jam 15 menit',
    lessons: 84,
    instructor: { id: 3, name: 'Siti Coder', avatar: 'https://i.pravatar.cc/100?u=siti' },
    tags: ['Laravel', 'PHP', 'API', 'Testing', 'Architecture'],
    isPublished: true,
    createdAt: '2024-03-01T12:00:00Z',
    updatedAt: '2024-07-15T09:00:00Z'
  },
  {
    id: 4,
    slug: 'react-nextjs-fullstack',
    title: 'React 18 + Next.js 14 Full-Stack: App Router & Server Actions',
    shortDesc: 'Master Next.js 14 App Router, Server Components, & Server Actions untuk produksi.',
    longDesc: `Next.js 14 udah beda banget sama versi lama. App Router + Server Components + Server Actions = game changer.

**Yang Akan Lu Pelajari:**
- App Router: Layout, Page, Loading, Error, Not-Found
- Server Components vs Client Components (kapan pakai mana)
- Server Actions: Mutasi data tanpa API route
- Streaming & Suspense untuk UX yang smooth
- Data Fetching: fetch() extend, cache, revalidate
- Authentication: NextAuth.js v5 (Auth.js)
- Database: Prisma + PostgreSQL / Neon / Supabase
- UI: Shadcn/UI + Tailwind CSS
- State: Zustand / Jotai / React Query (untuk client)
- Testing: Vitest + Playwright
- Deploy: Vercel (gratis) / Docker ke VPS

**Project:** E-commerce minimal tapi full-featured: Cart, Checkout (Midtrans/Stripe), Order History, Admin Dashboard.`,
    thumbnail: 'https://cdn-icons-png.flaticon.com/512/5968/5968292.png',
    category: 'Frontend',
    level: 'Intermediate',
    price: 599000,
    originalPrice: 899000,
    rating: 4.7,
    totalReviews: 234,
    totalStudents: 1876,
    duration: '16 jam 20 menit',
    lessons: 56,
    instructor: { id: 4, name: 'Rizki Frontend', avatar: 'https://i.pravatar.cc/100?u=rizki' },
    tags: ['React', 'Next.js', 'TypeScript', 'Prisma', 'Tailwind'],
    isPublished: true,
    createdAt: '2024-04-10T10:00:00Z',
    updatedAt: '2024-07-20T16:00:00Z'
  },
  {
    id: 5,
    slug: 'golang-microservices',
    title: 'Golang Microservices: gRPC, Kafka, & Kubernetes',
    shortDesc: 'Bangun sistem terdistribusi yang scalable pake Go, gRPC, Kafka, & K8s.',
    longDesc: `Microservices bukan cuma "pecah service". Butuh pola pikir distributed systems.

**Module 1: Go Fundamentals untuk Production**
- Project Layout Standard (cmd, internal, pkg, api)
- Dependency Injection pake Wire / uber-go/dig
- Error Handling: pkg/errors, sentinel errors, wrap
- Testing: Table-driven, Mockery, Testcontainers
- Observability: OpenTelemetry, Prometheus, Grafana

**Module 2: gRPC & Protocol Buffers**
- Proto3 Syntax, Option, Well-Known Types
- Unary, Server/Client/Bidirectional Streaming
- Interceptors: Auth, Logging, Metrics, Retry
- gRPC-Gateway buat REST proxy
- ConnectRPC (alternatif modern)

**Module 3: Event-Driven pake Kafka**
- Producer/Consumer Pattern, Consumer Groups
- Exactly-Once Semantics, Idempotency
- Schema Registry (Avro/Protobuf)
- Kafka Connect & ksqlDB
- Outbox Pattern untuk Transactional Outbox

**Module 4: Deploy & Operate di Kubernetes**
- Operator Pattern / Custom Controller
- Service Mesh: Istio / Linkerd (mTLS, Traffic Split)
- GitOps: ArgoCD / Flux
- Chaos Engineering: LitmusChaos
- Cost Optimization: VPA, Cluster Autoscaler, Karpenter`,
    thumbnail: 'https://cdn-icons-png.flaticon.com/512/919/919853.png',
    category: 'Backend',
    level: 'Expert',
    price: 899000,
    originalPrice: 1499000,
    rating: 4.85,
    totalReviews: 156,
    totalStudents: 892,
    duration: '25 jam 10 menit',
    lessons: 72,
    instructor: { id: 5, name: 'Doni Gopher', avatar: 'https://i.pravatar.cc/100?u=doni' },
    tags: ['Go', 'gRPC', 'Kafka', 'Kubernetes', 'Microservices'],
    isPublished: true,
    createdAt: '2024-05-01T09:00:00Z',
    updatedAt: '2024-07-25T13:00:00Z'
  },
  {
    id: 6,
    slug: 'python-data-engineering',
    title: 'Python Data Engineering: Airflow, Spark, & Modern Stack',
    shortDesc: 'Dari ETL ke ELT, bangun data pipeline yang robust & scalable.',
    longDesc: `Data Engineering sekarang bukan cuma "bikin script Python". Butuh arsitektur yang proper.

**Stack Modern yang Dipakai:**
- **Orchestration:** Apache Airflow (TaskFlow API, Dynamic Task Mapping)
- **Processing:** Apache Spark (PySpark), Polars, DuckDB
- **Storage:** PostgreSQL, ClickHouse, Apache Iceberg, Delta Lake
- **Streaming:** Kafka, Redpanda, RisingWave, Flink SQL
- **Quality:** Great Expectations, Soda Core, dbt Tests
- **Catalog:** DataHub, Amundsen
- **Transform:** dbt Core (SQL-first transformation)
- **Deploy:** Docker, Kubernetes, Terraform

**Project Nyata:**
Bangun **Real-time Analytics Platform** untuk e-commerce:
1. CDC dari PostgreSQL → Kafka (Debezium)
2. Stream Processing → RisingWave / Flink SQL
3. Batch Layer → Airflow + dbt + ClickHouse
4. Serving Layer → API (FastAPI) + Dashboard (Superset/Metabase)
5. Alerting & Data Quality Monitoring`,
    thumbnail: 'https://cdn-icons-png.flaticon.com/512/5087/5087602.png',
    category: 'Data',
    level: 'Advanced',
    price: 699000,
    originalPrice: 999000,
    rating: 4.75,
    totalReviews: 203,
    totalStudents: 1434,
    duration: '20 jam 00 menit',
    lessons: 68,
    instructor: { id: 6, name: 'Maya Data', avatar: 'https://i.pravatar.cc/100?u=maya' },
    tags: ['Python', 'Airflow', 'Spark', 'dbt', 'Kafka', 'ClickHouse'],
    isPublished: true,
    createdAt: '2024-06-01T11:00:00Z',
    updatedAt: '2024-07-28T10:00:00Z'
  }
];

const DEFAULT_BLOG_POSTS = [
  {
    id: 1,
    slug: 'kenapa-docker-sering-error-port',
    title: 'Kenapa Docker Sering Error Port? Solusi Gampang Biar Nggak Bingung',
    excerpt: 'Kisah tragis seorang Bos yang mencoba menjalankan dua container di port yang sama. Pelajari cara mengatasinya sebelum server lu meledak.',
    content: `## Masalah Klasik: "Port Already Allocated"

Lu jalanin \`docker run -p 8080:80 nginx\` — lancar. Lu jalanin lagi container lain di port 8080 — **BOOM**:

\`\`\`
docker: Error response from daemon: driver failed programming external connectivity on endpoint hungry_einstein: Bind for 0.0.0.0:8080 failed: port is already allocated.
\`\`\`

### Kenapa Bisa Terjadi?

1. **Container lain masih jalan** di port yang sama
2. **Container mati tapi port masih nempel** (ghost container)
3. **Host port konflik** sama service lain (systemd, dll)
4. **Docker Desktop/VM** port forwarding issue

### Solusi Cepat

**1. Cek container yang jalan:**
\`\`\`bash
docker ps --format "table {{.Names}}\t{{.Ports}}"
\`\`\`

**2. Cek SEMUA container (termasuk yang stop):**
\`\`\`bash
docker ps -a --filter "publish=8080"
\`\`\`

**3. Kill yang nge-block:**
\`\`\`bash
docker rm -f <container_name>
\`\`\`

**4. Atau ganti host port:**
\`\`\`bash
docker run -p 8081:80 nginx  # host:container
\`\`\`

### Best Practice: Pakai Docker Compose

\`\`\`yaml
# docker-compose.yml
services:
  web:
    image: nginx
    ports:
      - "8080:80"  # host:container
  api:
    image: my-api
    ports:
      - "3000:3000"
\`\`\`

Jalanin: \`docker compose up -d\`. Nggak akan konflik karena Compose manage port mapping.

### Pro Tip: Pakai Reverse Proxy (Nginx/Traefik/Caddy)

Biar cuma 1 port (80/443) yang keluar, sisanya internal:

\`\`\`yaml
services:
  traefik:
    image: traefik:v3.0
    command:
      - "--api.insecure=true"
      - "--providers.docker=true"
      - "--entrypoints.web.address=:80"
    ports:
      - "80:80"
      - "8080:8080"  # dashboard
    volumes:
      - "/var/run/docker.sock:/var/run/docker.sock:ro"

  web:
    image: nginx
    labels:
      - "traefik.enable=true"
      - "traefik.http.routers.web.rule=Host(\`lms.local\`)"
      - "traefik.http.services.web.loadbalancer.server.port=80"
\`\`\`

Sekarang akses \`http://lms.local\` (tambahin ke \`/etc/hosts\`). **Satu port, banyak service.** 🎯

---

**Kesimpulan:** Jangan pakai port host manual untuk production. Pakai **Docker Compose + Reverse Proxy**. Hidup lu jadi tenang.`,
    category: 'DevOps',
    tags: ['Docker', 'Troubleshooting', 'Port', 'Traefik'],
    author: { id: 1, name: 'Bima The Boss', avatar: 'https://i.pravatar.cc/100?u=bima' },
    publishedAt: '2024-01-20T08:00:00Z',
    readTime: '5 menit',
    views: 12450,
    likes: 342,
    isPublished: true
  },
  {
    id: 2,
    slug: 'misteri-hilangnya-file-artisan',
    title: 'Misteri Hilangnya File Artisan: Cara Pulihkan Nyawa Project Laravel Lu',
    excerpt: 'Satu hari yang mencekam saat perintah \`php artisan\` tidak lagi dikenali. Inilah cara mengembalikan "nyawa" project Laravel lu.',
    content: `## Gejala: "Could not open input file: artisan"

Lu ketik \`php artisan migrate\` — biasanya lancar. Tapi sekarang:

\`\`\`
Could not open input file: artisan
\`\`\`

Lu cek \`ls -la\` — **file artisan nggak ada!** 😱

### Penyebab Umum

1. **Git ignore salah** — artisan ke-ignore
2. **Clone repo tanpa file hidden** — artisan itu file biasa tapi kadang ke-skip
3. **Deploy script hapus file "tidak perlu"**
4. **Copy folder tanpa file root** (cp -r * nggak copy file hidden)

### Solusi: Regenerate Artisan

**Cara 1: Laravel Installer (paling cepat)**
\`\`\`bash
laravel new temp-project --no-interaction
cp temp-project/artisan .
rm -rf temp-project
\`\`\`

**Cara 2: Composer Create-Project**
\`\`\`bash
composer create-project laravel/laravel temp --no-interaction
cp temp/artisan .
rm -rf temp
\`\`\`

**Cara 3: Manual (kalau offline)**
Buat file \`artisan\` di root project:

\`\`\`php
<?php

define('LARAVEL_START', microtime(true));

// Determine if the application is in maintenance mode...
if (file_exists(\$maintenance = __DIR__.'/storage/framework/maintenance.php')) {
    require \$maintenance;
}

// Register the Composer autoloader...
require __DIR__.'/vendor/autoload.php';

// Bootstrap the application...
\$app = require_once __DIR__.'/bootstrap/app.php';

// Run the application...
\$kernel = \$app->make(Illuminate\\Contracts\\Console\\Kernel::class);

\$status = \$kernel->handle(
    \$request = Illuminate\\Http\\Request::capture()
);

\$kernel->terminate(\$request, \$status);

exit(\$status);
\`\`\`

Lalu: \`chmod +x artisan\`

### Verifikasi

\`\`\`bash
php artisan --version
# Laravel Framework 11.x.x
\`\`\`

### Preventif: Tambahin ke .gitignore yang BENAR

\`\`\`gitignore
# Laravel
/vendor
/node_modules
/public/hot
/public/storage
/storage/*.key
.env
.env.backup
.phpunit.result.cache
Homestead.json
Homestead.yaml
npm-debug.log
yarn-error.log
/.fleet
/.idea
/.vscode

# JANGAN ignore artisan!
# artisan  ← HAPUS BARIS INI KALO ADA
\`\`\`

---

**Moral:** File \`artisan\` adalah **nyawa project Laravel**. Jangan pernah di-ignore, jangan dihapus, jangan di-skip saat copy. Simpan deket hati. ❤️`,
    category: 'PHP Laravel',
    tags: ['Laravel', 'Artisan', 'Troubleshooting', 'Git'],
    author: { id: 3, name: 'Siti Coder', avatar: 'https://i.pravatar.cc/100?u=siti' },
    publishedAt: '2024-01-15T14:30:00Z',
    readTime: '4 menit',
    views: 8920,
    likes: 218,
    isPublished: true
  },
  {
    id: 3,
    slug: 'belajar-git-rebase-vs-merge',
    title: 'Git Rebase vs Merge: Kapan Pakai Yang Mana? (Biar Histori Nggak Berantakan)',
    excerpt: 'Bingung milih rebase atau merge? Ini penjelasan santai pake analogi kehidupan sehari-hari biar gampang diinget.',
    content: `## Analogi Sederhana

**Merge** = Lu nulis diary, temen lu nulis diary. Gabungin jadi satu buku tebal, urut waktu. Ada tanda "gabungan di sini".

**Rebase** = Lu nulis diary, temen lu nulis diary. Lu **nulis ulang** diary temen lu biar kayak lu nulis sendiri dari awal. Riwayat jadi linear, bersih.

---

### Merge: "Gabungin Aja, Nggak Pusing"

\`\`\`bash
git checkout main
git pull origin main
git checkout feature/login
git merge main          # atau: git merge origin/main
# resolve conflict kalau ada
git push origin feature/login
\`\`\`

**Kelebihan:**
- Aman, nggak rewrite history
- Cocok buat tim besar, branch shared
- GitHub/GitLab "Merge button" pakai ini

**Kekurangan:**
- History jadi **berantakan** (banyak merge commit)
- \`git log --oneline --graph\` kayak spaghetti

---

### Rebase: "Rapihin Dulu, Baru Gabung"

\`\`\`bash
git checkout feature/login
git fetch origin
git rebase origin/main  # ambil update main, taruh commit lu di atasnya
# resolve conflict PER COMMIT (bukan sekaligus)
git push -f origin feature/login  # PAKSA push karena history berubah
\`\`\`

**Kelebihan:**
- History **linear, bersih, enak dibaca**
- Mudah \`git bisect\` cari bug
- Review PR lebih gampang (commit per commit)

**Kekurangan:**
- **Rewrite history** — bahaya kalau branch sudah di-share orang lain
- Conflict resolve bisa repetitif (per commit)
- \`git push -f\` butuh permission/force push

---

### Kapan Pakai Mana?

| Situasi | Rekomendasi |
|---------|-------------|
| Branch **hanya lu** yang kerjain | **Rebase** ✅ |
| Branch **di-share** ke tim lain | **Merge** ✅ |
| PR ke **main/master** (protected) | **Merge** (via PR) |
| Sync feature branch dengan **main** | **Rebase** (lokal) |
| Hotfix urgent ke **production** | **Merge** (cepat, aman) |
| Squash commit sebelum PR | **Rebase -i** ✅ |

---

### Workflow Gua (Best of Both Worlds)

\`\`\`bash
# 1. Branch baru dari main yang fresh
git checkout main && git pull
git checkout -b feature/awesome

# 2. Kerjain, commit sering (WIP ok)
git add . && git commit -m "wip: coba-coba"

# 3. Sebelum push PR: rebase interactive rapihin commit
git rebase -i main
# squash jadi 1-2 commit yang meaningful

# 4. Push & buat PR
git push -u origin feature/awesome

# 5. Setelah approve & CI pass: Squash & Merge di GitHub/GitLab
# (history main tetap linear, feature branch dibuang)
\`\`\`

---

### Golden Rule: **JANGAN REBASE BRANCH YANG SUDAH DI-SHARE**

Kalau temen lu sudah \`git pull\` branch lu → **jangan rebase**. Merge aja.

Kalau lu yakin **hanya lu** yang punya branch itu → **rebase bebas**.

---

**TL;DR:** Rebase buat rapihin history lokal. Merge buat gabungin ke shared branch. Paham konsep, nggak hafal perintah. 🎯`,
    category: 'Git',
    tags: ['Git', 'Rebase', 'Merge', 'Workflow'],
    author: { id: 1, name: 'Bima The Boss', avatar: 'https://i.pravatar.cc/100?u=bima' },
    publishedAt: '2024-02-05T10:00:00Z',
    readTime: '7 menit',
    views: 15670,
    likes: 523,
    isPublished: true
  },
  {
    id: 4,
    slug: 'database-indexing-yang-bener',
    title: 'Database Indexing yang Bener: Biar Query Lu Nggak Lemot Kayak Kura-kura',
    excerpt: 'Index itu kayak daftar isi buku. Tanpa dia, database mesti baca halaman 1 sampe habis. Yuk bikin index yang bener.',
    content: `## Index = Daftar Isi Buku

Bayangin buku 1000 halaman nggak ada daftar isi. Lu cari "Bab 12: Docker". Lu mesti buka halaman 1, 2, 3... sampe ketemu. **Full Table Scan.**

Index = daftar isi. Lu buka daftar isi → lihat "Bab 12: halaman 245" → lompat ke halaman 245. **Index Seek.**

---

### Jenis Index Umum

| Jenis | Cocok Untuk | Contoh |
|-------|-------------|--------|
| **B-Tree (Default)** | Equality, Range, Sorting | \`WHERE id = 5\`, \`WHERE created_at > '2024-01-01'\`, \`ORDER BY name\` |
| **Hash** | Equality only (exact match) | \`WHERE email = 'x@y.com'\` (PostgreSQL: \`HASH\` index) |
| **GIN/GiST** | Full-text search, JSONB, Array | \`WHERE tags @> ARRAY['docker']\`, \`WHERE to_tsvector(body) @@ query\` |
| **Partial** | Subset data (WHERE condition) | \`CREATE INDEX ON orders (user_id) WHERE status = 'active'\` |
| **Composite** | Multiple columns together | \`WHERE user_id = 1 AND status = 'paid'\` |

---

### Composite Index: Urutan Kolom PENTING

\`\`\`sql
-- Query: WHERE user_id = 1 AND status = 'paid' ORDER BY created_at DESC

-- Index yang BENER:
CREATE INDEX idx_orders_user_status_created ON orders (user_id, status, created_at DESC);

-- Index yang SALAH (tidak optimal untuk query di atas):
CREATE INDEX idx_orders_status_user ON orders (status, user_id);
\`\`\`

**Aturan:** Kolom **equality** dulu, baru **range/sort**. Urutan di index = urutan di WHERE.

---

### Contoh Nyata: Laravel Migration

\`\`\`php
Schema::table('orders', function (Blueprint \$table) {
    // Composite index untuk query: user_id + status + created_at
    \$table->index(['user_id', 'status', 'created_at'], 'idx_orders_user_status_created');

    // Partial index (PostgreSQL) - hanya index yang active
    // Butuh DB::statement raw
    DB::statement("
        CREATE INDEX idx_orders_active_user ON orders (user_id)
        WHERE status IN ('pending', 'processing', 'shipped')
    ");

    // Full-text search (PostgreSQL)
    \$table->fullText(['title', 'description'], 'idx_products_search');
});
\`\`\`

---

### Cek Index Dipakai Atau Nggak (PostgreSQL)

\`\`\`sql
EXPLAIN ANALYZE
SELECT * FROM orders WHERE user_id = 1 AND status = 'paid';
\`\`\`

Lihat output:
- **Index Scan** / **Bitmap Heap Scan** → ✅ Index dipakai
- **Seq Scan** → ❌ Full table scan (index nggak dipakai / nggak ada)

---

### Anti-Pattern: Over-Indexing

Index bikin **INSERT/UPDATE/DELETE lambat** (harus update index juga).

**Tanda over-indexing:**
- Table punya > 5-7 index
- Write performance turun drastis
- Disk usage naik banyak

**Solusi:**
- Drop index yang nggak dipakai (cek \`pg_stat_user_indexes\`)
- Pakai **Partial Index** buat filter umum
- Pertimbangkan **Covering Index** (INCLUDE columns) buat query read-only

---

### Checklist Sebelum Bikin Index

1. [ ] Query ini **sering dijalankan**? (bukan sekali sebulan)
2. [ ] Table **besar** (> 10k rows)? Kecil nggak butuh index.
3. [ ] Kolom **selectivity tinggi**? (nilai unik banyak, misal email vs gender)
4. [ ] Query pakai **WHERE / JOIN / ORDER BY** kolom ini?
5. [ ] Sudah cek \`EXPLAIN\` — benar-benar **Seq Scan**?
6. [ ] Nggak bikin **terlalu banyak index** di table yang sering write?

---

**Kesimpulan:** Index itu **obat**, bukan **vitamin**. Minum pas butuh, jangan tiap hari. Ukur dulu (\`EXPLAIN\`), baru minum. 💊`,
    category: 'Database',
    tags: ['PostgreSQL', 'MySQL', 'Index', 'Performance', 'SQL'],
    author: { id: 2, name: 'Ahmad Networker', avatar: 'https://i.pravatar.cc/100?u=ahmad' },
    publishedAt: '2024-02-18T09:00:00Z',
    readTime: '8 menit',
    views: 9840,
    likes: 287,
    isPublished: true
  },
  {
    id: 5,
    slug: 'testing-laravel-pest-php',
    title: 'Testing Laravel pake Pest PHP: Biar Code Lu Tidur Nyenyak Malam',
    excerpt: 'PHPUnit itu powerful tapi syntax-nya verbose. Pest bikin testing jadi enjoy & readable. Yuk migrasi.',
    content: `## Kenapa Pest?

\`\`\`php
// PHPUnit - verbose, boilerplate
public function test_user_can_login()
{
    \$user = User::factory()->create(['password' => bcrypt('password')]);
    
    \$response = \$this->postJson('/api/login', [
        'email' => \$user->email,
        'password' => 'password'
    ]);
    
    \$response->assertStatus(200)
              ->assertJsonStructure(['token', 'user']);
}
\`\`\`

\`\`\`php
// Pest - clean, expressive, joyful
test('user can login', function () {
    \$user = User::factory()->create(['password' => 'password']);
    
    \$this->postJson('/api/login', [
        'email' => \$user->email,
        'password' => 'password'
    ])->assertOk()
      ->assertJsonStructure(['token', 'user']);
});
\`\`\`

---

### Install & Setup

\`\`\`bash
composer require pestphp/pest --dev --with-all-dependencies
./vendor/bin/pest --init
\`\`\`

**plugins wajib:**
\`\`\`bash
composer require pestphp/pest-plugin-laravel --dev
composer require pestphp/pest-plugin-livewire --dev  # kalau pakai Livewire
composer require pestphp/pest-plugin-faker --dev
\`\`\`

---

### Fitur Keren Pest

**1. Expectations (Fluent Assertions)**
\`\`\`php
expect(\$user->name)->toBe('Bima');
expect(\$collection)->toHaveCount(5);
expect(\$response)->toBeJson();
expect(fn() => \$service->call())->toThrow(Exception::class, 'Error message');
\`\`\`

**2. Dataset (Data-Driven Testing)**
\`\`\`php
dataset('invalid_emails', [
    'empty' => '',
    'no_at' => 'bimaemail.com',
    'no_domain' => 'bima@',
    'double_at' => 'bima@@email.com',
]);

test('email validation fails for invalid formats', function (string \$email) {
    \$this->postJson('/register', ['email' => \$email])
         ->assertValidationError('email');
})->with('invalid_emails');
\`\`\`

**3. Architectural Testing (Enforce Structure)**
\`\`\`php
// tests/Architecture/Test.php
test('controllers only depend on services, not models directly')
    ->expect('App\\Http\\Controllers')
    ->toOnlyUseClassesFrom([
        'App\\Services',
        'App\\Http\\Requests',
        'App\\Http\\Resources',
        'Illuminate\\*',
    ]);
\`\`\`

**4. Parallel Testing (Cepet Banget)**
\`\`\`bash
./vendor/bin/pest --parallel
# Atau di phpunit.xml: <php><env name="PEST_PARALLEL" value="true"/></php>
\`\`\`

**5. Snapshot Testing**
\`\`\`php
test('api response matches snapshot', function () {
    \$response = \$this->getJson('/api/user/1');
    expect(\$response->json())->toMatchSnapshot();
});
\`\`\`

**6. Watch Mode (TDD Flow)**
\`\`\`bash
./vendor/bin/pest --watch
# File berubah → test auto jalan → feedback instan
\`\`\`

---

### Migration dari PHPUnit

Pest **kompatibel 100%** dengan PHPUnit. Test lama tetep jalan.

\`\`\`bash
# Jalanin semua (Pest + PHPUnit)
./vendor/bin/pest

# Atau tetap pakai phpunit
./vendor/bin/phpunit
\`\`\`

---

### Best Practice Structure

\`\`\`text
tests/
├── Feature/
│   ├── Auth/
│   │   ├── LoginTest.php
│   │   └── RegisterTest.php
│   ├── Course/
│   │   ├── EnrollmentTest.php
│   │   └── PurchaseTest.php
│   └── Api/
│       └── CourseApiTest.php
├── Unit/
│   ├── Services/
│   │   └── PaymentServiceTest.php
│   └── Models/
│       └── UserTest.php
├── Architecture/
│   └── LayerTest.php
├── Pest.php          # Config global
└── Datasets/         # Shared datasets
    └── InvalidEmails.php
\`\`\`

---

### CI/CD: GitHub Actions

\`\`\`yaml
# .github/workflows/test.yml
name: Tests
on: [push, pull_request]
jobs:
  test:
    runs-on: ubuntu-latest
    services:
      mysql:
        image: mysql:8
        env:
          MYSQL_ROOT_PASSWORD: secret
          MYSQL_DATABASE: lms_test
        ports: [3306:3306]
        options: --health-cmd="mysqladmin ping" --health-interval=10s
    steps:
      - uses: actions/checkout@v4
      - uses: shivammathur/setup-php@v2
        with:
          php-version: '8.3'
          extensions: mbstring, pdo_mysql
          coverage: xdebug
      - run: composer install --prefer-dist --no-progress
      - run: cp .env.testing .env
      - run: php artisan migrate --force
      - run: ./vendor/bin/pest --parallel --coverage --min=80
\`\`\`

---

**Kesimpulan:** Pest bikin testing **enjoyable**, bukan beban. Syntax bersih, fitur modern, parallel cepat. **Migrasi sekarang**, nanti lu ngerasain bedanya saat deploy malam minggu. 🌙✨`,
    category: 'PHP Laravel',
    tags: ['Laravel', 'Pest', 'Testing', 'TDD', 'CI/CD'],
    author: { id: 3, name: 'Siti Coder', avatar: 'https://i.pravatar.cc/100?u=siti' },
    publishedAt: '2024-03-10T16:00:00Z',
    readTime: '10 menit',
    views: 11200,
    likes: 401,
    isPublished: true
  }
];

const DEFAULT_USERS = [
  {
    id: 1,
    email: 'bima@lms.blog',
    password: '$2b$10$hash_bima_password', // bcrypt('bima123')
    firstName: 'Bima',
    lastName: 'The Boss',
    role: 'admin',
    avatar: 'https://i.pravatar.cc/200?u=bima',
    createdAt: '2024-01-01T00:00:00Z',
    lastLogin: '2024-07-30T10:00:00Z',
    isActive: true,
    enrollments: [1, 2, 3]
  },
  {
    id: 2,
    email: 'siswa@demo.com',
    password: '$2b$10$hash_siswa_password', // bcrypt('siswa123')
    firstName: 'Siswa',
    lastName: 'Demo',
    role: 'user',
    avatar: 'https://i.pravatar.cc/200?u=siswa',
    createdAt: '2024-02-15T00:00:00Z',
    lastLogin: '2024-07-29T14:00:00Z',
    isActive: true,
    enrollments: [1, 3]
  }
];

// ---------- Storage Helpers ----------
function getStorage(key, defaultValue = []) {
  try {
    const data = localStorage.getItem(key);
    return data ? JSON.parse(data) : defaultValue;
  } catch (e) {
    console.error(`Error reading ${key}:`, e);
    return defaultValue;
  }
}

function setStorage(key, value) {
  try {
    localStorage.setItem(key, JSON.stringify(value));
    return true;
  } catch (e) {
    console.error(`Error writing ${key}:`, e);
    return false;
  }
}

function initStorage() {
  if (!localStorage.getItem(STORAGE_KEYS.USERS)) {
    setStorage(STORAGE_KEYS.USERS, DEFAULT_USERS);
  }
  if (!localStorage.getItem(STORAGE_KEYS.COURSES)) {
    setStorage(STORAGE_KEYS.COURSES, DEFAULT_COURSES);
  }
  if (!localStorage.getItem(STORAGE_KEYS.BLOG_POSTS)) {
    setStorage(STORAGE_KEYS.BLOG_POSTS, DEFAULT_BLOG_POSTS);
  }
  if (!localStorage.getItem(STORAGE_KEYS.ENROLLMENTS)) {
    setStorage(STORAGE_KEYS.ENROLLMENTS, []);
  }
  if (!localStorage.getItem(STORAGE_KEYS.SETTINGS)) {
    setStorage(STORAGE_KEYS.SETTINGS, {
      siteName: 'LMS Blog',
      maintenanceMode: false,
      registrationEnabled: true
    });
  }
}

// ---------- Auth Helpers ----------
function getCurrentUser() {
  const userData = localStorage.getItem(STORAGE_KEYS.CURRENT_USER);
  return userData ? JSON.parse(userData) : null;
}

function setCurrentUser(user) {
  if (user) {
    localStorage.setItem(STORAGE_KEYS.CURRENT_USER, JSON.stringify(user));
  } else {
    localStorage.removeItem(STORAGE_KEYS.CURRENT_USER);
  }
}

function isLoggedIn() {
  return !!getCurrentUser();
}

function isAdmin() {
  const user = getCurrentUser();
  return user && user.role === 'admin';
}

function login(email, password) {
  const users = getStorage(STORAGE_KEYS.USERS);
  // Simple check (in real app, verify bcrypt)
  const user = users.find(u => u.email === email && u.isActive);
  if (user) {
    // Simulate password check (demo: password = email prefix + '123')
    const expectedPass = email.split('@')[0] + '123';
    if (password === expectedPass) {
      const { password: _, ...safeUser } = user;
      setCurrentUser(safeUser);
      // Update last login
      const updatedUsers = users.map(u => u.id === user.id ? { ...u, lastLogin: new Date().toISOString() } : u);
      setStorage(STORAGE_KEYS.USERS, updatedUsers);
      return { success: true, user: safeUser };
    }
  }
  return { success: false, message: 'Email atau password salah' };
}

function register(userData) {
  const users = getStorage(STORAGE_KEYS.USERS);
  if (users.find(u => u.email === userData.email)) {
    return { success: false, message: 'Email sudah terdaftar' };
  }
  const newUser = {
    id: Date.now(),
    ...userData,
    role: 'user',
    avatar: `https://i.pravatar.cc/200?u=${userData.email}`,
    createdAt: new Date().toISOString(),
    lastLogin: null,
    isActive: true,
    enrollments: []
  };
  const { password: _, ...safeUser } = newUser;
  users.push(newUser);
  setStorage(STORAGE_KEYS.USERS, users);
  setCurrentUser(safeUser);
  return { success: true, user: safeUser };
}

function logout() {
  localStorage.removeItem(STORAGE_KEYS.CURRENT_USER);
}

// ---------- Course Helpers ----------
function getCourses(filters = {}) {
  let courses = getStorage(STORAGE_KEYS.COURSES);
  
  if (filters.published !== undefined) {
    courses = courses.filter(c => c.isPublished === filters.published);
  }
  if (filters.category) {
    courses = courses.filter(c => c.category.toLowerCase() === filters.category.toLowerCase());
  }
  if (filters.search) {
    const q = filters.search.toLowerCase();
    courses = courses.filter(c => 
      c.title.toLowerCase().includes(q) || 
      c.shortDesc.toLowerCase().includes(q) ||
      c.tags.some(t => t.toLowerCase().includes(q))
    );
  }
  if (filters.instructorId) {
    courses = courses.filter(c => c.instructor.id === filters.instructorId);
  }
  
  return courses;
}

function getCourseById(id) {
  const courses = getStorage(STORAGE_KEYS.COURSES);
  return courses.find(c => c.id === parseInt(id) || c.slug === id);
}

function getCourseBySlug(slug) {
  const courses = getStorage(STORAGE_KEYS.COURSES);
  return courses.find(c => c.slug === slug);
}

function createCourse(courseData) {
  const courses = getStorage(STORAGE_KEYS.COURSES);
  const newCourse = {
    id: Date.now(),
    slug: courseData.title.toLowerCase().replace(/[^a-z0-9]+/g, '-').replace(^-|-$/g, ''),
    ...courseData,
    rating: 0,
    totalReviews: 0,
    totalStudents: 0,
    createdAt: new Date().toISOString(),
    updatedAt: new Date().toISOString()
  };
  courses.push(newCourse);
  setStorage(STORAGE_KEYS.COURSES, courses);
  return newCourse;
}

function updateCourse(id, updates) {
  const courses = getStorage(STORAGE_KEYS.COURSES);
  const idx = courses.findIndex(c => c.id === parseInt(id));
  if (idx === -1) return null;
  courses[idx] = { ...courses[idx], ...updates, updatedAt: new Date().toISOString() };
  setStorage(STORAGE_KEYS.COURSES, courses);
  return courses[idx];
}

function deleteCourse(id) {
  const courses = getStorage(STORAGE_KEYS.COURSES);
  const filtered = courses.filter(c => c.id !== parseInt(id));
  setStorage(STORAGE_KEYS.COURSES, filtered);
  return true;
}

// ---------- Blog Helpers ----------
function getBlogPosts(filters = {}) {
  let posts = getStorage(STORAGE_KEYS.BLOG_POSTS);
  
  if (filters.published !== undefined) {
    posts = posts.filter(p => p.isPublished === filters.published);
  }
  if (filters.category) {
    posts = posts.filter(p => p.category.toLowerCase() === filters.category.toLowerCase());
  }
  if (filters.search) {
    const q = filters.search.toLowerCase();
    posts = posts.filter(p => 
      p.title.toLowerCase().includes(q) || 
      p.excerpt.toLowerCase().includes(q) ||
      p.tags.some(t => t.toLowerCase().includes(q))
    );
  }
  if (filters.authorId) {
    posts = posts.filter(p => p.author.id === filters.authorId);
  }
  
  return posts.sort((a, b) => new Date(b.publishedAt) - new Date(a.publishedAt));
}

function getBlogPostById(id) {
  const posts = getStorage(STORAGE_KEYS.BLOG_POSTS);
  return posts.find(p => p.id === parseInt(id) || p.slug === id);
}

function getBlogPostBySlug(slug) {
  const posts = getStorage(STORAGE_KEYS.BLOG_POSTS);
  return posts.find(p => p.slug === slug);
}

function createBlogPost(postData) {
  const posts = getStorage(STORAGE_KEYS.BLOG_POSTS);
  const newPost = {
    id: Date.now(),
    slug: postData.title.toLowerCase().replace(/[^a-z0-9]+/g, '-').replace(^-|-$/g, ''),
    ...postData,
    views: 0,
    likes: 0,
    publishedAt: new Date().toISOString(),
    isPublished: postData.isPublished !== false
  };
  posts.push(newPost);
  setStorage(STORAGE_KEYS.BLOG_POSTS, posts);
  return newPost;
}

function updateBlogPost(id, updates) {
  const posts = getStorage(STORAGE_KEYS.BLOG_POSTS);
  const idx = posts.findIndex(p => p.id === parseInt(id));
  if (idx === -1) return null;
  posts[idx] = { ...posts[idx], ...updates };
  setStorage(STORAGE_KEYS.BLOG_POSTS, posts);
  return posts[idx];
}

function deleteBlogPost(id) {
  const posts = getStorage(STORAGE_KEYS.BLOG_POSTS);
  const filtered = posts.filter(p => p.id !== parseInt(id));
  setStorage(STORAGE_KEYS.BLOG_POSTS, filtered);
  return true;
}

// ---------- Enrollment Helpers ----------
function getEnrollments(userId = null) {
  const enrollments = getStorage(STORAGE_KEYS.ENROLLMENTS);
  if (userId) {
    return enrollments.filter(e => e.userId === parseInt(userId));
  }
  return enrollments;
}

function isEnrolled(userId, courseId) {
  const enrollments = getStorage(STORAGE_KEYS.ENROLLMENTS);
  return enrollments.some(e => e.userId === parseInt(userId) && e.courseId === parseInt(courseId));
}

function enrollUser(userId, courseId) {
  if (isEnrolled(userId, courseId)) return { success: false, message: 'Sudah terdaftar' };
  const enrollments = getStorage(STORAGE_KEYS.ENROLLMENTS);
  const enrollment = {
    id: Date.now(),
    userId: parseInt(userId),
    courseId: parseInt(courseId),
    enrolledAt: new Date().toISOString(),
    progress: 0,
    completedLessons: []
  };
  enrollments.push(enrollment);
  setStorage(STORAGE_KEYS.ENROLLMENTS, enrollments);
  
  // Update course student count
  const course = getCourseById(courseId);
  if (course) {
    updateCourse(courseId, { totalStudents: course.totalStudents + 1 });
  }
  
  // Update user enrollments
  const users = getStorage(STORAGE_KEYS.USERS);
  const userIdx = users.findIndex(u => u.id === parseInt(userId));
  if (userIdx !== -1) {
    users[userIdx].enrollments.push(parseInt(courseId));
    setStorage(STORAGE_KEYS.USERS, users);
    // Update current user if it's them
    const currentUser = getCurrentUser();
    if (currentUser && currentUser.id === parseInt(userId)) {
      setCurrentUser({ ...currentUser, enrollments: [...currentUser.enrollments, parseInt(courseId)] });
    }
  }
  
  return { success: true, enrollment };
}

// ---------- UI Helpers ----------
function formatCurrency(amount) {
  return new Intl.NumberFormat('id-ID', { style: 'currency', currency: 'IDR', minimumFractionDigits: 0 }).format(amount);
}

function formatDate(dateString) {
  return new Date(dateString).toLocaleDateString('id-ID', { day: 'numeric', month: 'long', year: 'numeric' });
}

function formatRelativeTime(dateString) {
  const diff = Date.now() - new Date(dateString).getTime();
  const minutes = Math.floor(diff / 60000);
  const hours = Math.floor(diff / 3600000);
  const days = Math.floor(diff / 86400000);
  
  if (minutes < 1) return 'Baru saja';
  if (minutes < 60) return `${minutes} menit lalu`;
  if (hours < 24) return `${hours} jam lalu`;
  if (days < 7) return `${days} hari lalu`;
  return formatDate(dateString);
}

function truncate(text, length = 150) {
  if (text.length <= length) return text;
  return text.substring(0, length).trim() + '...';
}

function showToast(message, type = 'info') {
  const container = document.getElementById('toast-container') || createToastContainer();
  const toast = document.createElement('div');
  const bgColor = {
    success: 'bg-green-600',
    error: 'bg-red-600',
    warning: 'bg-yellow-600',
    info: 'bg-blue-600'
  }[type] || 'bg-blue-600';
  
  toast.className = `${bgColor} text-white px-6 py-3 rounded-xl shadow-lg mb-2 transform transition-all duration-300 animate-slide-in`;
  toast.innerHTML = `<div class="flex items-center gap-3"><span>${message}</span><button onclick="this.parentElement.parentElement.remove()" class="ml-4 text-white/70 hover:text-white">✕</button></div>`;
  container.appendChild(toast);
  
  setTimeout(() => {
    toast.style.opacity = '0';
    toast.style.transform = 'translateX(100%)';
    setTimeout(() => toast.remove(), 300);
  }, 4000);
}

function createToastContainer() {
  const container = document.createElement('div');
  container.id = 'toast-container';
  container.className = 'fixed top-5 right-5 z-[9999] flex flex-col gap-2';
  document.body.appendChild(container);
  return container;
}

function showModal(html, options = {}) {
  const modal = document.createElement('div');
  modal.className = 'fixed inset-0 z-[9998] flex items-center justify-center p-4';
  modal.innerHTML = `
    <div class="absolute inset-0 bg-black/50 backdrop-blur-sm" onclick="${options.closeOnOverlay !== false ? 'this.parentElement.remove()' : ''}"></div>
    <div class="relative bg-white rounded-3xl shadow-2xl max-w-2xl w-full max-h-[90vh] overflow-y-auto animate-scale-in">
      ${html}
    </div>
  `;
  document.body.appendChild(modal);
  return modal;
}

function closeModal(modal) {
  modal.style.opacity = '0';
  setTimeout(() => modal.remove(), 200);
}

// ---------- Initialize ----------
document.addEventListener('DOMContentLoaded', () => {
  initStorage();
  
  // Add toast styles
  if (!document.getElementById('toast-styles')) {
    const style = document.createElement('style');
    style.id = 'toast-styles';
    style.textContent = `
      @keyframes slide-in { from { opacity: 0; transform: translateX(100%); } to { opacity: 1; transform: translateX(0); } }
      @keyframes scale-in { from { opacity: 0; transform: scale(0.95); } to { opacity: 1; transform: scale(1); } }
      .animate-slide-in { animation: slide-in 0.3s ease-out; }
      .animate-scale-in { animation: scale-in 0.2s ease-out; }
    `;
    document.head.appendChild(style);
  }
  
  // Update nav based on auth
  updateAuthNav();
});

// Export for global access
window.LMS = {
  STORAGE_KEYS,
  getStorage,
  setStorage,
  initStorage,
  getCurrentUser,
  setCurrentUser,
  isLoggedIn,
  isAdmin,
  login,
  register,
  logout,
  getCourses,
  getCourseById,
  getCourseBySlug,
  createCourse,
  updateCourse,
  deleteCourse,
  getBlogPosts,
  getBlogPostById,
  getBlogPostBySlug,
  createBlogPost,
  updateBlogPost,
  deleteBlogPost,
  getEnrollments,
  isEnrolled,
  enrollUser,
  formatCurrency,
  formatDate,
  formatRelativeTime,
  truncate,
  showToast,
  showModal,
  closeModal
};