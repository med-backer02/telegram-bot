import asyncio
from importlib import import_module
from aiogram import executor

from app import bot, dp, logger



modules=["pm_menu","filter"]
LOADED_MODULES =[]
for module_name in modules:
        # Load pm_menu at last
        if module_name == "pm_menu":
            continue
        logger.debug(f"Importing <d><n>{module_name}</></>")
        imported_module = import_module("app.handlers." + module_name)
        LOADED_MODULES.append(module_name)
loop = asyncio.get_event_loop()
import_module("handlers.pm_menu")

async def before_srv_task(loop):
    for module in [m for m in LOADED_MODULES if hasattr(m, "__before_serving__")]:
        logger.debug("Before serving: " + module.__name__)
        loop.create_task(module.__before_serving__(loop))



async def start(_):
    logger.debug("Starting before serving task for all modules...")
    loop.create_task(before_srv_task(loop))

logger.info("Starting loop..")
logger.info("Aiogram: Using polling method")

executor.start_polling(dp, loop=loop, on_startup=start)