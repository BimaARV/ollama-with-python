# ============================================================
# PPPoE Add-ons (v2) — Mikrotik RouterOS 6.49.19
# - Monitoring ke Telegram (threshold + pppoe disconnect alert)
# - Backup export scheduler (daily, rotasi 7 hari)
# - DNS flush scheduler (daily, jam 04:00)
# - Queue hierarchy tree:
#     Root:  pppoe-aggregate (100M parent)
#       |- pppoe-tier-10M (10M limit, 1:8)
#       |- pppoe-tier-20M (20M limit, 1:8)
#       |- pppoe-tier-30M (30M limit, 1:8)
#       |- pppoe-tier-50M (50M limit, 1:8)
# ============================================================

# ----------- EDIT SESUAI TOPOLOGI LOKAL -----------
:local tgBotToken ""
:local tgChatId   ""
# Backup file email opsional — kosongkan kalau pakai ftp/smb
:local backupEmailTo ""
:local backupEmailFrom ""
:local backupEmailSmtp ""
:local backupEmailPort "25"

:local pppoeRootParent "pppoe-aggregate"
:local aggregateMaxLimit "100M"     ; total ceiling semua PPPoE client
:local ratio 8                       ; 1:8
# ---------------------------------------------------

# ===========================================================
# SECTION A: Queue Tree hierarchy (1:8)
# ===========================================================
# Idempotent: bersihkan dulu kalau sudah ada
:do { /queue tree remove [find where name=$pppoeRootParent] } on-add={}
:do { /queue tree remove [find where name~"pppoe-tier-"] } on-add={}

# Root aggregate (100M total)
/queue tree
add name=$pppoeRootParent parent=none max-limit=$aggregateMaxLimit \
    packet-mark=no-mark comment="PPPoE aggregate parent (100M total)"

# Per-tier child
/queue tree
add name=pppoe-tier-10M parent=$pppoeRootParent \
    max-limit=100M limit-at=10M packet-mark=pppoe-10M \
    queue=default comment="10M profile, 1:8"

add name=pppoe-tier-20M parent=$pppoeRootParent \
    max-limit=100M limit-at=20M packet-mark=pppoe-20M \
    queue=default comment="20M profile, 1:8"

add name=pppoe-tier-30M parent=$pppoeRootParent \
    max-limit=100M limit-at=30M packet-mark=pppoe-30M \
    queue=default comment="30M profile, 1:8"

add name=pppoe-tier-50M parent=$pppoeRootParent \
    max-limit=100M limit-at=50M packet-mark=pppoe-50M \
    queue=default comment="50M profile, 1:8"

# Packet marks per tier — digunakan mangle
/ip firewall mangle
:do { /ip firewall mangle remove [find where comment~"PPPMARK"] } on-add={}

# Mark new connection dari PPPoE client -> assign packet-mark sesuai source IP range
add chain=forward action=mark-connection new-connection-mark=conn-pppoe-10M \
    src-address=192.168.113.10-192.168.113.62 passthrough=yes \
    comment="PPPMARK: tier 10M connection"
add chain=forward action=mark-packet connection-mark=conn-pppoe-10M \
    packet-mark=pppoe-10M passthrough=yes \
    comment="PPPMARK: tier 10M packet"

add chain=forward action=mark-connection new-connection-mark=conn-pppoe-20M \
    src-address=192.168.113.65-192.168.113.126 passthrough=yes \
    comment="PPPMARK: tier 20M connection"
add chain=forward action=mark-packet connection-mark=conn-pppoe-20M \
    packet-mark=pppoe-20M passthrough=yes \
    comment="PPPMARK: tier 20M packet"

add chain=forward action=mark-connection new-connection-mark=conn-pppoe-30M \
    src-address=192.168.113.129-192.168.113.190 passthrough=yes \
    comment="PPPMARK: tier 30M connection"
add chain=forward action=mark-packet connection-mark=conn-pppoe-30M \
    packet-mark=pppoe-30M passthrough=yes \
    comment="PPPMARK: tier 30M packet"

add chain=forward action=mark-connection new-connection-mark=conn-pppoe-50M \
    src-address=192.168.113.193-192.168.113.254 passthrough=yes \
    comment="PPPMARK: tier 50M connection"
