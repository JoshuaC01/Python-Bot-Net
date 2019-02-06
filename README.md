# Python3 GUI Reverse Shell
Welcome to the Python3 GUI Reverse shell, this project was made, developed and documented by me.
If you find any issues or bugs with the project dont be afraid to message me
## Known Bugs
 - File browser does not properly recieve data
 - PyQt5 will sometimes randomly freeze/crash(I suspect this is to do with having all my proccesing on one thread)
 
## Setup
### Client
1. Run(python 3.7 required, do this on any PC, this is to compile the package) `pip install pyinstaller pathlib`
2. Configure settings in `client.py` with your server's ip and port
3. Package client into an exe with `pyinstaller --onefile --windowed client.py`
4. Run `client.exe` on your target machine

### Server
1. Requires Python 3.7, run `pip install pyqt5 pyinstaller`
2. If you want to just run from python skip to step 4
3. Run `pyinstaller --onefile master.py`
4. Run either `master.py` or `master.exe` depending on which one you chose to use

## TODO
- [X] ~~Add Shell~~
- [X] ~~Add File Broswer~~
- [X] ~~Fix Shell~~
- [ ] Fix File Browser
- [ ] Put all windows on a seperate thread to avoid crashing
- [ ] Use the logging feature properly
- [ ] Add timestamps to log
- [ ] Make a reciever manager(so you dont try to recieve from the same thread twice at the same time)
- [ ] Allow client to hold other clients(like a botnet)