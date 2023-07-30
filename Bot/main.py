from telebot import *
import sqlite3
import os
import bt

bot = telebot.TeleBot('BOT-KEY')

# Получаем путь до нашей директории
dirname = os.path.dirname(__file__)
path = dirname + os.sep

# В модуле bt хранятся все большие сообщения бота
# это может показаться неудобным, однако намного неудобнее
# разбираться в огромном коде, где очень много текста с тройными кавычками
# именно поэтому я принял такое решение

# Зато теперь бот выглядит очень аккуратно :3
bt = bt.msg()



# markup самого первого меню, используется часто
default_markup = types.ReplyKeyboardMarkup(resize_keyboard=True)

btn_add = types.KeyboardButton("⚜️ Добавить игру")
btn_remove = types.KeyboardButton("🪓 Удалить игру")
btn_list = types.KeyboardButton("📜 Список игр")
btn_author = types.KeyboardButton("🌱 Об авторе")

default_markup.add(btn_list)
default_markup.add(btn_add, btn_remove)
default_markup.add(btn_author)

# markup с inline-кнопкой 'Обратно'
back_inline_markup = types.InlineKeyboardMarkup(row_width=1)
btn_back = types.InlineKeyboardButton(text="🔺 Обратно в меню", callback_data='1')
back_inline_markup.add(btn_back)

# markup с inline-кнопкой 'Обратно', который возвращает пользователя к списку игр
back_togamelist_inline_markup = types.InlineKeyboardMarkup(row_width=1)
btn_back = types.InlineKeyboardButton(text="🔺 Обратно к списку", callback_data='2')
back_togamelist_inline_markup.add(btn_back)

# Пустой markup
empty_markup = types.ReplyKeyboardRemove()

# markup выбора
choice_markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
btn_ok = types.KeyboardButton("🪀 Всё верно")
btn_change_name = types.KeyboardButton("🎣 Изменить название")
btn_change_mark = types.KeyboardButton("🏹 Изменить оценку")
btn_change_comment = types.KeyboardButton("🎭 Изменить комментарий")

choice_markup.add(btn_ok)
choice_markup.add(btn_change_name, btn_change_mark)
choice_markup.add(btn_change_comment)

# markup списка игр
gamelist_markup = types.ReplyKeyboardMarkup(resize_keyboard=True)

btn_check_com = types.KeyboardButton("📜 Просмотреть отзыв об игре")
btn_back = types.KeyboardButton("🔺 Вернуться в меню")

gamelist_markup.add(btn_check_com, btn_back)

# markup для изменения оценки или комментария к игре (выходит после открытия отзыва об игре)
change_mark_or_comment_markup = types.ReplyKeyboardMarkup(resize_keyboard=True)

btn_change_mark = types.KeyboardButton("🏹 Изменить оценку")
btn_change_comment = types.KeyboardButton("🎭 Изменить комментарий")

change_mark_or_comment_markup.add(btn_change_mark, btn_change_comment)

# Удаление одной игры markup
deletegame_markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
btn_yes = types.KeyboardButton("🪓 Удалить")
deletegame_markup.add(btn_yes)



# Работа с базой данных
def init(id):
    connect = sqlite3.connect(path + 'users.db')
    cursor = connect.cursor()

    # Создаём базу данных, если её еще нету
    cursor.execute("""CREATE TABLE IF NOT EXISTS ids(id INTEGER, db_name TEXT)""")
    connect.commit()

    # Создаём таблицу игр специально для пользователя, если её ещё нету
    table_id = "table_" + str(id)
    cursor.execute(f"CREATE TABLE IF NOT EXISTS {table_id}(game_name TEXT, game_score INTEGER, game_comment TEXT)")
    connect.commit()

    # Связываем id пользователя и id таблицы в изначальной таблицы бд
    # если этого еще не сделано
    cursor.execute(f"SELECT id FROM ids WHERE id={id}")
    data = cursor.fetchone()
    if data is None:
        new_user = [id, table_id]
        cursor.execute("INSERT INTO ids VALUES(?,?)", new_user)
        connect.commit()

