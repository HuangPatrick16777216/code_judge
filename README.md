# Code Judge
Command line code judge

<br>


# How To Use
**Before using, please read the warning in `server.py`**

Required Python modules:
* `colorama`

## Setting up the server
1. Take the server file `src/server.py` and place it in an empty directory.
2. Run the server. You will be asked for an IP via stdin. Enter your local IP address.
3. You may optionally put a file named `settings.json` in the same directory as the server with an `ip` key specifying the local IP of the server.
4. The server is set up. It will print messages when events occur, such as a client connecting.

## Using a client
1. Run `src/client.py`. You may use `settings.json` in the same way as the server, stated above.
2. You will be asked whether you would like to quit or submit a solution.
3. If you chose to submit, you will be asked for a language. `Python 3.8.0`, `Python 2.7.17`, and `C++ (g++ 7.5.0)` are the default ones. Adjust as needed to fit your system (this was developed on Ubuntu). You may also need to adjust the  subprocess commands found in `server.Grader.grader`.
4. Next, select a problem ID. The client will contact the server to get avaliable problems and their IDs.
5. Last, choose a file and you will see the server grade your submission.

<br>


# Making Your Own Problems
They **must** be made with Python, due to the built in pickle module.

* Each problem is a Python dictionary pickled into a binary file. JSON support may be added in the future.
* The structure of each problem goes like this:
```
{
    "name": "My Problem",
    "pid": 1,
    "difficulty": 5,
    "cases": [
        ["in data\n for case one", "out data\n for case one"],
        ["indata for case2", "out data for c2"]
    ]
}
```
* `name` is the name of your problem.
* `pid` is the problem's unique ID. If a PID comes up a second time, it will be skipped.
* `difficulty` is a number to tell the contestants roughly how difficult the problem is. The difficulty value is not used by the server, and you can use any scale you like.
* `cases` is a list of (input, output) strings, communicated via stdin/stdout. Each entry in the list is one case.
