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

population = string.ascii_letters + string.punctuation + string.digits
key_len = 512

# If user supplies first argument, use it as the path to the config.ini to
# write to, else use 'config.ini' in the current directory
if len(sys.argv) - 1 >= 1:
    config_ini_path = sys.argv[1]
else:
    config_ini_path = 'config.ini'
print("Writing secret key to "
      "ini file `{}'...".format(os.path.abspath(config_ini_path)))

print('Generating key...')
random_bytes = os.urandom(key_len)
# Work through the random data from /dev/urandom byte by byte, converting it to
# characters from population
key = ''.join(population[int(x / 256 * len(population))] for x in random_bytes)
secrets_section = """
[secrets]
secret_key = {}
""".format(key)

if not os.path.exists(config_ini_path):
    print("`{}' does not exist, so copying over "
          "config.example.ini...".format(config_ini_path))
    copyfile('config.example.ini', config_ini_path)

print("Appending [secrets] section with key to "
      "`{}'...".format(config_ini_path))
open('config.ini', 'a').write(secrets_section)

print('Done!')
