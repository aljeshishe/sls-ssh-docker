import requests


def notify(msg):
    apiToken = '5803765903:AAH2ayWpVcook4JpoiHvMzgOvJCjsLItcmw'
    chatID = '99044115'
    apiURL = f'https://api.telegram.org/bot{apiToken}/sendMessage'

    response = requests.post(apiURL, json={'chat_id': chatID, 'text': msg})
    response.raise_for_status()
