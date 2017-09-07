#!/usr/bin/env python3

"""
Generate a 4096-bit Django SECRET_KEY and append it as a [secrets]
section to a config.ini. Use `config.ini' if the first argument does not
hold a path to a config.ini, and copy over `config.example.ini' if it
does not exist.
"""

import string
import sys
import os
import os.path
from shutil import copyfile

POPULATION = string.ascii_letters + string.punctuation + string.digits
KEY_LEN = 512
SECRETS_SECTION = """
[secrets]
secret_key = {}
"""

def main(argv):
    """
    Generate a Django SECRET_KEY and append it as a [secrets] section to
    a config.ini.
    """

    # If user supplies first argument, use it as the path to the config.ini to
    # write to, else use 'config.ini' in the current directory
    if len(argv) - 1 >= 1:
        config_ini_path = argv[1]
    else:
        config_ini_path = 'config.ini'
    print("Writing secret key to "
          "ini file `{}'...".format(os.path.abspath(config_ini_path)))

    print('Generating key...')
    random_bytes = os.urandom(KEY_LEN)
    # Work through the random data from /dev/urandom byte by byte, converting it to
    # characters from POPULATION
    key = ''.join(POPULATION[int(x / 256 * len(POPULATION))] for x in random_bytes)
    secrets_section = SECRETS_SECTION.format(key)

    if not os.path.exists(config_ini_path):
        print("`{}' does not exist, so copying over "
              "config.example.ini...".format(config_ini_path))
        copyfile('config.example.ini', config_ini_path)

    print("Appending [secrets] section with key to "
          "`{}'...".format(config_ini_path))
    open(config_ini_path, 'a').write(secrets_section)

    print('SECRET_KEY generation Done!')
    return 0

if __name__ == '__main__':
    sys.exit(main(sys.argv))
