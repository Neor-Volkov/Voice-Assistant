# Voice Assistant v 1.1
from pyowm import OWM
from pyowm.utils.config import get_default_config
import pyttsx3
import os
import random
import webbrowser
import datetime
import time
import speech_recognition as sr
import pandas as pd
from fuzzywuzzy import fuzz
from colorama import *

# раздел глобальных переменных
# Погода
config_dict = get_default_config()
config_dict['language'] = 'ru'

place = "Харьков"
owm = OWM('fd5321547e631b45b33d6d1cc673754f')
mgr = owm.weather_manager()
observation = mgr.weather_at_place('Харьков')
w = observation.weather

status = w.detailed_status               # 'clouds'
w.wind()                                 # {'speed': 4.6, 'deg': 330}
humidity = w.humidity                    # 87
temp = w.temperature('celsius')['temp']  # {'temp_max': 10.5, 'temp': 9.7, 'temp_min': 9.0}
# w.rain                                 # {}
heat_index = w.heat_index                # None
clouds = w.clouds                        # 75

task = ''
text = ''
r = sr.Recognizer()
engine = pyttsx3.init()
adress = ''
j = 0
task_number = 0


ndel = ['морган', 'морген', 'морг', 'моргэн', 'морда',
        'ладно', 'не могла бы ты', 'пожалуйста', 'сколько', 'текущее', 'сейчас']

commands = ['привет',
            'выключи комп', 'выруби компьютер',
            'пока',
            'покажи список команд',
            'выключи компьютер', 'выключай компьютер',
            'вырубись', 'отключись',
            'подбрось монетку', 'подкинь монетку', 'кинь монетку',
            'открой vk', 'открой браузер', 'включи vk', 'открой интернет', 'открой youtube', 'включи музон',
            'открой viber', 'включи viber', 'открывай viber',
            'найди', 'найти', 'ищи', 'кто такой',
            'как дела', 'как жизнь', 'как настроение', 'как ты',
            'открой лаунчер аризоны', 'запусти лаунчер аризоны', 'запускай лаунчер аризоны',
            'включай лаунчер аризоны', 'заходи на аризону', 'включай аризону',
            'текущее время', 'сколько времени', 'сколько время', 'сейчас времени', 'который час',
            'крути винилы', 'крути винил',
            'какая погода', 'погода', 'погода на улице', 'какая погода на улице',
            'история запросов', 'выведи историю запросов', 'покажи историю запросов',
            'открой музыку', 'вруби музыку',
            'переведи',
            'планы', 'на будущее', 'что планируется',
            'открой протокол разработки', 'протокол разработки', ]


# раздел описания функций комманд

def pri_com():  # выводит на экран историю запросов
    z = {}
    mas = []
    mas2 = []
    mas3 = []
    mas4 = []
    file = open('commands.txt', 'r', encoding='UTF-8')
    k = file.readlines()
    for i in range(len(k)):
        line = str(k[i].replace('\n', '').strip())
        mas.append(line)
    file.close()
    for i in range(len(mas)):
        x = mas[i]
        if x in z:
            z[x] += 1
        if not (x in z):
            b = {x: 1}
            z.update(b)
        if not (x in mas2):
            mas2.append(x)
    for i in mas2:
        mas3.append(z[i])
    for i in range(1, len(mas3) + 1):
        mas4.append(str(i) + ') ')
    #     list = pd.DataFrame({
    pd.DataFrame({
        'command': mas2,
        'count': mas3
    }, index=mas4)
    list.index.name = '№'
    print(list)


def plans():
    global engine
    engine.say('Моя задача будет заключаться в помощи в управлении системой умного дома'
               'На данный момент ведется работа над виртуальной частью программного обеспечения'
               'Так же ведется работа по оптимизации всех существующих в коде функций'
               'В дальнейшем планируется работа над технической частью проекта'
               'Она будет состоять из создания эллементов умного дома с помощью микроконтроллеров Arduino'
               'В конечном итоге виртуальная и техническая части проекта будут обьеденены'
               'Моя конечная цель будет достигнута')


