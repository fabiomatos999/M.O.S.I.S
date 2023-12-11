"""Wrapper module for getIPAddress shell script."""
import subprocess


def getIpAddress(networkDevice: str) -> str:
    """Return IP address from network device.

    :param networkDevice The device name given by 'ip -a'
    on the Raspberry Pi
    """
    try:
        proc = subprocess.check_output(
            ["./getIPAddress.bash", networkDevice], )
        ipAddress = proc.decode()
        ipAddress = ipAddress.strip("\n")
        return ipAddress
    except Exception as e:
        raise e
