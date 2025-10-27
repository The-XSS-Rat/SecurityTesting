#!/usr/bin/env python3
"""
Subdomain Orchestrator GUI — Full version

Features:
- GUI (Tkinter) to run multiple scan jobs concurrently
- Workflows (save/load) define combinations of tools, flags, and default worker counts
- Steps: passive enumeration -> DNS brute force (gobuster) -> permutation brute force (internal) -> dedupe -> ffuf probe -> portscan (nmap/masscan)
- Per-job overrides for workers per tool
- Live logging per-job and job manager
- Results saved to results/<job_id>/

Author: The XSS Rat (style)
"""

import os
import json
import asyncio
import threading
import subprocess
import shlex
import time
import uuid
from datetime import datetime
from pathlib import Path
import tkinter as tk
from tkinter import ttk, messagebox, filedialog, simpledialog

# ----------------------------
# Configuration / Defaults
# ----------------------------
APP_DIR = Path(__file__).parent.resolve()
RESULTS_DIR = APP_DIR / "results"
WORKFLOWS_FILE = APP_DIR / "workflows.json"
DEFAULT_WORDLIST = "/usr/share/wordlists/rockyou.txt"  # user should change if needed
DEFAULT_DNS_WORDLIST = "/usr/share/wordlists/subdomains-top1million-5000.txt"  # example for dns bruteforce

# Default tool templates - user may edit when saving workflows
# Note: these templates can include placeholders: {target}, {wordlist}, {threads}, {output}
DEFAULT_TOOLS = {
    "subfinder": {
        "cmd": "subfinder -d {target} -silent",
        "default_workers": 4
    },
    "amass": {
        "cmd": "amass enum -d {target} -passive -norecursive",
        "default_workers": 4
    },
    "assetfinder": {
        "cmd": "assetfinder --subs-only {target}",
        "default_workers": 2
    },
    "findomain": {
        "cmd": "findomain -t {target} --quiet",
        "default_workers": 4
    },
    # DNS brute with gobuster dns
    "gobuster_dns": {
        "cmd": "gobuster dns -d {target} -w {wordlist} -t {threads} -q",
        "default_workers": 20
    },
    # ffuf content discovery (simple)
    "ffuf": {
        "cmd": "ffuf -u http://{host}/FUZZ -w {wordlist} -t {threads} -mc 200 -s -o {output}",
        "default_workers": 10
    },
    # nmap scan (full TCP ports with -Pn)
    "nmap": {
        "cmd": "nmap -Pn -sV -p- --min-rate 1000 -oA {output} {host}",
        "default_workers": 1
    },
    # masscan quick scan (optional, may require root)
    "masscan": {
        "cmd": "masscan -p1-65535 {host} --rate 1000 -oG {output}",
        "default_workers": 1
    }
}

# Permutation generator settings (internal simple permuter)
PERMUTATION_SUFFIXES = ["dev", "test", "staging", "stage", "www", "beta", "old"]
PERMUTATION_PREFIXES = ["dev", "test", "beta", "stg", "old"]

# ----------------------------
# Utilities
# ----------------------------
def ensure_dir(p: Path):
    p.mkdir(parents=True, exist_ok=True)

def now_str():
    return datetime.now().strftime("%Y%m%d_%H%M%S")

def run_subprocess_sync(cmd, cwd=None):
    """Run a command synchronously and return (returncode, stdout, stderr)."""
    try:
        proc = subprocess.Popen(shlex.split(cmd), stdout=subprocess.PIPE, stderr=subprocess.PIPE, cwd=cwd)
        out, err = proc.communicate()
        return proc.returncode, out.decode(errors="ignore"), err.decode(errors="ignore")
    except FileNotFoundError as e:
        return 127, "", str(e)

