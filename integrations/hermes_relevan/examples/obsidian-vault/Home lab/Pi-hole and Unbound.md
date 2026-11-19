---
title: Pi-hole and Unbound
tags: [homelab, dns]
---
Pi-hole runs on the Raspberry Pi 4 at 192.168.1.53 with Unbound as the recursive resolver on port 5335.
The router hands out 192.168.1.53 as the only DNS server over DHCP. If DNS breaks, check that
unbound.service is running and that the root hints file is newer than six months. #dns
