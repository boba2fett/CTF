# BWI Challenge
https://www.get-in-it.de/coding-challenge?utm_campaign=coding-challenge&utm_content=code-and-win

This is my solution for the coding challenge.

## Execute
### Install dependencies
If not already present install python3 with pip:
```
sudo apt update
sudo apt install python3 python3-pip -y
```
Install dependencies for script:
```
python3 -m pip install -U -r requirements.txt
```
### Usage
```
usage: load.py [-h] [-o OUTPUT] datafile

Calculates the best load list for a specified data file in json format

positional arguments:
  datafile              datafile to read data from

optional arguments:
  -h, --help            show this help message and exit
  -o OUTPUT, --output OUTPUT
                        output loadlist to specified file
```

### Example
For this Challenge:
```
python3 load.py data.json -o loadlist.json
```

### Solution
The solution is already in `loadlist.json`

Of course the best would be a whole bruteforce atempt on which items to take with, but there are too many possibilities to consider, so we just bruteforce the best combination of drivers and transporters and witch transporter to start with loading the best value per weight items, but with a capacity use of 99.94%, I think there is no better solution.

The solution is held general not only to solve this load problem, but any presented in the right json format.

# BWI Challenge Deutsch German
https://www.get-in-it.de/coding-challenge?utm_campaign=coding-challenge&utm_content=code-and-win

Das ist meine Lösung.

## Ausführen
### Abhängigkeiten installieren
Wenn noch nicht vorhanden installiere python3 und pip:
```
sudo apt update
sudo apt install python3 python3-pip -y
```
Und die Abhängigkeien für dieses Skript
```
python3 -m pip install -U -r requirements.txt
```
### Benutzung
```
usage: load.py [-h] [-o OUTPUT] datafile

Calculates the best load list for a specified data file in json format

positional arguments:
  datafile              datafile to read data from

optional arguments:
  -h, --help            show this help message and exit
  -o OUTPUT, --output OUTPUT
                        output loadlist to specified file
```

### Beispiel
Für diese Challenge:
```
python3 load.py data.json -o loadlist.json
```

### Lösung
Die Lösung befindet sich bereits in `loadlist.json`

Die perfekte Lösung wäre natürlich alle Kombinationen der Hardware Teile durchzuprobieren, dafür sind es aber deutlich zu viele Möglichkeiten, deshalb werden nur die Fahrer über die Transporter rotiert und die Reihenfolge der Transporter in die die besten Teile basierend auf dem Wert pro Gewicht geladen werden durchprobiert.

Die Lösung ist generell gehalten um auch mit andere Eingaben in Form von json zu akzeptieren.