add chain=forward action=mark-packet connection-mark=conn-pppoe-50M \
    packet-mark=pppoe-50M passthrough=yes \
    comment="PPPMARK: tier 50M packet"

# ===========================================================
# SECTION B: DNS Flush scheduler (daily 04:00)
# ===========================================================
/system script
:do { /system script remove [find where name=scripts-flush-dns] } on-add={}
add name=scripts-flush-dns \
    comment="Flush DNS cache & connection tracking" \
    source={

# Flush DNS cache (kalo ada) + reset connection tracking
/ip dns cache flush

# Reset connection tracking biar stale entries gak makan memory
/ip firewall connection remove [find where protocol=tcp && (connection-state=time-wait || connection-state=close-wait || connection-state=fin-wait || connection-state=last-ack)]

:log info "DNS & connection tracking flushed"
}

# Scheduler: 04:00 tiap hari
/system scheduler
:do { /system scheduler remove [find where name=sched-flush-dns] } on-add={}
add name=sched-flush-dns interval=1d start-time=04:00:00 \
    on-event=scripts-flush-dns \
    comment="DNS flush harian"

# ===========================================================
# SECTION C: Backup scheduler (daily 03:00, rotasi 7 hari)
# ===========================================================
/system script
:do { /system script remove [find where name=scripts-backup-daily] } on-add={}
add name=scripts-backup-daily \
    comment="Daily config + RSC export backup, rotasi 7 hari" \
    source={

:local ts [/system clock get date]
:local tstime [/system clock get time]
:local stamp ($ts . "_" . $tstime)
:replace "stamp" [pick $stamp 0 4] "-" [pick $stamp 5 7] "-" [pick $stamp 8 11] "/" [pick $stamp 11 13] ":" [pick $stamp 14 16] ":" [pick $stamp 17 end]
:local stamp ($ts . "_" . [:pick $tstime 0 2] . [:pick $tstime 3 5])
:local fname "backup-$stamp"

# Binary backup (untuk full restore)
/system backup save name=$fname
delay 2

# RSC export (untuk version-control)
/export file=$fname.rsc
delay 2

# Hapus backup > 7 hari
:foreach f in=[/file find] do={
    :if ([:typeof [:file get $f name]] = "str") do={
        :if ([:find [/file get $f name] "backup-"] = 0) do={
            :if (([/file get $f type] = "backup") && ([:len [/file get $f name]] > 8)) do={
                :local dt [/file get $f name]
                :if ([:tonum [:pick $dt 7 11]] > 0) do={
                    :if ([/file get $f creation-time] < ([:system clock get time]-604800)) do={
                        /file remove [find name=[/file get $f name]]
                    }
                }
            }
        }
    }
}

# Notifikasi Telegram
:if ([:len $tgBotToken] > 0 && [:len $tgChatId] > 0) do={
    /tool fetch url="https://api.telegram.org/bot$tgBotToken/sendMessage" \
        http-method=post \
        http-data="chat_id=$tgChatId&parse_mode=HTML&text=Backup harian berhasil: $fname.backup + $fname.rsc"
}

:log info "Daily backup complete: $fname"
}

# Scheduler backup
/system scheduler
:do { /system scheduler remove [find where name=sched-backup-daily] } on-add={}
add name=sched-backup-daily interval=1d start-time=03:00:00 \
    on-event=scripts-backup-daily \
    comment="Backup harian 03:00"

# Weekly backup upload ke remote (optional) — schedule tiap Minggu 02:00
:do { /system script remove [find where name=scripts-backup-remote] } on-add={}
add name=scripts-backup-remote \
    comment="Upload weekly backup ke remote (sesuaikan host/dest)" \
    source={
# Uncomment & sesuaikan kalau pakai ftp/sftp ke backup-server
# /tool fetch address="backup.example.com" src-path="backup.backup" \
#     user="bkp" password="secret" \
#     mode=ftp dst-path="/router-backups/weekly.backup"
}

:do { /system scheduler remove [find where name=sched-backup-remote] } on-add={}
add name=sched-backup-remote interval=7d start-date=jan/01/2025 start-time=02:00:00 \
    on-event=scripts-backup-remote \
    comment="Weekly remote upload"

