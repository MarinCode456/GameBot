class msg:
    authorMessage = '''✨ Это мой первый проект на языке программирования Python, реализованный с помощью библиотеки telebot.
    
🌪 Благодаря ему я теперь немного больше понимаю как составлять продуманные проекты. А ещё я наконец-то сделал то, что давно хотел - программка для составления списка пройденных игр. 

🛠 Возможно, весь функционал не особо подходит для бота, функции топорно реализованы, но я всё равно рад, что у меня получилось сделать программу, которую буду использовать в дальнейшем.

        Мой телеграм - https://t.me/dathrisdate
        Телеграмм канал - https://t.me/+lM49VObwJ_RiNDli
        Гитхаб - https://github.com/MarinCode456

🖥 В своём телеграмм канале я каждый день пишу то, чем занимаюсь в плане программирования. Там можно найти промежуток разработки этого бота (1 день по 15), а также совсем новые проекты. 

🔭 На гитхабе же планирую выкладывать все свои наработки и проекты.'''

    startMessage = '''===================== Логово Роджера =====================
                                
💀 Хэй! На связи Роджер. 
                        
🔮 Именно я запомню твой игровой опыт, чтобы ты мог создать коллекцию пройденных игр!
                        
=========================================================
                        
🎲 В меню ниже выбери, что ты хочешь сделать со своей картотекой и мы приступим к игре:'''

    youNotHaveGamesToDeleteMessage = '''===================== Логово Роджера =====================
                                
💀 У тебя же пока нет игр!
                        
🔮 Что будем делать дальше?
                        
=========================================================
                        
🎲 В меню ниже выбери, что ты хочешь сделать со своей картотекой и мы приступим к игре:'''

    backMessage = '''===================== Логово Роджера =====================
                                
💀 Что будем делать дальше?
                        
=========================================================
                        
🎲 В меню ниже выбери, что ты хочешь сделать со своей картотекой и мы приступим к игре:'''

    startContinueMessage = '''===================== Логово Роджера =====================
                                
💀 Хэй! На связи Роджер. 
                        
🔮 Что будем делать?
                        
=========================================================
                        
🎲 В меню ниже выбери, что ты хочешь сделать со своей картотекой и мы приступим к игре:'''


    addGameMessage = '''===================== Логово Роджера =====================
                                
💀 Йо-хо-хо!
                        
=========================================================
                        
🎲 Для начала введи название игры ниже:'''

    addGameMessageNotUniqueName = '''===================== Логово Роджера =====================
                                
💀 Такое название игры уже есть в твоём списке!
                        
=========================================================
                        
🎲 Введи любое другое название игры:'''

    wtfMessage = '''===================== Логово Роджера =====================
                               
💀 Я тебя не понял
                     
=========================================================
                     
🎲 В меню ниже выбери, что ты хочешь сделать со своей картотекой и мы приступим к игре:'''

    weAddGameWhatNextMessage = '''===================== Логово Роджера =====================
                               
💀 Игра успешно добавлена! 
                     
🔮 Что будем делать дальше?
                     
=========================================================
                     
🎲 В меню ниже выбери, что ты хочешь сделать со своей картотекой и мы приступим к игре:'''

    weDeleteGameWhatNextMessage = '''===================== Логово Роджера =====================
                               
💀 Игра успешно удалена!
                     
🔮 Что будем делать дальше?
                     
=========================================================
                     
🎲 В меню ниже выбери, что ты хочешь сделать со своей картотекой и мы приступим к игре:'''

    allrightAndWtfMessage = '''🎲 Всё верно? 
    
Я не понял, что ты написал. Выбери действие из меню снизу:'''

    ifYesSend1Message = '''
🔮 Если да, нажмите на кнопку "Удалить":'''

    ifYesSend1MessageAgain = '''
🔮 Если да, нажмите на кнопку "Удалить", либо вернитесь в меню:'''





    @staticmethod
    def whatMarkMessage(gameInfo):
        return '''===================== Логово Роджера =====================
                               
💀 Итак, мы добавляем: ''' + gameInfo[0] + '''
                     
=========================================================
                     
🎲 Какую оценку от 1 до 10 ты бы поставил этой игре?
'''
    @staticmethod
    def whatMarkMessage2(gameInfo):
        return '''===================== Логово Роджера =====================
                               
💀 Итак, мы добавляем: ''' + gameInfo[0] + '''
                     
=========================================================
                     
🎲 Какую оценку от 1 до 10 ты бы поставил этой игре?

(До этого вы написали нечто невразумительное, напишите число от 1 до 10)
'''

    @staticmethod
    def whatCommentMessage(gameInfo):
        return '''===================== Логово Роджера =====================
                               
💀 Итак, мы добавляем: ''' + gameInfo[0] + '''

C оценкой: ''' + gameInfo[1] + ''' 
                     
=========================================================
                     
🎲 Теперь одним большим сообщением опиши свои впечатления от игры:
'''

    @staticmethod
    def fullGameInfoMessage(gameInfo):
        return '''===================== Логово Роджера =====================
                               
💀 Итак, мы добавляем: ''' + gameInfo[0] + '''

C оценкой: ''' + gameInfo[1] + '''

И таким комментарием: ''' + gameInfo[2] + '''
                     
========================================================='''

    @staticmethod
    def gameListMessage(gameList):
        gameListMessage = '''===================== Логово Роджера =====================
                                    
💀 Вот твой список игр: 
'''

        if len(gameList) != 0:
            # Добавляем игры в список по одной
            counter = 1
            for row in gameList:
                line = row.split(":")
                gameListMessage = gameListMessage + f'\n {counter}. {line[0]} - {line[1]}'
                counter += 1

            gameListMessage += '''
\n========================================================='''
        # Если у человека ещё нет ни одной игры в списке
        else:
            gameListMessage += '''
Здесь пока нет игр.
\n========================================================='''

        return gameListMessage
    
    @staticmethod
    def whichGameToSeeComment(gameList):
        return '''🎲 Для какой игры вы хотите просмотреть комментарий?

Введите число от 1 до ''' + str(len(gameList)) + " в соответствии со списком выше:"
    
    @staticmethod
    def whichGameToSeeComment2(gameList):
        return '''💀 Чего-чего? Я тебя не понял.

🎲 Для какой игры вы хотите просмотреть комментарий?

Введите число от 1 до ''' + str(len(gameList)) + " в соответствии со списком выше:"
    
    @staticmethod
    def startTimeToAddMessage():
        # Начальный текст, но после того как пользователь без игр
        # нажал на "посмотреть отзыв"
        return '''===================== Логово Роджера =====================
                                
💀 Но у тебя же нет игр?
                        
🔮 Самое время их добавить!
                        
=========================================================
                        
🎲 В меню ниже выбери, что ты хочешь сделать со своей картотекой и мы приступим к игре:'''

    @staticmethod
    def whichGameWeDelete(gameListLen):
        return '''😿 Это грустно

Выбери игру, которую хочешь удалить. 

🔮 Для этого введи число от 1 до ''' + str(gameListLen) + " в соответствии со списком выше:"
    
    @staticmethod
    def whichGameWeDeleteNotRightValue(gameListLen):
        return '''🔮 Выбери игру, которую хочешь удалить (от 1 до ''' + str(gameListLen) + ''')'''