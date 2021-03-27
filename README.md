Bei diesem Projekt handelt es sich um die Implementierung der Prüfungsvorleistung Spezielle Anwendungen der Informatik <br>
der HTW Berlin mit folgender [Aufgabenstellung](https://gitlab.com/baumannpa_teaching/ros-ai-task)

Das Ziel ist eine Anwendung zur Handschrifterkennung mittels künstlicher Intelligenz.

-----

- [ROS Grundlagen](#ros-grundlagen)
    - [Nodes](#ros-nodes)
    - [Topics](#ros-topics)
    - [Messages](#ros-messages)
    - [Master](#ros-master)
- [Implementierung](#implementierung)
    - [Task 1](#task-1)
    - [Task 2](#task-2)
    - [Task 3](#task-3)
- [Ausführung](#ausführung)    

# ROS Grundlagen

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

# Implementierung

### Task 1

Nach dem ersten Teil der Aufgabe sieht der Graph der Anwendung folgendermaßen aus

![Graph-Task-1](afterTask1.png "Graph after Task 1")

Der Talker Node stellt die Kamera dar welche die Bilder oder den Videostream an den <br>
Processor(in diesem Fall listener genannt) zur weiteren Verarbeitung sendet. Dies wird realisiert durch das <br>
Publisher-Subscriber Prinzip. Die Kamera/talker published das Bild an das Topic "image" und der Prozessor/listener <br>
subscribed das Topic um die Nachrichten, also die Bilder zu erhalten. Der Prozessor Verarbeited die ankommenden Bilder <br>
und published diese anschließend selbst an das Topic "afterProcessing". <br>
Die Kamera/talker published ausserdem eine Custommessage(IntWithHeader.msg), bei der es sich um ein integer mit <br>
Header(notwendig zur späteren Synchronisierung) handelt, and das Topic "integer"

Zum Bauen der Anwendung muss der Befehl

> catkin_make

ausgeführt werden und anschließend kann die Anwendung mit

>roslaunch beginner_tutorials talker-listener.launch 

ausgeführt werden. Dafür wurde das File talker-listener.launch erstellt in welchem die zu startenden Nodes definiert
wurden.

### Task 2

### Task 3

# Ausführung

## 2. Workspace
To contain different packages, a workspace is needed. It's not just a directory, it also needs to be <br>
sourced. This is accomplished by typing
> source /opt/ros/noetic/setup.bash

Working with ROS, one will soon encounter the word "catkin". Catkin is the official build <br>
system of ROS and helps generating executables, libraries and interfaces. Also, it makes the <br>
distribution of packages easier. To use catkin in our workspace, we need a src-folder in our <br>
designated working directory. That's where our source code goes. Then we type while being in <br>
the directory that contains the src-folder:
> catkin_make

This will create a *CMakeLists.txt* file in the src-folder, which contains the installation rules. <br>
Further, our current directory will now contain a build-folder and a devel-folder. These two should <br>
not be modified by us, as they contain important information for the whole project structure. <br>
But we do need to source the devel-folder:
> source devel/setup.bash

Now that our workspace is set up, we can start building packages. A package can contain <br>
a Node, a dataset or any other kind of a useful module. As mentioned before, packages <br>
belong into the src-folder. If you want to create a package using catkin, you can simply type:
> catkin_create_pkg package_name {dependencies}

## 3. Execution
Of course we don't only want to write code, but also execute it. There are two ways to do that. <br>
The first one is to start everything step by step. To do that, we first need to start the Master:
> roscore

Then we can start our publishing node by typing:
> rosrun package_name file_name_publisher

And finally we can run our subscriber. If we switched the order, there would have been <br>
a problem, because our subscriber wouldn't have anyone to subscribe to.
> rosrun package_name file_name_subscriber

To combine all these commands one can use ROS Launch. within a *.launch* file, one can list in XML all the Nodes that need to be <br>
started and will additionally start the roscore, if it hasn't been started yet.
> roslaunch package_name file.launch

The RQT, an available user-interface, which stands for ROS QT and can easily be adjusted to one's own needs. <br>
To run the GUI, write:
> rosrun rqt_gui rqt_gui

Another important feature RQT offers is the RQT Graph. It displays the Master, Nodes and the <br>
way these are connected.
> rosrun rqt_graph rqt_graph
