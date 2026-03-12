# Lab Writeup #01 — Nmap Recon on Ubuntu Target

**Date:** 12/03/2026
**Target:** 192.168.56.102 (Ubuntu 24.04)
**Attacker:** 192.168.56.101 (Kali Linux)

## TL;DR
Ran initial Nmap service scan against Ubuntu VM. Found 2 open ports: SSH (22) and HTTP (80).

## Commands Used
nmap -sV -sC -Pn 192.168.56.102 -oN ~/lab/scans/ubuntu-day1.txt

## Results
- Port 22: OpenSSH 9.6p1
- Port 80: Apache httpd 2.4.58 — default Ubuntu page

## What This Means
SSH is available — potential brute force vector.
Apache web server is running — enumerate further with Nikto/Gobuster.

## MITRE ATT&CK
- T1046 — Network Service Discovery

## Next Steps
- Run Nikto against port 80
- Attempt SSH enumeration
- Install DVWA on Apache target