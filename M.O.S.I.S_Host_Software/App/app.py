#!/usr/bin/env python3
"""Launches app.py using python3 without calling interpreter explicitly."""
import rsyncCopy
from cliArgs import args
from routes import app, website

app.register_blueprint(website)

if __name__ == "__main__":
    if not args.nobackup:
        try:
            rsyncCopy.rsync_recursive_copy(
                "pi@{}:/home/pi/".format(args.ipaddress),
                "/home/uwu/Downloads/")
        except Exception:
            raise ValueError("Invalid IP Address or Hostname was inputted.")
    # from waitress import serve
    # serve(app, host="0.0.0.0", port=5000)
    app.run(debug=True)