# Получение названия таблицы пользователя
def getUserTable(userid):
    connect = sqlite3.connect(path + 'users.db')
    cursor = connect.cursor()

    cursor.execute(f"SELECT db_name FROM ids WHERE id = ?", (userid,))
    return cursor.fetchone()[0]

# Добавление новой игры
def addNewGame(userid, gameInfo):
    connect = sqlite3.connect(path + 'users.db')
    cursor = connect.cursor()

    usertable = getUserTable(userid)
    cursor.execute(f"INSERT INTO {usertable} VALUES(?,?,?)", gameInfo)
    connect.commit()

# Удаление одной игры по номеру из списка
def deleteGame(userid, gameName):
    connect = sqlite3.connect(path + 'users.db')
    cursor = connect.cursor()
    table = getUserTable(userid)

    cursor.execute(f"DELETE FROM {table} WHERE game_name = ?", (gameName, ))
    connect.commit()

# Получаем список игр пользователя в удобной форме
def getGameList(userid):
    connect = sqlite3.connect(path + 'users.db')
    cursor = connect.cursor()
    table = getUserTable(userid)

    cursor.execute(f"SELECT * FROM {table}")
    records = cursor.fetchall()

    # Формируем список, в котором записываются значения
    # НАЗВАНИЕИГРЫ:ОЦЕНКА - одна запись, тип str
    gameList = []
    for row in records:
        newStr = row[0] + ":" + str(row[1])
        gameList.append(newStr)
    
    return gameList

# Получаем всю информацию об игре в формате:
# НАЗВАНИЕИГРЫ:ОЦЕНКА:КОММЕНТАРИЙ
# По её номеру в списке
def getGameInfo(userid, gameid):
    # Получаем название и оценку
    gameList = getGameList(userid)
    gameString = gameList[int(gameid)-1] + ":" + getComment(userid, gameid)
    return gameString.split(":")

# Получаем список комментариев по порядку
def getAllComments(userid):
    connect = sqlite3.connect(path + 'users.db')
    cursor = connect.cursor()
    table = getUserTable(userid)

    cursor.execute(f"SELECT * FROM {table}")
    records = cursor.fetchall()

    commentsList = []
    for row in records:
        commentsList.append(row[2])

    return commentsList

# Получаем комментарий по переданному индексу
def getComment(userid, gameid):
    return getAllComments(userid)[int(gameid)-1]

# Проверка уникальности имени игры
def isUnique(userid, gamename):
    connect = sqlite3.connect(path + 'users.db')
    cursor = connect.cursor()
    table = getUserTable(userid)

    cursor.execute(f"SELECT game_score FROM {table} WHERE game_name = ?", (gamename,))
    record = cursor.fetchone()
    
    # Если record = none - значит такой игры ещё нету в списке
    # Если же нет, значит игра уже есть
    if record is None:
        return True
    else:
        return False
    
# Обновляем оценку игре из списка
def updateGameMark(userid, gamename, mark):
    connect = sqlite3.connect(path + 'users.db')
    cursor = connect.cursor()
    table = getUserTable(userid)

    cursor.execute(f"UPDATE {table} SET game_score = ? WHERE game_name = ?", (mark, gamename))
    connect.commit()

# Обновляем комментарий игре из списка
def updateGameComment(userid, gamename, comment):
    connect = sqlite3.connect(path + 'users.db')
    cursor = connect.cursor()
    table = getUserTable(userid)

    cursor.execute(f"UPDATE {table} SET game_comment = ? WHERE game_name = ?", (comment, gamename))
    connect.commit()






# Приветствие
@bot.message_handler(commands=['start'])
def hello(message):
    # Создаём файл базы данных, если его ещё нет
    # + создаём таблицу для пользователя и вносим его в дб
    init(message.chat.id)
    bot.send_message(message.from_user.id, bt.startMessage, reply_markup=default_markup)
    
