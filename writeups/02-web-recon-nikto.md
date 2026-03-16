# Lab Writeup #02 — Web Recon with Nikto

**Date:** 16/03/2026
**Target:** 192.168.56.102 (Ubuntu 24.04 — Apache 2.4.58)
**Attacker:** 192.168.56.101 (Kali Linux)

## TL;DR
Ran Nikto web scanner against Apache server on port 80. Found 4 misconfigurations
including missing security headers and an ETag inode leak. No critical 
vulnerabilities on a fresh install — but these misconfigs would matter on a 
real server.

## Commands Used
```bash
nikto -h http://192.168.56.102 -o ~/lab/scans/ubuntu-nikto-day2.txt
```
- `-h` = target host (the IP we're scanning)
- `-o` = save output to a file (important for documenting evidence in real engagements)

## Results
- X-Frame-Options header missing → vulnerable to clickjacking attacks
- X-Content-Type-Options header missing → browser may misinterpret file types
- ETag inode leak (CVE-2003-1418) → server leaks internal filesystem information
- HTTP Methods allowed: GET, POST, OPTIONS, HEAD → normal, no dangerous methods like PUT or DELETE

## What This Means
A fresh Apache install has no critical vulnerabilities but is misconfigured by 
default. Missing security headers are easy wins for an attacker. The ETag leak 
is a low-severity finding but shows up in real pentest reports constantly.

Nikto is a noisy scanner — it made 8,102 requests in 26 seconds. On a real 
target, a SOC analyst watching logs would detect this immediately.

## Screenshots
![Apache Default Page](../scans/ubuntu-apache-day2.png)
![Nikto Scan Output](../scans/ubuntu-nikto-day2.png)

## MITRE ATT&CK
- T1190 — Exploit Public-Facing Application
- T1046 — Network Service Discovery

## Next Steps
- Install DVWA on Apache for web app attack practice
- Run Gobuster to find hidden directories