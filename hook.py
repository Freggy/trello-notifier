import os
from discord import Discord
from flask import Flask, request
from trello import TrelloClient


DISCORD_API_TOKEN   = os.environ.get('DISCORD_API_TOKEN')
DISCORD_CHANNEL_ID  = os.environ.get('DISCORD_CHANNEL_ID')
TRELLO_API_KEY      = os.environ.get('TRELLO_API_KEY')
TRELLO_API_SECRET   = os.environ.get('TRELLO_API_SECRET')
TRELLO_API_TOKEN    = os.environ.get('TRELLO_API_TOKEN')
MODEL_ID            = os.environ.get('MODEL_ID')

app = Flask(__name__)
discord = Discord(DISCORD_API_TOKEN, DISCORD_CHANNEL_ID)
trello_client = TrelloClient(api_key=TRELLO_API_KEY,
                             api_secret=TRELLO_API_SECRET,
                             token=MODEL_ID)

template = """
    **Card ID:** {} \n 
    **Requester:** {} \n
    **Assignee:** {} \n
    **Description:** \n
    ```
    {}
    ```
    """


@app.route('/', methods=['POST'])
def callback():
    json = request.get_json()
    if json['action']['type'] == "updateCard":
        user = json['action']['memberCreator']['fullName']
        desc = json['action']['data']['card']['desc']
        card_id = json['action']['data']['card']['id']
        assingees = get_assignees(json['action']['data']['card']['idMembers'])
        discord.send_message(template.format(card_id, user, assignees, desc))
    return "200"


def get_assignees(member_ids):
    assignees = []
    for id in member_ids:
        assignees.append('@' + trello_client.get_member(id).full_name)
    if assignees: # List is not empty
        return ', '.join(str(a) for a in assignees)
    return " "


if __name__ == '__main__':
    trello_client.create_hook(TRELLO_API_KEY, MODEL_ID)
    app.run(host="0.0.0.0", port=1337)
