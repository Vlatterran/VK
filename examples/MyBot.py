import asyncio
import logging
import time
import pathlib
import yaml
import core.VK as VK
from examples.schedule import Schedule


def main():
    
    try:
        config_file = 'config.yaml'
        with open(config_file, 'r') as file:
            config= yaml.safe_load(file)
            print(config)
        token=config["token"]
        log_path=config["log_path"]
        admin=config["bot_admin"]

    except ImportError:
        import os
        token = os.environ['token']
        admin = int(os.environ['admin'])
    bot = VK.Bot(access_token=token, bot_admin_id=admin, log_file='log.log', loglevel=20)

    @bot.command('пары', use_doc=True)
    def lectures(day: str = 'сегодня'):
        """
        Отправляет расписание на указанный день
        По умолчанию используется текущая дата

        Args:
            day: день, на который будет выдано расписание
        Returns:
            None
        """
        return Schedule.lectures(day)

    @bot.command('week', names=['неделя'])
    def week():
        pass

    @bot.command(access_level=VK.AccessLevel.BOT_ADMIN)
    def cache():
        return bot.session.cache

    @bot.command(access_level=VK.AccessLevel.BOT_ADMIN)
    async def logs(message: VK.Message):
        await bot.session.reply(message, attachments=[await bot.session.upload_document('logs\\log.log', message.chat)])

    @bot.command()
    async def timer(delay: int = 10):
        await asyncio.sleep(delay)
        return 'end'

    bot.start()


if __name__ == '__main__':
    main()