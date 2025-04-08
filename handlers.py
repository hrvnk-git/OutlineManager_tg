from aiogram import F, Router
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from aiogram.types import Message

import inline_kb as ikb
import reply_kb as rkb
from manager import add_key, delete_key, get_keys
from reply_kb import ButtonNames

router = Router()


class ManageKeys(StatesGroup):
    add_key = State()
    delete_key = State()


@router.message(Command("start"))
async def cmd_start(message: Message):
    await message.answer(
        "Я бот для управления сервером Outline VPN", reply_markup=rkb.main
    )


@router.message(F.text == ButtonNames.ALL_KEYS)
@router.message(Command("all_keys"))
async def cmd_load(message: Message):
    keys = get_keys()
    for name, data in keys.items():
        await message.answer(
            text=f"*{name}*\n`{data[0]}`\nИспользовано: {data[1]} GB",
            parse_mode="Markdown",
            reply_markup=ikb.main,
        )


@router.message(F.text == ButtonNames.ADD_KEY)
@router.message(Command("add_key"))
async def add_key_first(message: Message, state: FSMContext):
    await state.set_state(ManageKeys.add_key)
    await message.answer("Введите имя для ключа")


@router.message(ManageKeys.add_key)
async def add_key_second(message: Message, state: FSMContext):
    # await state.update_data(name=message.text)
    # data = await state.get_data()
    new_key = add_key(message.text)
    if not new_key:
        await message.answer("Ключ с таким именем уже существует")
        return
    await message.answer(
        f"Ключ добавлен!\n*{new_key[0]}*\n`{new_key[1]}`", parse_mode="Markdown"
    )
    await state.clear()


@router.message(F.text == ButtonNames.DEL_KEY)
@router.message(Command("delete_key"))
async def delete_key_first(message: Message, state: FSMContext):
    await state.set_state(ManageKeys.delete_key)
    await message.answer("Введите имя ключа для удаления")


@router.message(ManageKeys.delete_key)
async def delete_key_second(message: Message, state: FSMContext):
    # await state.update_data(name=message.text)
    # data = await state.get_data()
    result = delete_key(message.text)
    if not result:
        await message.answer("Ключ не найден")
    await message.answer(f"Ключ *{message.text}* удален", parse_mode="Markdown")
    await state.clear()
