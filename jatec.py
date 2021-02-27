import requests
import vk_api
import random
import time
import re
import sqlite3
import unicodedata
from vk_api.utils import get_random_id
from vk_api.bot_longpoll import VkBotLongPoll, VkBotEventType


vk = vk_api.VkApi(token="288a049bde237888b0eaaedaf76d0c9020b2e349181ab64825d8c10d3d4f9e8da4f85351e6394b33f8d08")
vk._auth_token()
vk.get_api()
longpoll = VkBotLongPoll(vk, 192963552)

#Пикчи
kap = ['photo-192963552_457239028', 'photo-192963552_457239029', 'photo-192963552_457239037']
ziga = ['photo-192963552_457239027', 'photo-192963552_457239026', 'photo-192963552_457239054', 'photo-192963552_457239053']
kurwab = ['photo-192963552_457239034', 'photo-192963552_457239024']
bent = ['photo-192963552_457239022', 'photo-192963552_457239033', 'photo-192963552_457239041', 'photo-192963552_457239045']
gitler = ['photo-192963552_457239040', 'photo-192963552_457239039', 'photo-192963552_457239038', 'photo-192963552_457239036', 'photo-192963552_457239049', 'photo-192963552_457239064']
cho = ['photo-192963552_457239044']
jatecky = ['photo-192963552_457239058', 'photo-192963552_457239059', 'photo-192963552_457239060']
photo_levak = ['photo-192963552_457239063']


#Массивы
k = ['kappa', 'каппа']
Kurwabot = [':sw:', 'курва', 'шатлворт', 'kurwa']
Hohol = ['ï']
O = ['0/', 'o/', 'о/']
gnul = ['гну', 'сру', 'gnu']
hitler = ['гитлер', 'hitler']
shock = ['шок', 'срыв покровов']
sticker = ['киев', 'kiev', 'украина']
pravda = ['правда что', 'правда, что']
levak = ['совок', 'коммунист', 'гомунизд', 'левак', 'левый', 'ссcр']
pukich = ['puk', 'пук']
kick = ['@all', '@online']


help = """
            #List_of_commands:
            #Picture
                -- kappa | каппа
                -- гну | сру | gnu
                -- шок | срыв | покровов
                -- 0/ | o/(eng) | о/(ru)
                -- ï
                -- :sw: | курва | kurwa | шатлворт
                -- гитлер | hitler
                -- киев | kiev | украина
                -- совок | коммунист | ссср
            #Сommand
                -- Правда что <text>
                -- Кубик
            #Admin_command
                -- +ban @id
                -- -ban @id
                -- +shield @id
            """

commands = [ ['puk_man', 'puk', 'пук'], 'шо']
commands_ban = []
counts_command = []
old_tick_command = []
new_tick_command = []

def create_counts_command():
    for command in commands:
        counts_command.append(0)
        new_tick_command.append(time.perf_counter())
        old_tick_command.append(time.perf_counter())

def processing_command(_command):
    ret = 'null'
    try:
        is_if = True
        command = ''
        index = 0
        for c_m in commands:
            if type(c_m) == list:
                if _command in c_m:
                    command = c_m[0]
                    is_if = False
                    break
            elif c_m == _command:
                command = c_m
                is_if = False
                break
            index += 1
        if is_if:
            return ret
        upd_old_tick = True
        new_tick_command[index] = time.perf_counter()
        tick = new_tick_command[index] - old_tick_command[index]
        if command in commands_ban:
            if tick > 10:
                commands_ban.remove(command)
                ret = 'unban_' + command
            else:
                upd_old_tick = False
        elif tick < 20:
            counts_command[index] += 1
            if counts_command[index] == 6:
                commands_ban.append(command)
                counts_command[index] = 0
                ret = 'ban_' + command
        elif tick > 30:
            counts_command[index] = 0
        if upd_old_tick:
            old_tick_command[index] = time.perf_counter()
    except ValueError:
        return
    return ret

create_counts_command()


conn = sqlite3.connect("jatecky.sqlite")
cursor = conn.cursor()

cursor.execute('''CREATE TABLE IF NOT EXISTS osn(
user_id INTEGER)
''')

cursor.execute('''CREATE TABLE IF NOT EXISTS admin(
user_id INTEGER)
''')

cursor.execute('''CREATE TABLE IF NOT EXISTS blacklist(user_id INTEGER,
admin_id INTEGER)''')

cursor.execute('CREATE TABLE IF NOT EXISTS whitelist(user_id INTEGER)')

def check_to_admin(admin_id):
     cursor.execute('SELECT * FROM admin WHERE user_id=' + str(admin_id))
     ret = True
     if not cursor.fetchone():
          ret = False
     return ret

