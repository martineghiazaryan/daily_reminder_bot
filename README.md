### **📌 Telegram Daily Planner Bot**
A **personal Telegram bot** that helps you **schedule tasks, send reminders, and track progress**. The bot can also send **voice reminders** using **Google Text-to-Speech (gTTS)**.  

🚀 **Built with:**  
- `python-telegram-bot`  
- `APScheduler`  
- `PostgreSQL`  
- `gTTS` (Google Text-to-Speech)  

---

## **📜 Features**
✅ **Add tasks with reminders** (`/add HH:MM Task Description`)  
✅ **View pending tasks** (`/tasks`)  
✅ **Mark tasks as completed** (`/done <Task ID>`)  
✅ **Edit a task** (`/edit <Task ID> <New Task Description>`)  
✅ **Receive voice reminders at scheduled times**  
✅ **Automatic task storage in PostgreSQL**  

---

## **🛠 Installation & Setup**
### **1️⃣ Clone the Repository**
```bash
git clone https://github.com/yourusername/daily-planner-bot.git
cd daily-planner-bot
```

### **2️⃣ Create a Virtual Environment**
```bash
python -m venv venv
source venv/bin/activate  # For macOS/Linux
venv\Scripts\activate  # For Windows
```

### **3️⃣ Install Dependencies**
```bash
pip install -r requirements.txt
```

### **4️⃣ Set Up Environment Variables**
Create a **`.env`** file in the project directory and add:
```
TG_BOT_TOKEN=your-telegram-bot-token
DATABASE_URL=postgresql://yourusername:yourpassword@localhost:5432/daily_planner
```

### **5️⃣ Initialize PostgreSQL Database**
1. Open PostgreSQL:
   ```bash
   psql -U postgres
   ```
2. Create a new database:
   ```sql
   CREATE DATABASE daily_planner;
   ```
3. Switch to the database:
   ```sql
   \c daily_planner;
   ```
4. Create the tasks table:
   ```sql
   CREATE TABLE tasks (
       id SERIAL PRIMARY KEY,
       user_id BIGINT NOT NULL,
       task TEXT NOT NULL,
       due_time TIME NOT NULL,
       status TEXT DEFAULT 'pending'
   );
   ```

### **6️⃣ Run the Bot**
```bash
python planner.py
```
---

## **🚀 Usage**
### **Start the Bot**
```plaintext
/start
```
👉 **Bot replies with instructions.**

### **Add a Task**
```plaintext
/add 16:30 Study LLM Course
```
👉 **Task is added and scheduled for reminders.**

### **View Tasks**
```plaintext
/tasks
```
👉 **Lists all pending tasks.**

### **Mark a Task as Done**
```plaintext
/done 1
```
👉 **Marks task #1 as completed.**

### **Edit a Task**
```plaintext
/edit 2 Go to the gym
```
👉 **Updates task #2 description.**

---

## **🔔 How Voice Reminders Work**
- The bot **schedules a reminder** at the specified time.
- At the time, it sends:
  - `🔔 Reminder: Task Description`
  - 🎤 **A voice message saying the reminder**  
- Uses `gTTS` (Google Text-to-Speech) to generate speech.

---

## **🐞 Troubleshooting**
❌ **Bot doesn’t respond?**  
✔️ Make sure the bot is running:  
```bash
python planner.py
```

❌ **Voice reminders don’t work?**  
✔️ Run a manual test:
```python
import asyncio
asyncio.run(send_voice_reminder(YOUR_TELEGRAM_ID, "Test Reminder"))
```

❌ **Database connection issues?**  
✔️ Verify PostgreSQL:
```bash
psql -U postgres -d daily_planner
```
✔️ Check environment variables:
```bash
echo $DATABASE_URL  # Linux/macOS
echo %DATABASE_URL%  # Windows
```

---

## **📌 Future Improvements**
🔹 Add support for **recurring tasks**  
🔹 Integrate with **Google Calendar**  
🔹 Add **priority levels** (High, Medium, Low)  

---

## **🤝 Contributing**
1. **Fork the repo**  
2. **Create a new branch** (`feature-xyz`)  
3. **Commit your changes** (`git commit -m "Added feature xyz"`)  
4. **Push to GitHub** (`git push origin feature-xyz`)  
5. **Create a Pull Request** 🎉  

**🚀 Built with ❤️ by [Your Name](https://github.com/martineghiazaryan)**  

---

✅ **Now, add this `README.md` file to your repository!** Let me know if you need any edits. 🚀🔥
