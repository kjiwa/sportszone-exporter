"""A Team Cowboy API client."""

import hashlib
import httplib
import json
import random
import sys
import time
import urllib


class TeamCowboyException(Exception):
  """A Team Cowboy error."""
  pass


class TeamCowboy(object):
  """A Team Cowboy API client."""

  def __init__(self, public_key, private_key):
    """Creates a new client.

    Args:
      public_key: The API public key.
      private_key: The API private key.
    """
    self._public_key = public_key
    self._private_key = private_key
    self._host = 'api.teamcowboy.com'
    self._path = '/v1/'

  def auth_get_user_token(self, username, password):
    """Gets an authentication token for the given user.

    Args:
      username: The username.
      password: The password.

    Returns:
      An authentication token for the given user.
    """
    params = {
        'username': username,
        'password': password
    }

    return self._send('POST', 'Auth_GetUserToken', params, True)

  def test_get_request(self, test_param=''):
    """Sends a GET request to the test endpoint.

    Args:
      test_param: An optional string to send.

    Returns:
      A dict containing a 'helloWorld' attribute and, optionally, a 'testParam'
      attribute.
    """
    params = {'testParam': test_param}
    return self._send('GET', 'Test_GetRequest', params)

  def test_post_request(self, test_param=''):
    """Sends a POST request to the test endpoint.

    Args:
      test_param: An optional string to send.

    Returns:
      A dict containing a 'helloWorld' attribute and, optionally, a 'testParam'
      attribute.
    """
    params = {'testParam': test_param}
    return self._send('POST', 'Test_PostRequest', params)

  def user_get_teams(self, user_token, dashboard_teams_only=False):
    params = {
        'userToken': user_token['token'],
        'dashboardTeamsOnly': '1' if dashboard_teams_only else '0'
    }

    return self._send('GET', 'User_GetTeams', params)

  def team_get_events(
      self, user_token, team_id, season_id=None, filter_type='future',
      start_date_time=None, end_date_time=None, offset=0, qty=10,
      include_rsvp_info=False):
    """Gets a list of events for a given team.

    Args:
      user_token: The user's auth token.
      team_id: The team ID.
      season_id: The season ID.
      filter_type: The search filter type.
      start_date_time: The start date from when to search.
      end_date_time: The end date until when to search.
      offset: The event offset.
      qty: The number of games to fetch.
      include_rsvp_info: Whether to include RSVP info.

    Returns:
      A list of events matching the given criteria.
    """
    params = {
        'userToken': user_token['token'],
        'teamId': str(team_id),
        'seasonId': str(season_id) if season_id else '',
        'includeRSVPInfo': 'true' if include_rsvp_info else '',
        'filter': filter_type,
        'startDateTime': start_date_time if start_date_time else '',
        'endDateTime': end_date_time if end_date_time else '',
        'offset': str(offset),
        'qty': str(qty)
    }

    return self._send('GET', 'Team_GetEvents', params)

  def _send(self, http_method, tc_method, params, use_https=False):
    """Prepares and sends a request to Team Cowboy.

    Args:
      http_method: The HTTP method to use.
      tc_method: The Team Cowboy method name.
      params: The method parameters.
      use_https: Whether to use HTTPS.

    Returns:
      A dict with response data.

    Raises:
      TeamCowboyException: When an error is returned.
    """
    params.update({
        'api_key': self._public_key,
        'method': tc_method,
        'timestamp': str(int(time.time())),
        'nonce': str(self._generate_nonce())
    })

    params['sig'] = self._generate_signature(params, http_method)
    data = urllib.urlencode(params)

    if use_https:
      http = httplib.HTTPSConnection(self._host)
    else:
      http = httplib.HTTPConnection(self._host)

    if http_method == 'POST':
      headers = {'Content-Type': 'application/x-www-form-urlencoded'}
      http.request(http_method, self._path, data, headers)
    else:
      http.request(http_method, '%s?%s' % (self._path, data))

    response = http.getresponse()
    result = json.loads(response.read())
    http.close()

    body = result['body']
    if 'error' in body:
      raise TeamCowboyException(body)

    return body

  def _generate_nonce(self):
    """Generates a one-time-use number.

    Team Cowboy allows any value, so long as it is unique (it is unclear how
    uniqueness is defined).

    Returns:
      A one-time-use number.
    """
    return random.randint(10000000, sys.maxint)

  def _generate_signature(self, params, method):
    """Generates a request signature.

    Args:
      params: A dict of request parameters.
      method: The HTTP method of the request.

    Returns:
      A signature for the HTTP request.
    """

    encoded = [
        '%s=%s' % (urllib.quote(i).lower(), urllib.quote(params[i]).lower())
        for i in sorted(params)]

    s = '%s|%s|%s|%s|%s|%s' % (
        self._private_key, method, params['method'], params['timestamp'],
        params['nonce'], '&'.join(encoded))

    return hashlib.sha1(s).hexdigest().lower()
