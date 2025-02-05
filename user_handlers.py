from aiogram import Router, F
from aiogram import types
from aiogram.filters import CommandStart, Command
from aiogram.fsm.context import FSMContext
from aiogram.enums import ChatAction
from Keyboards import main_inlines_kb, tags, recommend, ai_button_kb, first_button_kb, lol_button_kb
from ai_generators import generate
from aiogram.fsm.state import State, StatesGroup
from context import ContexManager

from weather import get_weather


context = ContexManager()
user_router = Router()

class Work(StatesGroup):
    process = State()
    eda = State()
    dasdasd = State()

#Храним состояние генерации в FSM контексте
async def set_processing(state: FSMContext, is_processing: bool):
    await state.update_data(is_processing=is_processing)

async def is_processing(state: FSMContext):
    data = await state.get_data()
    return data.get("is_processing", False)


#База
@user_router.message(F.text == "Начать новый диалог")
async def clear1(message: types.Message):
    context.contex = {}
    await message.answer(text="История очищена")





# Старт
@user_router.message(CommandStart())
async def cmd_start(message: types.Message):
    await message.answer(
        f"Привет, <b>{message.from_user.first_name}</b>!\nТы попал на бота команды <b>BackSpace</b> 🌌, я уверен, вам очень понравится)",
        reply_markup=first_button_kb, parse_mode='HTML')





@user_router.message(F.text=="Меню")
async def cmd_next(message: types.Message):
    await message.answer("Вот, что я умею ",
                         reply_markup=main_inlines_kb)

@user_router.message(F.text=="Вернуться в меню")
async def cmd_next(message: types.Message):
    await message.answer("Вот, что я знаю о Екатеринбурге ",
                         reply_markup=main_inlines_kb)

@user_router.callback_query(F.data == "weather")
async def cmd_weather(callback: types.CallbackQuery):
    weather = await get_weather()
    await callback.answer("weather")
    await callback.message.answer(weather)





@user_router.callback_query(F.data == "tag")
async def cmd_zanatie(callback: types.CallbackQuery):
    await callback.message.answer("Что вас интересует?",
                         reply_markup=tags)


@user_router.callback_query(F.data == "recommend")
async def cmd_zanatie(callback: types.CallbackQuery):
    await callback.message.answer("Что вас интересует?",
                         reply_markup=recommend)


@user_router.callback_query(F.data == "movie")
async def cmd_start_ai(callback: types.CallbackQuery, state: FSMContext):
    await callback.message.answer("Какой фильм ты хочешь посмотреть? ", reply_markup=ai_button_kb)
    await state.set_state(Work.process)
    await set_processing(state, False)  # Устанавливаем, что генерация пока не началась






@user_router.callback_query(F.data == "rest")
async def cmd_start_eda_callback(callback: types.CallbackQuery, state: FSMContext):
    kek = await callback.message.answer("Сейчас расскажу про рестораны и кафе", reply_markup=lol_button_kb)
    timer_message = await callback.message.answer("⏳")
    await state.set_state(Work.eda)
    user_id = callback.from_user.id
    user_text = "Расскажи про рестораны и кафе в Екатеринбурге, напиши адрес"

    # Добавляем сообщение пользователя в контекст
    context.add_message(user_id, {"role": "user", "content": user_text})
    # Получаем историю сообщений
    history = context.get_context(user_id)
    await callback.bot.send_chat_action(chat_id=callback.from_user.id, action=ChatAction.TYPING)
    # Отправляем всю историю сообщений в модель
    res = await generate(history)
    # Добавляем ответ модели в контекст
    model_response = res.choices[0].message.content
    context.add_message(user_id, {"role": "assistant", "content": model_response})

    await callback.bot.delete_message(chat_id=callback.from_user.id, message_id=timer_message.message_id)
    await callback.bot.delete_message(chat_id=callback.from_user.id, message_id=kek.message_id)
    await callback.message.answer(model_response)
    await state.clear()
    await callback.message.answer("<i>Если нужна более подробная информация, воспользуйтесь функцией"
                                  " <b>Вопрос онлайн-гиду 👨‍💻</b></i>",
                                  reply_markup=main_inlines_kb, parse_mode='HTML')