# Inilne-кнопка Обратно
@bot.callback_query_handler(func=lambda call: True)
def back(message):
    if message.data == '1':
        bot.send_message(message.from_user.id, bt.backMessage, reply_markup=default_markup)
        bot.clear_step_handler_by_chat_id(chat_id = message.from_user.id)
    elif message.data == '2':
        gameList = getGameList(message.from_user.id)
        bot.send_message(message.from_user.id, bt.gameListMessage(gameList), reply_markup=gamelist_markup)
        bot.clear_step_handler_by_chat_id(chat_id = message.from_user.id)



# Последующие действия
@bot.message_handler(content_types=["text"])
def text_message(message):
    # Кнопка об авторе
    if message.text == "🌱 Об авторе":
        bot.send_message(message.from_user.id, bt.authorMessage, reply_markup=empty_markup)
        bot.send_photo(message.from_user.id, open(path + "photo.jpg", 'rb'), reply_markup=back_inline_markup)

    # Кнопка списка игр
    elif message.text == "📜 Список игр":
        gameList = getGameList(message.from_user.id)
        bot.send_message(message.from_user.id, bt.gameListMessage(gameList), reply_markup=gamelist_markup)

    # Возвращение в меню
    elif message.text == "🔺 Вернуться в меню":
        bot.send_message(message.from_user.id, bt.startContinueMessage, reply_markup=default_markup)

    # Добавление игры
    elif message.text == "⚜️ Добавить игру":
        bot.send_message(message.chat.id,"Отлично!", reply_markup=empty_markup)
        bot.send_message(message.from_user.id, bt.addGameMessage, reply_markup = back_inline_markup)
        bot.register_next_step_handler(message, nsAddGame)

    # Удаление игры
    elif message.text == "🪓 Удалить игру":
        gameList = getGameList(message.from_user.id)
        gameListLen = len(gameList)
        if gameListLen > 1:
            gameList = getGameList(message.from_user.id)
            bot.send_message(message.from_user.id, bt.gameListMessage(gameList), reply_markup=empty_markup)
            bot.send_message(message.from_user.id, bt.whichGameWeDelete(gameListLen), reply_markup=back_inline_markup)
            bot.register_next_step_handler(message, nsDeleteGame, gameList)
        elif gameListLen == 1:
            gameName = gameList[0].split(':')[0]

            bot.send_message(message.from_user.id, "🎲 Вы точно хотите удалить игру " + gameName + "?", reply_markup=deletegame_markup)
            bot.send_message(message.from_user.id, bt.ifYesSend1Message, reply_markup=back_inline_markup)
            bot.register_next_step_handler(message, nsDelete1Game, gameName)
        else:
            bot.send_message(message.from_user.id, bt.youNotHaveGamesToDeleteMessage, reply_markup=default_markup)

    # Просмотр отзыва об игре
    elif message.text == "📜 Просмотреть отзыв об игре":
        gameListLen = len(getGameList(message.from_user.id))
        if gameListLen > 1:
            bot.send_message(message.from_user.id,"Без проблем", reply_markup=empty_markup)
            gameList = getGameList(message.from_user.id)
            bot.send_message(message.from_user.id, bt.whichGameToSeeComment(gameList), reply_markup = back_togamelist_inline_markup)
            bot.register_next_step_handler(message, nsCheckComment)
        elif gameListLen == 1:
            bot.send_message(message.from_user.id, "🎲 Вот ваш комментарий:", reply_markup=change_mark_or_comment_markup)
            bot.send_message(message.from_user.id, getComment(message.from_user.id, '1'), reply_markup=back_togamelist_inline_markup)
            bot.register_next_step_handler(message, nsAfterComment, '1')
        else:
            # Если у пользователя ещё нет ни одной игры в списке
            # Значит он и не может посмотреть отзывы
            bot.send_message(message.from_user.id, bt.startTimeToAddMessage(), reply_markup=default_markup)

    # Если пользователь написал куралесицу
    else:
        bot.send_message(message.from_user.id, bt.wtfMessage, reply_markup=default_markup)




