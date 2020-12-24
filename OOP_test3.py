# Voice Assistant v 1.3
from pyowm import OWM
from pyowm.utils.config import get_default_config
import pyttsx3
import os
import random
import webbrowser
import datetime
import time
import speech_recognition as sr
from fuzzywuzzy import fuzz
from colorama import *


class Assistant:

    def __init__(self):
        config_dict = get_default_config()
        config_dict['language'] = 'ru'
        owm = OWM('fd5321547e631b45b33d6d1cc673754f')
        mgr = owm.weather_manager()
        self.observation = mgr.weather_at_place('Харьков')
        self.w = self.observation.weather
        self.status = self.w.detailed_status               # 'clouds'
        self.w.wind()                                 # {'speed': 4.6, 'deg': 330}
        self.humidity = self.w.humidity                    # 87
        self.temp = self.w.temperature('celsius')['temp']  # {'temp_max': 10.5, 'temp': 9.7, 'temp_min': 9.0}
        # w.rain                                 # {}
        self.heat_index = self.w.heat_index                # None
        self.clouds = self.w.clouds                        # 75
        self.place = "Харьков"
        self.r = sr.Recognizer()
        self.engine = pyttsx3.init()
        self.adress = []
        self.tallys = []
        self.j = 0
        self.x = 0
        self.task_number = 0

        self.ndel = ['морган', 'морген', 'морг', 'моргэн', 'морда',
                     'ладно', 'не могла бы ты', 'пожалуйста', 'сколько', 'текущее', 'сейчас']

        self.commands = ['привет',
                         'выключи комп', 'выруби компьютер',
                         'пока',
                         'покажи список команд',
                         'выключи компьютер', 'выключай компьютер',
                         'вырубись', 'отключись',
                         'подбрось монетку', 'подкинь монетку', 'кинь монетку',
                         'открой vk', 'открой браузер', 'включи vk', 'открой интернет', 'открой youtube',
                         'включи музон',
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
    def plans(self):
        self.engine.say('Моя задача будет заключаться в помощи в управлении компьютером'
                        'На данный момент ведется работа над виртуальной частью программного обеспечения'
                        'Так же ведется работа по оптимизации всех существующих в коде функций'
                        'В будущем в планах написать систему распознавания лица'
                        'И сделать уровни допуска к командам'
                        'В конечном итоге моя цель будет достигнута')

    def comparison(self, *args):  # осуществляет поиск самой подходящей под запрос функции
        self.j = args
        self.x = args
        self.commands = args
        commands = []
        x = 0
        ans = ''
        j = 0
        for i in range(len(commands)):
            k = fuzz.ratio(x, commands[i])
            if (k > 50) & (k > j):
                ans = commands[i]
        if (ans != 'пока') & (ans != 'привет'):
            return str(ans)

    def show_cmds(self):  # выводит на экран список доступных комманд
        self.is_not_used()
        my_com = ['привет', 'открой файл', 'выключи компьютер', 'пока', 'покажи список команд',
                  'открой vk', 'открой viber', 'открой интернет', 'открой youtube', 'включи музыку', 'очисти файл',
                  'покажи cтатистику', 'сколько время', 'какая погода']
        for i in my_com:
            print(i)
        time.sleep(2)

    def is_not_used(self):
        pass

    def protocol(self):
        self.engine.say('Протокол разработки открыт')
        os.startfile('C:/Users/Ruslan/PycharmProjects/Voice_Assistant/protocol.txt')

    def web_search(self):
        task = ''
        mas = ['пожалуйста', 'давай', 'морган']
        keys = ('найди', 'найти', 'ищи', 'кто такой')
        k = ['Вот что я нашла по вашему запросу', 'Вот что мне удалось найти', 'Вот что я нашла']
        text = ''
        for i in mas:
            task = task.replace(i, '')
            task = task.replace(' ', ' ')
        task = task.strip()
        for i in keys:
            if i in task:
                task = 'найди'
        if 'найди' in text:
            zapros = text.replace('найди', '').strip()
            webbrowser.open(f'https://www.google.com/search?q={zapros}&oq={zapros}'
                            f'81&aqs=chrome..69i57j46i131i433j0l5.2567j0j7&sourceid=chrome&ie=UTF-8')
            self.engine.say(random.choice(k))

        elif 'найти' in text:
            zapros = text.replace('найти', '').strip()
            webbrowser.open(f'https://www.google.com/search?q={zapros}&oq={zapros}'
                            f'81&aqs=chrome..69i57j46i131i433j0l5.2567j0j7&sourceid=chrome&ie=UTF-8')
            self.engine.say(random.choice(k))

        elif 'ищи' in text:
            zapros = text.replace('ищи', '').strip()
            webbrowser.open(f'https://www.google.com/search?q={zapros}&oq={zapros}'
                            f'81&aqs=chrome..69i57j46i131i433j0l5.2567j0j7&sourceid=chrome&ie=UTF-8')
            self.engine.say(random.choice(k))

        elif 'кто такой' in text:
            zapros = text.replace('кто такой', '').strip()
            webbrowser.open(f'https://www.google.com/search?q={zapros}&oq={zapros}'
                            f'81&aqs=chrome..69i57j46i131i433j0l5.2567j0j7&sourceid=chrome&ie=UTF-8')
            self.engine.say(random.choice(k))

    def vinil(self):
        self.is_not_used()
        webbrowser.open('https://www.youtube.com/watch?v=zqY-Wr43j94&t=0s')

    def monetka(self):
        self.engine.say("Подбрасываю...")
        k = ["Выпал Орёл", "Выпала Решка"]
        self.engine.say(random.choice(k))

    def clear_task(self, text):  # удаляет ключевые слова
        ndel = ['морган', 'морген', 'морг', 'моргэн', 'морда',
                'ладно', 'не могла бы ты', 'пожалуйста', 'сколько', 'текущее', 'сейчас']
        self.is_not_used()
        for z in ndel:
            text = text.replace(z, '').strip()
            text = text.replace('  ', ' ').strip()

    def hello(self):  # функция приветствия
        hour = int(datetime.datetime.now().hour)

        if hour >= 4 | hour <= 12:
            z = ["Доброе утро, чем могу быть полезна?", 'Что вам угодно?', 'Привет. Чем-нибудь помочь?']
            self.engine.say(random.choice(z))
        elif hour >= 12 | hour <= 18:
            z = ["Добрый день, чем могу быть полезна?", 'Что вам угодно?', 'Привет. Чем-нибудь помочь?']
            x = random.choice(z)
            self.engine.say(x)
        elif hour >= 18 | hour <= 23:
            z = ["Добрый вечер, чем могу быть полезна?", 'Что вам угодно?', 'Привет. Чем-нибудь помочь?']
            self.engine.say(random.choice(z))
        else:
            z = ["Доброй ночи, чем могу быть полезна?", 'Что вам угодно?', 'Привет. Чем-нибудь помочь?']
            self.engine.say(random.choice(z))

    def viber(self):
        os.startfile("C:/Users/Ruslan/AppData/Local/Viber/Viber.exe")
        self.engine.say("Вайбер открыт")

    def quite(self):  # функция выхода из программы
        x = ['надеюсь мы скоро увидимся!', 'рада была помочь', 'Я отключаюсь']
        self.engine.say(random.choice(x))
        self.engine.runAndWait()
        self.engine.stop()
        os.system('cls')
        exit(0)

    #     'какая погода': , 'погода': weather_pogoda,
    #     'погода на улице': weather_pogoda, 'какая погода на улице': weather_pogoda,
    def weather_pogoda(self):
        self.engine.say("В городе " + str(self.place) + " сейчас " + str(self.status))
        self.engine.say("Температура " + str(round(self.temp)) + " градусов по цельсию")
        self.engine.say("Влажность составляет " + str(self.humidity) + "%")
        self.engine.say("Скорость ветра " + str(self.w.wind()['speed']) + " метров в секунду")
        print("В городе " + str(self.place) + " сейчас " + str(self.status))
        print("Температура " + str(round(self.temp)) + " градусов по цельсию")
        print("Влажность составляет " + str(self.humidity) + "%")
        print("Скорость ветра " + str(self.w.wind()['speed']) + " метров в секунду")
        if self.temp < 0:
            self.engine.say("Сегодня очень холодно, одевайте куртку")
            print("Сегодня очень холодно, одевайте куртку")
        elif self.temp < 10:
            self.engine.say("Сегодня холодно, одевайтесь теплее")
            print("Сегодня холодно, одевайтесь теплее")
        elif self.temp > 20:
            self.engine.say("Сегодня тепло можете одеваться легко")
            print("Сегодня тепло можете одеваться легко")
        elif self.temp < 19:
            self.engine.say("На улице прохладно, рекомендую одеть ветровку")
            print("На улице прохладно, рекомендую одеть ветровку")
        if str(self.status) == "дождь":
            self.engine.say("Возьмите с собой зонтик")
            print("Возьмите с собой зонтик")

    def brows(self):  # открывает браузер
        webbrowser.open('https://google.com')
        self.engine.say("Браузер открыт!")

    def howyou(self):
        self.engine.say("Всегда готова к работе!")

    def arz(self):
        self.engine.say("Аризона лаунчер открыт")
        os.system('G:/games/ARIZONA GAMES/arizona-starter.exe')

    def ovk(self):  # открывает вк
        self.engine.say("Вконтакте открыто")
        webbrowser.open('https://vk.com/feed')

    def youtube(self):  # открывает ютюб
        self.engine.say("Youtube открыт")
        webbrowser.open('https://www.youtube.com')

    def timethis(self):  # время
        now = datetime.datetime.now()
        self.engine.say("Сейчас " + str(now.hour) + ":" + str(now.minute))
        print("Сейчас " + str(now.hour) + ":" + str(now.minute))

    def shut(self):  # выключает компьютер
        self.engine.say('До скорых встреч!')
        os.system('shutdown /s /f /t 10')
        self.quite()

    def music(self):  # включает музыку
        self.is_not_used()
        k = ['https://www.youtube.com/watch?v=UkSr9Lw5Gm8&t=0s', 'https://www.youtube.com/watch?v=YlsQ6hjSZ8A&t=0s',
             'https://www.youtube.com/watch?v=bcyvZIoQp9A&t=0s', 'https://www.youtube.com/watch?v=eQxmhqaR2OA&t=0s']
        webbrowser.open(random.choice(k))

    def check_translate(self):
        text = ''
        tr = 0
        variants = ['переведи', 'перевести', 'переводить', 'перевод']
        for i in variants:
            if (i in text) & (tr == 0):
                text = ''
                word = text
                word = word.replace('переведи', '').strip()
                word = word.replace('перевести', '').strip()
                word = word.replace('переводить', '').strip()
                word = word.replace('перевод', '').strip()
                word = word.replace('слово', '').strip()
                word = word.replace('слова', '').strip()
                webbrowser.open('https://translate.google.ru/#view=home&op=translate&sl=auto&tl=ru&text={}'
                                .format(word))
                tr = 1
                text = ''
                k = ['Вот что мне удалось найти', 'Вот что я нашла по вашему запросу']
                self.engine.say(random.choice(k))

    # распознавание

    def talk(self):
        text = ''
        print('Я вас слушаю: ')
        with sr.Microphone() as sourse:
            self.r.adjust_for_ambient_noise(sourse)
            audio = self.r.listen(sourse, phrase_time_limit=5)
            try:
                text = (self.r.recognize_google(audio, language="ru-RU")).lower()
            except sr.UnknownValueError:
                pass
            except TypeError:
                pass
            os.system('cls')
            print(text)
            self.clear_task(text)
            return text

    # выполнение команд

    def cmd_exe(self):
        text = ''
        cmds = {
            'привет': self.hello,
            ('выруби компьютер', 'выключай компьютер', 'выключи комп', 'выключи компьютер'): self.shut,
            ('подбрось монетку', 'подкинь монетку', 'кинь монетку'): self.monetka,
            ('найди', 'найти', 'ищи', 'кто такой'): self.web_search,
            ('как дела', 'как жизнь', 'как настроение', 'как ты'): self.howyou,
            ('открой viber', 'включи viber', 'открывай viber'): self.viber,
            ('открой лаунчер аризоны', 'запусти лаунчер аризоны', 'запускай лаунчер аризоны'): self.arz,
            ('включай лаунчер аризоны', 'заходи на аризону', 'включай аризону'): self.arz,
            ('пока', 'вырубись', 'отключись'): self.quite,
            'покажи список команд': self.show_cmds,
            ('открой браузер', 'открой интернет'): self.brows,
            'открой youtube': self.youtube,
            ('открой vk', 'включи vk'): self.ovk,
            ('открой музыку', 'включи музон', 'вруби музыку'): self.music,
            ('крути винилы', 'крути винил'): self.vinil,
            ('планы', 'на будущее', 'что планируется'): self.plans,
            'переведи': self.check_translate,
            ('текущее время', 'сколько времени', 'сколько время', 'сейчас времени', 'который час'): self.timethis,
            ('какая погода', 'погода', 'погода на улице', 'какая погода на улице'): self.weather_pogoda,
            ('открой протокол разработки', 'протокол разработки'): self.protocol,
        }
        self.check_translate()
        self.web_search(),
        text = self.comparison(self, text)
        print(text)
        if text in cmds:
            if (text != 'привет') & (text != 'пока') & (text != 'покажи список команд') \
                    & (text != 'текущее время') & (text != 'сколько времени') \
                    & (text != 'сколько время') & (text != 'сейчас времени') & (text != 'который час') \
                    & (text != 'планы') & (text != 'какая погода') \
                    & (text != 'как дела') & (text != 'как жизнь') & (text != 'как настроение') & (text != 'как ты')\
                    & (text != 'погода') & (text != 'погода на улице') & (text != 'какая погода на улице'):
                k = ['Секундочку', 'Сейчас сделаю', 'уже выполняю']
                self.engine.say(random.choice(k))
            cmds[text]()
        elif text == '':
            pass
        else:
            print('Команда не найдена!')
        self.task_number += 1
        if self.task_number % 10 == 0:
            self.engine.say('У вас будут еще задания?')

        self.engine.runAndWait()
        self.engine.stop()

    # исправляет цвет

    print(Fore.YELLOW + '', end='')
    os.system('cls')
    # основной бесконечный цикл

    def main(self):
        text = ''
        try:
            self.talk()
            if text != '':
                self.cmd_exe()
                self.talk()
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
    morgan = Assistant()
    morgan.main()
