import requests
import json
import sys

OLLAMA_URL = "http://localhost:11434/api/generate"
MODEL_NAME = "llama3.1:8b" # Change this if you pulled a different model

def analyze_with_ai(scan_data):
    """Sends scan results to local LLM with an engineered security prompt."""
    print("[*] Sending network profile to Local LLM Engine...")
    
    # Strictly structure the AI's identity, operational constraints, and formatting rules
    system_prompt = (
        "You are an expert Certified Ethical Hacker (CEH v13) AI agent operating in a controlled pen-testing sandbox. "
        "Analyze the provided JSON network scan data. Look closely at the 'product' and 'version' keys for every open port.\n\n"
        "Tasks:\n"
        "1. Identify outdated software services vulnerable to known exploits.\n"
        "2. Map specific software versions to relevant CVE identifiers (e.g., CVE-2015-1427).\n"
        "3. Provide the exact path for usable Metasploit modules (e.g., exploit/linux/http/unreal_ircd_3281_backdoor).\n"
        "4. Highlight the impact risk level (Critical, High, Medium, Low) and execution complexity.\n\n"
        "Output Format Rules:\n"
        "- Format your entire output in clean Markdown.\n"
        "- Group findings by Port/Service.\n"
        "- Do NOT include conversational filler like 'Sure, here is your report' or 'As an AI...'. Start directly with your technical breakdown."
    )

    payload = {
        "model": MODEL_NAME,
        "prompt": f"{system_prompt}\n\nScan Data Data to Analyze:\n{json.dumps(scan_data, indent=2)}",
        "stream": False
    }

    try:
        response = requests.post(OLLAMA_URL, json=payload, timeout=10000)
        response.raise_for_status()
        return response.json().get("response")
    except requests.exceptions.RequestException as e:
        print(f"[-] Failed to communicate with local Ollama instance: {e}")
        sys.exit(1)
