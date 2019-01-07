from discord import Discord
from flask import Flask, request
from trello import TrelloClient


app = Flask(__name__)
discord = Discord('DISCORD_TOKEN', 'CHANNEL_ID')
trello_client = TrelloClient(api_key='TRELLO_API_KEY',
                             api_secret='TRELLO_API_SECRET',
                             token='TRELLO_TOKEN')

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
    trello_client.create_hook('CALLBACK_URL', 'MODEL_ID')
    app.run(host="0.0.0.0", port=1337)
