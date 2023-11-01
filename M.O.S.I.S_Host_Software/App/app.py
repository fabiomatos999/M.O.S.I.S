#!/usr/bin/env python3
"""Launches app.py using python3 without calling interpreter explicitly."""
import rsyncCopy
from cliArgs import args
import webbrowser
from datetime import datetime
from routes import app, website


app.register_blueprint(website)


def getCurrentTime() -> str:
    """Return current time in 'yyyy-MM-ddTHH:mm:ss.zzz' format."""
    date = datetime.now()
    return date.strftime('%Y-%m-%-dT%H:%M:%S.%f')


if __name__ == "__main__":
    if not args.nobackup:
        try:
            rsyncCopy.rsync_recursive_copy(
                "pi@{}:/home/pi/".format(args.ipaddress), args.output)
        except Exception:
            raise ValueError("Invalid IP Address or Hostname was inputted.")
    from waitress import serve
    webbrowser.open("http://127.0.0.1:5000", new=2, autoraise=True)
    #serve(app, host="0.0.0.0", port=5000)
    app.run(debug=True)
