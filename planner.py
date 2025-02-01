import os
import logging
import asyncio
import psycopg2
from datetime import datetime
from gtts import gTTS
from telegram import Update, Bot
from telegram.ext import CommandHandler, CallbackContext, Application
from apscheduler.schedulers.background import BackgroundScheduler
from dotenv import load_dotenv


# Load environment variables from .env file
load_dotenv()

TOKEN = os.getenv("TG_BOT_TOKEN")
DATABASE_URL = os.getenv("DATABASE_URL")

# PostgreSQL Database Connection
conn = psycopg2.connect(DATABASE_URL)
cursor = conn.cursor()

# Configure Logging
logging.basicConfig(format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO)

# Task Scheduler
scheduler = BackgroundScheduler()
scheduler.start()


async def add_task(update: Update, context: CallbackContext) -> None:
    try:
        user_id = update.message.chat_id
        message = update.message.text.split(" ", 2)

        if len(message) < 3:
            await update.message.reply_text("Usage: /add HH:MM Task Description")
            return

        time_str = message[1]
        task_text = message[2]
        due_time = datetime.strptime(time_str, "%H:%M").time()

        cursor.execute("INSERT INTO tasks (user_id, task, due_time, status) VALUES (%s, %s, %s, 'pending') RETURNING id", 
                       (user_id, task_text, due_time))
        task_id = cursor.fetchone()[0]
        conn.commit()

        await update.message.reply_text(f"✅ Task #{task_id} added: '{task_text}' at {time_str}")

        now = datetime.now().time()
        if due_time > now:
            run_time = datetime.combine(datetime.today(), due_time)
            scheduler.add_job(lambda: asyncio.run(send_voice_reminder(user_id, task_text)), 'date', run_date=run_time)

    except Exception as e:
        await update.message.reply_text(f"❌ Error: {e}")


async def list_tasks(update: Update, context: CallbackContext) -> None:
    user_id = update.message.chat_id

    cursor.execute("SELECT id, task, due_time, status FROM tasks WHERE user_id=%s AND status='pending' ORDER BY due_time ASC", (user_id,))
    tasks = cursor.fetchall()

    if not tasks:
        await update.message.reply_text("📋 No pending tasks for today!")
        return

    task_list = "📌 **Your Tasks for Today:**\n"
    for task in tasks:
        task_list += f"🕒 {task[2]} - {task[1]} (ID: {task[0]})\n"

    await update.message.reply_text(task_list, parse_mode="Markdown")


async def complete_task(update: Update, context: CallbackContext) -> None:
    try:
        task_id = int(context.args[0])
        cursor.execute("UPDATE tasks SET status='done' WHERE id=%s", (task_id,))
        conn.commit()
        await update.message.reply_text(f"✅ Task {task_id} marked as complete!")
    except:
        await update.message.reply_text("❌ Usage: /done <Task ID>")


async def edit_task(update: Update, context: CallbackContext) -> None:
    try:
        user_input = update.message.text.split(" ", 2)
        if len(user_input) < 3:
            await update.message.reply_text("Usage: /edit <Task ID> <New Task Description>")
            return

        task_id = int(user_input[1])
        new_task_text = user_input[2]

        cursor.execute("UPDATE tasks SET task=%s WHERE id=%s", (new_task_text, task_id))
        conn.commit()

        await update.message.reply_text(f"✏️ Task {task_id} updated to: {new_task_text}")
    except Exception as e:
        await update.message.reply_text(f"❌ Error: {e}")


async def send_voice_reminder(user_id, task_text):
    try:
        # Generate voice message
        tts = gTTS(text=f"Here is your reminder: {task_text}", lang="en")
        voice_file = f"reminder_{task_text}.mp3"
        tts.save(voice_file)

        # Send voice message
        bot = Bot(token=TOKEN)
        with open(voice_file, "rb") as voice:
            await bot.send_voice(chat_id=user_id, voice=voice)

        # Delete the voice file after sending
        os.remove(voice_file)
        print(f"🎤 Voice reminder sent to {user_id}: {task_text}")

    except Exception as e:
        print(f"❌ Error in sending voice reminder: {e}")

def run_async(func, *args):
    loop = asyncio.get_event_loop()
    if loop.is_running():
        loop.create_task(func(*args))
    else:
        loop.run_until_complete(func(*args))



async def start(update: Update, context: CallbackContext) -> None:
    await update.message.reply_text("👋 Welcome! Use /add <HH:MM> <Task> to add a task, /tasks to view tasks, and /done <ID> to complete a task.")


def main():
    # Create application instance
    app = Application.builder().token(TOKEN).build()

    # Add command handlers
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("add", add_task))
    app.add_handler(CommandHandler("tasks", list_tasks))
    app.add_handler(CommandHandler("done", complete_task))
    app.add_handler(CommandHandler("edit", edit_task))

    # Start polling
    print("🤖 Bot is running...")
    app.run_polling()


if __name__ == "__main__":
    main()
