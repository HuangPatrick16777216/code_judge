# Code Judge
Command line code judge

<br>

# How To Use
**Before using, please read the warning in `server.py`**

Required Python modules:
* `colorama`
* `tkinter`

## Setting up the server
1. Take the server file `src/server.py` and place it in an empty directory.
2. Run the server. You will be asked for an IP via stdin. Enter your local IP address.
3. You may optionally put a file named `settings.json` in the same directory as the server with an `ip` key specifying the local IP of the server.
4. The server is set up. It will print messages when events occur, such as a client connecting.