async def run_subprocess_async(cmd, cwd=None):
    """Run a command as asyncio subprocess and return (rc, stdout, stderr)."""
    try:
        proc = await asyncio.create_subprocess_shell(cmd, stdout=asyncio.subprocess.PIPE, stderr=asyncio.subprocess.PIPE, cwd=cwd)
        out, err = await proc.communicate()
        return proc.returncode, (out.decode(errors="ignore") if out else ""), (err.decode(errors="ignore") if err else "")
    except FileNotFoundError as e:
        return 127, "", str(e)

def safe_read_lines(path):
    try:
        with open(path, "r", errors="ignore") as f:
            return [l.strip() for l in f if l.strip()]
    except FileNotFoundError:
        return []

# ----------------------------
# Workflow & Job Models
# ----------------------------
def load_workflows():
    if WORKFLOWS_FILE.exists():
        try:
            return json.loads(WORKFLOWS_FILE.read_text())
        except Exception:
            return {}
    return {}

def save_workflows(workflows):
    WORKFLOWS_FILE.write_text(json.dumps(workflows, indent=2))

# Default single workflow (if none exist)
DEFAULT_WORKFLOW = {
    "name": "default_basic",
    "steps": [
        {"tool": "subfinder", "enabled": True, "flags": "", "workers": DEFAULT_TOOLS["subfinder"]["default_workers"]},
        {"tool": "amass", "enabled": True, "flags": "", "workers": DEFAULT_TOOLS["amass"]["default_workers"]},
        {"tool": "assetfinder", "enabled": True, "flags": "", "workers": DEFAULT_TOOLS["assetfinder"]["default_workers"]},
        {"tool": "gobuster_dns", "enabled": True, "flags": "", "workers": DEFAULT_TOOLS["gobuster_dns"]["default_workers"], "wordlist": DEFAULT_DNS_WORDLIST},
        {"tool": "permutation", "enabled": True, "flags": "", "workers": 10, "wordlist": DEFAULT_WORDLIST},
        {"tool": "ffuf", "enabled": True, "flags": "", "workers": DEFAULT_TOOLS["ffuf"]["default_workers"], "wordlist": "/usr/share/wordlists/common.txt"},
        {"tool": "nmap", "enabled": True, "flags": "", "workers": DEFAULT_TOOLS["nmap"]["default_workers"]}
    ],
    "notes": "passive -> brute -> permute -> probe -> portscan"
}

# ----------------------------
# Permutation generator (internal, simple)
# ----------------------------
def generate_permutations(base_subs, wordlist_path, max_per_domain=2000):
    """
    Very simple permuter:
    - For each discovered subdomain root (e.g. test.example.com -> test, example.com -> example)
    - For each word in small wordlist, produce prefix/suffix variants: word + base, base + word
    - Also add common prefixes/suffixes.
    This is intentionally conservative and local; replace with dnsgen/altdns for heavy lifting.
    """
    words = []
    if wordlist_path and os.path.exists(wordlist_path):
        try:
            with open(wordlist_path, "r", errors="ignore") as f:
                for i, line in enumerate(f):
                    if i >= 2000:  # limit read on big wordlists
                        break
                    w = line.strip()
                    if w:
                        words.append(w)
        except Exception:
            words = []
    else:
        words = ["dev","test","stage","beta","www","admin","portal"]

    out = set()
    for s in base_subs:
        # base without domain: take first label
        labels = s.split(".")
        if len(labels) < 2:
            continue
        base = labels[0]
        domain = ".".join(labels[1:])
        # add prefix/suffix quick combos
        for p in PERMUTATION_PREFIXES:
            out.add(f"{p}-{base}.{domain}")
            out.add(f"{p}{base}.{domain}")
        for su in PERMUTATION_SUFFIXES:
            out.add(f"{base}-{su}.{domain}")
            out.add(f"{base}{su}.{domain}")
        # words from provided list (limited)
        for w in words[:200]:  # limit to first 200 words to avoid explosion
            out.add(f"{w}-{base}.{domain}")
            out.add(f"{base}-{w}.{domain}")
            out.add(f"{w}{base}.{domain}")
            if len(out) >= max_per_domain:
                break
        if len(out) >= max_per_domain:
            break

    return sorted(out)

