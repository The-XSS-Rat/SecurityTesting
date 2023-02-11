import subprocess

def scan_contract_mythril(contract_file):
    result = subprocess.run(["myth -x --max-depth 100 " + contract_file], shell=True, stdout=subprocess.PIPE)
    return result.stdout.decode("utf-8")

def scan_contract_oyente(contract_file):
    result = subprocess.run(["oyente " + contract_file], shell=True, stdout=subprocess.PIPE)
    return result.stdout.decode("utf-8")

def scan_contract_securify(contract_file):
    result = subprocess.run(["securify " + contract_file], shell=True, stdout=subprocess.PIPE)
    return result.stdout.decode("utf-8")

contract_file = "your_contract_file.sol"
scan_results_mythril = scan_contract_mythril(contract_file)
print("Results from Mythril:")
print(scan_results_mythril)

scan_results_oyente = scan_contract_oyente(contract_file)
print("Results from Oyente:")
print(scan_results_oyente)

scan_results_securify = scan_contract_securify(contract_file)
print("Results from Securify:")
print(scan_results_securify)
