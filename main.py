from aiogram import Bot, types
from aiogram.dispatcher import dispatcher
from aiogram import executor
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, ReplyKeyboardRemove
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher.filters import Text
from aiogram.dispatcher.filters.state import StatesGroup, State
from aiogram.dispatcher import FSMContext
from sqlite import db_start, create_profile, print_list, edit_profile, delete_line
from openaifunc import send
import re

token = '6616246938:AAFvZ9zM8bXuyvYhcnEFdiMBPA5OBnWucFU'

HELPCOMMAND = """
/help - список команд
/start - начать работу с ботом
/description - описание бота
/list - весь список ваших поздравлений
/add - добавить новую запись о празднике
/delete - удалить запись о празднике
/edit - редактирует уже существующую запись 
/cancel - отменяет 
"""

storage = MemoryStorage()
bot = Bot(token)

dp = dispatcher.Dispatcher(bot = bot,
                           storage = storage)

#состояния
class ProfileStatesGroup(StatesGroup):
       name = State()
       holiday = State()
       date = State()
       add = State()
       user_name = State()

class EditProfileState(StatesGroup):
       number = State()
       new_name = State()
       new_holiday = State()
       new_date = State()

class DeleteProfileState(StatesGroup):
       del_num = State()

#Кнопки для основных команд.
kb = ReplyKeyboardMarkup(resize_keyboard=True,  
                         one_time_keyboard=True)
button_question = ('/question')
kb.add(KeyboardButton('/help')).insert(KeyboardButton('/delete')).insert(button_question).insert(KeyboardButton('/add')).insert(KeyboardButton('/list')).insert(KeyboardButton('/edit'))

#для запуска
async def on_startup(_):
      print('Бот был успешно запущен!')
      await db_start()

#Обработка команды /cancel для прерывания состояний процесса
@dp.message_handler(commands=['cancel'], state='*')
async def cmd_cancel(message: types.message, state: FSMContext):
      if state is None:
            return
      
      await state.finish() 
      await message.reply("Вы прервали нынешний процесс.", reply_markup = kb)

#Обработчик команды /start
@dp.message_handler(commands=['start'])
async def start_command(message: types.message) -> None:
      await message.answer(text="Привет! Приятного пользования моим ботом!",
                           reply_markup = kb)

#Обработчик команды /help
@dp.message_handler(commands=['help'])
async def help_command(message: types.message) ->None:
      await message.reply(text=HELPCOMMAND)

#Обработчик команды /list
@dp.message_handler(commands=['list'])
async def help_command(message: types.message):
      await message.answer(text="Вот список твоих записей:")
      await message.reply(await print_list(message.from_user.id),
                          reply_markup = kb)

#Обработчик команды /add
@dp.message_handler(commands=['add'])
async def add_command(message: types.message) -> None:
      await message.reply(text="Напиши имя человека которого нужно будет поздравить:")
      await ProfileStatesGroup.name.set()

text_pattern = re.compile(r"^[a-zA-Zа-яА-ЯёЁ\s]+$")

#Проверка на то что Имя написано в виде текста
@dp.message_handler(lambda message: not text_pattern.match(message.text), state=ProfileStatesGroup.name)
async def holiday_check(message: types.message):
        await message.reply('Вы неправильно ввели данные! Попробуйте ввести имя еще раз:')

#Обработчик ввода имени.
@dp.message_handler(state = ProfileStatesGroup.name)
async def name_add(message: types.message, state = FSMContext) -> None:
       async with state.proxy() as data:
              data['name'] = message.text

       await message.reply('Теперь отправь название праздника с которым его нужно будет поздравить:')
       await ProfileStatesGroup.holiday.set()

text_pattern1 = re.compile(r"^[a-zA-Zа-яА-ЯёЁ\s]+$")

#Проверка на то что Праздник написан в виде текста
@dp.message_handler(lambda message: not text_pattern1.match(message.text), state=ProfileStatesGroup.holiday)
async def holiday_check(message: types.message):
        await message.reply('Вы неправильно ввели данные! Попробуйте ввести название праздника еще раз:')

#Обработчик ввода праздника
@dp.message_handler(state = ProfileStatesGroup.holiday)
async def holiday_add(message: types.message, state = FSMContext) -> None:
       async with state.proxy() as data:
              data['holiday'] = message.text

       await message.reply('Теперь напиши дату праздника в формате ДД_ММ, Пример: 31-12:')
       await ProfileStatesGroup.date.set()

date_pattern = re.compile(r"^(0[1-9]|[12][0-9]|3[01])-(0[1-9]|1[0-2])$")

#Проверка на то что Дата написана правильно 
@dp.message_handler(lambda message: not date_pattern.match(message.text), state=ProfileStatesGroup.date)
async def holiday_check(message: types.message):
        await message.reply("Это не дата. Пожалуйста, отправьте дату в формате ДД-ММ:")

