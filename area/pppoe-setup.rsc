# ============================================================
# PPPoE Setup — Mikrotik RouterOS 6.49.19
# - 4 profile: 10M, 20M, 30M, 50M (burst 100M)
# - Circuit ratio 1:8
# - Pool subnet 192.168.113.0/24, blok /26 non-overlap per profile
# ============================================================

# ----------- EDIT SESUAI TOPOLOGI LOKAL -----------
:local pppoeIface  "ether2"          # ether yg nge-broadcast PPPoE ke client
:local publicIface  "ether1"          # ether uplink/WAN
:local dnsPrimary   "8.8.8.8"
:local dnsSecondary "1.1.1.1"
# ---------------------------------------------------

# --------- STEP 1: Hapus config lama (idempotent) ----
# Uncomment baris berikut kalau mau reset total (HATI-HATI di production).
# /ppp profile remove [find where name~"PPPOE-"]
# /ppp secret remove [find]
# /ip pool remove [find where name~"pool-pppoe-"]
# /queue simple remove [find where name~"cst-"]
# -----------------------------------------------------

# STEP 2: IP address gateway PPPoE (interface ppp)
:do { /ip address remove [find where interface="pppoe-out"] } on-add={}
/ip address add address=192.168.113.1/24 interface=pppoe-out comment="PPPoE gateway"

/ip firewall connection tracking
/ip firewall connection
set tcp-established-timeout=1h
set tcp-close-timeout=10m
set tcp-close-wait-timeout=10m
set tcp-fin-wait-timeout=10m
set tcp-last-ack-timeout=10m
set tcp-syn-received-timeout=5m
set tcp-syn-sent-timeout=5m
set tcp-time-wait-timeout=10m

# STEP 3: IP Pool per profile (non-overlap, blok /26)
/ip pool
add name=pool-pppoe-10M  ranges=192.168.113.10-192.168.113.62
add name=pool-pppoe-20M  ranges=192.168.113.65-192.168.113.126
add name=pool-pppoe-30M  ranges=192.168.113.129-192.168.113.190
add name=pool-pppoe-50M  ranges=192.168.113.193-192.168.113.254

# STEP 4: PPP Profile
#   max-limit = burst ceiling (100M)
#   limit-at  = CIR (committed) = bandwidth dedicated
#   circuit   = ratio komunikasi PPPoE saat negotiate
#   on-up     = pasang simple queue + active session shaping
/ppp profile
add name=PPPOE-10M \
    local-address=192.168.113.1 \
    remote-address=pool-pppoe-10M \
    dns-server=$dnsPrimary,$dnsSecondary \
    circuit-rate-up=1250000 circuit-rate-down=1250000 \
    max-limit=100M/100M limit-at=10M/10M \
    only-one=no \
    use-compression=no use-vj-compression=no use-encryption=no \
    comment="10Mbps share, 100M burst, 1:8 ratio"

add name=PPPOE-20M \
    local-address=192.168.113.1 \
    remote-address=pool-pppoe-20M \
    dns-server=$dnsPrimary,$dnsSecondary \
    circuit-rate-up=2500000 circuit-rate-down=2500000 \
    max-limit=100M/100M limit-at=20M/20M \
    only-one=no \
    use-compression=no use-vj-compression=no use-encryption=no \
    comment="20Mbps share, 100M burst, 1:8 ratio"

add name=PPPOE-30M \
    local-address=192.168.113.1 \
    remote-address=pool-pppoe-30M \
    dns-server=$dnsPrimary,$dnsSecondary \
    circuit-rate-up=3750000 circuit-rate-down=3750000 \
    max-limit=100M/100M limit-at=30M/30M \
    only-one=no \
    use-compression=no use-vj-compression=no use-encryption=no \
    comment="30Mbps share, 100M burst, 1:8 ratio"

add name=PPPOE-50M \
    local-address=192.168.113.1 \
    remote-address=pool-pppoe-50M \
    dns-server=$dnsPrimary,$dnsSecondary \
    circuit-rate-up=6250000 circuit-rate-down=6250000 \
    max-limit=100M/100M limit-at=50M/50M \
    only-one=no \
    use-compression=no use-vj-compression=no use-encryption=no \
    comment="50Mbps share, 100M burst, 1:8 ratio"

# STEP 5: PPPoE Server
/interface pppoe-server server
set authentication=pap,chap,mschap1,mschap2 \
    default-profile=none \
    interface=$pppoeIface \
    keepalive-timeout=60 \
    max-mru=1492 max-mtu=1492 \
    one-session-per-host=no \
    service-name=internet \
    disabled=no

# STEP 6: NAT Masquerade untuk PPPoE client ke internet
/ip firewall nat
add chain=srcnat out-interface=$publicIface action=masquerade \
    comment="NAT PPPoE -> Internet" \
    place-before=0

