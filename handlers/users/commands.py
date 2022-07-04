import pytz
from aiogram import types
from aiogram.dispatcher import FSMContext
from datetime import datetime
import asyncpg
from filters.filters import IsChannel, IsGroup


from loader import dp, bot, db_chan, db_user
from keyboards.inline.addchan import AddChan
from states.state import MessageState
from states.add import AddState


@dp.message_handler(commands=['addChan'])
async def addChan(message: types.Message, state: FSMContext):
    text = 'Iltimos botni kanalingiz yoki gruhingizga admin sifatida obuna qiling va kanalingizdan istalgan birorta habarni forward qilib tashlang, agar gruh bo\'lsa shart emas!'
    await message.answer(text)
    
    user_id = message.from_user.id
    user_name = message.from_user.username
    
    
    async with state.proxy() as data:
        data['user_id'] = user_id
        data['user_name'] = user_name
        
    
    await AddState.chan_id.set()
      

@dp.message_handler(state=AddState.chan_id)
async def get_chan_forward(message: types.Message, state: FSMContext):
    chan_id = message.forward_from_chat.id
    chan_link = message.forward_from_chat.username
    
    async with state.proxy() as data:
        data['chan_id'] = chan_id
        
        try:
            db_chan.channel_id = chan_id
            db_chan.admin_id = data['user_id']
            db_chan.channel_link = chan_link
            db_chan.admin_link = data['user_name']
            await db_chan.add_channel()
            
            await state.finish()
        
        except asyncpg.exceptions.UniqueViolationError:
            await db_user.select_user(telegram_id=message.from_user.id)
            
            
    
            

@dp.message_handler(IsGroup(), content_types=types.ContentType.NEW_CHAT_MEMBERS)
async def new_grmember(message: types.Message, state: FSMContext):
    for member in message.new_chat_members:
        if member.username == 'devboysbot':
            print(f'Gruhga {member.id}, {member.username} -- qoshildi')
            
    await state.finish()


@dp.message_handler(commands=['send_message'])
async def send_message(message: types.Message):
    await message.answer('Habarni yuboring!')
    
    await MessageState.msg.set()
    

@dp.message_handler(state=MessageState.msg)
async def get_msg(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['msg'] = message.text
        data['msg_id'] = message.message_id
    
    text = 'Iltimos yuboriladigan vaqtni kiriting'
    await message.answer(text=text)
    
    await MessageState.time.set()
    
    
@dp.message_handler(state=MessageState.time)
async def get_time(message: types.Message, state: FSMContext):
    # tm = pytz.timezone('Asia/Tashkent')
    # tm = datetime.now(tm)
    # c_time = tm.strftime('%H:%M')
                
    user_id = message.from_user.id
    time = message.text
    
    async with state.proxy() as data:
        data['time'] = time
        data['user_id'] = user_id
        msg_id = data['msg_id']
    
    text = f'Yaxshi habaringiz soat {time}-da yuklanadi'
    await message.answer(text=text)
    
    await message.answer('Kanalingizni tanlang!')
    
    await MessageState.chan_id.set()
    

@dp.message_handler(state=MessageState.chan_id)
async def get_chanID(message: types.Message, state: FSMContext):
    chan_id = message.text
    
    async with state.proxy() as data:
         data['chan_id'] = chan_id
         
    await state.finish()
    
    
    # if time == c_time:
    #     print('-1')
    #     try: 
    #         await bot.copy_message(chat_id=CHANNEL, from_chat_id=user_id, message_id=msg_id)
    #         await message.answer('Habar yuklandi!')
            
    #     except:
    #         await message.answer('Error!')
            
    # elif time != c_time:
    #     print('-2')
    #     await message.answer('Vaqt kelsa jo\'natiladi')
    #     # a = True
    #     while True:
    #         tm = pytz.timezone('Asia/Tashkent')
    #         tm = datetime.now(tm)
    #         c_time = tm.strftime('%H:%M')
    #         print('11111')
    #         print(f'{c_time} ----- {time}')
    #         if c_time == time:
    #             print('22222')
    #             await bot.copy_message(chat_id=CHANNEL, from_chat_id=user_id, message_id=msg_id)
    #             await message.answer('Habar yuklandi!')
    #             break
        
    # else:
    #     await message.answer('Error!')