# ----------------------------
# Job Runner
# ----------------------------
class JobRunner:
    """
    Represents a job scan pipeline for a single target.
    Each job has its own directory in results and its own semaphores per tool based on workers.
    """

    def __init__(self, job_id, target, workflow, per_tool_overrides=None, gui_log_callback=None):
        """
        :param job_id: unique id
        :param target: domain
        :param workflow: workflow dict (with steps)
        :param per_tool_overrides: dict tool->workers override
        :param gui_log_callback: function(msg) for GUI logging
        """
        self.job_id = job_id
        self.target = target
        self.workflow = workflow
        self.overrides = per_tool_overrides or {}
        self.log = gui_log_callback or (lambda msg: print(f"[{job_id}] {msg}"))
        self.base_dir = RESULTS_DIR / f"{now_str()}_{job_id}"
        ensure_dir(self.base_dir)
        self.tool_semaphores = {}  # tool -> asyncio.Semaphore based on workers
        self._build_semaphores()

        # internal sets
        self.discovered = set()
        self.combined_file = self.base_dir / "combined.txt"

    def _build_semaphores(self):
        # per-step workers
        for step in self.workflow.get("steps", []):
            tool_name = step.get("tool")
            workers = int(step.get("workers", DEFAULT_TOOLS.get(tool_name, {}).get("default_workers", 1)))
            # override by job-level overrides
            if tool_name in self.overrides:
                try:
                    workers = int(self.overrides[tool_name])
                except:
                    pass
            # minimum 1
            if workers < 1:
                workers = 1
            self.tool_semaphores[tool_name] = asyncio.Semaphore(workers)

    async def _run_tool_cmd(self, cmd, out_path=None, tool_name=None):
        """
        Run a single shell command, save stdout to out_path if provided, and log.
        """
        self.log(f"[{tool_name}] CMD: {cmd}")
        rc, out, err = await run_subprocess_async(cmd)
        if out_path:
            try:
                with open(out_path, "w", errors="ignore") as f:
                    f.write(out)
            except Exception as e:
                self.log(f"[!] Failed saving output {out_path}: {e}")
        if rc == 127:
            self.log(f"[!] Tool not found or command failed: {err}")
        elif rc != 0:
            self.log(f"[!] {tool_name} returned code {rc}. stderr: {err.strip()[:400]}")
        else:
            self.log(f"[{tool_name}] finished, wrote {len(out.splitlines())} lines to {out_path if out_path else '<stdout>'}")
        return out.splitlines() if out else []

    async def run_passive_tools(self):
        """Run passive enumeration tools configured in workflow concurrently (bounded by semaphores)."""
        tasks = []
        for step in self.workflow.get("steps", []):
            if not step.get("enabled"):
                continue
            tool = step.get("tool")
            if tool in ("subfinder", "amass", "assetfinder", "findomain"):
                sem = self.tool_semaphores.get(tool, asyncio.Semaphore(1))
                # build command
                template = DEFAULT_TOOLS.get(tool, {}).get("cmd", "").strip()
                cmd = f"{template} {step.get('flags','')}".strip()
                cmd = cmd.format(target=self.target)
                out_path = self.base_dir / f"{tool}.txt"
                # create coroutine wrapper to respect semaphore
                async def run_with_sem(cmd=cmd, out_path=out_path, tool=tool, sem=sem):
                    async with sem:
                        return await self._run_tool_cmd(cmd, str(out_path), tool)
                tasks.append(run_with_sem())
        results = []
        if tasks:
            results = await asyncio.gather(*tasks)
        # collect discovered subdomains
        for step in self.workflow.get("steps", []):
            tool = step.get("tool")
            if tool in ("subfinder", "amass", "assetfinder", "findomain"):
                path = self.base_dir / f"{tool}.txt"
                for line in safe_read_lines(path):
                    if line:
                        self.discovered.add(line.strip())
        self.log(f"[+] Passive enumeration total found: {len(self.discovered)}")
        return results

    async def run_gobuster_dns(self, step):
        """Run DNS brute force via gobuster (if enabled)"""
        tool = "gobuster_dns"
        if not step.get("enabled"):
            return []
        sem = self.tool_semaphores.get(tool, asyncio.Semaphore(1))
        wordlist = step.get("wordlist") or DEFAULT_DNS_WORDLIST
        threads = int(step.get("workers", 20))
        template = DEFAULT_TOOLS.get(tool, {}).get("cmd", "")
        cmd = template.format(target=self.target, wordlist=wordlist, threads=threads)
        out_path = self.base_dir / f"{tool}.txt"
        async with sem:
            lines = await self._run_tool_cmd(cmd, str(out_path), tool)
        # add to discovered
        for l in safe_read_lines(out_path):
            self.discovered.add(l.strip())
        self.log(f"[+] After gobuster_dns discovered: {len(self.discovered)}")
        return lines

    async def run_permutation(self, step):
        """Run permutation brute force (internal)"""
        tool = "permutation"
        if not step.get("enabled"):
            return []
        sem = self.tool_semaphores.get(tool, asyncio.Semaphore(1))
        wordlist = step.get("wordlist") or DEFAULT_WORDLIST
        workers = int(step.get("workers", 10))
        # this is CPU/light IO bound - we'll just run the generator synchronously inside semaphore
        async with sem:
            sources = sorted(self.discovered)[:1000]  # limit to first 1000 discovered subdomains to avoid explosion
            self.log(f"[permutation] Generating permutations from {len(sources)} base subs (wordlist: {wordlist})")
            generated = generate_permutations(sources, wordlist, max_per_domain=1000)
            perm_path = self.base_dir / "permutations.txt"
            with open(perm_path, "w", errors="ignore") as f:
                for p in generated:
                    f.write(p + "\n")
            # we may attempt DNS resolve / check later, for now just add to discovered
            for p in generated:
                self.discovered.add(p)
            self.log(f"[permutation] Generated {len(generated)} permutations, combined total now {len(self.discovered)}")
            return generated

    async def run_ffuf_probe(self, step):
        """
        For each discovered host (or a filtered subset), run ffuf to probe for content.
        We'll run ffuf jobs concurrently but bounded by tool semaphore.
        """
        tool = "ffuf"
        if not step.get("enabled"):
            return []
        sem = self.tool_semaphores.get(tool, asyncio.Semaphore(1))
        ffuf_wordlist = step.get("wordlist") or DEFAULT_WORDLIST
        threads = int(step.get("workers", 10))
        template = DEFAULT_TOOLS.get(tool, {}).get("cmd", "")
        # choose hosts to probe - dedupe, maybe only hostnames with www or base name
        hosts = sorted(self.discovered)
        # limit probes per job to avoid overloading
        hosts = hosts[:200]
        self.log(f"[ffuf] Probing {len(hosts)} hosts with ffuf (wordlist={ffuf_wordlist})")
        async def run_ffuf_on_host(host):
            async with sem:
                output_name = self.base_dir / f"ffuf_{host.replace('/','_').replace(':','_')}.json"
                cmd = template.format(host=host, wordlist=ffuf_wordlist, threads=threads, output=str(output_name))
                await self._run_tool_cmd(cmd, str(output_name), "ffuf")
        tasks = [run_ffuf_on_host(h) for h in hosts]
        if tasks:
            await asyncio.gather(*tasks)
        return hosts

    async def run_portscan(self, step):
        """
        Perform a fast portscan per discovered host. Try masscan first (if present), then nmap.
        We'll run at most N concurrent portscans (controlled by semaphore).
        """
        tool_m = "masscan"
        tool_n = "nmap"
        sem_m = self.tool_semaphores.get(tool_m, asyncio.Semaphore(1))
        sem_n = self.tool_semaphores.get(tool_n, asyncio.Semaphore(1))
        workers_m = int(next((s for s in self.workflow.get("steps", []) if s.get("tool")==tool_m), {}).get("workers", 1) or 1)
        workers_n = int(next((s for s in self.workflow.get("steps", []) if s.get("tool")==tool_n), {}).get("workers", 1) or 1)

        # hosts to scan - limit and dedupe
        hosts = sorted(self.discovered)[:100]
        self.log(f"[portscan] Scanning {len(hosts)} hosts (masscan workers={workers_m}, nmap workers={workers_n})")

        async def scan_host(host):
            # attempt masscan quickly (if available)
            masscan_template = DEFAULT_TOOLS.get("masscan", {}).get("cmd")
            nmap_template = DEFAULT_TOOLS.get("nmap", {}).get("cmd")
            if masscan_template:
                out_path_m = self.base_dir / f"masscan_{host}.grep"
                async with sem_m:
                    cmd_m = masscan_template.format(host=host, output=str(out_path_m))
                    rc, out, err = await run_subprocess_async(cmd_m)
                    if rc == 127:
                        self.log("[masscan] not installed or failed, skipping masscan")
                    elif rc == 0 and os.path.exists(out_path_m):
                        lines = safe_read_lines(out_path_m)
                        # if masscan found open ports we can feed to nmap; else fallback to nmap full
                        self.log(f"[masscan] {host} scan wrote {len(lines)} lines")
            # always run nmap (some hosts may not require masscan)
            out_path_n = self.base_dir / f"nmap_{host}"
            async with sem_n:
                cmd_n = nmap_template.format(output=str(out_path_n), host=host)
                rc, out, err = await run_subprocess_async(cmd_n)
                if rc == 127:
                    self.log("[nmap] not installed or failed")
                else:
                    self.log(f"[nmap] scanned {host} (rc={rc})")
        # run with concurrency limited by semaphores controlling masscan/nmap combined
        tasks = [scan_host(h) for h in hosts]
        if tasks:
            await asyncio.gather(*tasks)
        return hosts

    def write_combined_results(self):
        ensure_dir(self.base_dir)
        with open(self.combined_file, "w", errors="ignore") as f:
            for s in sorted(self.discovered):
                f.write(s + "\n")
        self.log(f"[+] Combined results saved to {self.combined_file} ({len(self.discovered)} unique)")

    async def run_pipeline(self):
        """
        Full pipeline orchestration.
        Steps in order: passive -> gobuster_dns -> permutation -> dedupe (write) -> ffuf -> portscan
        """
        try:
            self.log(f"=== START JOB {self.job_id} target={self.target} at {datetime.now().isoformat()} ===")

            # passive enumeration
            await self.run_passive_tools()

            # DNS brute force / gobuster
            gob_step = next((s for s in self.workflow.get("steps", []) if s.get("tool")=="gobuster_dns"), None)
            if gob_step:
                await self.run_gobuster_dns(gob_step)

            # permutation
            perm_step = next((s for s in self.workflow.get("steps", []) if s.get("tool")=="permutation"), None)
            if perm_step:
                await self.run_permutation(perm_step)

            # write combined
            self.write_combined_results()

            # ffuf probing
            ffuf_step = next((s for s in self.workflow.get("steps", []) if s.get("tool")=="ffuf"), None)
            if ffuf_step:
                await self.run_ffuf_probe(ffuf_step)

            # portscan
            port_step = next((s for s in self.workflow.get("steps", []) if s.get("tool") in ("masscan","nmap")), None)
            if port_step:
                await self.run_portscan(port_step)

            self.log(f"=== JOB {self.job_id} COMPLETE: {len(self.discovered)} unique subdomains. Results: {self.base_dir} ===")
        except Exception as e:
            self.log(f"[!!!] Job {self.job_id} failed: {e}")

