import asyncio


def fire_and_forget(func):
    def wrapper(*args, **kwargs):
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        return loop.run_in_executor(None, func, *args, *kwargs)
    return wrapper