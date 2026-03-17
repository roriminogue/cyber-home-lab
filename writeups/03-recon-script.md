# Lab Writeup #03 — Automated Recon Script

**Date:** 17/03/2026

## TL;DR
Built a Bash script that automates Nmap and Nikto recon against a target IP.
Saves timestamped output files so results are never overwritten.

## What It Does
- Takes an IP as an argument
- Validates input (exits with error if no IP provided)
- Runs Nmap -sV -sC -Pn and saves output
- Runs Nikto and saves output
- Prints a summary of saved file locations

## Key Bash Concepts Used
- `$1` — first argument passed to the script (the target IP)
- `[ -z "$1" ]` — checks if input is empty, exits with error if so
- `mkdir -p` — creates folder only if it doesn't already exist
- `$(date +"%Y%m%d-%H%M%S")` — generates a timestamp for filenames

## Usage
./recon.sh 192.168.56.102

## Why This Matters
Manual recon on multiple targets is slow. Automation means consistent,
documented output every time — which is how professional pentesters work.