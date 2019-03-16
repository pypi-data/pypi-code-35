__author__ = ('Imam Omar Mochtar', ('iomarmochtar@gmail.com',))

import subprocess

class Utils(object):

    @staticmethod
    def runCmd(command):
        return subprocess.Popen(
            command, universal_newlines=True, shell=True,
            stdout=subprocess.PIPE, stderr=subprocess.PIPE).communicate()

    @staticmethod
    def chat_id(update):
        """
        wrapper to get chat id from conversation
        """
        return update.message.chat_id

    @staticmethod
    def user_details(update):
        """
        wrapper to get sender's information 
        """
        return update.message.from_user

    @staticmethod
    def is_group(update):
        """
        wrapper to get to check wether message comes from group or not 
        """
        return update.message.chat.type == 'group' 
        #return update.message.chat.title

    @staticmethod   
    def send(bot, update, text, chat_id=None, reply=False, **kwargs):
        chat_id = chat_id if chat_id else Utils.chat_id(update)
        # set to reply conversation if needed
        if reply:
            kwargs['reply_to_message_id'] = update.message.message_id
        bot.sendMessage(chat_id=chat_id, text=text, **kwargs)

    @staticmethod
    def send_doc(bot, update, path, filename, chat_id=None):
        """
        send document file 
        """
        chat_id = chat_id if chat_id else Utils.chat_id(update)
        bot.sendDocument(chat_id=chat_id, document=open(path, 'rb'), filename=filename)
