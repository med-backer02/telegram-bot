
from aiogram import types
from aiogram.dispatcher.handler import SkipHandler

from app import BOT_USERNAME, dp
from app import logger
def register(*args, cmds=None, f=None, allow_edited=True, allow_kwargs=False, **kwargs):
    if cmds and type(cmds) is str:
        cmds = [cmds]

    register_kwargs = {}

    if cmds and not f:
        regex = r"\A^{}(".format("/")


        for idx, cmd in enumerate(cmds):
            regex += cmd

            if not idx == len(cmds) - 1:
                regex += "|"

        if "disable_args" in kwargs:
            del kwargs["disable_args"]
            regex += f")($|@{BOT_USERNAME}$)"
        else:
            regex += f")(|@{BOT_USERNAME})(:? |$)"

        register_kwargs["regexp"] = regex

    elif f == "text":
        register_kwargs["content_types"] = types.ContentTypes.TEXT

    elif f == "welcome":
        register_kwargs["content_types"] = types.ContentTypes.NEW_CHAT_MEMBERS

    elif f == "leave":
        register_kwargs["content_types"] = types.ContentTypes.LEFT_CHAT_MEMBER

    elif f == "service":
        register_kwargs["content_types"] = types.ContentTypes.NEW_CHAT_MEMBERS
    elif f == "any":
        register_kwargs["content_types"] = types.ContentTypes.ANY

    logger.debug(f"Registred new handler: <d><n>{str(register_kwargs)}</></>")

    register_kwargs.update(kwargs)

    def decorator(func):
        async def new_func(*def_args, **def_kwargs):
            message = def_args[0]

            if cmds:
                message.conf["cmds"] = cmds

            if allow_kwargs is False:
                def_kwargs = dict()


            await func(*def_args, **def_kwargs)
            raise SkipHandler()

        if f == "cb":
            dp.register_callback_query_handler(new_func, *args, **register_kwargs)
        else:
            dp.register_message_handler(new_func, *args, **register_kwargs)
            if allow_edited is True:
                dp.register_edited_message_handler(new_func, *args, **register_kwargs)

    return decorator