# Catatan: rule NAT ini akan match semua src 192.168.113.0/24 yg keluar via $publicIface.
# Kalo lo punya rule NAT lain di router, hapus baris di atas & pastikan NAT masquerade
# untuk src-address=192.168.113.0/24 sudah ada di chain=srcnat out-interface=$publicIface.

# STEP 7: Firewall filter untuk PPPoE client (input chain)
/ip firewall filter
# Allow established/related dari PPPoE
add chain=input connection-state=established,related action=accept \
    comment="PPPoE: established/related" \
    place-before=0
# Allow new PPPoE connection dari interface PPPoE server
add chain=input in-interface=$pppoeIface protocol=tcp dst-port=1723 action=accept \
    comment="Allow PPPoE discovery" place-before=1
add chain=input in-interface=$pppoeIface protocol=udp dst-port=53 action=accept \
    comment="Allow DNS from PPPoE" place-before=1
# Drop invalid
add chain=input connection-state=invalid action=drop \
    comment="Drop invalid" place-before=1
# Allow ICMP limited
add chain=input protocol=icmp action=accept \
    comment="Allow ICMP" place-before=1

# Forward chain: allow from PPPoE client out
add chain=forward in-interface=all-ppp out-interface=$publicIface connection-state=new,established,related action=accept \
    comment="PPPoE -> WAN" place-before=0

# Drop everything from PPPoE client to router's own interface yg gak di-allow
add chain=input in-interface=all-ppp action=drop \
    comment="Drop PPPoE -> Router local (anti-attack)" \
    place-before=0

# STEP 8: Queue tree (shared bandwidth budget + simple queue per profile)
# Root queue sebagai anchor global.
# Pakai global-total dengan parent=none untuk max total semua PPPoE.
:do { /queue tree remove [find where name="pppoe-global"] } on-add={}
/queue tree
add name=pppoe-global parent=none max-limit=1G comment="Aggregate ceiling PPPoE traffic"

# Parent per profile (cap burst per profile)
:do { /queue tree remove [find where name~"pppoe-prf-"] } on-add={}
add name=pppoe-prf-10M parent=pppoe-global max-limit=100M
add name=pppoe-prf-20M parent=pppoe-global max-limit=100M
add name=pppoe-prf-30M parent=pppoe-global max-limit=100M
add name=pppoe-prf-50M parent=pppoe-global max-limit=100M

# Per-profile Simple Queue template
# Each customer uses Max-Limit & CIR dari queue yg dipasang via on-up di ppp secret per-user.
# Di bawah ini template yg dipasang otomatis saat user terkoneksi:

/queue simple
add name=cst-10M-TPL \
    target=192.168.113.10-192.168.113.62 \
    max-limit=100M/100M limit-at=10M/10M \
    burst-limit=200M/200M burst-threshold=80M/80M burst-time=8s/8s \
    queue=pcq-upload-default/pcq-download-default \
    parent=none packet-marks="" \
    comment="Template 10M (jangan dipakai manual)"

# Catatan: Untuk per-user shaping, lebih direkomendasikan pakai Simple Queue dinamis
# atau Queue Tree di-on-up dari ppp profile, contoh:
#
#   /ppp profile set PPPOE-10M on-up="/queue simple add name=\$user target=\$remote-address \\\
#       max-limit=100M/100M limit-at=10M/10M parent=none"
#   /ppp profile set PPPOE-10M on-down="/queue simple remove [find where name=\$user]"
#
# Di versi 6.49+ lo juga bisa set max-limit di PPP Profile langsung (sudah dilakukan
# di STEP 4), sehingga tiap PPP active session otomatis ke-shape sesuai profile.
# Cek di /ppp active apakah rx/tx-rate tidak melebihi limit-at (dedicated).
# -------------------------------------------------------------------------------------

# STEP 9: Contoh PPPoE secret (uncomment & ganti username/password)
/ppp secret
# add name=cust10-01 password=secretpass profile=PPPOE-10M service=pppoe comment="Customer 10M #1"
# add name=cust20-01 password=secretpass profile=PPPOE-20M service=pppoe comment="Customer 20M #1"
# add name=cust30-01 password=secretpass profile=PPPOE-30M service=pppoe comment="Customer 30M #1"
# add name=cust50-01 password=secretpass profile=PPPOE-50M service=pppoe comment="Customer 50M #1"

# ============================================================
# END
# Verifikasi cepat setelah apply:
#   /ip pool print
#   /ppp profile print
#   /ppp active print
#   /queue tree print stats where name=pppoe-global
#   /queue tree print where name~"pppoe-prf-"
# ============================================================
