from solana.rpc.api import Client
from aiogram import Bot, Dispatcher, types, executor
import datetime

# Настройки
import os
TOKEN = os.getenv("BOT_TOKEN")  # Токен бота через переменную окружения
bot = Bot(token=TOKEN)
dp = Dispatcher(bot)

# Подключение к Solana RPC
solana_client = Client("https://api.mainnet-beta.solana.com")

# Получение транзакций
def get_wallet_data(wallet_address):
    try:
        # Баланс кошелька
        balance = solana_client.get_balance(wallet_address)["result"]["value"] / 1e9

        # Заглушки данных
        profit_30d = 9.74
        roi = 128.15
        winrate = 83

        # Формирование отчета
        report = f"""
💼 Wallet: `{wallet_address}`
Balance: {balance:.2f} SOL | Asset's: 0$

Last 30d:
🟡🟢🟡🟢🟢🟢🟡\n🟡🟡🟡🟡🟡🟡🟡

🏆 Profit 30d: {profit_30d} SOL
🥇 ROI: {roi}%
🎯 Winrate: {winrate}%
"""
        return report
    except Exception as e:
        return f"Ошибка получения данных: {e}"

# Обработчик команды /start
@dp.message_handler(commands=["start"])
async def start_command(message: types.Message):
    await message.reply("Привет! Отправь мне адрес Solana-кошелька, чтобы я проверил его данные.")

# Обработчик сообщений с адресом кошелька
@dp.message_handler()
async def handle_wallet(message: types.Message):
    wallet_address = message.text.strip()
    if len(wallet_address) == 44:  # Простой способ проверки длины адреса
        report = get_wallet_data(wallet_address)
        await message.reply(report, parse_mode="Markdown")
    else:
        await message.reply("Пожалуйста, отправь корректный адрес Solana-кошелька.")

# Запуск бота
if __name__ == "__main__":
    executor.start_polling(dp, skip_updates=True)
