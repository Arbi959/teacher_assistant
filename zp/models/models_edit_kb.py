import copy
from aiogram import types
from ..keyboards import mark_salary_mk, mk_go, mk_groups_kb, mk_status_absent, mk_status_attend, mk_all_or_group_stat

__all__ = ["edit_msg_clicked_group", "edit_msg_clicked_salary", "edit_msg_clicked_back", "edit_status_student", "edit_msg_marks", "edit_status_mark"]


async def edit_msg_clicked_group(msg: types.Message):
    "Вывод всех групп"
    mk_res = await mk_groups_kb("output")
    if mk_res['inline_keyboard'][0]:
        await msg.edit_text("Выберите группу", reply_markup=mk_res)
    else:
        await msg.edit_text("У вас нет не одной группы", reply_markup=mk_res)


async def edit_msg_clicked_salary(msg: types.Message, salary):
    await msg.edit_text(f"Итоговая зарплата: {salary}р", reply_markup=mk_go)


async def edit_msg_clicked_back(msg: types.Message):
    await msg.edit_text("Выберите  один из вариантов ниже:", reply_markup=mark_salary_mk)


async def edit_msg_marks(msg: types.Message, clb, webapp=False):
    mk_res = await mk_groups_kb(clb, webapp)
    if mk_res['inline_keyboard'][0]:
        await msg.edit_text("Выберите группу", reply_markup=mk_res)
    else:
        await msg.edit_text("У вас нет не одной группы", reply_markup=mk_res)


counting = 0
async def edit_status_student(msg_edit: types.Message, txt_clb, txt_msg, count_student):
    global counting
    data_sudents = copy.deepcopy(msg_edit)  # копируем, чтобы менять данные где есть все данные о студентах, чтобы потом всё сохранить с актуальными данными
    # меняет статус на противополжный тому что есть
    if txt_msg == 'присутствует ✅':
        await msg_edit[txt_clb].edit_text(msg_edit[txt_clb].text.replace("присутствует ✅", "отсутствует ❌"), reply_markup=mk_status_attend(txt_clb))
        counting += 1
        data_sudents[txt_clb]['text'] = 0

    else:
        await msg_edit[txt_clb].edit_text(msg_edit[txt_clb].text.replace("отсутствует ❌", "присутствует ✅"), reply_markup=mk_status_absent(txt_clb))
        counting -= 1
        data_sudents[txt_clb]['text'] = 1
    return count_student - counting, data_sudents


async def edit_status_mark(msg_edit_mark: types.Message, txt_clb):
    global counting
    data_sudents = copy.deepcopy(msg_edit_mark)  # копируем, чтобы менять данные где есть все данные о студентах, чтобы потом всё сохранить с актуальными данными
    # меняет статус на противополжный тому что есть

    if txt_clb.split(" ")[1] == 'plus':
        txt_clb = txt_clb.replace("status_mark plus ", "")
        # await msg_edit_mark[txt_clb.replace("status_mark plus", "").strip().title()].edit_text(msg_edit_mark[txt_clb].text.replace("🟡", "🟢"))
        await msg_edit_mark[txt_clb].edit_text(msg_edit_mark[txt_clb].text.replace("🟡", "🟢"))
        data_sudents[txt_clb]['text'] = 1
    else:
        txt_clb = txt_clb.replace("status_mark minus ", "")
        await msg_edit_mark[txt_clb].edit_text(msg_edit_mark[txt_clb].text.replace("🟡", "🔴"))

        data_sudents[txt_clb]['text'] = 0.5

    return data_sudents


async def edit_all_or_groups(msg: types.Message):
    await msg.edit_text("Какая статистика вас интересует?:", reply_markup=mk_all_or_group_stat)
    msg.clean()