def clear_analis():  # очистка файла с историей запросов
    global engine
    file = open('commands.txt', 'w', encoding='UTF-8')
    file.close()
    engine.say('Файл аналитики очищен!')


def add_file(x):
    file = open('commands.txt', 'a', encoding='UTF-8')
    if x != '':
        file.write(x + '\n')
    file.close()


def comparison(x):  # осуществляет поиск самой подходящей под запрос функции
    global commands, j
    ans = ''
    for i in range(len(commands)):
        k = fuzz.ratio(x, commands[i])
        if (k > 50) & (k > j):
            ans = commands[i]
            j = k
    if (ans != 'пока') & (ans != 'привет'):
        add_file(ans)
    return str(ans)


def show_cmds():  # выводит на экран список доступных комманд
    my_com = ['привет', 'открой файл', 'выключи компьютер', 'пока', 'покажи список команд',
              'открой vk', 'открой viber', 'открой интернет', 'открой youtube', 'включи музыку', 'очисти файл',
              'покажи cтатистику', 'сколько время', 'какая погода']
    for i in my_com:
        print(i)
    time.sleep(2)


def protocol():
    engine.say('Протокол разработки открыт')
    os.startfile('C:/Users/Ruslan/PycharmProjects/Voice_Assistant/protocol.txt')


def web_search():
    global text, task
    mas = ['пожалуйста', 'давай', 'морган']
    keys = ('найди', 'найти', 'ищи', 'кто такой')
    k = ['Вот что я нашла по вашему запросу', 'Вот что мне удалось найти', 'Вот что я нашла']
    for i in mas:
        task = task.replace(i, '')
        task = task.replace(' ', ' ')
    task = task.strip()
    for i in keys:
        if i in task:
            task = 'найди'
    if 'найди' in text:
        add_file('найди')
        zapros = text.replace('найди', '').strip()
        webbrowser.open(f'https://www.google.com/search?q={zapros}&oq={zapros}'
                        f'81&aqs=chrome..69i57j46i131i433j0l5.2567j0j7&sourceid=chrome&ie=UTF-8')
        text = ''
        engine.say(random.choice(k))

    elif 'найти' in text:
        add_file('найти')
        zapros = text.replace('найти', '').strip()
        webbrowser.open(f'https://www.google.com/search?q={zapros}&oq={zapros}'
                        f'81&aqs=chrome..69i57j46i131i433j0l5.2567j0j7&sourceid=chrome&ie=UTF-8')
        text = ''
        engine.say(random.choice(k))

    elif 'ищи' in text:
        add_file('ищи')
        zapros = text.replace('ищи', '').strip()
        webbrowser.open(f'https://www.google.com/search?q={zapros}&oq={zapros}'
                        f'81&aqs=chrome..69i57j46i131i433j0l5.2567j0j7&sourceid=chrome&ie=UTF-8')
        text = ''
        engine.say(random.choice(k))

    elif 'кто такой' in text:
        add_file('кто такой')
        zapros = text.replace('кто такой', '').strip()
        webbrowser.open(f'https://www.google.com/search?q={zapros}&oq={zapros}'
                        f'81&aqs=chrome..69i57j46i131i433j0l5.2567j0j7&sourceid=chrome&ie=UTF-8')
        text = ''
        engine.say(random.choice(k))


def vinil():
    webbrowser.open('https://www.youtube.com/watch?v=zqY-Wr43j94&t=0s')


def monetka():
    engine.say("Подбрасываю...")
    k = ["Выпал Орёл", "Выпала Решка"]
    engine.say(random.choice(k))


def clear_task():  # удаляет ключевые слова
    global text, ndel
    for z in ndel:
        text = text.replace(z, '').strip()
        text = text.replace('  ', ' ').strip()


def hello():  # функция приветствия
    # hour = int(datetime.datetime.now().hour)
    z = ["Привет, чем могу быть полезна?", 'Что вам угодно?', 'Привет. Чем-нибудь помочь?']
    engine.say(random.choice(z))


