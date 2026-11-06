#!/bin/bash
echo "======================Hardware Requirement======================"
echo "12 GB+ Plus Free Storage" 
echo "4+ vCore CPU"
echo "RAM 16 GB+"
echo "----------------------------------------------------------------------"
sleep 15

echo "update repository............................"
apt update -y && apt upgrade -y
echo "downloading and Install ollama .............."
curl -fsSL https://ollama.com/install.sh | sh
echo "Show ollamba version"
ollama --version
echo "pull a lightweight, capable model llama3.1:8b.......... "
ollama run llama3.1:8b
/bye
echo "ollam service status"
systemctl  status  ollama
echo "Create a Virtual Environment & Activate it..............."
python3 -m venv venv
source venv/bin/activate
export PATH="$PATH:$(pwd)"
echo "install dependency packages ......................."
pip install python-nmap requests pymetasploit3 
apt update -y && apt install pandoc -y
msfrpcd -P Ceh@123 -p 55552 -S
echo "Everything is Ready For you wait few seconds!"
sleep 20
echo "Enjoy AI Automation Script"
sleep 5
./menu.sh
