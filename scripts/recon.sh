#!/bin/bash

# =============================================================================
# recon.sh - Automated reconnaissance script using Nmap and Nikto
# Usage: ./recon.sh <target-ip>
# =============================================================================

# --- Argument validation -----------------------------------------------------
# Exit early with a helpful message if no IP address was provided
if [ -z "$1" ]; then
    echo "[ERROR] No target IP provided."
    echo "Usage: $0 <ip-address>"
    echo "Example: $0 192.168.56.102"
    exit 1
fi

TARGET="$1"
TIMESTAMP=$(date +"%Y%m%d-%H%M%S")

# --- Output directory setup --------------------------------------------------
# Create the scans/ directory if it doesn't already exist (-p suppresses errors)
SCAN_DIR="scans"
mkdir -p "$SCAN_DIR"

# Build output filenames using the target IP and current timestamp
NMAP_OUT="$SCAN_DIR/${TARGET}-nmap-${TIMESTAMP}.txt"
NIKTO_OUT="$SCAN_DIR/${TARGET}-nikto-${TIMESTAMP}.txt"

# --- Banner ------------------------------------------------------------------
echo "=============================================="
echo "  Recon Script"
echo "  Target : $TARGET"
echo "  Time   : $(date)"
echo "=============================================="
echo ""

# --- Nmap scan ---------------------------------------------------------------
# -sV : probe open ports to determine service/version info
# -sC : run default NSE scripts (equivalent to --script=default)
# -Pn : skip host discovery (treat host as online) — useful when ICMP is blocked
echo "[*] Starting Nmap scan on $TARGET ..."
nmap -sV -sC -Pn "$TARGET" -oN "$NMAP_OUT"
echo "[+] Nmap scan complete. Output saved to: $NMAP_OUT"
echo ""

# --- Nikto scan --------------------------------------------------------------
# -h : target host to scan
# Nikto performs a web server vulnerability scan on common HTTP ports
echo "[*] Starting Nikto scan on $TARGET ..."
nikto -h "$TARGET" | tee "$NIKTO_OUT"
echo "[+] Nikto scan complete. Output saved to: $NIKTO_OUT"
echo ""

# --- Summary -----------------------------------------------------------------
# Print a final summary so the user knows exactly where the results landed
echo "=============================================="
echo "  Scan Summary"
echo "=============================================="
echo "  Target      : $TARGET"
echo "  Nmap output : $NMAP_OUT"
echo "  Nikto output: $NIKTO_OUT"
echo "=============================================="