# Функции для bot.register_next_step_handler

# Добавляем название игре
def nsAddGame(message):
    # !!! gameInfo - это список, где хранится вся информация об игре
    # на момент этой функции мы добавили в список только название
    if isUnique(message.from_user.id, message.text):
        gameInfo = [message.text]
        bot.send_message(message.from_user.id, bt.whatMarkMessage(gameInfo), reply_markup = back_inline_markup)
        bot.register_next_step_handler(message, nsAddMark, gameInfo)
    else:
        # Вызывается, если такое имя игры уже есть в таблице
        bot.send_message(message.from_user.id, "🎲 Я в замешательстве!")
        bot.send_message(message.from_user.id, bt.addGameMessageNotUniqueName, reply_markup = back_inline_markup)
        bot.register_next_step_handler(message, nsAddGame)

# Добавляем оценку игре
def nsAddMark(message, gameInfo):
    # На момент функции у нас есть уже название и оценка игры
    # Проверка, ввёл ли пользователь оценку от 1-10
    if message.text in ['1','2','3','4','5','6','7','8','9','10']:
        gameInfo.append(message.text)
        bot.send_message(message.from_user.id, bt.whatCommentMessage(gameInfo), reply_markup = back_inline_markup)
        bot.register_next_step_handler(message, nsAddComment, gameInfo)
    else:
        bot.send_message(message.from_user.id, bt.whatMarkMessage2(gameInfo), reply_markup = back_inline_markup)
        bot.register_next_step_handler(message, nsAddMark, gameInfo)

# Добавляем комментарий игре
def nsAddComment(message, gameInfo):
    # Это завершающая функция изменения игры, записываем отзыв
    gameInfo.append(message.text)
    bot.send_message(message.from_user.id, bt.fullGameInfoMessage(gameInfo), reply_markup = back_inline_markup)
    bot.send_message(message.from_user.id, '''🎲 Всё верно?''', reply_markup=choice_markup)
    bot.register_next_step_handler(message, nsFinallyAddGame, gameInfo)

# Спрашиваем у пользователя правильно ли мы его поняли
def nsFinallyAddGame(message, gameInfo):
    # Здесь, если всё хорошо, мы уже добавляем новую игру в таблицу
    # Если что-то не так, то меняем до того момента, как всё будет правильно

    if (message.text == "🪀 Всё верно"):
        # Всё ок, добавляем игру в базу данных
        addNewGame(message.chat.id, gameInfo)
        bot.send_message(message.from_user.id, bt.weAddGameWhatNextMessage, reply_markup=default_markup)
        
    elif (message.text == "🎣 Изменить название"):
        bot.send_message(message.chat.id, "🦴 Без проблем, кожаный", reply_markup=empty_markup)
        bot.send_message(message.chat.id, "💀 Введи новое название игры: ", reply_markup=back_inline_markup)
        bot.register_next_step_handler(message, nsChangeGame, gameInfo)

    elif (message.text == "🏹 Изменить оценку"):
        bot.send_message(message.chat.id, "🦴 Без проблем, кожаный", reply_markup=empty_markup)
        bot.send_message(message.chat.id, "💀 Введи новое новую оценку игры (от 1 до 10): ", reply_markup=back_inline_markup)
        bot.register_next_step_handler(message, nsChangeMark, gameInfo)

    elif (message.text == "🎭 Изменить комментарий"):
        bot.send_message(message.chat.id, "🦴 Без проблем, кожаный", reply_markup=empty_markup)
        bot.send_message(message.chat.id, "💀 Введи новый комментарий для игры: ", reply_markup=back_inline_markup)
        bot.register_next_step_handler(message, nsChangeComment, gameInfo)

    else:
        # бот тебя не понял, снова задаёт вопрос тот же самый
        bot.send_message(message.from_user.id, bt.fullGameInfoMessage(gameInfo), reply_markup = back_inline_markup)
        bot.send_message(message.from_user.id, bt.allrightAndWtfMessage, reply_markup=choice_markup)
        bot.register_next_step_handler(message, nsFinallyAddGame, gameInfo)

