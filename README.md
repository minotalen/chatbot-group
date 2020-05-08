# chatbot group

## Ordnerstruktur

```
chatbbot-group/
	static/
		css/
			css files hier
        js/
			js files hier
	templates/
		html files hier
	main.py (Server)
```

Bitte diese Struktur beibehalten, damit Flask richtig funktioniert.

Hier nochmal zum Nachlesen in der [Flask Dokumentation](https://exploreflask.com/en/latest/organizing.html).

## Installieren

Damit es läuft braucht jeder Python. Damit habt ihr auch pip und könnt in der Konsole folgende Befehle ausführen:

-Python installieren, empfohlenerweise in einem virtual environment(https://docs.python.org/3/library/venv.html), z.B. conda(https://anaconda.org/anaconda/conda)

-Konsole im git ordner öffnen

-Folgendes in die Konsole pasten und ausführen: `pip install -r requirements.txt`

Oder einzeln nacheinander:

`pip install Flask`

`pip install flask-socketio`

`pip install eventlet`

Sonst schaut nochmal in die [Flask-SocketIO Doku](https://flask-socketio.readthedocs.io/en/latest/).

## Ausführen

Aktuell läuft der Server lokal.

Öffnet einfach die Konsole im Order der `main.py` Datei und benutzt

`python main.py`

Wenn der Server gestartet ist, öffnet einen Browser unter addresse [http://localhost:5000](http://localhost:5000).

Prüft die Connection, indem ihr die developer tools öffnet und den Reiter Console anklickt. Dort sollte wenn alles geklappt hat `connected client` stehen. 

