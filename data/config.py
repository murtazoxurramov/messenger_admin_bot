from environs import Env

# environs kutubxonasidan foydalanish
env = Env()
env.read_env()

# .env fayl ichidan quyidagilarni o'qiymiz
BOT_TOKEN = env.str("BOT_TOKEN")  # Bot toekn
CREATOR = env.int("CREATOR")  # adminlar ro'yxati
IP = env.str("ip")  # Xosting ip manzili