# Меняем название
def nsChangeGame(message, gameInfo):
    # Проверяем уникальность введённого названия
    if isUnique(message.from_user.id, message.text):
        gameInfo[0] = message.text
        bot.send_message(message.from_user.id, bt.fullGameInfoMessage(gameInfo), reply_markup = back_inline_markup)
        bot.send_message(message.from_user.id, '''🎲 Всё верно?''', reply_markup=choice_markup)
        bot.register_next_step_handler(message, nsFinallyAddGame, gameInfo)
    else:
        bot.send_message(message.from_user.id, "🎲 Такое название игры уже есть в твоём списке!")
        bot.send_message(message.chat.id, "💀 Введи новое название игры: ", reply_markup=back_inline_markup)
        bot.register_next_step_handler(message, nsChangeGame, gameInfo)

# Меняем оценку
def nsChangeMark(message, gameInfo):
    if message.text in ['1','2','3','4','5','6','7','8','9','10']:
        gameInfo[1] = message.text
        bot.send_message(message.from_user.id, bt.fullGameInfoMessage(gameInfo), reply_markup = back_inline_markup)
        bot.send_message(message.from_user.id, '''🎲 Всё верно?''', reply_markup=choice_markup)
        bot.register_next_step_handler(message, nsFinallyAddGame, gameInfo)
    else:
        bot.send_message(message.chat.id, "🦴 Введи число, что ты как не родной", reply_markup=empty_markup)
        bot.send_message(message.chat.id, "💀 Введи новое новую оценку игры (от 1 до 10): ", reply_markup=back_inline_markup)
        bot.register_next_step_handler(message, nsChangeMark, gameInfo)

# Меняем комментарий
def nsChangeComment(message, gameInfo):
    gameInfo[2] = message.text
    bot.send_message(message.from_user.id, bt.fullGameInfoMessage(gameInfo), reply_markup = back_inline_markup)
    bot.send_message(message.from_user.id, '''🎲 Всё верно?''', reply_markup=choice_markup)
    bot.register_next_step_handler(message, nsFinallyAddGame, gameInfo)

# Просмотр комментария
def nsCheckComment(message):
    gameList = getGameList(message.from_user.id)
    gameAmount = len(gameList)
    userChoice = message.text

    # Список допустимых значений от 1 до кол-ва игр пользователя
    rightValues = []
    while gameAmount != 0:
        rightValues.append(str(gameAmount))
        gameAmount = gameAmount - 1

    # Проверяем, правильное ли значение написал пользовател, если нет, то возвращаем его сюда же
    if userChoice in rightValues:
        bot.send_message(message.from_user.id, "🎲 Вот ваш комментарий:", reply_markup=change_mark_or_comment_markup)
        bot.send_message(message.from_user.id, getComment(message.from_user.id, userChoice), reply_markup=back_togamelist_inline_markup)
        bot.register_next_step_handler(message, nsAfterComment, userChoice)
    else:
        bot.send_message(message.from_user.id, bt.whichGameToSeeComment2(gameList), reply_markup = back_togamelist_inline_markup)
        bot.register_next_step_handler(message, nsCheckComment)