def add_to_admin(admin_id):
     ret = 'added'
     if not check_to_admin(admin_id):
          cursor.execute("INSERT INTO admin VALUES(%s)" % (admin_id))
          conn.commit()
          ret = 'add'
     return ret

def check_to_osn(osn_id):
     cursor.execute('SELECT * FROM osn WHERE user_id=' + str(osn_id))
     ret = True
     if not cursor.fetchone():
          ret = False
     return ret

def add_to_osn(osn_id):
     ret = 'added'
     if not check_to_osn(osn_id):
          cursor.execute("INSERT INTO osn VALUES(%s)" % (osn_id))
          conn.commit()
          ret = 'add'
     return ret


def check_to_whitelist(user_id):
     cursor.execute('SELECT * FROM whitelist WHERE user_id=' + str(user_id))
     ret = True
     if not cursor.fetchone():
          ret = False
     return ret

def check_to_blacklist(user_id):
     cursor.execute('SELECT user_id FROM blacklist WHERE user_id=' + str(user_id))
     ret = True
     if not cursor.fetchone():
          ret = False
     return ret

def add_to_whitelist(user_id):
     ret = 'added'
     if not check_to_whitelist(user_id):
          cursor.execute("INSERT INTO whitelist VALUES(%s)" % (user_id))
          conn.commit()
          ret = 'add'
     return ret

def add_to_blacklist(user_id,admin_id):
     ret = 'whitelist'
     if not check_to_whitelist(user_id):
          ret = 'added'
          if not check_to_blacklist(user_id):
               cursor.execute("INSERT INTO blacklist VALUES(%s, %s)" % (user_id,
                                                                        admin_id))
               conn.commit()
               ret = 'add'
     return ret

def delete_from_blacklist(user_id):
    ret = 'outed'
    if check_to_blacklist(user_id):
        cursor.execute("DELETE FROM blacklist WHERE user_id=" + str(user_id))
        conn.commit()
        ret = 'out'
    return ret

def delete_from_whitelist(user_id):
    ret = 'outed'
    if check_to_whitelist(user_id):
        cursor.execute("DELETE FROM whitelist WHERE user_id=" + str(user_id))
        conn.commit()
        ret = 'out'
    return ret

def delete_from_admin(admin_id):
    ret = 'outed'
    if not check_to_admin(admin_id):
        cursor.execute("DELETE FROM admin WHERE user_id" + str(admin_id))
        conn.commit()
        ret = 'out'
    return ret

print("puk")
while True:
    try:
        for event in longpoll.listen():
            if event.type == VkBotEventType.MESSAGE_NEW:
                if event.object.peer_id != event.object.from_id and not check_to_blacklist(event.object.from_id):
                    s = event.object.text.lower()
                    admin_id = event.object.from_id
                    osn_id = event.object.from_id
                    p_c = processing_command(s)
                    if p_c == 'ban_puk_man':
                        vk.method("messages.send", {"peer_id": event.object.peer_id, "message": 'command banned for 10 sec',
                                            "random_id": 0})
                    elif p_c == 'unban_puk_man':
                        vk.method("messages.send", {"peer_id": event.object.peer_id, "message": 'commands unbanned',
                                            "random_id": 0})
                    if 'puk_man' not in commands_ban:
                        if s == 'puk':
                            vk.method("messages.send", {"peer_id": event.object.peer_id, "message": event.object.text,
                                                        "random_id": 0})
                        if s == 'пук':
                            vk.method("messages.send", {"peer_id": event.object.peer_id, "message": event.object.text,
                                                        "random_id": 0})
                    if event.object.text.lower() == 'дарья кто?':
                        vk.method("messages.send", {"peer_id": event.object.peer_id, "message": "самая крутая тян у которой все получица в жизни рэально, с днем рождения ее!=))",
                                            "random_id": 0})
                    if p_c == 'ban_шо':
                        vk.method("messages.send", {"peer_id": event.object.peer_id, "message": 'command banned for 10 sec',
                                            "random_id": 0})
                    elif p_c == 'unban_шо':
                        vk.method("messages.send", {"peer_id": event.object.peer_id, "message": 'command unbanned',
                                            "random_id": 0})
                    if s == 'шо' and 'шо' not in commands_ban:
                        vk.method("messages.send", {"peer_id": event.object.peer_id, "message": '🐖',
                                            "random_id": 0})

                    if event.object.text.lower() == 'гачи борьба':
                        vk.method("messages.send", {"peer_id": event.object.peer_id, "message": "непонел",
                                            "random_id": 0})


                    if any(word in event.object.text.lower() for word in k):
                            vk.method("messages.send", {"peer_id": event.object.peer_id, "attachment": random.choice(kap),
                                                "random_id": 0})

                    if any(word in event.object.text.lower() for word in Kurwabot):
                        vk.method("messages.send", {"peer_id": event.object.peer_id, "attachment": random.choice(kurwab),
                                                "random_id": 0})

                    if any(word in event.object.text.lower() for word in Hohol):
                        vk.method("messages.send", {"peer_id": event.object.peer_id, "attachment": "photo-192963552_457239043",
                                                "random_id": 0})

                    if any(word in event.object.text.lower() for word in O):
                        vk.method("messages.send", {"peer_id": event.object.peer_id, "attachment": random.choice(ziga),
                                                "random_id": 0})

                    if any(word in event.object.text.lower() for word in gnul):
                        vk.method("messages.send", {"peer_id": event.object.peer_id, "attachment": random.choice(bent),
                                                "random_id": 0})

                    if any(word in event.object.text.lower() for word in hitler):
                        vk.method("messages.send", {"peer_id": event.object.peer_id, "attachment": random.choice(gitler),
                                                "random_id": 0})

                    if any(word in event.object.text.lower() for word in shock):
                        vk.method("messages.send", {"peer_id": event.object.peer_id, "attachment": "photo-192963552_457239021",
                                                "random_id": 0})

                    if any(word in event.object.text.lower() for word in sticker):
                        vk.method("messages.send", {"peer_id": event.object.peer_id, "attachment": "doc-192963552_544447845",
                                                "random_id": 0})

                    if any(word in event.object.text.lower() for word in levak):
                        vk.method("messages.send", {"peer_id": event.object.peer_id, "attachment": random.choice(photo_levak),
                                                "random_id": 0})

                    if event.object.text.lower() == '-help':
                        vk.method("messages.send", {"peer_id": event.object.peer_id, "message": help,
                                                "random_id": 0})

                    if event.object.text.lower() in ['жатец', 'jatec']:
                        vk.method("messages.send", {"peer_id": event.object.peer_id, "attachment": random.choice(jatecky),
                                                "random_id": 0})

                    if event.object.text.lower() in ['кубик']:
                        vk.method("messages.send", {"peer_id": event.object.peer_id, "message": "На кубике выпала цифра {0}.".format(str(random.randrange(1,6))),
                                                "random_id": 0})
