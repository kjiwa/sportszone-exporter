"""A Sportszone client.

Given a Sportszone URL, the client will scrape the site for team and scheduling
information.
"""

import collections
import httplib
import time
import urlparse
from lxml import html

Game = collections.namedtuple(
    'Game', ['game_datetime', 'arena', 'home_away', 'opponent'])


class SportszoneException(Exception):
  """An exception thrown by the Sportszone client."""
  pass


class Sportszone(object):
  """A Sportszone client."""

  def __init__(self, base_url, league_id):
    """Creates a new Sportszone client.

    Args:
      base_url: The base URL.
      league_id: The league ID.
    """
    self._base_url = base_url
    self._league_id = league_id

  def get_schedule(self, team_id, season_id):
    """Gets a team schedule from Sportszone for a given season.

    Args:
      team_id: The team ID.
      season_id: The season ID.

    Returns:
      A list of games posted on a team's schedule.

    Raises:
      SportszoneException: Raised when there is an error reading the Sportszone
          schedule.
    """
    parsed = urlparse.urlparse(
        '%s?LeagueID=%d&TeamID=%d&SeasonID=%d&Page=Teams&Section=Schedule'
        % (self._base_url, self._league_id, team_id, season_id))

    if parsed.scheme == 'http':
      http = httplib.HTTPConnection(parsed.netloc)
    else:
      http = httplib.HTTPSConnection(parsed.netloc)

    http.request('GET', '%s?%s' % (parsed.path, parsed.query))
    response = http.getresponse()
    if response.status != 200:
      http.close()
      raise SportszoneException('Error retreiving page.')

    tree = html.fromstring(response.read())
    http.close()

    result = []
    rows = tree.xpath('//table[@class="text11"]/tbody/tr')
    for row in rows:
      # The expected structure is:
      #   0. Game number
      #   1. Day
      #   2. Date (e.g. May 14, 2015)
      #   3. Time (e.g. 8:10 PM)
      #   4. Arena
      #   5. Home/Away
      #   6. Opponent
      #   7. Score
      #   8. Result
      #   9. Boxscore

      if len(row) != 10 or row[0][0].text == '#':
        continue

      game_datetime = time.strptime(
          '%s %s' % (row[2].text, row[3].text), '%b %d, %Y %I:%M %p')
      arena = row[4][0][0].text
      home_away = row[5][0].text
      opponent = row[6][0].text

      game = Game(game_datetime, arena, home_away, opponent)
      result.append(game)

    return result
