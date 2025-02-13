import sys
import logging
from pathlib import Path
import importlib
from telethon import events

def load_plugins(plugin_name):
    path = Path(f"tigerMaf/plugins/{plugin_name}.py")
    name = "tigerMaf.plugins.{}".format(plugin_name)
    spec = importlib.util.spec_from_file_location(name, path)
    load = importlib.util.module_from_spec(spec)
    load.logger = logging.getLogger(plugin_name)
    spec.loader.exec_module(load)
    sys.modules["tigerMaf.plugins." + plugin_name] = load
    print("tigerMaf has Imported " + plugin_name)

async def progress_bar(iteration, total, prefix='', suffix='', decimals=1, length=20, fill='█'):
    percent = ("{0:." + str(decimals) + "f}").format(100 * (iteration / float(total)))
    filled_length = int(length * iteration // total)
    bar = fill * filled_length + '▒' * (length - filled_length)
    msg = f'\r{prefix} |{bar}| {percent}% {suffix}'
    return msg