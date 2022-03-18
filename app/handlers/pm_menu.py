import random
from contextlib import suppress

from aiogram.types.inline_keyboard import InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.utils.callback_data import CallbackData
from aiogram.utils.exceptions import MessageNotModified

from app.utils.decorator import register

from app.utils.test_and_question_loader import get_tests_name, get_questions
from app.utils.question_and_tests import User
from app.config import strings

Users={}
TESTS = get_tests_name()
testmenu_cb = CallbackData("test", "id", "tst")



def test_markup(tests):
    """
    id=i from TESTS : list
    :param tests:
    :return:
    """
    markup = InlineKeyboardMarkup()
    for id, test in enumerate(tests):
        markup.add(
            InlineKeyboardButton(test, callback_data=testmenu_cb.new(id=id+1, tst=test))
        )
    return markup



@register(cmds="start", no_args=True, only_pm=True)
async def start_cmd(message):
    await get_start_func(message)

async def get_start_func(message, edit=False):
    msg = message.message if hasattr(message, "message") else message

    task = msg.edit_text if edit else msg.reply
    buttons = InlineKeyboardMarkup()
    buttons.add(InlineKeyboardButton(strings["btn_help"], callback_data="get_help"))
    buttons.add(
        InlineKeyboardButton(strings["btn_lang"], callback_data="lang_btn"),
        InlineKeyboardButton(
            strings["btn_source"], url="https://www.cluber.com.ua/lifestyle/pritchi-lifestyle/2021/09/kto-mnogo-hochet-tot-malo-poluchit-pritcha-o-zhadnosti/"
        ),
    )
    buttons.add(
        InlineKeyboardButton(
            "➕ Testing ➕",
            callback_data="get_tests",
        )
    )
    # Handle error when user click the button 2 or more times simultaneously
    with suppress(MessageNotModified):
        await task(strings["start_hi"], reply_markup=buttons)

@register(regexp="get_help", f="cb")
async def help_cb(event):
    button = test_markup({})
    button.add(InlineKeyboardButton(strings["back"], callback_data="go_to_start"))
    with suppress(MessageNotModified):
        await event.message.edit_text(strings["help_header"], reply_markup=button)


@register(regexp="lang_btn", f="cb")
async def set_lang_cb(event):
    await event.answer(text="I dont work 🛠")


@register(regexp="go_to_start", f="cb")
async def back_btn(event):
    await get_start_func(event, edit=True)


@register(cmds="help", only_pm=True)
async def help_cmd(message):
    button = test_markup(TESTS)
    button.add(InlineKeyboardButton(strings["back"], callback_data="go_to_start"))
    await message.reply(strings["help_header"], reply_markup=button)

@register(regexp="get_tests", f="cb")
async def testmenu_cb_func(event):
    button = test_markup(TESTS)
    button.add(InlineKeyboardButton(strings["back"], callback_data="go_to_start"))
    with suppress(MessageNotModified):
        await event.message.edit_text(strings["test_header"], reply_markup=button)
        await event.answer()


question_cb = CallbackData("question","next_i", "right_", "option_id")
choices_count_answers_cb = CallbackData("choices_count_answers", "count")

@register(testmenu_cb.filter(), f="cb", allow_kwargs=True)
async def test(event, **kwargs):
    cb = kwargs['callback_data']
    user_id=event.message.from_user.id
    t_id, t_name = cb["id"], cb["tst"]
    questions = get_questions(t_id, offset=0, limit=100)
    Users[user_id] = User(0, len(questions), questions, [], t_name)

    text = [f"<del>Тест</del> «<b>{t_name}</b>»",
           f"🖊 <i>Выберите количество вопросов</i>",
           f""]

    markup = InlineKeyboardMarkup()
    choices_count_answers = {"1️⃣0️⃣":10, "2️⃣0️⃣":20,"3️⃣0️⃣":30, "4️⃣0️⃣":40, "5️⃣0️⃣":50, "6️⃣0️⃣":60}
    for choice_count_answers in choices_count_answers:
        markup.insert(
            InlineKeyboardButton(choice_count_answers,
                                 callback_data=choices_count_answers_cb.new(
                                     choices_count_answers[choice_count_answers]))
        )
    await event.message.edit_text("\n".join(text), reply_markup=markup)
    await event.answer()

@register(choices_count_answers_cb.filter(), f="cb", allow_kwargs=True)
async def to_accept_count_(event, **kwargs):
    cb = kwargs['callback_data']
    user_id = event.message.from_user.id
    choices_count_answers = int(cb["count"])
    questions = Users[user_id].questions[:choices_count_answers]
    Users[user_id].questions = questions
    Users[user_id].count_answers = len(Users[user_id].questions)

    first_question = questions[0]
    text=first_question.text.ljust(95, " ")+"📖"
    next_i = 1
    markup = InlineKeyboardMarkup()
    shuffle_options = first_question.answers
    random.shuffle(shuffle_options)
    for option in list(shuffle_options):
        option_id = first_question.answers.index(option)
        right_ = True if option == first_question.correct else False
        markup.add(
            InlineKeyboardButton(option, callback_data=question_cb.new(next_i, right_, option_id))
        )
    await event.message.edit_text(text, reply_markup=markup)
    await event.answer()


@register(question_cb.filter(), f="cb", allow_kwargs=True)
async def btn_response(event, **kwargs):
    cb = kwargs['callback_data']
    user_id = event.message.from_user.id
    next_i = int(cb["next_i"])
    right_ = cb["right_"]
    option_id = int(cb["option_id"])

    option_choiced = Users[user_id].questions[next_i-1].answers[option_id]
    Users[user_id].user_choice.append(option_choiced)

    if right_ == "True":
        User = Users[user_id]
        User.number_of_correct_answers += 1

    if next_i == int(Users[user_id].count_answers):
        Users[user_id].calculate()
        markup = InlineKeyboardMarkup()
        markup.add(
            InlineKeyboardButton("« " + strings["tests"], callback_data="get_tests")
        )

        percent = round(100/Users[user_id].count_answers*Users[user_id].number_of_correct_answers, 2)
        text = [f"🏁 Тест «{Users[user_id].test_name}» закончен!",
               f"",
               f"Вы ответили на {Users[user_id].count_answers} вопрос",
                f"",
                f"✅ Верно – {Users[user_id].number_of_correct_answers}",
                f"❌ Неверно – {Users[user_id].number_of_wrong_answers}",
                f"",
                f"🥇Percent {percent}%. ",
                f"",
                f" 🎅 VɎ ₥ØⱫⱧɆ₮Ɇ Ⱬ₳₦ØVØ ₱ⱤØɎ₮ł Ɇ₮Ø₮ ₮Ɇ₴₮. 🎅 "]
        await event.message.edit_text("\n".join(text), reply_markup=markup)
        await event.answer()
        del Users[user_id]

    else:
        question = Users[user_id].questions[next_i]
        text = question.text.ljust(95, " ")+"📖"
        markup = InlineKeyboardMarkup()
        shuffle_options = question.answers
        random.shuffle(shuffle_options)
        for option in list(shuffle_options):
            option_id = question.answers.index(option)
            right_ = True if option == question.correct else False
            markup.add(
                InlineKeyboardButton(option, callback_data=question_cb.new(next_i+1, right_, option_id))
            )
        await event.message.edit_text(text, reply_markup=markup)
        await event.answer()


