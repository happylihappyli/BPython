
fixed_tail = r'''def setquit():
    """Define new builtins 'quit' and 'exit'.

    These are objects which make the interpreter exit when called.
    The repr of each object contains a hint at how it works.

    """
    if os.sep == '\\':
        eof = 'Ctrl-Z plus Return'
    else:
        eof = 'Ctrl-D (i.e. EOF)'

    builtins.quit = _sitebuiltins.Quitter('quit', eof)
    builtins.exit = _sitebuiltins.Quitter('exit', eof)


def setcopyright():
    """Set 'copyright' and 'credits' in builtins"""
    builtins.copyright = _sitebuiltins._Printer("copyright", sys.copyright)
    builtins.credits = _sitebuiltins._Printer("credits", """\
Thanks to CWI, CNRI, BeOpen.com, Zope Corporation and a cast of thousands
for supporting Python development.  See www.python.org for more information.""")
    files, dirs = [], []
    # Not all modules are required to have a __file__ attribute.  See
    # PEP 420 for more details.
    here = getattr(sys, '_stdlib_dir', None)
    if not here and hasattr(os, '__file__'):
        here = os.path.dirname(os.__file__)
    if here:
        files.extend(["LICENSE.txt", "LICENSE"])
        dirs.extend([os.path.join(here, os.pardir), here, os.curdir])
    builtins.license = _sitebuiltins._Printer(
        "license",
        "See https://www.python.org/psf/license/",
        files, dirs)


def sethelper():
    builtins.help = _sitebuiltins._Helper()

def enablerlcompleter():
    """Enable default readline configuration on interactive prompts, by
    registering a sys.__interactivehook__.

    If the readline module can be imported, the hook will set the Tab key
    as completion key and register ~/.python_history as history file.
    This can be overridden in the sitecustomize or usercustomize module,
    or in a PYTHONSTARTUP file.
    """
    def register_readline():
        import atexit
        try:
            import readline
            import rlcompleter
        except ImportError:
            return

        # Reading the initialization (config) file may not be enough to set a
        # completion key, so we set one first and then read the file.
        readline_doc = getattr(readline, '__doc__', '')
        if readline_doc is not None and 'libedit' in readline_doc:
            readline.parse_and_bind('bind ^I rl_complete')
        else:
            readline.parse_and_bind('tab: complete')

        try:
            readline.read_init_file()
        except OSError:
            # An OSError here could have many causes, but the most likely one
            # is that there's no .inputrc file (or .editrc file in the case of
            # Mac OS X + libedit) in the expected location.  In that case, we
            # want to ignore the exception.
            pass

        if readline.get_current_history_length() == 0:
            # If no history was loaded, default to .python_history.
            # The guard is necessary to avoid doubling history size at
            # each interpreter exit when readline was already configured
            # through a PYTHONSTARTUP hook, see:
            # http://bugs.python.org/issue5845#msg198636
            history = os.path.join(os.path.expanduser('~'),
                                   '.python_history')
            try:
                readline.read_history_file(history)
            except OSError:
                pass

        def write_history():
            try:
                readline.write_history_file(history)
            except OSError:
                # bpo-19891, bpo-41193: Home directory does not exist
                # or is not writable, or the filesystem is read-only.
                pass

        atexit.register(write_history)

    sys.__interactivehook__ = register_readline

def venv(known_paths):
    global PREFIXES, ENABLE_USER_SITE

    env = os.environ
    if sys.platform == 'darwin' and '__PYVENV_LAUNCHER__' in env:
        executable = sys._base_executable = os.environ['__PYVENV_LAUNCHER__']
    else:
        executable = sys.executable
    exe_dir = os.path.dirname(os.path.abspath(executable))
    site_prefix = os.path.dirname(exe_dir)
    sys._home = None
    conf_basename = 'pyvenv.cfg'
    candidate_conf = next(
        (
            conffile for conffile in (
                os.path.join(exe_dir, conf_basename),
                os.path.join(site_prefix, conf_basename)
            )
            if os.path.isfile(conffile)
        ),
        None
    )

    if candidate_conf:
        virtual_conf = candidate_conf
        system_site = "true"
        # Issue 25185: Use UTF-8, as that's what the venv module uses when
        # writing the file.
        with open(virtual_conf, encoding='utf-8') as f:
            for line in f:
                if '=' in line:
                    key, _, value = line.partition('=')
                    key = key.strip().lower()
                    value = value.strip()
                    if key == 'include-system-site-packages':
                        system_site = value.lower()
                    elif key == 'home':
                        sys._home = value

        sys.prefix = sys.exec_prefix = site_prefix

        # Doing this here ensures venv takes precedence over user-site
        addsitepackages(known_paths, [sys.prefix])

        # addsitepackages will process site_prefix again if its in PREFIXES,
        # but that's ok; known_paths will prevent anything being added twice
        if system_site == "true":
            PREFIXES.insert(0, sys.prefix)
        else:
            PREFIXES = [sys.prefix]
        ENABLE_USER_SITE = False

    return known_paths


def execsitecustomize():
    """Run custom site specific code, if available."""
    try:
        try:
            import sitecustomize
        except ImportError as exc:
            if exc.name == 'sitecustomize':
                pass
            else:
                raise
    except Exception as err:
        if sys.flags.verbose:
            sys.excepthook(*sys.exc_info())
        else:
            sys.stderr.write(
                "Error in sitecustomize; set PYTHONVERBOSE for traceback:\n"
                "%s: %s\n" %
                (err.__class__.__name__, err))


def execusercustomize():
    """Run custom user specific code, if available."""
    try:
        try:
            import usercustomize
        except ImportError as exc:
            if exc.name == 'usercustomize':
                pass
            else:
                raise
    except Exception as err:
        if sys.flags.verbose:
            sys.excepthook(*sys.exc_info())
        else:
            sys.stderr.write(
                "Error in usercustomize; set PYTHONVERBOSE for traceback:\n"
                "%s: %s\n" %
                (err.__class__.__name__, err))


def main():
    """Add standard site-specific directories to the module search path.

    This function is called automatically when this module is imported,
    unless the python interpreter was started with the -S flag.
    """
    global ENABLE_USER_SITE

    orig_path = sys.path[:]
    known_paths = removeduppaths()
    if orig_path != sys.path:
        # removeduppaths() might make sys.path absolute.
        # fix __file__ and __cached__ of already imported modules too.
        abs_paths()

    known_paths = venv(known_paths)
    if ENABLE_USER_SITE is None:
        ENABLE_USER_SITE = check_enableusersite()
    known_paths = addusersitepackages(known_paths)
    known_paths = addsitepackages(known_paths)
    setquit()
    setcopyright()
    sethelper()
    if not sys.flags.isolated:
        enablerlcompleter()
        execsitecustomize()
        if ENABLE_USER_SITE:
            execusercustomize()

# Prevent extending of sys.path when python was started with -S and
# site is imported later.
if not sys.flags.no_site:
    main()

def _script():
    help = """\
%s [--user-base] [--user-site]

Without arguments print some useful information
With arguments print the value of USER_BASE and/or USER_SITE separated
by '%s'.

Exit codes with --user-base or --user-site:
  0 - user site directory is enabled
  1 - user site directory is disabled by user
  2 - user site directory is disabled by super user
      or for security reasons
 >2 - unknown error
"""
    args = sys.argv[1:]
    if not args:
        user_base = getuserbase()
        user_site = getusersitepackages()
        print("sys.path = [")
        for dir in sys.path:
            print("    %r," % (dir,))
        print("]")
        def exists(path):
            if path is not None and os.path.isdir(path):
                return "exists"
            else:
                return "doesn't exist"
        print(f"USER_BASE: {user_base!r} ({exists(user_base)})")
        print(f"USER_SITE: {user_site!r} ({exists(user_site)})")
        print(f"ENABLE_USER_SITE: {ENABLE_USER_SITE!r}")
        sys.exit(0)

    buffer = []
    if '--user-base' in args:
        buffer.append(USER_BASE)
    if '--user-site' in args:
        buffer.append(USER_SITE)

    if buffer:
        print(os.pathsep.join(buffer))
        if len(buffer) == 1 and buffer[0] is None:
            sys.exit(1)
        sys.exit(0)
    else:
        print(help % (sys.argv[0], os.pathsep))
        sys.exit(1)

if __name__ == '__main__':
    _script()
'''

import os

with open("Lib/site.py", "r", encoding="utf-8") as f:
    lines = f.readlines()

# Keep first 400 lines (indices 0-399)
# If the file has fewer lines, this will just take what's there, but we expect more.
# However, we must ensure we don't duplicate or miss lines at the junction.
# Line 401 is where setquit starts.
# So we take lines[:400].

head = lines[:400]

# Ensure the last line of head has a newline
if head and not head[-1].endswith('\n'):
    head[-1] += '\n'

# Ensure there is a blank line before def setquit()
if head and head[-1].strip() != '':
    head.append('\n')

with open("Lib/site.py", "w", encoding="utf-8") as f:
    f.writelines(head)
    f.write(fixed_tail)
