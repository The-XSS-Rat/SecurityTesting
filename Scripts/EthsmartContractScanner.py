import subprocess

def scan_contract(contract_file):
    result = subprocess.run(["myth -x --max-depth 100 " + contract_file], shell=True, stdout=subprocess.PIPE)
    return result.stdout.decode("utf-8")

contract_file = "your_contract_file.sol"
scan_results = scan_contract(contract_file)
print(scan_results)
