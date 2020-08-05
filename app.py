from aiogram import Bot, Dispatcher, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from data import config

bot = Bot(token=config.BOT_TOKEN, parse_mode=types.ParseMode.HTML)
storage = MemoryStorage()
dp = Dispatcher(bot, storage=storage)

async def on_startup(dp):
    web_hook = await bot.get_webhook_info()
    if web_hook.url != config.WEBHOOK_URL:
        if not web_hook.url:
            await bot.delete_webhook()
        await bot.set_webhook(config.WEBHOOK_URL)
        # await bot.set_webhook(config.WEBHOOK_URL, certificate=open(config.WEBHOOK_SSL_CERT, 'r'))
        import filters
        import middlewares
        filters.setup(dp)
        middlewares.setup(dp)

        from utils.notify_admins import on_startup_notify
        await on_startup_notify(dp)
    print(await bot.get_webhook_info())


async def on_shutdown(dp):
    await bot.delete_webhook()
    await dp.storage.close()
    await dp.storage.wait_closed()


if __name__ == '__main__':
    from aiogram import executor
    from handlers import dp

    executor.start_webhook(
        dispatcher=dp,
        webhook_path=config.WEBHOOK_PATH,
        on_startup=on_startup,
        on_shutdown=on_shutdown,
        skip_updates=True,
        host=config.WEBAPP_HOST,
        port=config.WEBAPP_PORT,
    )
