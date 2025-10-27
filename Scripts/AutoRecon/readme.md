# 🐀 Subdomain Orchestrator GUI (Full Version)

A complete, GUI-based subdomain and reconnaissance orchestrator written in **Python** using **Tkinter**.  
Created in **The XSS Rat** style for ethical hackers and bug bounty hunters who love efficient, multi-stage recon automation.

---

## ⚡ Overview

This tool orchestrates a **multi-step subdomain enumeration workflow** through a friendly graphical interface.  
You can chain together passive tools, brute-force stages, permutations, probes, and port scans — all running concurrently with live logs.

Each job is isolated with its own working directory under `results/`, making it easy to track scans for different targets or workflows.

---

## ✨ Features

- 🧠 **Workflow system** — Save and load JSON-defined toolchains.
- ⚙️ **Multi-stage pipeline**:
  1. Passive enumeration (`subfinder`, `amass`, `assetfinder`, `findomain`)
  2. DNS brute force (`gobuster`)
  3. Permutation brute force (built-in)
  4. Deduplication + results merging
  5. HTTP probing (`ffuf`)
  6. Port scanning (`masscan` + `nmap`)
- 👥 **Concurrent job management** — Run multiple targets simultaneously.
- 📁 **Results per job** — Stored under `results/<timestamp>_<job_id>/`
- 🧩 **Per-tool overrides** — Customize worker/thread counts dynamically.
- 🧾 **Batch mode** — Load multiple targets from a text file.
- 💬 **Live logging** — View tool output and job status in real-time from the GUI.
- 🧱 **Simple JSON workflows** — Easy to customize and extend.

---

## 🧰 Requirements

Install dependencies:
```bash
sudo apt install python3 python3-tk subfinder amass assetfinder findomain gobuster ffuf nmap masscan
```

Optional but recommended:
- **rockyou.txt** or similar wordlist for fuzzing
- `/usr/share/wordlists/subdomains-top1million-5000.txt` for DNS brute-forcing

You’ll also need:
- Python ≥ 3.8
- A Unix-based system (Linux/Mac). Windows works but some commands may differ.

---

## 🚀 Quickstart

```bash
git clone https://github.com/yourusername/subdomain-orchestrator
cd subdomain-orchestrator
python3 orchestrator.py
```

Then:
1. Select a **workflow** (or edit one).
2. Enter your **target domain**.
3. Optionally add **worker overrides** (e.g. `gobuster_dns:20,ffuf:10`).
4. Hit **Start Job**.
5. Watch the logs live.

Results will appear in:
```
results/<timestamp>_<job_id>/
```

---

## 🧩 Workflow Configuration

Workflows are stored in:
```
workflows.json
```

A default example:
```json
{
  "name": "default_basic",
  "steps": [
    {"tool": "subfinder", "enabled": true, "flags": "", "workers": 4},
    {"tool": "amass", "enabled": true, "flags": "", "workers": 4},
    {"tool": "assetfinder", "enabled": true, "flags": "", "workers": 2},
    {"tool": "gobuster_dns", "enabled": true, "wordlist": "/usr/share/wordlists/subdomains-top1million-5000.txt", "workers": 20},
    {"tool": "permutation", "enabled": true, "wordlist": "/usr/share/wordlists/rockyou.txt", "workers": 10},
    {"tool": "ffuf", "enabled": true, "wordlist": "/usr/share/wordlists/common.txt", "workers": 10},
    {"tool": "nmap", "enabled": true, "workers": 1}
  ],
  "notes": "passive -> brute -> permute -> probe -> portscan"
}
```

You can edit workflows directly from the GUI (JSON editor) or manually in the file.

---

## 🖥️ GUI Overview

- **Workflow Selection:** Choose or edit existing workflows.  
- **Target Field:** Input your target domain.  
- **Job Name:** Optional custom label for the job.  
- **Overrides Field:** Set custom worker counts (e.g. `ffuf:8,nmap:2`).  
- **Buttons:**
  - **Start Job** — Launches a new job.
  - **Batch Mode** — Run multiple targets from a text file.
  - **Stop Job** — Attempt to stop a running job.
  - **Open Results Dir** — Opens the results folder.

The bottom pane shows:
- **Jobs Table:** Track running/completed jobs.
- **Live Logs:** Real-time updates from each subprocess.

---

## 📊 Output Structure

Each job produces a directory under `results/`, containing:
```
subfinder.txt
amass.txt
assetfinder.txt
gobuster_dns.txt
permutations.txt
ffuf_<host>.json
nmap_<host>.nmap
masscan_<host>.grep
combined.txt
```

`combined.txt` merges all unique subdomains from all steps.

---

## ⚠️ Notes & Limitations

- Process stopping is **best-effort**; subprocesses may persist.
- Ensure you have correct permissions for `masscan` (may require `sudo`).
- Heavy wordlists or large targets can increase runtime significantly.
- Designed for **educational and ethical use** only.

---

## 🧑‍💻 Author

**The XSS Rat**  
[https://thexssrat.com](https://thexssrat.com)  
[YouTube Channel](https://www.youtube.com/@TheXSSRat)

---

## 📜 License

MIT License.  
Use responsibly — for learning, labs, and legal bug bounty testing only.
