
import logging
import os
import sys
from optparse import OptionParser

from kokki.kitchen import Kitchen

def build_parser():
    parser = OptionParser(usage="Usage: %prog [options] <command> ...")
    parser.add_option("-f", "--file", dest="filename", help="Look for the command in FILE", metavar="FILE", default="kitchen.py")
    parser.add_option("-l", "--load", dest="config", help="Load dumped kitchen from FILE", metavar="FILE", default=None)
    parser.add_option("-d", "--dump", dest="dump", help="Dump a serialized representation of what would be run to FILE (default to YAML, can specify <format>:<filename> e.g. pickle:kitchen.dump)", metavar="FILE", default=None)
    parser.add_option("-v", "--verbose", dest="verbose", default=False, action="store_true")
    return parser

def main():
    parser = build_parser()
    options, args = parser.parse_args()
    if not args and not options.config:
        parser.error("must specify at least one command")

    logging.basicConfig(level=logging.INFO)
    if options.verbose:
        logger = logging.getLogger('kokki')
        logger.setLevel(logging.DEBUG)

    if options.config:
        if ':' in options.config:
            format, filename = options.config.split(':', 1)
        else:
            format, filename = "yaml", options.config
        if format == "yaml":
            import yaml
            with open(options.config, "rb") as fp:
                kit = yaml.load(fp.read())
        elif format == "pickle":
            import cPickle as pickle
            with open(filename, "rb") as fp:
                kit = pickle.load(fp)
    else:
        path = os.path.abspath(options.filename)
        if not os.path.isdir(path):
            path = os.path.dirname(path)
        if path not in sys.path:
            sys.path.insert(0, path)

        if os.path.isdir(options.filename):
            files = [os.path.join(path, f) for f in sorted(os.listdir(path)) if f.endswith('.py')]
        else:
            files = [options.filename]

        globs = {}
        for fname in files:
            globs["__file__"] = os.path.abspath(fname)
            with open(fname, "rb") as fp:
                source = fp.read()
            exec compile(source, fname, 'exec') in globs
        del globs['__file__']

        kit = Kitchen()
        roles = []
        for c in args:
            try:
                roles.append(globs[c])
            except KeyError:
                sys.stderr.write("Function for role '%s' not found in config" % c)
                sys.exit(1)
        for r in roles:
            r(kit)

    if options.dump:
        if ':' in options.dump:
            format, filename = options.dump.split(':', 1)
        else:
            format, filename = "yaml", options.dump
        if format == "yaml":
            import yaml
            if filename == "-":
                print yaml.dump(kit)
            else:
                with open(filename, "wb") as fp:
                    yaml.dump(kit, fp)
        elif format == "pickle":
            import cPickle as pickle
            if filename == "-":
                print pickle.dumps(kit)
            else:
                with open(filename, "wb") as fp:
                    pickle.dump(kit, fp, pickle.HIGHEST_PROTOCOL)
        sys.exit(0)

    kit.run()

if __name__ == "__main__":
    main()
