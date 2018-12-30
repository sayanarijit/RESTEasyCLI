from __future__ import print_function

import os
from subprocess import Popen

CMDDIR = 'tests/commands'

def main():
    for f in os.listdir(CMDDIR):
        print('*', f, '--------------------------\n')
        path = os.path.join(CMDDIR, f)
        with open(path) as f:
            cmds = [x.strip() for x in f.readlines() if x.strip()]
        for cmd in cmds:
            print('Executing: ', cmd)
            if Popen(cmd, shell=True).wait() != 0:
                raise RuntimeError(cmd)
            print()
        print()

if __name__ == "__main__":
    main()