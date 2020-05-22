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

**Für nltk bitte wordnet installieren**
Dazu einfach in die Python Konsole gehen und eintippen

`import nltk` und danach

`nltk.download('wordnet')`

## Bekannte Fehler

Beim Upgrade von pip mit `python -m pip install --upgrade pip`:

Schließt vor dem Ausführen des Befehls alle Fenster, die irgendeine Datei aus dem Virtual Environment geöffnet haben. Das führt sonst zu folgendem Fehler:

```
  File "C:\Users\Kevin Katzkowski\Documents\Uni\Chatbot\venv\lib\site-packages\pip__main__.py", line 16, in <module>
    from pip._internal.cli.main import main as _main  # isort:skip # noqa
ModuleNotFoundError: No module named 'pip._internal.cli'
```

Solltet ihr diesen Fehler bereits haben, müsst ihr das Virtual Enviroment löschen und ein Neues anlegen. Das Virtual Enviroment sollte `venv` heißen, damit es von der gitignore ignoriert wird.

## Ausführen

Aktuell läuft der Server lokal.

Öffnet einfach die Konsole im Order der `main.py` Datei und benutzt

`python main.py`

Wenn der Server gestartet ist, öffnet einen Browser unter addresse [http://localhost:5000](http://localhost:5000).

Prüft die Connection, indem ihr die developer tools öffnet und den Reiter Console anklickt. Dort sollte wenn alles geklappt hat `connected client` stehen.

## Rooms.csv
Die `rooms.csv` beinhaltet die spielbaren Räume, in denen sich der Spieler befindet. Die Datei bietet Infos dazu, was man alles in welchem Raum machen kann und wie er aussieht.

Spaltentrennung mit "$"!!!

Und so ist die `rooms.csv` mit Syntax aufgebaut. Wichtig! Die Überschriften sind selbst nicht in der CSV drin:

| ID | Room Name | Introduction | Description | Connections | Triggers |
| -- | --------- |--------------|----------|-------------|-------------|
| 0 | room 1 | "As you go into this room you feel really weird. You see blabla" | "You look around the room and see two doors and an old lady." | door?1;trap door?2 | collect Key&"Congrats you collected an old key";use key&"You open the door with a key" |


ID: Die Raum-ID, für jeden Raum einzigartig, gleich der Zeilenzahl.

Room Name: Einzigartiger Name für den Raum als String.

Introduction: Ein Text der beim Betreten des Raumes gezeigt wird

Triggers: Raumspezifische Trigger-Sätze, nachdem diese aufgerufen wurden wird der Text hinter & gezeigt. "trigger sentence"&"what happens after".

Connections: Die Räume, die mit dem in der Zeile gezeigten Raum verbunden sind. Der erste string zeigt den Alias des Raumes, die der Spieler im Text benutzen kann. Da der Spieler vor betreten des Raumes, nicht seinen richtigen Namen kennt. "that weird door"?"room 2"

Description: Wird bei "look around" ausgeführt. Beschreibt den Raum, wenn man schon drinne steht. "This room is old and dirty. It is dark"

Notes: Informationen, diese Spalte wird nicht vom code benutzt. Allerdings beschreibt sie beispielsweise boolische Werte, die eingebeut werden müssen.

## Server maintenance 

Prozess von der SSH session trennen:

-  into your remote box. type `screen` Then start the process you want.
- Press Ctrl-A then Ctrl-D. This will **detach** your screen session but leave your processes running. You can now log out of the remote box.
- If you want to come back later, log on again and type `screen -r` This will **resume** your screen session, and you can see the output of your process.