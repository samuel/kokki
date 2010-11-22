VERSION = "0.4.1"

# August 9, 2010 -- ss -- made a long version to use in generated files
# TODO: make a switch to control generation of "long banners" in generated
#       files.  I like to have this info when i go back to a system after a
#       while but don't want to have to hand-code globs of stuff into every
#       template.  The switch will control how much information is automatically
#       inserted at the top of every file.
LONG_VERSION = "Kokki version %s : http://github.com/samuel/kokki" % VERSION

def version():
    return VERSION

def long_version():
    return LONG_VERSION
