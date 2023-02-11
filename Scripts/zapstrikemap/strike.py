import subprocess

with open("urls.txt") as f:
    urls = f.read().splitlines()

for url in urls:
    print("Running XSStrike on:", url)
    with open("xsstrike_output_" + url.replace("/", "_") + ".txt", "w") as f:
        subprocess.run(["xsstrike", "-u", url], stdout=f, stderr=subprocess.STDOUT)
    print("Running sqlmap on:", url)
    with open("sqlmap_output_" + url.replace("/", "_") + ".txt", "w") as f:
        subprocess.run(["sqlmap", "-u", url, "--batch"], stdout=f, stderr=subprocess.STDOUT)
    print("Running OWASP ZAP on:", url)
    with open("zap_output_" + url.replace("/", "_") + ".txt", "w") as f:
        subprocess.run(["zap-cli", "start", "--quick-scan", url], stdout=f, stderr=subprocess.STDOUT)
