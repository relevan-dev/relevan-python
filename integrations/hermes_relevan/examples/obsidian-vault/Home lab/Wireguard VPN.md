---
title: Wireguard VPN
tags: [homelab, vpn]
---
WireGuard runs on the OPNsense router, port 51820 UDP. Peers: laptop 10.8.0.2, phone 10.8.0.3.
Split tunnel: only 192.168.1.0/24 goes through the tunnel. Rotate the phone key if it is lost.