# ----------------------------
# GUI
# ----------------------------
class OrchestratorGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Subdomain Orchestrator — The XSS Rat")
        self.workflows = load_workflows() or {"default_basic": DEFAULT_WORKFLOW}
        if not self.workflows:
            self.workflows = {"default_basic": DEFAULT_WORKFLOW}
        self._jobs = {}  # job_id -> dict with runner, thread, status
        self._build_ui()

    def _build_ui(self):
        # top frame: workflow selection
        top = ttk.Frame(self.root)
        top.pack(fill="x", padx=6, pady=6)

        ttk.Label(top, text="Workflow:").grid(row=0, column=0, sticky="w")
        self.workflow_combo = ttk.Combobox(top, values=list(self.workflows.keys()))
        self.workflow_combo.grid(row=0, column=1, sticky="ew", padx=4)
        self.workflow_combo.set(list(self.workflows.keys())[0])
        ttk.Button(top, text="Edit Workflow", command=self.edit_workflow).grid(row=0, column=2, padx=4)
        ttk.Button(top, text="Save Workflow As...", command=self.save_workflow_as).grid(row=0, column=3, padx=4)
        ttk.Button(top, text="Reload Workflows", command=self.reload_workflows).grid(row=0, column=4, padx=4)

        # middle: target input and per-tool worker overrides
        mid = ttk.Frame(self.root)
        mid.pack(fill="x", padx=6, pady=6)

        ttk.Label(mid, text="Target domain:").grid(row=0, column=0, sticky="w")
        self.target_entry = ttk.Entry(mid)
        self.target_entry.grid(row=0, column=1, sticky="ew", columnspan=3, padx=4)

        ttk.Label(mid, text="Job name (optional):").grid(row=1, column=0, sticky="w")
        self.jobname_entry = ttk.Entry(mid)
        self.jobname_entry.grid(row=1, column=1, sticky="ew", columnspan=3, padx=4)

        # per-tool overrides
        ttk.Label(mid, text="Per-tool worker overrides (tool:workers comma-separated):").grid(row=2, column=0, columnspan=4, sticky="w")
        self.overrides_entry = ttk.Entry(mid)
        self.overrides_entry.grid(row=3, column=0, columnspan=4, sticky="ew", padx=4)

        # job control buttons
        controls = ttk.Frame(self.root)
        controls.pack(fill="x", padx=6, pady=6)
        ttk.Button(controls, text="Start Job", command=self.start_job).pack(side="left")
        ttk.Button(controls, text="Start Multiple Jobs (batch from file)", command=self.start_jobs_from_file).pack(side="left", padx=4)
        ttk.Button(controls, text="Stop Selected Job", command=self.stop_selected_job).pack(side="left", padx=4)
        ttk.Button(controls, text="Open Results Dir", command=self.open_results_dir).pack(side="left", padx=4)

        # bottom: job list and logs
        bottom = ttk.PanedWindow(self.root, orient="horizontal")
        bottom.pack(fill="both", expand=True, padx=6, pady=6)

        # left: job table
        left = ttk.Frame(bottom)
        bottom.add(left, weight=1)
        ttk.Label(left, text="Jobs:").pack(anchor="w")
        self.jobs_tree = ttk.Treeview(left, columns=("id","target","status","started"), show="headings", selectmode="browse")
        for c in ("id","target","status","started"):
            self.jobs_tree.heading(c, text=c)
            self.jobs_tree.column(c, width=150, anchor="w")
        self.jobs_tree.pack(fill="both", expand=True)
        self.jobs_tree.bind("<<TreeviewSelect>>", self.on_job_select)

        # right: log output
        right = ttk.Frame(bottom)
        bottom.add(right, weight=3)
        ttk.Label(right, text="Log:").pack(anchor="w")
        self.log_text = tk.Text(right, height=30, bg="#111", fg="#0f0", insertbackground="white")
        self.log_text.pack(fill="both", expand=True)

    def log(self, msg):
        ts = datetime.now().strftime("%H:%M:%S")
        self.log_text.insert("end", f"[{ts}] {msg}\n")
        self.log_text.see("end")
        print(msg)

    def reload_workflows(self):
        self.workflows = load_workflows() or {"default_basic": DEFAULT_WORKFLOW}
        self.workflow_combo['values'] = list(self.workflows.keys())
        self.log("[+] Workflows reloaded.")

    def edit_workflow(self):
        name = self.workflow_combo.get()
        if name not in self.workflows:
            messagebox.showerror("Error", "Workflow not found")
            return
        wf = self.workflows[name]
        # open a simple editor dialog (JSON)
        txt = json.dumps(wf, indent=2)
        editor = tk.Toplevel(self.root)
        editor.title(f"Edit workflow: {name}")
        text = tk.Text(editor, width=100, height=40)
        text.pack(fill="both", expand=True)
        text.insert("1.0", txt)
        def save_and_close():
            try:
                new = json.loads(text.get("1.0","end"))
                self.workflows[name] = new
                save_workflows(self.workflows)
                self.reload_workflows()
                editor.destroy()
                self.log(f"[+] Workflow {name} updated.")
            except Exception as e:
                messagebox.showerror("JSON error", str(e))
        ttk.Button(editor, text="Save", command=save_and_close).pack()

    def save_workflow_as(self):
        # save current selected workflow under a new name (file dialog)
        name = self.workflow_combo.get()
        if name not in self.workflows:
            messagebox.showerror("Error", "Workflow not found")
            return
        wf = self.workflows[name]
        newname = simpledialog.askstring("Save Workflow As", "New workflow name:")
        if not newname:
            return
        wf_copy = dict(wf)
        wf_copy["name"] = newname
        self.workflows[newname] = wf_copy
        save_workflows(self.workflows)
        self.reload_workflows()
        self.log(f"[+] Workflow saved as {newname}")

    def parse_overrides(self, text):
        """Parse 'tool:workers,tool2:workers' style input into dict."""
        out = {}
        if not text:
            return out
        parts = text.split(",")
        for p in parts:
            if ":" in p:
                t,w = p.split(":",1)
                try:
                    out[t.strip()] = int(w.strip())
                except:
                    pass
        return out

    def start_job(self):
        target = self.target_entry.get().strip()
        if not target:
            messagebox.showerror("Error", "Enter a target domain")
            return
        workflow_name = self.workflow_combo.get()
        if workflow_name not in self.workflows:
            messagebox.showerror("Error", "Select a valid workflow")
            return
        workflow = self.workflows[workflow_name]
        job_id = (self.jobname_entry.get().strip() or f"job_{uuid.uuid4().hex[:6]}")
        overrides = self.parse_overrides(self.overrides_entry.get().strip())
        # create runner
        job_runner = JobRunner(job_id=job_id, target=target, workflow=workflow, per_tool_overrides=overrides, gui_log_callback=lambda m, jid=job_id: self.job_log(jid,m))
        # create asyncio thread to run pipeline (wrap in thread to not block)
        def run_in_thread(runner: JobRunner):
            asyncio.run(runner.run_pipeline())
            self._jobs[job_id]["status"] = "finished"
            self.update_job_row(job_id)
        # insert job into table
        started = datetime.now().isoformat()
        self._jobs[job_id] = {"runner": job_runner, "thread": None, "status": "running", "started": started}
        self.jobs_tree.insert("", "end", iid=job_id, values=(job_id, target, "running", started))
        # start thread
        t = threading.Thread(target=run_in_thread, args=(job_runner,), daemon=True)
        self._jobs[job_id]["thread"] = t
        t.start()
        self.log(f"[+] Job {job_id} started for {target}")

    def start_jobs_from_file(self):
        """
        Accept a simple text file where each line is:
        target,workflow_name,overrides
        overrides example: gobuster_dns:30,ffuf:8
        """
        path = filedialog.askopenfilename(title="Select batch file (.txt)", filetypes=[("Text files","*.txt"),("All files","*.*")])
        if not path:
            return
        with open(path, "r", errors="ignore") as f:
            for line in f:
                line=line.strip()
                if not line or line.startswith("#"):
                    continue
                parts = [p.strip() for p in line.split(",")]
                target = parts[0]
                workflow_name = parts[1] if len(parts) > 1 else self.workflow_combo.get()
                overrides = parts[2] if len(parts) > 2 else ""
                self.target_entry.delete(0, "end")
                self.target_entry.insert(0, target)
                self.workflow_combo.set(workflow_name)
                self.overrides_entry.delete(0, "end")
                self.overrides_entry.insert(0, overrides)
                self.start_job()
                time.sleep(0.2)

    def stop_selected_job(self):
        sel = self.jobs_tree.selection()
        if not sel:
            messagebox.showerror("Error", "Select a job in the list")
            return
        jid = sel[0]
        job = self._jobs.get(jid)
        if not job:
            messagebox.showerror("Error", "Job not found")
            return
        # we cannot reliably kill asyncio tasks started in subprocesses from python without tracking PIDs.
        # as a best-effort, mark as stopping and attempt to join thread (user may have to manually kill tool processes)
        job["status"] = "stopping"
        self.update_job_row(jid)
        self.log(f"[!] Stopping job {jid} — best effort (may not kill external tool processes).")

    def open_results_dir(self):
        ensure_dir(RESULTS_DIR)
        # open file explorer - platform-specific
        import webbrowser, sys
        if sys.platform.startswith("linux"):
            subprocess.Popen(["xdg-open", str(RESULTS_DIR)])
        elif sys.platform.startswith("darwin"):
            subprocess.Popen(["open", str(RESULTS_DIR)])
        elif sys.platform.startswith("win"):
            os.startfile(str(RESULTS_DIR))
        else:
            webbrowser.open(str(RESULTS_DIR))

    def on_job_select(self, event):
        sel = self.jobs_tree.selection()
        if not sel:
            return
        jid = sel[0]
        self.show_job_logs(jid)

    def update_job_row(self, job_id):
        job = self._jobs.get(job_id)
        if not job:
            return
        status = job.get("status","running")
        self.jobs_tree.item(job_id, values=(job_id, job["runner"].target if job.get("runner") else "", status, job.get("started","")))

    def job_log(self, job_id, msg):
        self.log(f"[{job_id}] {msg}")

    def show_job_logs(self, job_id):
        # show combined file if exists
        job = self._jobs.get(job_id)
        if not job:
            return
        runner = job.get("runner")
        if not runner:
            return
        combined = runner.combined_file
        self.log_text.delete("1.0","end")
        self.log_text.insert("end", f"==== Logs for job {job_id} (target: {runner.target}) ====\n")
        # show files present in results dir
        for path in sorted(runner.base_dir.glob("*")):
            self.log_text.insert("end", f"-- {path.name} --\n")
            # show small files
            if path.is_file() and path.stat().st_size < 200000:
                try:
                    with open(path, "r", errors="ignore") as f:
                        data = f.read()
                    self.log_text.insert("end", data + "\n\n")
                except Exception as e:
                    self.log_text.insert("end", f"[Could not read file: {e}]\n")
            else:
                self.log_text.insert("end", f"[File too large to display or not readable]\n\n")
        self.log_text.see("end")

# ----------------------------
# Main
# ----------------------------
def main():
    ensure_dir(RESULTS_DIR)
    # ensure workflows file exists
    wfs = load_workflows()
    if not wfs:
        save_workflows({"default_basic": DEFAULT_WORKFLOW})
    root = tk.Tk()
    app = OrchestratorGUI(root)
    root.mainloop()

if __name__ == "__main__":
