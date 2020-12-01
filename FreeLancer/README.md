# TITLE: Freelancer

## CHALLENGE INFOS

Type: Web

Server: 157.245.46.178:32726

Task: Can you test how secure my website is? Prove me wrong and capture the flag!

## FIRST THOUGHTS

It might be a SQL injection
I already saw the theme on start.bootstrap, maybe it's not that different

## ATTEMPS

Let's try using gobuster to scan the directories of the website

```bash

gobuster dir -u http://157.245.46.178:32726/ -w /usr/share/wordlists/dirb/big.txt

```

Here is the result

```bash
===============================================================
Gobuster v3.0.1
by OJ Reeves (@TheColonial) & Christian Mehlmauer (@_FireFart_)
===============================================================
[+] Url:            http://157.245.46.178:32726/
[+] Threads:        10
[+] Wordlist:       /usr/share/wordlists/dirb/big.txt
[+] Status codes:   200,204,301,302,307,401,403
[+] User Agent:     gobuster/3.0.1
[+] Timeout:        10s
===============================================================
2020/12/01 04:19:42 Starting gobuster
===============================================================
/.htpasswd (Status: 403)
/.htaccess (Status: 403)
/administrat (Status: 301)
/css (Status: 301)
/favicon.ico (Status: 200)
/img (Status: 301)
/js (Status: 301)
/mail (Status: 301)
/robots.txt (Status: 200)
/server-status (Status: 403)
/vendor (Status: 301)
===============================================================
2020/12/01 04:21:26 Finished
===============================================================
```

We can see /administrat is really interesting
I tried to look up robots.txt, .htpasswor and .htaccess but wasn't able to read them
Then i tried to scan for .php and html files and found out that the server was running php code on backend

```bash
gobuster dir -u http://157.245.46.178:32726/ -w /usr/share/wordlists/dirbuster/directory-list-lowercase-2.3-medium.txt -x php, html
```

Let's search for /administrat/panel.php

![/administrat/index.php](/login.png "/administrat/index.php")

## SOLUTION
