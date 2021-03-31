Bei diesem Projekt handelt es sich um die Implementierung der Prüfungsvorleistung Spezielle Anwendungen der Informatik <br>
der HTW Berlin mit folgender [Aufgabenstellung](https://gitlab.com/baumannpa_teaching/ros-ai-task)

Das Ziel ist eine Anwendung zur Handschrifterkennung mittels künstlicher Intelligenz.

Das unter Task 3 beschriebene und verwendete Model ist [hier](https://github.com/marfen/spezAnw-mnist) zu finden.

-----

- [Ausführung](#ausführung)   
- [Implementierung](#implementierung)
    - [Task 1](#task-1)
        - [ROS Grundlagen](#ros-grundlagen)
        - [Nodes](#ros-nodes)
        - [Topics](#ros-topics)
        - [Messages](#ros-messages)
        - [Master](#ros-master)
    - [Task 2](#task-2)
    - [Task 3](#task-3)
        - [ROS Anpassungen](#ros-anpassungen)
        - [Model trainieren](#model-trainieren)
            - [MNIST-Datensatz vorbereiten](#mnist-datensatz-vorbereiten)
            - [Model](#model)
            - [Vergleich der Modelvarianten](#vergleich-unterschiedlich-trainierter-models)

---

# Ausführung 

### model trainieren
### trainiertes model in ros einfügen 
### ros starten
Zum Bauen der Anwendung muss der Befehl

> catkin_make

ausgeführt werden und anschließend kann die Anwendung mit

>roslaunch beginner_tutorials talker-listener.launch 

ausgeführt werden. Dafür wurde das File talker-listener.launch erstellt in welchem die zu startenden Nodes definiert
wurden.
---


# Implementierung

# Task 1

### ROS Grundlagen

ROS - kurz für Robot Operating System - ist ein Framework für Roboter dessen Entwicklung ursprünglich <br>
2007 am Stanford Artificial Intelligence Laboratory im Rahmen des Standford-AI-Projects (STAIR) begann<br>
und nun seit 2013 duch das ROS Industrial Consortium gefördert und unterstützt wird.

ROS ist eine Sammlung von Tools, Bibliotheken und Konventionen mit dem Ziel das Erstellen von komplexen <br>
und robusten Roboter Systemen zu vereinfachen


### ROS Nodes

Nodes sind zunächst einmal eigenständige Prozesse die bestimmte Dinge erledigen. Mehrere Nodes zusammen <br>
ergeben einen Graph und sie kommunizieren miteinander unter Verwendung von Topics, Messages und Services. <br>
ROS Anwendungen sollten möglichst fein granular mit vielen Nodes erstellt werden wobei jeder Node genau <br>
eine Aufgabe übernimmt

### ROS Topics

Ein Topic ist im Prinzip ein Bus über welchen Nodes Nachrichten austauschen. Um das zu realisieren wird das <br>
publisher-subscriber Prinzip verwendet. Einzelne Nodes können Nachrichten zu einem bestimmten Topic publizieren <br>
während andere Nodes die Topics abonnieren/subscriben können. Einzelne Nodes wissen dabei nicht zwingend mit <br>
welchen anderen Nodes sie dabei kommunizieren. Topics dienen der unidirektionalen Kommunikation, werden Antworten <br>
benötigt findet das Prinzip der Services anwendung.

### ROS Messages

ROS Messages beschreiben eine simple Datenstruktur zum Nachrichtenaustausch über Topics und Services.<br>
Sie enthalten zum Beispiel primitive Datentypen, können aber auch mit anderen Messages ineinander verschachtelt <br>
werden und mit einem Header mit Metadaten wie Zeitstempel versehen werden. <br>
Für Unidirektionale Kommunikation via Topics lautet die Dateiendung .msg. Die Erweiterung dazu für Services <br>
die ausserdem eine Response beinhalten haben die Endung .srv

### ROS Master

Der ROS Master stellt Namens und Registrierungsservices für die restlichen Nodes zur verfügung und verwaltet
publisher und subscriber von Topics und Services. Das Ziel ist es den anderen Nodes zu ermöglichen sich gegenseitig<br> 
zu finden


### Implementierung 
Der Talker Node stellt die Kamera dar welche die Bilder oder den Videostream an den <br>
Processor(in diesem Fall listener genannt) zur weiteren Verarbeitung sendet. Dies wird realisiert durch das <br>
Publisher-Subscriber Prinzip. Die Kamera/talker initialisiert je einen Publisher für jedes Topic, wandelt die Bilder <br>
in Messages vom Typ Image des Pakets sensor_msgs um und published die Message anschließend an das Topic "image". <br>
Für den Integer wurde eine Custom-Message namens IntWithHeader erstellt, diese enthält einen Header und int32, im <br>
talker/Kamera wird nun ein IntWithHeader Objekt erzeugt und das int32 Feld mit einem beliebigen Integer initialisiert und <br>
an das Topic "integer" gepublished.

Der Listener/Prozessor Node enthält die Funktion listener() in welcher ein Subscriber auf das Topic "image" <br>
initialisiert wird und eine Message vom Typ Image erwartet. Die erhaltene Image Message wird nun in der Callback Methode zunächst, <br>
wieder in ein Bild transformiert, anschließend in Graustufen umgewandelt und wieder in eine Image Message transformiert. <br>
Im nächsten Schritt wird ein neuer Publisher an das Topic "processedImage" initialisiert und die Message wird publiziert.<br>


Nach dem ersten Teil der Aufgabe sieht der Graph der Anwendung folgendermaßen aus

![Graph-Task-1](src/images/afterTask1.png "Graph after Task 1")



# Task 2

In Aufgabe 2 wurde ein Controller Node hinzugefügt der die aus Aufgabe 1 erstellten Topics "integer" und "processedImage"<br>
subscribed und diese synchronisiert in einem Python dict() abspeichert um die Paare richtig zuordnen zu können. <br>
Die listener() Funktion des Skripts übernimmt den Part des subscribens und synchronisierens der eingehenden Messages.<br>
Die Image Message wird nun wieder in ein Bild umgewandelt und der Integer aus der IntWithHeader Message wird ebenfalls <br>
in einer variable gespeichert um beide anschließend im Dict() ablegen zu können.

Im nächsten Schritt wurde der AI_service hinzugefügt, dieser soll später dazu genutzt werden die vorbereiteten Bilder vom <br>
Controller zu erhalten und mithilfe eines zuvor trainierten Models die jeweiigen Ziffern erkennen und sein Ergebnis an <br>
den Controller zurückzusenden.

Der Service ist nach einem Server-Client Prinzip umgesetzt wonach der AI_service selbst als Server dient und der Controller <br>
als Client. Beim Start des Servers wird ein Service mit dem Namen "number_prediction_service" initialisiert, und der <br>
zu verwendene Message Typ AI.srv und die auszuführende Methode "predictNumberFromImage" angegeben. 

Die AI.srv Message enthält für die Request an den Service wieder eine Image Message und als Antwort an den Client ein int32 <br>
mit dem Ergebnis der vorhersage. 

Die Methode predictNumberFromImage() die bei Anfragen an den Service ausgeführt wird nimmt die AI.srv Message entgegen, wandelt <br>
die Image Message wieder in ein Bild um und gibt zum aktuellen Zeitpunkt lediglich eine festgelegte Zahl als Integer zurück <br>
an den Client.
 
Im Client, also dem Controller wurde die prediction_service_client() Methode hinzugefügt, welche eine Image Message <br>
entgegennimmt. Die Methode initialisiert unter Angabe des Namen des zu startenden Service und des zu verwendenden Message Typ <br>
einen Service Proxy und ruft diesen unter Angabe der zu untersuchenden Image Message auf und gibt die Antwort des Service <br>
zurück. Die Funktion wird am Ender der Callback Methode des Controller aufgerufen.


Nach dem zweiten Teil der Aufgabe sieht der Graph folgendermaßen aus, die Verbindungen "processedImage" und "int" <br>
zwischen dem Controller und AI_service könne aufgrund eines Bugs leider nicht angezeigt werden
![Graph-Task-2](src/images/afterTask2.png "Graph after Task 2")


# Task 3

## ROS Anpassungen

Für Aufgabe 3 wurden in der ROS Anwendung nur noch kleinere Änderungen vorgenommen. 

Der Talker wählt nun zufällig ein zu sendendes Bild aus dem MNSIT Datensatz.
Desweiteren wurden sowohl das Skript zu erzeugung des Models als auch die bereits trainierten Models hinzugefügt, um dieses <br>
im AI_Service laden zu können.
Im Controller werden nun die Vorhersage des AI_service und der Wahre Wert des Talker/Kamera miteinander verglichen.
## Model Trainieren

Klassifizierung mithilfe eines Convolutional Neural Network (CNN)
Grundidee dass zwischen den Zuständen von nah aneinanderliegenden Pixeln eine Verbindung besteht

### MNIST Datensatz vorbereiten

    Bild 28*28 pixel
  ### transform to tensor
  tensor <br>
    Ein tensor vom rang n in m dimensionen ist ein mathematisches objekt mit n indizes and m^n komponenten und
    unterliegt bestimmten transformationsregeln <br>
    siehe block <br>
  #### normalize
    https://discuss.pytorch.org/t/understanding-transform-normalize/21730/4
    https://www.youtube.com/watch?v=lu7TCu7HeYc
    abbilden der informationen auf einer neuen skala von 0-1 zur relativierung und besseren einordnung innerhalb eines sets
    verschiedene features können dadurch auf der gleichen skala eingeordnet werden
    
    z = (x - mean) / standard deviation

    mean = 1/n (Summe i=1 bis n: xi) Formel einfügen

    standard deviation  formel einfügen

    schwarz weiß werte werden normalisiert

    Farbwerte des schwarzweißbildes abgebildet auf 0-1 floatzahlen, quasi helligkeit

## Model

Das Model ist aufgebaut in folgenden Layern

    super(Model1, self).__init__()
        self.conv1 = Conv2d(1, 10, 5)       1 input, 10 output, 5 kernel
        self.conv2 = Conv2d(10, 20, 5)      10 input (=output layer davor), 20 output, kernel5 
        self.fc1 = Linear(320, 80)          320 input (= 4 x 4 x 20), 80 output, zufällig gewählt
        self.fc2 = Linear(80, 10)           80 input (=output layer davor), output 10 (Ziffern 0-9)

### Convolutional Layer

Ein Convolutional Layer dient dazu die Komplexität eines Bildes zu verringern und macht sich dazu die Tatsache zu nutzen <br>
dass nur zwischen nah beieinander liegenden Pixeln eine Relation besteht, und erhält dadurch die Beziehungen von <br>
unterschiedlichen Bildbereichen zueinander. <br>
Eine Convolution verkleinert das Bild sozusagen mit einem Pixelfilter. <br>
Wird zum Beispiel ein 5x5 Bild mit einem 3x3 Filter auch Faltungsmatrix genannt, bei einem Stride(Verschiebung des Filters bei jedem Schritt) von <br>
1x1 verkleinert erhält man wiederum ein 3x3 Bild. Dabei wird die Filter Matrix an das obere Rechte Eck des Bildes angelegt <br>
und die Produkte aller übereinanderliegenden Zellen addiert, die summe wird nun in das erste Feld der Ergebnismatrix eingetragen.
Anschließend wird der Filter um eine Zelle nach rechts verschoben und wieder alle Produkte der übereinanderliegenden Zellen <br>
addiert, das Ergebnis in der Ergebnismatrix ebenfalls um eine Zelle verschoben eingetragen und anschließend der Filter verschoben. <br>
Wird dies nun ein weiters mal angewendet befindet man sich mit dem Filter nun am rechten Ende der Ausgangsmatrix, und die <br>
Ergebnismatrix hat 3 Zellen in der erste Zeile, nun wird der Filter bei der Verschiebung in der Zeiten Zeile und ersten Spalte <br>
der Ausgangsmatrix angesetzt, und das Ergebnis in der Zielmatrix ebenfalls in der zweiten Zeile und ersten Spalte eingetragen. <br>
wird dieses Verfahren nun so weiterverfolgt erhält man zum Schluss die 3x3 Ergebnismatrix, in der die Verhältnisse der einzelnen <br>
Berreiche weiterhin bestand haben. 

In einem Convolutional Layer werden nun die Zellen der Ausgangsmatrix als Neuronen bezeichnet und die Zellen der Faltungsmatrix <br>
werden nach dem gleichen Verschiebungsschema als Gewichte für die nächsten Layer eingetragen, wobei bedingt durch den Prozess <br>
oft die gleichen Gewichte eingetragen werden.

   
### Fully Connected Layer

1. Layer
320 input (= 4 x 4 x 20), 80 output, zufällig gewählt
   
2. Layer
80 input (=output layer davor), output 10 (Ziffern 0-9)



### forward function

    def forward(self, x):
        x = self.conv1(x)
        x = F.max_pool2d(x, 2)              # 2x2 pooling, max Werte
        x = self.conv2(x)
        x = F.max_pool2d(x, 2)

        x = x.view(-1, 320)                 #ignoriert 1. Dimension und legt 320 pixel nebeneinander
        x = F.sigmoid(self.fc1(x))
        x = F.sigmoid(self.fc2(x))
        return F.log_softmax(x, dim=1)      # höchster output 1, rest 0 (klassifizierung)

### Pooling Layer 
Nach jedem Convolutional Layer wird zur weiteren reduzierung der Komplexität durch Verkleinerung der Größe und <br>
Reduzierung der Parameter ein Poolinglayer eingesetzt.  <br>
Beim Pooling werden Bereiche nach vorgegebener Poolingsize zusammengefasst und entweder das Maximum, der Durchschnitt, <br>
oder die Summe der Gewichte weiterverwendet. In diesem Fall beträgt die Poolingsize 2x2 und es weren die Maximal-Werte <br>
der Gewichte weiterverwendet.

### activation function
        
        definiert output eines neurons basierend auf einem set von inputs
        weighted sums jeder verbindung zum gleichen neuron in der darauffolgenden schicht werden an die activation function weitergegeben
        activation function transformiert die summen in zahlen zwischen unterem und oberen limit der summen

        
   ### relu

    Formel bild einfügen
        wenn input kleiner/gleich null -> 0
        wenn input größer null output=input
   ###sigmoid
            
        formel bild einfügen
            wenn input negativ, je kleiner die summe -> transformierung nahe 0
            wenn input positiv, je größer die summe -> transformierung nahe 1
            wenn input nahe 0 -> transformierung zwischen 0 und 1
    softmax

  
## vergleich unterschiedlicher Models

### Model1 mit Sigmoid Activation Function

### Model2 mit ReLu Activation Function


