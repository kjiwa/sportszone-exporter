"""A Sportszone client.

Given a Sportszone URL, the client will scrape the site for team and scheduling
information.
"""

import collections
import requests
import time
from lxml import etree
from lxml import html

Game = collections.namedtuple(
    'Game', ['game_datetime', 'arena', 'home_away', 'opponent'])

class SportszoneException(Exception):
  """An exception thrown by the Sportszone client."""

  def __init__(self, cause):
    """Creates a new Sportszone exception.

    Args:
      cause: The causing exception.
    """
    self._cause = cause

  def __str__(self):
    """Returns a string representation of the exception.

    Returns:
      A string representation of the exception.
    """
    return repr(self._cause)

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
    """
    url = ('%s?LeagueID=%d&TeamID=%d&SeasonID=%d&Page=Teams&Section=Schedule'
           % (self._base_url, self._league_id, team_id, season_id))

    try:
      page = requests.get(url)
    except Exception, e:
      raise SportszoneException(e)

    tree = html.fromstring(page.text)

    result = []
    rows = tree.xpath('//table[@class="text11"]/tbody/tr')
    for row in rows:
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
