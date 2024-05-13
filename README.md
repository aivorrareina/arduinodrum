# Robot Drum Machine

## Dependencias python

```shell
 python -m venv venv 
 source venv/bin/activate
 python3 -m pip install alsa-midi
```

## Comando para arrancar servicio
```
sudo /home/angel/arduinodrum/venv/bin/python3 /home/angel/arduinodrum/server.py 
```

## Servidor service file

```
[Unit]
Description=Puto robot servidor
After=syslog.target network.target

[Service]
WorkingDirectory=/home/angel/arduinodrum/
ExecStart=/home/angel/arduinodrum/venv/bin/python3 server.py 

Restart=always
RestartSec=120

[Install]
WantedBy=multi-user.target
```