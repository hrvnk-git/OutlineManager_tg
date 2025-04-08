from aiogram import F, Router
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery

import inline_kb as ikb
from manager import delete_key

router = Router()


@router.callback_query(F.data == "delete_key")
async def process_delete_key(callback_query: CallbackQuery, state: FSMContext):
    await state.set_data({"key_name": callback_query.message.text.split("\n")[0]})
    await callback_query.message.edit_text(
        "Вы уверены что хотите удалить ключ?", reply_markup=ikb.delete_key
    )


@router.callback_query(F.data == "yes")
async def confirm_delete(callback_query: CallbackQuery, state: FSMContext):
    key_name = (await state.get_data())["key_name"]
    result = delete_key(name=key_name)
    if not result:
        await callback_query.answer("Ключ не найден")
        return
    await callback_query.answer()
    await callback_query.message.edit_text(
        f"Ключ *{key_name}* удален", parse_mode="Markdown"
    )
    await state.clear()


@router.callback_query(F.data == "no")
async def cancel_delete(callback_query: CallbackQuery):
    await callback_query.message.answer("Удаление ключа отменено")
    await callback_query.message.delete()
    # await callback_query.message.edit_reply_markup(reply_markup=None)
