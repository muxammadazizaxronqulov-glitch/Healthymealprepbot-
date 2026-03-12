from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters, ContextTypes

user_data = {}

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Assalomu alaykum! Bo'yingizni kiriting (cm):")
    user_data[update.effective_user.id] = {"step": "height"}

async def message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    uid = update.effective_user.id
    text = update.message.text

    if uid not in user_data:
        await update.message.reply_text("Iltimos /start bilan boshlang.")
        return

    step = user_data[uid]["step"]

    try:
        if step == "height":
            user_data[uid]["height"] = float(text)
            user_data[uid]["step"] = "weight"
            await update.message.reply_text("Vazningizni kiriting (kg):")
        elif step == "weight":
            user_data[uid]["weight"] = float(text)
            user_data[uid]["step"] = "age"
            await update.message.reply_text("Yoshingizni kiriting:")
        elif step == "age":
            user_data[uid]["age"] = int(text)
            user_data[uid]["step"] = "gender"
            await update.message.reply_text("Jinsingizni tanlang (erkak/ayol):")
        elif step == "gender":
            data = user_data[uid]
            height = data["height"]
            weight = data["weight"]
            age = data["age"]
            gender = text.lower()
            if gender not in ["erkak", "ayol"]:
                await update.message.reply_text("Iltimos, 'erkak' yoki 'ayol' deb yozing.")
                return
            calories = 10*weight + 6.25*height - 5*age + (5 if gender=="erkak" else -161)
            bmi = weight / ((height/100)**2)
            if bmi < 18.5:
                bmi_category = "Siz ozg‘insiz"
            elif bmi < 25:
                bmi_category = "Siz normal vazndasiz"
            elif bmi < 30:
                bmi_category = "Siz ortiqcha vazndasiz"
            else:
                bmi_category = "Siz semizsiz"

            meal_plan = (
                "Nonushta: 500 kcal\n"
                "Tushlik: 700 kcal\n"
                "Kechki ovqat: 600 kcal\n"
                "Snack: 200 kcal"
            )

            await update.message.reply_text(
                f"{bmi_category}\n"
                f"Sizning BMI: {bmi:.1f}\n"
                f"Kunlik kaloriya (saqlash): {int(calories)} kcal\n"
                f"Vazn tashlash: {int(calories-500)} kcal\n"
                f"Vazn yig‘ish: {int(calories+400)} kcal\n\n"
                f"Oddiy meal plan:\n{meal_plan}"
            )
            await update.message.reply_text("Qayta hisoblash uchun /start yozing.")
            user_data[uid]["step"] = "done"
    except:
        await update.message.reply_text("Iltimos, faqat raqam kiriting.")

# BotFather tokeningizni shu yerga yozing
TOKEN = "8384557375:AAFad_NHZX6s50G5Nj8qBS2f4_wUson3ATA

# Telefon resurslari uchun polling intervalini 1 soniyaga qo‘ydik
app = ApplicationBuilder().token(TOKEN).build()
app.add_handler(CommandHandler("start", start))
app.add_handler(MessageHandler(filters.TEXT & (~filters.COMMAND), message))

app.run_polling(poll_interval=1.0)
