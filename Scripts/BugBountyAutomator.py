import os
import sys
import subprocess

def install_requirements(tool):
    requirements = {
        'nmap': 'apt-get install nmap',
        'gobuster': 'apt-get install gobuster',
        'ffuf': 'apt-get install ffuf',
        'amass': 'snap install amass',
        'recon-ng': 'pip3 install recon-ng',
        'nuclei': 'GO111MODULE=on go get -u -v github.com/projectdiscovery/nuclei/v2/cmd/nuclei'
    }

    if tool in requirements:
        print(f"Installing requirements for {tool}:")
        os.system(requirements[tool])
    else:
        print(f"No installation requirements found for {tool}")

def execute_tool(tool, args):
    tool_commands = {
        'nmap': f'nmap {args}',
        'gobuster': f'gobuster {args}',
        'ffuf': f'ffuf {args}',
        'amass': f'amass {args}',
        'recon-ng': f'recon-ng {args}',
        'nuclei': f'nuclei {args}'
    }

    if tool in tool_commands:
        print(f"Executing {tool}:")
        os.system(tool_commands[tool])
    else:
        print(f"No execution command found for {tool}")

def main():
    tools = ['nmap', 'gobuster', 'ffuf', 'amass', 'recon-ng', 'nuclei']

    print("Select a tool to execute:")
    for i, tool in enumerate(tools):
        print(f"{i+1}. {tool}")

    choice = int(input("Enter the number of the tool you want to execute: "))
    if 0 < choice <= len(tools):
        tool = tools[choice-1]

        install_option = input(f"Do you want to install the requirements for {tool}? (y/n): ")
        if install_option.lower() == 'y':
            install_requirements(tool)

        args = input(f"Enter the arguments for {tool}: ")
        execute_tool(tool, args)
    else:
        print("Invalid choice. Exiting.")

if __name__ == "__main__":
    main()
