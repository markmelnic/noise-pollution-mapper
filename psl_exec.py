
import sys
import subprocess

def exec_gps():
    cmd = ["PowerShell", "-ExecutionPolicy", "Unrestricted", "-File", ".\\pshell.ps1"]
    ec = str(subprocess.check_output(cmd, shell=True))
    return ec[80:-13].split(" ")
