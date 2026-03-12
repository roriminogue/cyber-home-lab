# Cyber Home Lab

Personal cybersecurity home lab for practicing offensive and defensive security techniques. This repo documents my lab setup, tool usage, and writeups from hands-on exercises.

> **Disclaimer:** All activity in this lab is performed on systems I own and control. Never use these techniques against systems without explicit authorization.

---

## Lab Setup

| Component | Details |
|-----------|---------|
| Hypervisor | VirtualBox |
| Network Mode | Host-Only Adapter + NAT |
| Attacker Machine | Kali Linux — `192.168.56.10` |
| Target Machine | Ubuntu 24.04 — `192.168.56.20` |

### Network Topology

```
[ Host Machine ]
       |
  [ VirtualBox ]
   /           \
[Kali Linux]  [Ubuntu 24.04]
192.168.56.10  192.168.56.20
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
| [Wireshark](https://www.wireshark.org) | Traffic Analysis | Packet capture and protocol dissection for network forensics |
| [Burp Suite](https://portswigger.net/burp) | Web App Testing | HTTP proxy, scanner, and fuzzer for web application security testing |
| [Hydra](https://github.com/vanhauser-thc/thc-hydra) | Credential Attacks | Fast, parallelized login brute-forcing across multiple protocols |
| [Metasploit](https://www.metasploit.com) | Exploitation | Exploit framework for vulnerability research and post-exploitation |

---

## Skills Practiced

- **Red Team / Pentesting** — reconnaissance, enumeration, exploitation, post-exploitation
- **Blue Team** — traffic analysis, log review, detection, and incident response fundamentals

---

## Writeups

| # | Target / Room | Category | Platform | Date | Status |
|---|--------------|----------|----------|------|--------|
| 1 | _Coming soon_ | — | — | — | — |
| 2 | _Coming soon_ | — | — | — | — |
| 3 | _Coming soon_ | — | — | — | — |

> Writeups are organized by date. Each entry links to a dedicated markdown file in [writeups/](writeups/).

---

## Repo Structure

```
cyber-home-lab/
├── README.md
├── writeups/          # Individual exercise writeups
├── scripts/           # Custom automation and helper scripts
└── notes/             # Reference notes and cheat sheets
```

---

## Author

**roriminogue** — [GitHub](https://github.com/roriminogue)
