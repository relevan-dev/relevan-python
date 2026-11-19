---
title: Proxmox backup plan
tags: [homelab, backups]
created: 2026-03-02
---
Nightly vzdump of every VM to the Synology NAS at 02:00, mode snapshot, zstd compression.
Keep 7 daily, 4 weekly and 3 monthly copies. The Home Assistant VM (id 104) also gets an
offsite copy to Backblaze B2 every Sunday through rclone. Restore test last passed on 2026-02-20:
VM 104 came back in 11 minutes. #proxmox
