# cmaker
<img src="https://github.com/drink-uranium/cmaker/blob/main/cmaker.png">
fun project i made, the point of it is to help with the process of compiling source code automatically.
functionality:
this python script compiles: cmake; scons; makefile; can use and compile github repos with links.

all packages needed:
sudo apt install python3-full python3-venv python3-pip build-essential git cmake libboost-all-dev scons

build instructions:
create virtal enviorment as to not mess up your OS
"python3 -m venv venv"

activate the environment
"source venv/bin/activate"

install pyinstall inside the venv
pip install pyinstaller"

run pyinstall
pyinstaller --onefile --windowed cmaker.py

the app with be in .dist/cmaker

and to deactivate the venv
deactivate
