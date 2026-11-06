import json
from pymetasploit3.msfrpc import MsfRpcClient

def check_metasploit_payloads(scan_data, rpc_password):
    """
    Connects to Metasploit RPC, cross-references scan data to find compatible 
    exploit modules, and lists available payloads for them.
    """
    print("[*] Connecting to Metasploit RPC server...")
    try:
        # Initialize connection to msfrpcd
        client = MsfRpcClient(rpc_password, port=55552, ssl=False)
    except Exception as e:
        print(f"[-] Connection failed. Is msgrpc loaded in msfconsole? Error: {e}")
        return

    print("[+] Connected successfully! Verifying targets...\n")

    # Iterate through target ports discovered in your scan data
    for item in scan_data.get("ports", []):
        service = item.get("product", "")
        version = item.get("version", "")
        
        if not service:
            continue
            
        search_query = f"{service} {version}".strip()
        print(f"[*] Querying Metasploit database for: '{search_query}'")
        
        # Search the framework for matching exploit modules
        matched_modules = client.modules.search(search_query)
        
        # Filter for exploit types only
        exploits = [m for m in matched_modules if m.get('type') == 'exploit']
        
        if not exploits:
            print(f"    [-] No direct exploit modules found for {search_query}.\n")
            continue
            
        print(f"    [+] Found {len(exploits)} matching exploit module(s):")
        
        for exp in exploits:
            module_name = exp.get('fullname')
            print(f"    --> Module: {module_name}")
            
            try:
                # Load the specific exploit module instance
                exploit_mod = client.modules.use('exploit', module_name)
                
                # Fetch compatible payloads specifically validated for this module
                available_payloads = exploit_mod.target_payloads
                
                if available_payloads:
                    print(f"        [✓] Available Payloads ({len(available_payloads)} total):")
                    # List the first 5 suggested payloads for scannability
                    for payload in available_payloads[:5]:
                        print(f"            - {payload}")
                    if len(available_payloads) > 5:
                        print(f"            ... and {len(available_payloads) - 5} more.")
                else:
                    print("        [-] No specific target payloads returned for this module configuration.")
                    
            except Exception as mod_err:
                print(f"        [-] Could not inspect module payloads: {mod_err}")
        print("\n" + "="*50 + "\n")

if __name__ == "__main__":
    # Mock data structured exactly like your local AI scan pipeline input
    mock_scan_results = {
        "target": "127.0.0.1",
        "ports": [
            {"port": 21, "service": "ftp", "product": "vsftpd", "version": "2.3.4"},
            {"port": 6667, "service": "irc", "product": "UnrealIRCd", "version": "3.2.8.1"}
        ]
    }
    
    # Run automation using the password established in Phase 1
    rpc_password = "Ceh@123" 
    check_metasploit_payloads(mock_scan_results, rpc_password)
