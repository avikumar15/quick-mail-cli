from importlib import import_module
from pkgutil import iter_modules

heavy_tick = '\u2705'
heavy_exclamation = '\u2757'

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
