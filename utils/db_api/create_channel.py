from utils.db_api.postgresql import Database


class CreateChannels(Database):

    def __init__(self):
        super().__init__()
        self._channel_id = None
        self._admin_id = None
        self._channel_link = None
        self._admin_link = None
        

    @property
    def channel_id(self):
        return self._channel_id

    @channel_id.setter
    def channel_id(self, channel_id):
        if len(channel_id) <= 20:
            self._channel_id = channel_id
        else:
            self._channel_id = None

    @property
    def channel_link(self):
        return self._channel_link

    @channel_link.setter
    def channel_link(self, channel_link):
        if len(channel_link) <= 20:
            self._channel_link = channel_link
        else:
            self._channel_link = 'Mavjud emas'

    @property
    def admin_id(self):
        return self._admin_id

    @admin_id.setter
    def admin_id(self, admin_id):
        if len(admin_id) <= 20:
            self._admin_id = admin_id
        else:
            self._admin_id = None

    @property
    def admin_link(self):
        return self._admin_link

    @admin_link.setter
    def admin_link(self, admin_link):
        if len(admin_link) <= 20:
            self._admin_link = admin_link
        else:
            self._admin_link = 'Mavjud emas'

    
    async def create_table_channels(self):
        sql = """
        CREATE TABLE IF NOT EXISTS Channels (
            id SERIAL PRIMARY KEY,
            
            channel_id BIGINT NOT NULL UNIQUE,
            channel_link varchar(20) not null,
            
            admin_id BIGINT NOT NULL UNIQUE,
            admin_link varchar(20)
        );
        """
        await self.execute(sql, execute=True)

    async def add_channel(self):
        sql = "INSERT INTO Channels (channel_id, admin_id, channel_link, admin_link) VALUES($1, $2, $3, $4) returning *"
        return await self.execute(
            sql,
            self.channel_id,
            self.admin_id,
            self.channel_link,
            self.admin_link,
            fetchrow=True,
        )

    async def get_channels(self):
        sql = "SELECT DISTINCT admin_id, admin_link FROM Channels"
        return await self.execute(sql, fetch=True)

    async def get_admins(self, admin_id):
        sql = f"SELECT DISTINCT channel_id, channel_link FROM Channels WHERE admin_id='" \
              f"{admin_id}'"
        return await self.execute(sql, fetch=True)

    async def count_channels(self, channel_id, channel_link=None):
        if self.channel_id:
            sql = f"SELECT COUNT(*) FROM Channels WHERE channel_link='{channel_link}' AND channel_id='{channel_id}'"
        else:
            sql = f"SELECT COUNT(*) FROM Channels WHERE channel_id='{channel_id}'"
        return await self.execute(sql, fetchval=True)

    async def get_channels(self, admin_id):
        sql = f"SELECT * FROM Channels WHERE admin_id='{admin_id}'"
        return await self.execute(sql, fetch=True)

    async def update_admin_channel(self):
        sql = "UPDATE Channels SET channel_link=$1 WHERE channel_id=$2"
        return await self.execute(sql, self.channel_link, self.channel_id, execute=True)

    async def get_channel(self, channel_id):
        sql = f"SELECT * FROM Channels WHERE id={channel_id}"
        return await self.execute(sql, fetchrow=True)

    async def delete_channels(self):
        await self.execute("DELETE FROM Channels WHERE TRUE", execute=True)

    async def drop_channels(self):
        await self.execute("DROP TABLE Channels", execute=True)