#    if hour >= 0 & hour < 12:
#        z = ["Доброе утро, чем могу быть полезна?", 'Что вам угодно?', 'Привет. Чем-нибудь помочь?']
#        x = random.choice(z)
#        engine.say(x)
#
#    elif hour >= 12 & hour < 18:
#        z = ["Добрый вечер, чем могу быть полезна?", 'Что вам угодно?', 'Привет. Чем-нибудь помочь?']
#        x = random.choice(z)
#        engine.say(x)
#
#    else:
#        z = ["Добрый вечер, чем могу быть полезна?", 'Что вам угодно?', 'Привет. Чем-нибудь помочь?']
#        x = random.choice(z)
#        engine.say(x)


def viber():
    os.startfile("C:/Users/Ruslan/AppData/Local/Viber/Viber.exe")
    engine.say("Вайбер открыт")


def quite():  # функция выхода из программы
    global engine
    x = ['надеюсь мы скоро увидимся!', 'рада была помочь', 'Я отключаюсь']
    engine.say(random.choice(x))
    engine.runAndWait()
    engine.stop()
    os.system('cls')
    exit(0)


#     'какая погода': , 'погода': weather_pogoda,
#     'погода на улице': weather_pogoda, 'какая погода на улице': weather_pogoda,
def weather_pogoda():
    global engine
    engine.say("В городе " + str(place) + " сейчас " + str(status))
    engine.say("Температура " + str(temp) + " градусов по цельсию")
    engine.say("Влажность составляет " + str(humidity) + "%")
    engine.say("Скорость ветра " + str(w.wind()['speed']) + " метров в секунду")
    print("В городе " + str(place) + " сейчас " + str(status))
    print("Температура " + str(temp) + " градусов по цельсию")
    print("Влажность составляет " + str(humidity) + "%")
    print("Скорость ветра " + str(w.wind()['speed']) + " метров в секунду")
    if temp < 10:
        engine.say("Сегодня холодно, одевайтесь теплее")
        print("Сегодня холодно, одевайтесь теплее")
    elif temp < 0:
        engine.say("Сегодня очень холодно, одевайте куртку")
        print("Сегодня очень холодно, одевайте куртку")
    elif temp > 20:
        engine.say("Сегодня тепло можете одеваться легко")
        print("Сегодня тепло можете одеваться легко")
    elif temp < 19:
        engine.say("На улице прохладно, рекомендую одеть ветровку")
        print("На улице прохладно, рекомендую одеть ветровку")
    if str(status) == "дождь":
        engine.say("Возьмите с собой зонтик")
        print("Возьмите с собой зонтик")


def brows():  # открывает браузер
    webbrowser.open('https://google.com')
    engine.say("Браузер открыт!")


def howyou():
    engine.say("Всегда готова к работе!")


def arz():
    global engine
    engine.say("Аризона лаунчер открыт")
    os.system('G:/games/ARIZONA GAMES/arizona-starter.exe')


def ovk():  # открывает вк
    engine.say("Вконтакте открыто")
    webbrowser.open('https://vk.com/feed')


def youtube():  # открывает ютюб
    engine.say("Youtube открыт")
    webbrowser.open('https://www.youtube.com')


def timethis():  # время
    now = datetime.datetime.now()
    engine.say("Сейчас " + str(now.hour) + ":" + str(now.minute))
    print("Сейчас " + str(now.hour) + ":" + str(now.minute))


def shut():  # выключает компьютер
    engine.say('До скорых встреч!')
    os.system('shutdown /s /f /t 10')
    quite()


def music():  # включает музыку
    k = ['https://www.youtube.com/watch?v=UkSr9Lw5Gm8&t=0s', 'https://www.youtube.com/watch?v=YlsQ6hjSZ8A&t=0s',
         'https://www.youtube.com/watch?v=bcyvZIoQp9A&t=0s', 'https://www.youtube.com/watch?v=eQxmhqaR2OA&t=0s']
    webbrowser.open(random.choice(k))


def check_translate():
    global text, engine
    tr = 0
    variants = ['переведи', 'перевести', 'переводить', 'перевод']
    for i in variants:
        if (i in text) & (tr == 0):
            word = text
            word = word.replace('переведи', '').strip()
            word = word.replace('перевести', '').strip()
            word = word.replace('переводить', '').strip()
            word = word.replace('перевод', '').strip()
            word = word.replace('слово', '').strip()
            word = word.replace('слова', '').strip()
            webbrowser.open('https://translate.google.ru/#view=home&op=translate&sl=auto&tl=ru&text={}'.format(word))
            tr = 1
            text = ''
            k = ['Вот что мне удалось найти', 'Вот что я нашла по вашему запросу']
            engine.say(random.choice(k))


