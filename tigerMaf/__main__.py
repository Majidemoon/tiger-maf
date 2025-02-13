import glob
from pathlib import Path
from tigerMaf.utils import load_plugins
import logging
from . import app
from tigerMaf.scheduler import start_scheduler
from telethon.tl.functions.bots import SetBotCommandsRequest, ResetBotCommandsRequest
from telethon.tl.types import BotCommand, BotCommandScopeDefault

logging.basicConfig(format='[%(levelname) 5s/%(asctime)s] %(name)s: %(message)s',
                    level=logging.WARNING)

path = "tigerMaf/plugins/*.py"
files = glob.glob(path)
for name in sorted(files):
    with open(name) as a:
        patt = Path(a.name)
        plugin_name = patt.stem
        load_plugins(plugin_name.replace(".py", ""))

print("Successfully deployed!")
print("Enjoy!")

if __name__ == "__main__":
    scheduler = start_scheduler()

    try:
        app.run_until_disconnected()
    except (KeyboardInterrupt, SystemExit):
        scheduler.shutdown()