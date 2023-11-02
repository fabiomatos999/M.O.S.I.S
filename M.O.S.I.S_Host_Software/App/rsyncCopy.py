"""rsync subproccess recursive copy module."""
import subprocess


def rsync_recursive_copy(source: str, destination: str):
    """
    Call rsync and recursively copy files from source to destination.

    Will raise an exception if rsync has invalid source
    or destination arguments or if rsync is not installed
    in system path.
    """
    try:
        subprocess.check_call(["scp", "-r", source, destination],
                              )
    except Exception as err:
        raise err
