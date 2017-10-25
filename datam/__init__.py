import subprocess

__version__ = ''

try:
    # if we are running in a git repo, look up the hash
    cmd = subprocess.Popen(('git','describe','--always'), stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    cmd_out, cmd_err = cmd.communicate()
    assert cmd_out
    __version__ = cmd_out.strip()
except:
    # otherwise check for a version file
    try:
        from . version import __version__
    except:
        pass
