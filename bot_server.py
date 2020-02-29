#
# This is a server file for the bot.
# Run this file and send a message the following message to the bot that is configured in the telegram_config.cfg
#       Message: /mychatid
# The bot will reply to your message with the Chat ID, this means the bot is running and working properly.
# You can add additional commands to the bottom of this file
#

from bot import telegram_chatbot
import os
import re
import os.path
from os import path
from shutil import copyfile

basePath = os.path.dirname(os.path.abspath(__file__))
chatids_index_file = basePath + '/telegram_chatids.index'

# Check if chat ids indexing file exists, if not create a file... This file has been .ignored
if path.exists(chatids_index_file) == False:
    # Create a copy from the sample file
    open(chatids_index_file, 'a').close()

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

bot = telegram_chatbot(basePath + "/telegram_config.cfg")

update_id = None

print("Bot is listening...")

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
                
                # Send welcome message
                bot.send_message("This is awkward.. This suppose to be the website message.", from_)

            else:

                # Check for command
                command = get_command(message)

                # Check if command is not empty
                if command is not None:
                    
                    # Send Telegram Chat ID
                    if command[0] == '/mychatid':

                        # Send Telegram Chat ID
                        bot.send_message("Your chat ID is " + str(from_), from_)

                    # Inform sender that it was not a valid command
                    else:
                        
                        bot.send_message("You must be crazy. You know I am a bot and I am stupid. LOL! ", from_)

                # If command is not set, then notify that bot is dum
                else:
                    bot.send_message("Whoops! I am not sure what you meant", from_)
                    
                
