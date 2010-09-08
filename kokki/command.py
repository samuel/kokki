
import logging
import os
import sys
from optparse import OptionParser

from kokki.environment import Environment

def build_parser():
    parser = OptionParser(usage="Usage: %prog [options] <command> ...")
    parser.add_option("-f", "--file", dest="filename", help="Look for the command in FILE", metavar="FILE", default="kitchen.py")
    return parser

def main():
    logging.basicConfig(level=logging.INFO)

    parser = build_parser()
    options, args = parser.parse_args()
    if not args:
        parser.error("must specify at least one command")

    path = os.path.dirname(os.path.abspath(options.filename))
    if path not in sys.path:
        sys.path.insert(0, path)

    with open(options.filename, "rb") as fp:
        kitchen = fp.read()

    globs = {}
    exec compile(kitchen, options.filename, 'exec') in globs

    env = Environment()
    for c in args:
        globs[c](env)
    env.run()

if __name__ == "__main__":
    main()
