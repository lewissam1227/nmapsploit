import os
import re
import subprocess
import xml.etree.ElementTree as ET

def perform_nmap_scan(target, output_file):
    command = f"nmap -sV -oX {output_file} {target}"
    print(f"Running nmap scan on {target}")
    subprocess.run(command, shell=True, check=True, stdout=subprocess.DEVNULL)

def parse_nmap_output(output_file):
    tree = ET.parse(output_file)
    root = tree.getroot()
    services = []

    for host in root.findall("host"):
        for ports in host.findall("ports"):
            for port in ports.findall("port"):
                service = port.find("service")
                if service is not None:
                    services.append({
                        "port": port.get("portid"),
                        "name": service.get("name"),
                        "product": service.get("product"),
                        "version": service.get("version"),
                    })

    return services

def search_exploits(services):
    for service in services:
        product = service["product"]
        version = service["version"]

        if product and version:
            search_term = f"{product} {version}"
        elif product:
            search_term = product
        else:
            search_term = service["name"]

        print(f"Searching exploits for: {search_term}")
        command = f"searchsploit {search_term}"
        subprocess.run(command, shell=True)

def main():
    target = input("Enter the target IP address: ")
    output_file = "nmap_output.xml"

    perform_nmap_scan(target, output_file)
    services = parse_nmap_output(output_file)
    search_exploits(services)

if __name__ == "__main__":
    main()
