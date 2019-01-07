import requests
import json


class Discord():
    def __init__(self, token, channel_id):
        self.channel_id = channel_id
        self.header = {
            "Authorization": "Bot {}".format(token),
            "User-Agent": "LUXOR",#
            "Content-Type": "application/json",
        }

    def send_message(self, message):
        baseURL = "https://discordapp.com/api/channels/{}/messages".format(self.channel_id)
        r = requests.post(baseURL, headers=self.header, data=json.dumps({"content":message}))

   def mark_finished():
