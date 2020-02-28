from bot import telegram_chatbot
import os
import re

basePath = os.path.dirname(os.path.abspath(__file__))
chatids_index_file = basePath + '/chatids.index'

def write_chatid( chat_id ):
    with open(chatids_index_file, 'a') as chatids_file:
        chatids_file.write(str(chat_id) + ":")
    chatids_file.close()

def read_chatid(chat_id):
    with open(chatids_index_file, 'r') as chatids_file:
        c = chatids_file.read()
        c = c[:-1]
    chatids_file.close()

    s = c.split(':')

    if str(chat_id) in s:
        return True
    return False

def get_all_other_chat_ids(chat_id):
    with open(chatids_index_file, 'r') as chatids_file:
        c = chatids_file.read()
        c = c[:-1]
    chatids_file.close()

    s = c.split(':')

    if str(chat_id) in s:
        s.remove(str(chat_id))

    return s

# Get Command from string
def get_command(string):
    p = re.compile('/[a-z]+')
    s = re.findall(p, string)
    if s:
        return [s[0], string.replace(s[0],'')]
    return None

bot = telegram_chatbot(basePath + "/config.cfg")

update_id = None

print("VCP bot in running")

while True:
    updates = bot.get_updates(offset=update_id)
    updates = updates["result"]
    if updates:
        for item in updates:
            
            update_id = item["update_id"]

            try:
                message = str(item["message"]["text"])
            except:
                message = None

            from_ = item["message"]["from"]["id"]

            # Record Chat ID
            if read_chatid(from_) == False:
                write_chatid(from_)

            # Check for /start command
            if message == '/start':
            
                bot.send_message("Welcome, please inform me if there is a VCP. If anyone else inform me I will let you know.", from_)

            else:

                # Check for command
                command = get_command(message)

                # Check if command is not empty
                if command is not None:

                    if command[0] == '/reportvcp':

                        # Check for the location
                        if command[1] == '':

                            # Send a notification
                            bot.send_message("Whoops! Seems like you forgot to mention the location. Try again.", from_)
                        
                        else:
                            
                            # Send thank you message
                            bot.send_message("Thank you. I\'ll inform everyone else.", from_)

                            # Alert all others
                            for p in get_all_other_chat_ids(from_):
                                bot.send_message("There might be a VCP at \n" + command[1], p)

                # If command is not set, then notify that bot is dum
                else:
                    bot.send_message("Whoops! I am not sure what you meant", from_)
                    
                
