import asyncio
import logging
from aiogram import Bot, Dispatcher, Router
from aiogram.types import Message
from flask_sqlalchemy import SQLAlchemy
from flask import Flask

# Flask va ma'lumotlar bazasi sozlamalari
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///shop.db'
app.config['SECRET_KEY'] = 'your_secret_key'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

# Modelni aniqlaymiz (models.py bilan bir xil)
class Product(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    code = db.Column(db.String(5), unique=True, nullable=False)
    name = db.Column(db.String(100), nullable=False)
    price_in = db.Column(db.Float, nullable=False)
    price_out = db.Column(db.Float, nullable=False)

# Telegram botni ulash
TOKEN = "7111059406:AAHXcuDaZYEjsCjFk6-fNeu0QZkKiXeB1bA"
bot = Bot(token=TOKEN)
dp = Dispatcher()
router = Router()  # Router yaratamiz

# Mahsulotni ma'lumotlar bazasidan qidirish funksiyasi
def get_product_info(code):
    with app.app_context():
        product = Product.query.filter_by(code=code).first()
        if product:
            return f"📦 *{product.name}*\n💰 Sotish narxi: {product.price_out} sum\n📥 Kelgan narxi: {product.price_in} sum"
        else:
            return "❌ Mahsulot topilmadi"

# Xabarlarni qayta ishlovchi funksiya
@router.message()
async def send_product_info(message: Message):
    code = message.text.strip()
    if len(code) == 5 and code.isdigit():
        response = get_product_info(code)
    else:
        response = "⚠️ Iltimos, to'g'ri 5 xonali mahsulot kodini kiriting."
    
    await message.reply(response, parse_mode="Markdown")

# Botni ishga tushirish
async def main():
    logging.basicConfig(level=logging.INFO)
    dp.include_router(router)  # Routerni Dispatcher-ga qo'shamiz
    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())



from flask import request

@app.route('/')
def home():
    return "Bot is running!"

if __name__ == "__main__":
    import os
    port = int(os.environ.get("PORT", 5000))  # Railway выдаст PORT
    app.run(host="0.0.0.0", port=port)
