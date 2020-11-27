# TITLE: MD5 for life

## CHALLENGE INFOS

Type: Web

Server: 144.126.196.140:32140

Task: Can you encrypt fast enough?

## FIRST THOUGHTS

It might use MD5 as Hash algorithm
Maybe a python script can help us

## ATTEMPS

Let's try with burpsuite to see what packets is the server sending and how the client responds...
The server sends a packet with the following data:
{
    "hash": *string to hash*
}

So we might just want to send a packet back to the server in just few milliseconds...

## SOLUTION

Script: Python script
Libraries: requests, hashlib, bs4

We used a python script to intercept what the server is sending to us and, after that, we hash the string and send it back to the server...

Flag: HTB{N1c3_ScrIpt1nG_B0i!}