cmds = {
    'привет': hello,
    'выруби компьютер': shut, 'выключи комп': shut, 'выключи компьютер': shut, 'выключай компьютер': shut,
    'подбрось монетку': monetka, 'подкинь монетку': monetka, 'кинь монетку': monetka,
    'найди': web_search, 'найти': web_search, 'ищи': web_search, 'кто такой': web_search,
    'как дела': howyou, 'как жизнь': howyou, 'как настроение': howyou, 'как ты': howyou,
    'открой viber': viber, 'включи viber': viber, 'открывай viber': viber,
    'открой лаунчер аризоны': arz, 'запусти лаунчер аризоны': arz, 'запускай лаунчер аризоны': arz,
    'включай лаунчер аризоны': arz, 'заходи на аризону': arz, 'включай аризону': arz,
    'пока': quite, 'вырубись': quite, 'отключись': quite,
    'покажи список команд': show_cmds,
    'открой браузер': brows, 'открой интернет': brows,
    'открой youtube': youtube, 'открой vk': ovk, 'включи vk': ovk,
    'история запросов': pri_com, 'выведи историю запросов': pri_com, 'покажи историю запросов': pri_com,
    'очисти историю запросов': clear_analis, 'удали историю запросов': clear_analis,
    'открой музыку': music, 'включи музон': music, 'вруби музыку': music,
    'крути винилы': vinil, 'крути винил': vinil,
    'планы': plans, 'на будущее': plans, 'что планируется': plans,
    'переведи': check_translate,
    'текущее время': timethis, 'сколько времени': timethis, 'сколько время': timethis,
    'сейчас времени': timethis, 'который час': timethis,
    'какая погода': weather_pogoda, 'погода': weather_pogoda, 'погода на улице': weather_pogoda,
    'какая погода на улице': weather_pogoda,
    'открой протокол разработки': protocol, 'протокол разработки': protocol,
}


# распознавание

def talk():
    global text
    text = ''
    with sr.Microphone() as sourse:
        print('Я вас слушаю: ')
        r.adjust_for_ambient_noise(sourse)
        audio = r.listen(sourse, phrase_time_limit=5)
        try:
            text = (r.recognize_google(audio, language="ru-RU")).lower()
        except sr.UnknownValueError:
            pass
        except TypeError:
            pass
        os.system('cls')
        clear_task()

# выполнение команд


def cmd_exe():
    global cmds, engine, task_number, text
    check_translate()
    web_search(),
    text = comparison(text)
    print(text)
    if text in cmds:
        if (text != 'привет') & (text != 'пока') & (text != 'покажи список команд') \
                & (text != 'текущее время') & (text != 'сколько времени') \
                & (text != 'сколько время') & (text != 'сейчас времени') & (text != 'который час') \
                & (text != 'планы') & (text != 'какая погода') \
                & (text != 'как дела') & (text != 'как жизнь') & (text != 'как настроение') & (text != 'как ты')\
                & (text != 'погода') & (text != 'погода на улице') & (text != 'какая погода на улице'):
            k = ['Секундочку', 'Сейчас сделаю', 'уже выполняю']
            engine.say(random.choice(k))
        cmds[text]()
    elif text == '':
        pass
    else:
        print('Команда не найдена!')

    task_number += 1
    if task_number % 10 == 0:
        engine.say('У вас будут еще задания?')

    engine.runAndWait()
    engine.stop()


# исправляет цвет

print(Fore.YELLOW + '', end='')
os.system('cls')


# основной бесконечный цикл


def main():
    global j, text
    try:
        talk()
        if text != '':
            cmd_exe()
            talk()
            j = 0
    except UnboundLocalError:
        pass
    except NameError:
        pass
    except TypeError:
        pass
    except IndentationError:
        pass
    except IndexError:
        pass
    except ValueError:
        pass


while True:
    main()
