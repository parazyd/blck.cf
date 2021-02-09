blck
====

an ephemeral pastebin. you can only retrieve the paste once, and
afterwards it's deleted from the server.


installation
------------

get `python-flask` and execute `blck.py`.

if not running in debug mode, you also need `bjoern`. find it at
https://github.com/jonashaag/bjoern.

run `blck.py -h` to see usage info.


nginx
-----

```
location / {
	proxy_set_header Host $host;
	proxy_set_header X-Real-IP $remote_addr;
	proxy_set_header X-Forwarded-Proto https;
	proxy_pass http://127.0.0.1:5000;
}
```


usage
-----

either use the website, or curl:

```
curl -F 'c=@-' http://blck.cf < file
```
