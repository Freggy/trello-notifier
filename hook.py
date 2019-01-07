from discord import Discord
from flask import Flask, request
from trello import TrelloClient

app = Flask(__name__)
discord = Discord('DISCORD_TOKEN', 'CHANNEL_ID')
trello_client = TrelloClient(api_key='TRELLO_API_KEY',
                             api_secret='TRELLO_API_SECRET',
                             token='TRELLO_TOKEN')

@app.route('/', methods=['POST'])
def callback():
    json = request.get_json()
    if json['action']['type'] == "updateCard":
        user = json['action']['memberCreator']['fullName']
        desc = json['action']['data']['card']['desc']
        s = "> UPLOAD REQUEST < \n\n **Requester:** {} \n **Description:** \n {}".format(user, desc)
        discord.send_message(s)
    return "200"

if __name__ == '__main__':
    trello_client.create_hook('CALLBACK_URL', 'MODEL_ID')
    app.run(host="0.0.0.0", port=1337)
