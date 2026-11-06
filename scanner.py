import nmap
import json
import sys

def run_network_scan(target_ip):
    """Scans the target IP for open ports and service versions."""
    nm = nmap.PortScanner()
    print(f"[*] Initializing Nmap scan for target: {target_ip}...")
    
    try:
        # -sV: Version detection, -T4: Faster execution, -F: Fast scan (top 100 ports)
        nm.scan(target_ip, arguments="-sV -T4 -F")
    except Exception as e:
        print(f"[-] Nmap scan failed: {e}")
        sys.exit(1)

    if target_ip not in nm.all_hosts():
        print("[-] Target host seems down or unreachable.")
        return None

    scan_results = {
        "target": target_ip,
        "status": nm[target_ip].state(),
        "vulnerabilities_found": []
    }

    for proto in nm[target_ip].all_protocols():
        ports = nm[target_ip][proto].keys()
        for port in ports:
            service_info = nm[target_ip][proto][port]
            port_data = {
                "port": port,
                "protocol": proto,
                "state": service_info.get("state"),
                "service_name": service_info.get("name"),
                "product": service_info.get("product"),
                "version": service_info.get("version"),
                "extrainfo": service_info.get("extrainfo")
            }
            scan_results["vulnerabilities_found"].append(port_data)
            
    return scan_results

if __name__ == "__main__":
    # Test the scanner independently
    test_target = "127.0.0.1"
    results = run_network_scan(test_target)
    print(json.dumps(results, indent=4))
