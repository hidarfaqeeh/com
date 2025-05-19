async def log_event(bot, channel_id, text):
    await bot.send_message(channel_id, text)