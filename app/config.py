import os
token = os.getenv('BOT_TOKEN')
owner_id = os.getenv('OWNER_ID')

dbname =os.getenv('DB_NAME')
user=os.getenv('USER_DB')
password=os.getenv('PASSWORD_OF_DB')
#host=os.getenv('DATABASE_URL')
host = os.getenv('HOST_OF_DB')
DB_URI = os.getenv('DB_URI')
strings={
    "start_hi":"👋 Привет! Меня зовут Kakashi. Я помогу вам с тестами!\n",
    "btn_help":"❔ Помощь",
    "btn_lang":"🇷🇺 Язык",
    "btn_source":"📜 Source code",
    "btn_channel":"🙋‍♀️ Новости Kakashi",
    "btn_group": "👥 Support Group",
    "back": "« Bᴀᴄᴋ",
    "tests":"ᴛᴇsᴛs",
    "help_header":"👋 Привет! Меня зовут <b>Kakashi</b>. Я бот для тестирования, здесь, чтобы помочь "
                  "вам с тестами!\n",
    "test_header":"📒 <i>Выберите тест</i>"
}
