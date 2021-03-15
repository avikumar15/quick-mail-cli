import os
from importlib import import_module
from pkgutil import iter_modules

quick_mail_dir = os.path.expanduser('~/.quickmail')
quick_mail_creds_file = os.path.expanduser('~/.quickmail/credentials.json')
quick_mail_token_file = os.path.expanduser('~/.quickmail/token.pickle')
quick_mail_template_dir = os.path.expanduser('~/.quickmail/templates/')
command_dir_path = 'quickmail.commands'

# Emojis
heavy_tick = '\u2705'
heavy_exclamation = '\u2757'
wink_face = '\U0001F609'
grinning_face = '\U0001F601'
thinking_cloud = '\U0001F4AC'
party_popper_tada = '\U0001F389'
sasta_tada = '\U0001F38A'
military_medal = '\U0001F396'
trophy = '\U0001F3C6'
first_medal = '\U0001F947'
smiling_face = '\U0001F642'


def walk_modules(path):
    """Loads a module and all its submodules from the given module path and
    returns them. If *any* module throws an exception while importing, that
    exception is thrown back.
    """

    mods = []
    mod = import_module(path)
    mods.append(mod)
    if hasattr(mod, '__path__'):
        for _, sub_path, is_package in iter_modules(mod.__path__):
            full_path = path + '.' + sub_path
            if is_package:
                mods += walk_modules(full_path)
            else:
                sub_module = import_module(full_path)
                mods.append(sub_module)
    return mods
