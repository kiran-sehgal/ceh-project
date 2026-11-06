import argparse
import os
from scanner import run_network_scan
from ai_engine import analyze_with_ai

def main():
    parser = argparse.ArgumentParser(description="CEH v13 AI-Powered Vulnerability Scanner & Exploit Suggester")
    parser.add_argument("-t", "--target", required=True, help="Target IP address to scan (e.g., 192.168.56.101)")
    parser.add_argument("-o", "--output", default="Exploit_Report.md", help="Filename for the generated Markdown report")
    args = parser.parse_args()

    target = args.target
    output_file = args.output

    print(f"\n=== CEH v13 AI OFFENSIVE SECURITY TOOL ===")
    
    # 1. Run network reconnaissance
    raw_scan_data = run_network_scan(target)
    
    if not raw_scan_data or not raw_scan_data["vulnerabilities_found"]:
        print("[-] No open services discovered. Exiting pipeline.")
        return

    print(f"[+] Discovered {len(raw_scan_data['vulnerabilities_found'])} open services.")

    # 2. Feed data to LLM and generate report
    ai_report = analyze_with_ai(raw_scan_data)

    # 3. Write final report to file
    try:
        with open(output_file, "w", encoding="utf-8") as f:
            f.write(ai_report)
        print(f"\n[+] Success! Vulnerability report saved to: {os.path.abspath(output_file)}")
        print("===========================================\n")
    except IOError as e:
        print(f"[-] Failed to write report file: {e}")

if __name__ == "__main__":
    main()
