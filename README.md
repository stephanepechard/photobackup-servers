# PhotoBackup servers
You can use PhotoBackup with many different servers, as long as you
follow the defined API. Here you can find:

* a Django server ;
* a Bottle server, only 100-line long.


# Bottle server
The simplest one. Install and enter the virtual environment with:

    make && source venv/bin/activate

Launch it with:

    gunicorn -w 4 photobackup:app -b 127.0.0.1:8010 

Host and port is just an example, right? :-)


# Anyone's server

Can't find the server that suit your needs?
Write it and push it to this repository!
