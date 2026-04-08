import asyncio
import json
import os
from twitchio.ext import commands

# 1. إعداد ملف تخزين البيانات
DATA_FILE = 'attendance_data.json'
current_session_attended = set()


def load_data():
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE, 'r', encoding='utf-8') as f:
            try:
                return json.load(f)
            except:
                return {}
    return {}


def save_data(data):
    with open(DATA_FILE, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=4)


user_attendance = load_data()


# 2. بناء كلاس البوت
class Bot(commands.Bot):
    def __init__(self):
        # في الإصدارات الجديدة، نمرر الـ Loop للـ super
        super().__init__(
            token='oauth:tbd99x87lxi9j3hmv8e2of75svtcrf',
            prefix='!',
            initial_channels=['realpud']
        )

    async def event_ready(self):
        print(f'تم الاتصال بنجاح! البوت شغال الآن باسم: {self.nick}')

    @commands.command(name='تحضير')
    async def attendance(self, ctx):
        user = ctx.author.name
        if user in current_session_attended:
            await ctx.send(f'عذراً {user}، أنت محضر مسبقاً في هذا البث! ✋')
            return

        user_attendance[user] = user_attendance.get(user, 0) + 1
        current_session_attended.add(user)
        save_data(user_attendance)

        count = user_attendance[user]
        await ctx.send(f'أهلاً {user}، تم 🌟 تحضيرك بنجاح! حضورك الإجمالي: {count}')


# 3. الطريقة الصحيحة لتشغيل البوت في بايثون 3.14
async def start_bot():
    bot = Bot()
    print("جاري تشغيل المحرك والاتصال بتويتش...")
    await bot.start()


if __name__ == "__main__":
    try:
        asyncio.run(start_bot())
    except KeyboardInterrupt:
        print("تم إيقاف البوت.")