@user_router.callback_query(F.data == "fast_fud")
async def cmd_start_eda_callback(callback: types.CallbackQuery, state: FSMContext):
    kek = await callback.message.answer("Сейчас расскажу про фаст-фуд", reply_markup=lol_button_kb)
    timer_message = await callback.message.answer("⏳")
    await state.set_state(Work.eda)
    user_id = callback.from_user.id
    user_text = "Расскажи про фаст-фуд рестораны в Екатеринбурге, напиши адрес, пиши информацию актуальную на 25 октября 2024 года, не пиши про KFC и McDonalds"

    # Добавляем сообщение пользователя в контекст
    context.add_message(user_id, {"role": "user", "content": user_text})
    # Получаем историю сообщений
    history = context.get_context(user_id)
    await callback.bot.send_chat_action(chat_id=callback.from_user.id, action=ChatAction.TYPING)
    # Отправляем всю историю сообщений в модель
    res = await generate(history)
    # Добавляем ответ модели в контекст
    model_response = res.choices[0].message.content
    context.add_message(user_id, {"role": "assistant", "content": model_response})

    await callback.bot.delete_message(chat_id=callback.from_user.id, message_id=timer_message.message_id)
    await callback.bot.delete_message(chat_id=callback.from_user.id, message_id=kek.message_id)
    await callback.message.answer(model_response)
    await state.clear()
    await callback.message.answer("<i>Если нужна более подробная информация, воспользуйтесь функцией"
                                  " <b>Вопрос онлайн-гиду 👨‍💻</b></i>",
                                  reply_markup=main_inlines_kb, parse_mode='HTML')



@user_router.callback_query(F.data == "razvet")
async def cmd_start_eda_callback(callback: types.CallbackQuery, state: FSMContext):
    kek = await callback.message.answer("Сейчас расскажу, как развлечься", reply_markup=lol_button_kb)
    timer_message = await callback.message.answer("⏳")
    await state.set_state(Work.eda)
    user_id = callback.from_user.id
    user_text = "Расскажи про развлечения в Екатеринбурге, напиши адрес: парки атракционов и развлечений, кино, выставки и события, НО актуальные на данные момент, то есть те которые либо идут сейчас либо скоро начнутся, пиши информацию актуальную на 25 октября 2024 года"

    # Добавляем сообщение пользователя в контекст
    context.add_message(user_id, {"role": "user", "content": user_text})
    # Получаем историю сообщений
    history = context.get_context(user_id)
    await callback.bot.send_chat_action(chat_id=callback.from_user.id, action=ChatAction.TYPING)
    # Отправляем всю историю сообщений в модель
    res = await generate(history)
    # Добавляем ответ модели в контекст
    model_response = res.choices[0].message.content
    context.add_message(user_id, {"role": "assistant", "content": model_response})
    await callback.bot.delete_message(chat_id=callback.from_user.id, message_id=timer_message.message_id)
    await callback.bot.delete_message(chat_id=callback.from_user.id, message_id=kek.message_id)
    await callback.message.answer(model_response)
    await state.clear()
    await callback.message.answer("<i>Если нужна более подробная информация, воспользуйтесь функцией"
                                  " <b>Вопрос онлайн-гиду 👨‍💻</b></i>",
                                  reply_markup=main_inlines_kb, parse_mode='HTML')

















@user_router.message(Work.process)
async def cmd_ai_process(message: types.Message, state: FSMContext):
    if await is_processing(state):
        await message.answer("Ваш предыдущий запрос все еще обрабатывается, пожалуйста подождите.")
        return

    await set_processing(state, True)  # Устанавливаем, что генерация началась

    user_id = message.from_user.id
    user_text = message.text

    # Добавляем сообщение пользователя в контекст
    context.add_message(user_id, {"role": "user", "content": user_text})

    # Получаем историю сообщений
    history = context.get_context(user_id)
    print(context.context)

    # Отправляем всю историю сообщений в модель
    res = await generate(history)

    # Добавляем ответ модели в контекст
    model_response = res.choices[0].message.content
    context.add_message(user_id, {"role": "assistant", "content": model_response})

    await message.bot.send_chat_action(chat_id=message.from_user.id, action=ChatAction.TYPING)
    await message.answer(model_response)

    await set_processing(state, False)  # Генерация завершена



@user_router.message()
async def echo_messages(message: types.Message):
    await message.bot.send_chat_action(chat_id=message.from_user.id, action=ChatAction.TYPING)
    if message.text:
        await message.answer(text="Подождите...\nУ меня нет команды на данное сообщение.\nВот мой весь список команд:\n"                                  "/start - Запуск бота\n")
    else:
        try:
            await message.copy_to(chat_id=message.chat.id)
        except TypeError:
            await message.reply(text="💥🫣 Ничего непонятно...")


