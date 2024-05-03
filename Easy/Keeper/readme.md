# Simple Writeup for notes

## Login in ticker subdomains using default creds ( root:password )

## Get creds of the ssh of the one of user

Username:lnorgaard
Password: Welcome2023!

## Login ssh and get the dmp and kdbx through zip

unzip and download loaclly with server python

## Using exploit to get know the passcodes

using keepass-dump-masterkey and a little osint
https://www.google.com/search?client=firefox-b-d&q=Mdgr%E2%97%8Fd+med+fl%E2%97%8Fde

we know the pass is rødgrød med fløde

## go to the root user in the db using keepassxc

`sh
sudo puttygen putty.ppk -O private-openssh -o id_rsa
sudo ssh -i id_rsa root@keeper.htb
`
convert ppk of the putty into id_rsa private and login root
