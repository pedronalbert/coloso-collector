import requests

from utils import API_KEY
from errors import RiotLimitError, RiotServerError

def getMatchTimeline(match, logger):
    logger.info('Fetching match timeline #{}'.format(match['gameId']))

    url = 'https://{}.api.riotgames.com/lol/match/v3/timelines/by-match/{}'.format(match['platformId'], match['gameId'])
    response = requests.get(url, params = { "api_key": API_KEY })

    if response.status_code == 200:
        logger.debug('Fetch Success')
        timeLines = response.json()

        return timeLines
    elif response.status_code == 429:
        retryAfter = int(response.headers['retry-after'])
        logger.warning('Fetch limit reached, retry after ' + str(retryAfter) + ' seconds')

        raise RiotLimitError(retryAfter)
    else:
        logger.warning('Fetch faled CODE: ' + str(response.status_code))
        raise RiotServerError