########################################################################
                    n = 'правда что'
                    if n in s:
                        r = s.replace(n, '')
                        Sooth = ['Да, ' + str(r), 'Не, нихуя']
                        reply = random.choice(Sooth)
                        vk.method("messages.send", {"peer_id": event.object.peer_id, "message": reply,
                                                "random_id": 0})
########################################################################

########################################################################
                    sentence = event.object.text
                    def find_caps(str):
                        arrayUpperWords = str.split()
                        find_upper_case = re.compile(r'(?:[А-Я]+)\b')
                        h = []
                        for i in arrayUpperWords:
                            t = find_upper_case.findall(i)
                            if t:
                                h.append(t[0])
                        ret = False
                        for i in h:
                            if len(i) >= 8:
                                ret = True
                        return ret

                    if find_caps(sentence):
                        vk.method("messages.send", {"peer_id": event.object.peer_id, "attachment": "photo-192963552_457239025",
                                                "random_id": 0})
########################################################################

                    command = 'жатец съесть'
                    if s.find(command) == 0:
                        user = vk.method("users.get", {"user_ids": event.object.from_id})
                        fullname = user[0]['first_name'] +  ' ' + user[0]['last_name']
                        print(fullname)
                        vk.method("messages.send", {"peer_id": event.object.peer_id,
                                                "message": user[0]['first_name'] + " съел " + user[0]['first_name'], "random_id": 0})

                    command = '+ban'

                    if s.find(command) == 0:
                        if check_to_admin(admin_id):
                            id_from_ban_list = s.replace(command + ' [id', '').replace(']', '').split('|')
                            statusBan = add_to_blacklist(int(id_from_ban_list[0]), admin_id)
                            print(id_from_ban_list)
                            if statusBan == 'whitelist':
                                vk.method("messages.send", {"peer_id": event.object.peer_id, "message": "user protected",
                                                "random_id": 0})

                            elif statusBan == 'added':
                                vk.method("messages.send", {"peer_id": event.object.peer_id, "message": "user is already banned",
                                                "random_id": 0})
                            else:
                                vk.method("messages.send", {"peer_id": event.object.peer_id, "message": "user banned",
                                                "random_id": 0})
                        else:
                            vk.method("messages.send", {"peer_id": event.object.peer_id, "message": "fuck you, leatherman",
                                                "random_id": 0})

                    command = '-ban'

                    if s.find(command) == 0:
                        if check_to_admin(admin_id):
                            id_out_ban_list = s.replace(command + ' [id', '').replace(']', '').split('|')
                            statusB = delete_from_blacklist(int(id_out_ban_list[0]))
                            print(id_out_ban_list)
                            if statusB == 'outed':
                                vk.method("messages.send", {"peer_id": event.object.peer_id, "message": "user not listed",
                                                "random_id": 0})
                            else:
                                vk.method("messages.send", {"peer_id": event.object.peer_id, "message": "removed from the list",
                                                "random_id": 0})
                        else:
                            vk.method("messages.send", {"peer_id": event.object.peer_id, "message": "fuck you, leatherman",
                                                "random_id": 0})


                    command = '+adm'

                    if s.find(command) == 0:
                        if check_to_osn(osn_id):
                            id_from_admin_list = s.replace(command + ' [id', '').replace(']', '').split('|')
                            statusAdm = add_to_admin(int(id_from_admin_list[0]))
                            print(id_from_admin_list)
                            if statusAdm == 'added':
                                vk.method("messages.send", {"peer_id": event.object.peer_id, "message": "already admin",
                                                "random_id": 0})
                            else:
                                vk.method("messages.send", {"peer_id": event.object.peer_id, "message": "gave adminka",
                                                "random_id": 0})
                        else:
                            vk.method("messages.send", {"peer_id": event.object.peer_id, "message": "fuck you, leatherman",
                                                "random_id": 0})

                    command = '-adm'

                    if s.find(command) == 0:
                        if check_to_osn(osn_id):
                            id_out_admin_list = s.replace(command + ' [id', '').replace(']', '').split('|')
                            statusAdm = add_to_admin(int(id_out_admin_list[0]))
                            print(id_out_admin_list)
                            if statusAdm == 'outed':
                                vk.method("messages.send", {"peer_id": event.object.peer_id, "message": "this user not admin",
                                                "random_id": 0})
                            else:
                                vk.method("messages.send", {"peer_id": event.object.peer_id, "message": "removed from the list of admins",
                                                "random_id": 0})
                        else:
                            vk.method("messages.send", {"peer_id": event.object.peer_id, "message": "fuck you, leatherman",
                                                "random_id": 0})




                    command = '+shield'

                    if s.find(command) == 0:
                        if check_to_admin(admin_id):
                            id_from_white_list = s.replace(command + ' [id', '').replace(']', '').split('|')
                            statusDef = add_to_whitelist(int(id_from_white_list[0]))
                            print(id_from_white_list)
                            if statusDef == 'added':
                                vk.method("messages.send", {"peer_id": event.object.peer_id, "message": "user already protected",
                                                "random_id": 0})
                            else:
                                vk.method("messages.send", {"peer_id": event.object.peer_id, "message": "protected core",
                                                "random_id": 0})
                        else:
                            vk.method("messages.send", {"peer_id": event.object.peer_id, "message": "fuck you, leatherman",
                                                "random_id": 0})

                    command = '-shield'

                    if s.find(command) == 0:
                        if check_to_osn(osn_id):
                            id_out_white_list = s.replace(command + ' [id', '').replace(']', '').split('|')
                            statusW = delete_from_whitelist(int(id_out_white_list[0]))
                            print(id_out_white_list)
                            if statusW == 'outed':
                                vk.method("messages.send", {"peer_id": event.object.peer_id, "message": "user not listed",
                                                "random_id": 0})
                            else:
                                vk.method("messages.send", {"peer_id": event.object.peer_id, "message": "removed from the list",
                                                "random_id": 0})
                        else:
                            vk.method("messages.send", {"peer_id": event.object.peer_id, "message": "fuck you, leatherman",
                                                "random_id": 0})

                    command = '+osn'

                    if s.find(command) == 0:
                        if check_to_osn(osn_id):
                            print(check_to_osn)
                            id_from_osn_list = s.replace(command + ' [id', '').replace(']', '').split('|')
                            statusOsn = add_to_osn(int(id_from_osn_list[0]))
                            print(id_from_osn_list)
                            if statusOsn == 'added':
                                vk.method("messages.send", {"peer_id": event.object.peer_id, "message": "already osn",
                                                "random_id": 0})
                            else:
                                vk.method("messages.send", {"peer_id": event.object.peer_id, "message": "gave osnova",
                                                "random_id": 0})
                        else:
                            vk.method("messages.send", {"peer_id": event.object.peer_id, "message": "fuck you, leatherman",
                                                "random_id": 0})



                    if any(word in event.object.text.lower() for word in kick):
                            vk.method("messages.send", {"peer_id": event.object.peer_id, "message": "пошел нахуй, пидарас",
                                                    "random_id": 0})
                            user = vk.method("users.get", {"user_ids": event.object.from_id})
                            user_id = user[0]['id']
                            vk.method("messages.removeChatUser", {
                            "chat_id": event.object.peer_id - 2000000000,
                            "member_id": user_id})
                            print(user_id)

    except Exception as E:
        time.sleep(2)