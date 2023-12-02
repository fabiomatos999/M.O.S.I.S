#!/usr/bin/env python3
"""Launches app.py using python3 without calling interpreter explicitly."""
import sshUtils
from cliArgs import args
import webbrowser
from routes import app, website
import dbReconstruct
import os

app.register_blueprint(website)

if __name__ == "__main__":
    dbr = dbReconstruct.DBReconstruct("static/Media")
    if not args.nobackup:
        try:
            sshUtils.scp_recursive_copy(
                "pi@{}:/home/pi/Documents".format(args.ipaddress),
                os.path.join("static", "Media"))
        except Exception:
            raise ValueError("Invalid IP Address or Hostname was inputted.")
    from waitress import serve
    webbrowser.open("http://127.0.0.1:5000", new=2, autoraise=True)
    waitress_config = {
        'host': '0.0.0.0',  # Listen on all available network interfaces
        'port': 5000,  # Specify the port to listen on
        'threads': 8  # Set the number of threads
    }
    # serve(app, **waitress_config)
    app.run(debug=True)
