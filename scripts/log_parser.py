#!/usr/bin/env python3

# =============================================================================
# log_parser.py - SSH failed login analyser for /var/log/auth.log
# Usage:
#   python3 log_parser.py
#   python3 log_parser.py --threshold 10
#   python3 log_parser.py --log /path/to/custom/auth.log
# =============================================================================

import re
import argparse
from collections import defaultdict

# --- Argument parsing --------------------------------------------------------
# Allow the user to override the default log path and suspicion threshold
parser = argparse.ArgumentParser(description="Analyse SSH failed login attempts from auth.log")
parser.add_argument(
    "--log",
    default="/var/log/auth.log",
    help="Path to the auth log file (default: /var/log/auth.log)"
)
parser.add_argument(
    "--threshold",
    type=int,
    default=5,
    help="Number of failures before an IP is flagged SUSPICIOUS (default: 5)"
)
args = parser.parse_args()

# --- Regex pattern -----------------------------------------------------------
# auth.log failed SSH lines look like one of:
#   Failed password for root from 192.168.1.10 port 22 ssh2
#   Failed password for invalid user admin from 10.0.0.5 port 43210 ssh2
# Capture group 1 = username, group 2 = IP address
FAILED_SSH_PATTERN = re.compile(
    r"Failed password for (?:invalid user )?(\S+) from ([\d\.]+)"
)

# --- Data structures ---------------------------------------------------------
# failures[ip] = total count of failed attempts
# usernames[ip] = set of unique usernames tried from that IP
failures = defaultdict(int)
usernames = defaultdict(set)

# --- Parse the log file ------------------------------------------------------
print(f"[*] Reading log file: {args.log}\n")

try:
    with open(args.log, "r", errors="replace") as f:
        for line in f:
            match = FAILED_SSH_PATTERN.search(line)
            if match:
                user, ip = match.group(1), match.group(2)
                failures[ip] += 1
                usernames[ip].add(user)

except FileNotFoundError:
    print(f"[ERROR] Log file not found: {args.log}")
    raise SystemExit(1)
except PermissionError:
    print(f"[ERROR] Permission denied reading: {args.log} — try running with sudo")
    raise SystemExit(1)

# --- Build and sort results --------------------------------------------------
# Sort by failure count descending so the noisiest IPs appear first
sorted_ips = sorted(failures.items(), key=lambda x: x[1], reverse=True)

# --- Print summary -----------------------------------------------------------
print(f"{'IP Address':<20} {'Failures':<10} {'Flag':<14} Usernames tried")
print("-" * 80)

for ip, count in sorted_ips:
    flag = "*** SUSPICIOUS ***" if count > args.threshold else ""
    tried = ", ".join(sorted(usernames[ip]))
    print(f"{ip:<20} {count:<10} {flag:<14} {tried}")

# --- Footer ------------------------------------------------------------------
total_ips = len(failures)
total_attempts = sum(failures.values())
suspicious = sum(1 for c in failures.values() if c > args.threshold)

print("-" * 80)
print(f"\n[+] Summary:")
print(f"    Total failed attempts : {total_attempts}")
print(f"    Unique source IPs     : {total_ips}")
print(f"    Suspicious IPs (>{args.threshold} failures): {suspicious}")
