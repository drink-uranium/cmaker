# cmaker
<img src="https://github.com/drink-uranium/cmaker/blob/main/cmaker.png">
<a href="https://github.com/user-attachments/files/21116024/cmaker.tar.gz">Download tar.gz Here</a>
<p>fun project i made, the point of it is to help with the process of compiling source code automatically.</p>
functionality:
<p>this python script compiles: cmake; scons; makefile; can use and compile github repos with links.</p>

all packages needed:
<p>"sudo apt install python3-full python3-venv python3-pip build-essential git cmake libboost-all-dev scons"</p>

build instructions:
create virtal enviorment as to not mess up your OS
<p>"python3 -m venv venv"</p>

activate the environment
<p>"source venv/bin/activate"</p>

install pyinstall inside the venv
<p>"pip install pyinstaller"</p>

run pyinstall
<p>"pyinstaller --onefile --windowed cmaker.py"</p>

the app with be in '.dist/cmaker'

and to deactivate the venv
<p>"deactivate"</p>