# ===========================================================
# SECTION D: Monitoring — Telegram alerts
# ===========================================================
# Script 1: Cek throughput aggregate > 90% (tiap 5 menit)
/system script
:do { /system script remove [find where name=scripts-monitor-throughput] } on-add={}
add name=scripts-monitor-throughput \
    comment="Monitor throughput root, alert jika > 90% capacity" \
    source={

:local rootname "pppoe-aggregate"
:local threshold 90
:local rateMax [/queue tree get [find name=$rootname] max-limit]
# byte/s @ rate (di queue tree v6: tx-rate/rx-rate)
:local txRate [/queue tree get [find name=$rootname] rate]
:local txPct (([:tonum $txRate] * 100) / [:tonum $rateMax])

:local need 1
:if ([:len $tgBotToken] = 0 || [:len $tgChatId] = 0) do={ :set need 0 }

# State file buat dedup alert (cooldown 10 menit)
:local sf "thr-state"
:local lastSent 0
:if ([/file get $sf value] != "") do={ :set lastSent [:tonum [/file get $sf value]] }

:if ($txPct >= $threshold && ([:tonum [/system clock get time]] - $lastSent > 600)) do={
    :if ($need = 1) do={
        /tool fetch url="https://api.telegram.org/bot$tgBotToken/sendMessage" \
            http-method=post http-data="chat_id=$tgChatId&parse_mode=HTML&text=$(hostname): PPPoE aggregate throughput $txPct% (TX)"
    }
    :log warning "PPPoE aggregate utilisation $txPct% (> $threshold%)"
    /file set $sf contents="last=$(/system clock get time)"
}

# Cleanup state file kalo traffic sudah turun
:if ($txPct < $threshold - 10) do={
    :if ([/file exists $sf]) do={ /file remove $sf }
}
}

:do { /system scheduler remove [find where name=sched-monitor-throughput] } on-add={}
/system scheduler add name=sched-monitor-throughput interval=5m on-event=scripts-monitor-throughput \
    comment="Monitor throughput tiap 5 menit"

# Script 2: Alert jumlah PPP aktif turun signifikan (10 menit window)
/system script
:do { /system script remove [find where name=scripts-monitor-pppoe] } on-add={}
add name=scripts-monitor-pppoe \
    comment="Alert jika jumlah PPP aktif turun drastis" \
    source={

:local cf "ppp-count-state"
:local currentCount [:len [find]]
:local prevCount 0
:if ([/file get $cf contents] != "") do={ :set prevCount [:tonum [/file get $cf contents]] }

:local dropPct 0
:if ($prevCount > 0) do={
    :set dropPct (100 - (($currentCount * 100) / $prevCount))
}

# Alert jika drop >= 30% & prevCount >= 20 (skip alert untuk jumlah kecil)
:if ($prevCount >= 20 && $dropPct >= 30) do={
    :if ([:len $tgBotToken] > 0 && [:len $tgChatId] > 0) do={
        /tool fetch url="https://api.telegram.org/bot$tgBotToken/sendMessage" \
            http-method=post http-data="chat_id=$tgChatId&parse_mode=HTML&text=$(hostname): PPPoE drop alert: $prevCount -> $currentCount ($dropPct%)"
    }
    :log warning "PPPoE sessions drop from $prevCount to $currentCount ($dropPct%)"
}

/file set $cf contents="$currentCount"

# Buat state file kalo belum ada
:if (![/file exists $cf]) do={
    /file set $cf contents="$currentCount"
}
}

:do { /system scheduler remove [find where name=sched-monitor-pppoe] } on-add={}
/system scheduler add name=sched-monitor-pppoe interval=10m on-event=scripts-monitor-pppoe \
    comment="Monitor PPPoE count tiap 10 menit"

# ===========================================================
# SECTION E: Init state file untuk monitoring
# ===========================================================
/file
# State files untuk dedup alert
add contents="last=0" name="thr-state" type="text" policy="ftp,reboot,read,write,policy,test,password,sniff,sensitive"
add contents="0" name="ppp-count-state" type="text" policy="ftp,reboot,read,write,policy,test,password,sniff,sensitive"

# ============================================================
# END v2 add-ons
# Verifikasi:
#   /queue tree print stats where name=pppoe-aggregate
#   /ip firewall mangle print stats where comment~"PPPMARK"
#   /system scheduler print
#   /system script print
# ============================================================
