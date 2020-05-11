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

## Rooms.csv
Die `rooms.csv` beinhaltet die spielbaren Räume, in denen sich der Spieler befindet. Die Datei bietet Infos dazu, was man alles in welchem Raum machen kann und wie er aussieht.

Und so ist die `rooms.csv` mit Syntax aufgebaut. Wichtig! Die Überschriften sind selbst nicht in der CSV drin:

| ID | Room Name | Introduction | Description | Connections | Triggers |
| -- | --------- |--------------|----------|-------------|-------------|
| 0 | "room 1" | "As you go into this room you feel really weird. You see blabla" | "You look around the room and see two doors and an old lady." | "door"?"room 2";"trap door"?"hidden room"| "collect Key"&"Congrats you collected an old key";"use key"&"You open the door with a key" |


ID: Die Raum-ID, für jeden Raum einzigartig, gleich der Zeilenzahl.

Room Name: Einzigartiger Name für den Raum als String.

Introduction: Ein Text der beim Betreten des Raumes gezeigt wird

Triggers: Raumspezifische Trigger-Sätze, nachdem diese aufgerufen wurden wird der Text hinter & gezeigt. "trigger sentence"&"what happens after".

Connections: Die Räume, die mit dem in der Zeile gezeigten Raum verbunden sind. Der erste string zeigt den Alias des Raumes, die der Spieler im Text benutzen kann. Da der Spieler vor betreten des Raumes, nicht seinen richtigen Namen kennt. "that weird door"?"room 2"

Description: Wird bei "look around" ausgeführt. Beschreibt den Raum, wenn man schon drinne steht. "This room is old and dirty. It is dark"

Notes: Informationen, diese Spalte wird nicht vom code benutzt. Allerdings beschreibt sie beispielsweise boolische Werte, die eingebeut werden müssen.
