to get the server set up:

cd into the servers directory that you want to run
(either FingerPrintScanner/Servers/client_server or FingerPrintScanner/Servers/auth_server).
run `workon FingerPrintScanner`
If it fails, run `mkvirtualenv FingerPrintScanner`
run `pip install -r requirements.txt`
run `. develop.sh`

to get the server running:
Set up the server using the instructions above.
now, while still in the server directory, run `./manage.py runserver`.
The host for this server will be `http://127.0.0.1:8000/`

If you are trying to run BOTH servers, one of the runserver commands should look
like: `./manage.py runserver 127.0.0.1:8010`. The host for this server will be
`http://127.0.0.1:8010/`