#Обработчик ввода даты
@dp.message_handler(state = ProfileStatesGroup.date)
async def dateholiday_add(message: types.message, state = FSMContext) -> None:
       async with state.proxy() as data:
              data['date'] = message.text
              data['user_id'] = message.from_user.id

       async with state.proxy() as data:
              text = await send(f"Напиши поздравление для моего друга {data['name']}, у него будет {data['holiday']}")
              await message.reply(text)

       await create_profile(state, user_id=message.from_user.id)
       await message.reply('Все данные внесены успешно.',
                           reply_markup = kb)
       await state.finish()

#Обработчик команды /description
@dp.message_handler(commands=['description'])
async def description_command(message: types.message):
       await message.answer(text="Чат-бот в Telegram предназначен для хранения информации о датах, именах и названиях праздников близких людей и автоматической генерации поздравлений, \
                            которые отправляются в указанный день. Пользователи могут взаимодействовать с ботом, добавлять, \
                            редактировать и удалять поздравления. Бот предоставляет удобный способ хранения и автоматической отправки персонализированных поздравлений, помогая пользователям не забывать о важных событиях и праздниках у своих близких.")


#Обработчик команды /edit
@dp.message_handler(commands=['edit'])
async def edit_command(message: types.message) -> None:
      await message.reply(await print_list(message.from_user.id))
      await message.reply(text="Напиши номер человека из списка, данные которого ты хочешь исправить:")
      await EditProfileState.number.set()
      
#Проверка на то что число написано в виде числа)))
@dp.message_handler(lambda message: not message.text.isdigit(), state=EditProfileState.number)
async def holiday_check(message: types.message):
        await message.reply('Вы неправильно ввели данные, выберите число еще раз:')

@dp.message_handler(state=EditProfileState.number)
async def holiday_add(message: types.message, state = FSMContext) -> None:
       async with state.proxy() as data:
              data['number'] = message.text

       await message.reply(text='Введи новое имя:')
       await EditProfileState.new_name.set()

#Проверка на то что Имя написано в виде текста
@dp.message_handler(lambda message: not text_pattern.match(message.text), state=EditProfileState.new_name)
async def new_name_check(message: types.message):
        await message.reply('Вы неправильно ввели данные! Попробуйте ввести имя еще раз:')

#Обработчик ввода имени.
@dp.message_handler(state = EditProfileState.new_name)
async def new_name_add(message: types.message, state = FSMContext) -> None:
       async with state.proxy() as data:
              data['newname'] = message.text

       await message.reply('Теперь отправь название праздника с которым его нужно будет поздравить:')
       await EditProfileState.new_holiday.set()


#Проверка на то что Праздник написан в виде текста
@dp.message_handler(lambda message: not text_pattern1.match(message.text), state=EditProfileState.new_holiday)
async def holiday_check(message: types.message):
        await message.reply('Вы неправильно ввели данные! Попробуйте ввести название праздника еще раз:')

#Обработчик ввода праздника
@dp.message_handler(state = EditProfileState.new_holiday)
async def holiday_add(message: types.message, state = FSMContext) -> None:
       async with state.proxy() as data:
              data['newholiday'] = message.text

       await message.reply('Теперь напиши дату праздника в формате ДД_ММ, Пример: 31-12:')
       await EditProfileState.new_date.set()

#Проверка на то что Дата написана правильно 
@dp.message_handler(lambda message: not date_pattern.match(message.text), state=EditProfileState.new_date)
async def new_date_check(message: types.message):
        await message.reply("Это не дата. Пожалуйста, отправьте дату в формате ДД-ММ:")

#Обработчик ввода даты
@dp.message_handler(state = EditProfileState.new_date)
async def date_add(message: types.message, state = FSMContext) -> None:
       async with state.proxy() as data:
              data['newdate'] = message.text
              data['user_id'] = message.from_user.id
              await edit_profile(data['user_id'], data['number'], data['newname'], data['newholiday'], data['newdate'])
       await message.reply('Все данные изменены успешно.',
                           reply_markup = kb)
       await state.finish()

#Обработчик команды /delete
@dp.message_handler(commands=['delete'])
async def del_command(message: types.message) -> None:
      await message.reply(await print_list(message.from_user.id))
      await message.reply(text="Напиши номер человека из списка, данные которого ты хочешь удалить:")
      await DeleteProfileState.del_num.set()
      
#Проверка на то что число написано в виде числа)))
@dp.message_handler(lambda message: not message.text.isdigit(), state=DeleteProfileState.del_num)
async def holiday_check(message: types.message):
        await message.reply('Вы неправильно ввели данные, выберите число еще раз:')

@dp.message_handler(state = DeleteProfileState.del_num)
async def delete(message: types.message, state = FSMContext) -> None:
       async with state.proxy() as data:
              data['del_num'] = message.text
              await delete_line(message.from_user.id, data['del_num'])

       await message.reply(text='Запись успешно удалена!)', reply_markup = kb)
       await state.finish()

executor.start_polling(dp, skip_updates=True, on_startup=on_startup)