# Cyber Home Lab

Personal cybersecurity home lab for practicing offensive and defensive security techniques. Built as part of my final year at the University of Wollongong (Cybersecurity major, graduating 2026). This repo documents my lab setup, tools, scripts, and writeups from hands-on exercises.

> **Disclaimer:** All activity in this lab is performed on systems I own and control, or on authorised platforms (TryHackMe). Never use these techniques against systems without explicit authorisation.

---

## About

**roriminogue** — Final year CS student at the University of Wollongong, majoring in Cybersecurity (graduating 2026). This lab is my hands-on learning environment for building practical offensive and defensive security skills alongside my degree.

[![GitHub](https://img.shields.io/badge/GitHub-roriminogue-181717?logo=github)](https://github.com/roriminogue)
[![TryHackMe](https://img.shields.io/badge/TryHackMe-roriminogue-212C42?logo=tryhackme)](https://tryhackme.com/p/roriminogue)

---

## Lab Setup

| Component | Details |
|-----------|---------|
| Hypervisor | VirtualBox |
| Network Mode | Host-Only Adapter + NAT |
| Attacker Machine | Kali Linux — `192.168.56.10` |
| Target Machine | Ubuntu 24.04 — `192.168.56.20` |
| Vulnerable Web App | DVWA (Damn Vulnerable Web Application) on Ubuntu target |

### Network Topology

```
[ Host Machine ]
       |
  [ VirtualBox ]
   /           \
[Kali Linux]  [Ubuntu 24.04 + DVWA]
192.168.56.10   192.168.56.20
       |               |
       +---[Host-Only]--+
               |
             [NAT]
               |
         [ Internet ]
```

**Host-Only** keeps attacker and target isolated on a private subnet. **NAT** gives both VMs outbound internet access for updates and downloading tools without exposing them to the broader network.

---

## Tools

| Tool | Category | Purpose |
|------|----------|---------|
| [Nmap](https://nmap.org) | Reconnaissance | Network scanning, host discovery, service/version detection, OS fingerprinting |
| [Nikto](https://github.com/sullo/nikto) | Web Reconnaissance | Web server scanner — detects misconfigurations, outdated software, and exposed paths |
| [Burp Suite](https://portswigger.net/burp) | Web App Testing | HTTP proxy, Intruder fuzzer, and scanner for web application security testing |
| [Hydra](https://github.com/vanhauser-thc/thc-hydra) | Credential Attacks | Fast, parallelised login brute-forcing across SSH, HTTP, and other protocols |
| [Metasploit](https://www.metasploit.com) | Exploitation | Exploit framework for vulnerability research, exploitation, and post-exploitation |
| [Wireshark](https://www.wireshark.org) | Traffic Analysis | Packet capture and protocol dissection for network forensics |
| [Python](https://www.python.org) | Scripting | Custom tooling — log parsing, automation, and data analysis |
| [Bash](https://www.gnu.org/software/bash/) | Scripting | Recon automation, workflow scripting |

---

## Scripts

Custom scripts built during this lab — located in [scripts/](scripts/).

| Script | Language | Description |
|--------|----------|-------------|
| [recon.sh](scripts/recon.sh) | Bash | Automated Nmap + Nikto scanner — takes an IP, saves timestamped output to `scans/` |
| [log_parser.py](scripts/log_parser.py) | Python | Parses `auth.log` for failed SSH attempts, counts per IP, flags brute-force sources |

---

## Writeups

| # | Title | Category | Platform | Date |
|---|-------|----------|----------|------|
| 01 | [Nmap Recon — Ubuntu Target](writeups/01-ubuntu-nmap-recon.md) | Reconnaissance | Home Lab | Mar 2026 |
| 02 | [Web Recon with Nikto — 4 Misconfigs Found](writeups/02-web-recon-nikto.md) | Web Reconnaissance | Home Lab | Mar 2026 |
| 03 | [Automated Recon Script (Nmap + Nikto)](writeups/03-recon-script.md) | Scripting / Automation | Home Lab | Mar 2026 |
| 04 | [DVWA Brute Force with Burp Suite Intruder](writeups/04-dvwa-bruteforce.md) | Web App / Credential Attack | Home Lab | Mar 2026 |
| 05 | [SSH Log Parser — Brute Force Detection](writeups/05-ssh-log-parser.md) | Blue Team / Scripting | Home Lab | Mar 2026 |
| 06 | [TryHackMe — Basic Pentesting (Full Compromise)](writeups/06-thm-basic-pentesting.md) | Full Pentest | TryHackMe | Mar 2026 |

> Each writeup covers objective, methodology, tools used, findings, and key takeaways. Writeup files are in [writeups/](writeups/).

---

## Skills Practiced

**Red Team / Offensive**
- Network reconnaissance and enumeration (Nmap, Nikto)
- Web application attacks — brute forcing login forms with Burp Suite Intruder
- Full pentest workflow: recon → enumeration → exploitation → post-exploitation (TryHackMe)
- Exploitation with Metasploit

**Blue Team / Defensive**
- SSH auth log analysis and brute-force detection (custom Python parser)
- Traffic capture and protocol analysis (Wireshark)
- Understanding attacker patterns to inform defensive countermeasures

**Scripting & Automation**
- Bash automation for multi-tool recon pipelines
- Python scripting for log parsing and IP-based threat detection

---

## Repo Structure

```
cyber-home-lab/
├── README.md
├── writeups/          # Individual exercise writeups
├── scripts/           # Custom automation scripts (recon.sh, log_parser.py)
├── scans/             # Raw tool output (gitignored)
└── notes/             # Reference notes and cheat sheets
```

---

## Author

**roriminogue** — Final year CS @ University of Wollongong | Cybersecurity Major | Graduating 2026

[GitHub](https://github.com/roriminogue) · [TryHackMe](https://tryhackme.com/p/roriminogue)
