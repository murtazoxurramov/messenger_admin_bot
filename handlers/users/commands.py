from subprocess import call
import pytz
from aiogram import types
from aiogram.dispatcher import FSMContext
from datetime import datetime
from filters.channel import IsChannel


from loader import dp, bot
from keyboards.inline.addchan import AddChan
from states.state import MessageState
from states.add import AddState


@dp.message_handler(commands=['addChan'])
# @dp.message_handler(IsChannel(), content_types=types.ContentType.NEW_CHAT_MEMBERS)
async def addChan(message: types.Message, state: FSMContext):
    await message.answer('Ushbu pastdagi tugmani bosib kanalingizga obuna qilishingiz mumkin!', reply_markup=AddChan)
    
    user_id = message.from_user.id
    
    async with state.proxy() as data:
        data['user_id'] = user_id
        
    await AddState.chan_id.set()
    
    
@dp.message_handler(IsChannel(), state=AddState.chan_id, content_types=types.ContentType.NEW_CHAT_MEMBERS)
async def new_member(message: types.Message):
    
    for member in message.new_chat_members:
        if member.username == '@devboysbot':
            print(f'{member.id} - - qoshdi!')


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