# После вывода комментария к игре ждём, что напишет пользователь
def nsAfterComment(message, gameid):
    gameInfo = getGameInfo(message.from_user.id, gameid)

    if message.text == "🏹 Изменить оценку":
        bot.send_message(message.chat.id, "🦴 Без проблем, кожаный", reply_markup=empty_markup)
        bot.send_message(message.chat.id, "💀 Введи новое новую оценку игры (от 1 до 10): ", reply_markup=back_togamelist_inline_markup)
        bot.register_next_step_handler(message, nsChangeMarkOldGame, gameInfo)
    
    elif message.text == "🎭 Изменить комментарий":
        bot.send_message(message.chat.id, "🦴 Без проблем, кожаный", reply_markup=empty_markup)
        bot.send_message(message.chat.id, "💀 Введи новый комментарий к игре: ", reply_markup=back_togamelist_inline_markup)
        bot.register_next_step_handler(message, nsChangeCommentOldGame, gameInfo)

    # На случай, если что-то неясное
    else:
        bot.send_message(message.from_user.id, "🎲 Вот ваш комментарий:", reply_markup=change_mark_or_comment_markup)
        bot.send_message(message.from_user.id, getComment(message.from_user.id, gameid), reply_markup=back_togamelist_inline_markup)
        bot.register_next_step_handler(message, nsAfterComment, gameid)

# Изменение оценки уже существующей игры
def nsChangeMarkOldGame(message, gameInfo):
    # Проверка введённого значения
    if message.text in ['1','2','3','4','5','6','7','8','9','10']:
        updateGameMark(message.from_user.id, gameInfo[0], int(message.text))
        bot.send_message(message.chat.id, "🎲 Оценка изменена!", reply_markup=empty_markup)

        gameList = getGameList(message.from_user.id)
        bot.send_message(message.from_user.id, bt.gameListMessage(gameList), reply_markup=gamelist_markup)
    else:
        bot.send_message(message.chat.id, "🦴 Введи число, что ты как не родной", reply_markup=empty_markup)
        bot.send_message(message.chat.id, "💀 Введи новое новую оценку игры (от 1 до 10): ", reply_markup=back_inline_markup)
        bot.register_next_step_handler(message, nsChangeMarkOldGame, gameInfo)

# Изменение комментария уже существующей игры
def nsChangeCommentOldGame(message, gameInfo):
    updateGameComment(message.from_user.id, gameInfo[0], message.text)
    bot.send_message(message.chat.id, "🎲 Комментарий изменён!", reply_markup=empty_markup)

    gameList = getGameList(message.from_user.id)
    bot.send_message(message.from_user.id, bt.gameListMessage(gameList), reply_markup=gamelist_markup)

# Удаление игры
def nsDeleteGame(message, gameList):
    # Проверяем верно ли пользователь ввёл значение
    gameListLen = len(gameList)

    rightValues = []
    while gameListLen != 0:
        rightValues.append(str(gameListLen))
        gameListLen = gameListLen - 1

    if message.text in rightValues:
        gameNumber = int(message.text)
        gameName = gameList[gameNumber-1].split(":")[0]
        deleteGame(message.from_user.id, gameName)

        bot.send_message(message.chat.id, "🎲 Игра успешно удалена!", reply_markup=empty_markup)
        # Обновляем gameList и выводим список игр
        gameList = getGameList(message.from_user.id)
        bot.send_message(message.from_user.id, bt.gameListMessage(gameList), reply_markup=gamelist_markup)
    else:
        bot.send_message(message.chat.id, "🦴 Введи число, что ты как не родной", reply_markup=empty_markup)
        bot.send_message(message.chat.id, bt.whichGameWeDeleteNotRightValue(len(gameList)), reply_markup=back_inline_markup)
        bot.register_next_step_handler(message, nsDeleteGame, gameList)

# Удаление игры, в случае, если у пользователя только одна игра в списке
def nsDelete1Game(message, gameName):
    if message.text == "🪓 Удалить":
        # Если пользователь согласился на удаление игры, то введёт именно это
        deleteGame(message.from_user.id, gameName)
        bot.send_message(message.from_user.id, bt.weDeleteGameWhatNextMessage, reply_markup=default_markup)
    else:
        # Опять что-то невразумительное
        bot.send_message(message.from_user.id, "🎲 Вы точно хотите удалить игру " + gameName + "?", reply_markup=deletegame_markup)
        bot.send_message(message.from_user.id, bt.ifYesSend1MessageAgain, reply_markup=back_inline_markup)
        bot.register_next_step_handler(message, nsDelete1Game, gameName)

bot.polling(none_stop=True, interval=0)
