# Lab Writeup #05 — SSH Brute Force Detection Tool

**Date:** 19/03/2026
**Target:** 192.168.56.102 (Ubuntu 24.04)
**Attacker:** 192.168.56.101 (Kali Linux)

## TL;DR
Built a Python log parser that reads /var/log/auth.log and automatically
detects SSH brute force attempts. Tested by generating real failed login
traffic from Kali to Ubuntu.

## What It Does
- Reads Ubuntu's auth.log file
- Uses regex to find "Failed password" lines
- Counts failures per IP address
- Flags IPs exceeding a threshold as SUSPICIOUS
- Shows which usernames were attempted from each IP

## Key Concepts
- `re` module: regex pattern matching to extract IPs and usernames from
  unstructured log text
- `defaultdict`: dictionary that auto-initialises counts to 0
- `--threshold` flag: configurable detection sensitivity

## Test Results
Generated 3 failed SSH attempts from Kali (192.168.56.101) using fakeuser.
Script correctly flagged the IP as suspicious:

IP Address           Failures   Flag           Usernames tried
192.168.56.101       3          SUSPICIOUS     fakeuser

## Why This Matters
This is exactly what SIEM tools like Splunk and Microsoft Sentinel do at
scale — parse logs, count events per source, alert when thresholds are
exceeded. This script replicates that logic from scratch.

## MITRE ATT&CK (Defensive Mapping)
- Detects T1110.001 — Brute Force: Password Guessing
- Detects T1078 — Valid Account enumeration attempts

## Next Steps
- Add timestamp analysis to detect attacks within a time window
- Add GeoIP lookup to flag foreign IPs
- Extend to parse Apache access logs for web brute force