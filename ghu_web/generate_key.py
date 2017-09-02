#!/usr/bin/env python3

"""
Generate a 4096-bit Django SECRET_KEY and append it as a [secrets]
section to a config.ini. Use `config.ini' if the first argument does not
hold a path to a config.ini, and copy over `config.example.ini' if it
does not exist.
"""

import string
import os
from shutil import copyfile

population = string.ascii_letters + string.punctuation + string.digits
key_len = 512

print('Generating key...')
random_bytes = os.urandom(key_len)
# Work through the random data from /dev/urandom byte by byte, converting it to
# characters from population
key = ''.join(population[int(x / 256 * len(population))] for x in random_bytes)
secrets_section = """
[secrets]
secret_key = {}
""".format(key)

if not os.path.exists('config.ini'):
    print('config.ini does not exist, so copying over config.ini.example...')
    copyfile('config.example.ini', 'config.ini')

print('Appending [secrets] section with key to config.ini...')
open('config.ini', 'a').write(secrets_section)

print('Done!')
