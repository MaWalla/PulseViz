import subprocess
import re


class PactlException(Exception):
    pass


def list_sources():
    result = []

    try:
        process = subprocess.Popen(['pactl', 'list', 'sources'],
                                   stdout=subprocess.PIPE,
                                   stderr=subprocess.PIPE)
    except FileNotFoundError:
        raise PactlException('pactl could not be found on the system. Is PulseAudio or PipeWire installed?')

    stdout, _ = process.communicate(timeout=10.0)
    if process.returncode != 0:
        raise PactlException('pactl exited with return code {0}'.format(process.returncode))

    for line in stdout.splitlines(keepends=False):
        line = line.decode('utf-8')
        match = re.match('\\tName: (.*)$', line)
        if match is not None:
            result.append(match.group(1))

    return result
