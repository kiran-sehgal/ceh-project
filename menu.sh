#!/bin/bash

# Ensure virtual environment is active or can be activated
if [ -f "venv/bin/activate" ]; then
    source venv/bin/activate
else
    whiptail --title "Error" --msgbox "Virtual environment not found! Please run Step 2 first." 10 60
    exit 1
fi

while true; do
    # Main Menu Selection
    CHOICE=$(whiptail --title "AI Vulnerability & Payload Scanner" \
        --menu "Select an offensive security operation to execute:" 15 65 4 \
        "1" "Scan Target & Generate AI Report" \
        "2" "Identify Metasploit Payloads" \
        "3" "View Latest Exploit Report" \
        "4" "Exit Pipeline" 3>&1 1>&2 2>&3)

    # Check if user pressed Cancel
    if [ $? -ne 0 ]; then
        deactivate
        clear
        echo "[*] Pipeline exited safely."
        exit 0
    fi

    case $CHOICE in
        1)
            # Task 1: Scan Target
            TARGET_IP=$(whiptail --inputbox "Enter Target IP address (e.g., 192.168.56.101):" 10 60 "192.168.56.101" 3>&1 1>&2 2>&3)
            if [ $? -eq 0 ] && [ ! -z "$TARGET_IP" ]; then
                clear
                echo "=== Starting AI Network Scan ==="
                python main.py --target "$TARGET_IP"
                echo "================================"
                read -n 1 -s -r -p "Press any key to return to menu..."
            fi
            ;;
        2)
            # Task 2: Find Payloads via Metasploit RPC
            # First check if the RPC service port is active
            if ! ss -antp | grep -q "55552"; then
                whiptail --title "Dependency Missing" --msgbox "Metasploit RPC Server is not listening on port 55552!\nPlease run: msfrpcd -P Ceh@123 -p 55552 -S" 12 70
                continue
            fi

            whiptail --yesno "Execute Metasploit payload mapping automation script?" 10 60
            if [ $? -eq 0 ]; then
                clear
                echo "=== Launching Metasploit RPC Payload Matcher ==="
                python find_payload.py > payload_for_attack.txt
                cat payload_for_attack.txt
                echo "================================================"
                echo "[+] Output saved to payload_for_attack.txt"
                read -n 1 -s -r -p "Press any key to return to menu..."
            fi
            ;;
        3)
            # Auxiliary Feature: View the generated report inside TUI
            if [ -f "Exploit_Report.md" ]; then
                whiptail --title "Exploit_Report.md" --textbox Exploit_Report.md 22 75
            else
                whiptail --title "Not Found" --msgbox "No Exploit_Report.md found. Please run a scan first!" 10 60
            fi
            ;;
        4)
            deactivate
            clear
            echo "[*] Deactivated virtual environment. Goodbye!"
            exit 0
            ;;
    esac
done
