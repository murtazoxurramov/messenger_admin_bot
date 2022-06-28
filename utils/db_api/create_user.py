from utils.db_api.postgresql import Database


class CreateUsers(Database):

    async def __init__(self):
        super().__init__()
        self._full_name = None
        self._username = None
        self._contact = None
        self._lang = None
        self._telegram_id = None


    @property
    async def full_name(self):
        return await self._full_name

    @full_name.setter
    async def full_name(self, full_name):
        if isinstance(full_name, str):
            if len(full_name) <= 255:
                self._full_name = full_name
        else:
            self._full_name = None


    @property
    async def username(self):
        return await self._username

    @username.setter
    async def username(self, username):
        if isinstance(username, str):
            if len(username) <= 255:
                self._username = username
        else:
            self._username = None


    @property
    async def contact(self):
        return await self._contact

    @contact.setter
    async def contact(self, contact):
        if contact is not None:
            if len(contact) <= 12:
                self._contact = contact
        else:
            self._contact = None


    @property
    async def lang(self):
        return await self._lang

    @lang.setter
    async def lang(self, lang):
        if isinstance(lang, str):
            if len(lang) <= 3:
                self._lang = lang
        else:
            self._lang = None


    @property
    async def telegram_id(self):
        return await self._telegram_id

    @telegram_id.setter
    async def telegram_id(self, telegram_id):
        if telegram_id is not None:
            self._telegram_id = telegram_id
        else:
            self._telegram_id = None


    async def create_table_users(self):
        sql = """
        CREATE TABLE IF NOT EXISTS Users (
        id SERIAL PRIMARY KEY,
        full_name VARCHAR(255) NOT NULL,
        username varchar(255) NULL,
        lang varchar(3) NOT NULL,
        telegram_id BIGINT NOT NULL UNIQUE
        );
        """
        return await self.execute(sql, execute=True)


    async def add_user(self):
        sql = "INSERT INTO users (full_name, username, contact, lang, telegram_id) " \
              "VALUES($1, $2, $3, $4, $5) returning *"
        return await self.execute(sql, self.full_name, self.username, self.contact, self.lang, self.telegram_id,
                                  fetchrow=True)


    async def select_all_users(self):
        sql = "SELECT * FROM Users"
        return await self.execute(sql, fetch=True)


    async def select_user(self, **kwargs):
        sql = "SELECT * FROM Users WHERE "
        sql, parameters = self.format_args(sql, parameters=kwargs)
        return await self.execute(sql, *parameters, fetchrow=True)
    

    async def select_lang(self, **kwargs):
        sql = "SELECT * FROM Users WHERE "
        sql, parameters = self.format_args(sql, parameters=kwargs)
        return await self.execute(sql, *parameters, fetchrow=True)


    async def count_users(self):
        sql = "SELECT COUNT(*) FROM Users"
        return await self.execute(sql, fetchval=True)


    async def update_user_username(self):
        sql = "UPDATE Users SET username=$1 WHERE telegram_id=$2"
        return await self.execute(sql, self.username, self.telegram_id, execute=True)


    async def update_user_lang(self):
        sql = "UPDATE Users SET lang=$1 WHERE telegram_id=$2"
        return await self.execute(sql, self.lang, self.telegram_id, execute=True)


    async def delete_users(self):
        return await self.execute("DELETE FROM Users WHERE TRUE", execute=True)


    async def drop_users(self):
        return await self.execute("DROP TABLE Users", execute=True)


    async def __str__(self):
        return await f'{self.full_name}, {self.username}, {self.contact}, {self.lang}, {self.telegram_id}'