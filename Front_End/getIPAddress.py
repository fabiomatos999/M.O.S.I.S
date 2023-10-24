import subprocess

def getIpAddress(port: str) -> str:
    try:
        proc = subprocess.check_output(["./getIPAddress.bash", port], )
        ipAddress = proc.decode()
        ipAddress = ipAddress.strip("\n")
        return ipAddress
    except Exception as e:
        raise e
