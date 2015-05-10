"""A script that generates a CSV file of games to import into Team Cowboy."""

import csv
import datetime
import gflags
import pytz
import pytz.reference
import sportszone
import sys
import time
import translator

FLAGS = gflags.FLAGS

gflags.DEFINE_string('sportszone_url', None, 'The base Sportszone URL.')
gflags.DEFINE_integer('league_id', None, 'The Sportszone league ID.')
gflags.DEFINE_integer('team_id', None, 'The Sportszone team ID.')
gflags.DEFINE_integer('season_id', None, 'The Sportszone season ID.')
gflags.DEFINE_string('output_file', 'schedule.csv', 'The output file.')
gflags.DEFINE_string('home_color', 'White', 'The color of the home jerseys.')
gflags.DEFINE_string('away_color', 'Black', 'The color of the away jerseys.')

def _precondition(cond, msg):
  """Asserts the truth of a precondition or fails.

  Args:
    cond: The result of the precondition test.
    msg: A message to display upon failure.
  """
  if not cond:
    sys.stderr.write(msg)
    sys.exit(1)

def _tz():
  """Returns the local timezone, formatted for import into Team Cowboy.

  Team Cowboy does not specify the exact format it prefers for timezones and
  some values do not work such as 'America/Dawson' or 'US/Pacific-New'. For now
  we restrict the set to those timezone names starting with 'US/' and keep the
  first value we see.

  Returns:
    A formatted timezone string.
  """
  result = {}
  for tz in pytz.all_timezones:
    tz = pytz.timezone(tz)
    key = tz.localize(datetime.datetime.now()).strftime('%Z')
    if str(tz).startswith('US/') and key not in result:
      result[key] = tz

  return result[pytz.reference.LocalTimezone().tzname(datetime.datetime.now())]

def _write_csv(games, interpreter):
  """Writes a list of games to a CSV file suitable for importing to Team Cowboy.

  Args:
    games: A list of games to write.
    interpreter: A translator for mapping values between Sportszone and Team
        Cowboy.
  """
  with open(FLAGS.output_file, 'wb') as csvfile:
    writer = csv.writer(csvfile, delimiter='\t')
    writer.writerow([
        'Event Type', 'Start Date', 'Start Time', 'End Date', 'End Time',
        'Timezone ID', 'Home or Away', 'Opponent/Event Title', 'Location Name',
        'Shirt Color', 'Opponent Shirt Color', 'Allow RSVPs', 'Send Reminders',
        'Notes/Comments'
    ])

    allow_rsvps = 'Yes'
    event_type = 'game'
    notes_comments = ''
    send_reminders = 'Yes'
    timezone = _tz()

    for game in games:
      dt = datetime.datetime.fromtimestamp(time.mktime(game.game_datetime))
      start_date = dt.strftime('%Y-%m-%d')
      start_time = dt.strftime('%I:%M %p')

      dt += datetime.timedelta(hours=1)
      end_date = dt.strftime('%Y-%m-%d')
      end_time = dt.strftime('%I:%M %p')

      home_away = game.home_away.title()
      arena = interpreter.arena.get(game.arena, game.arena)

      if game.home_away is 'HOME':
        shirt_color = FLAGS.home_color
        opponent_shirt_color = FLAGS.away_color
      else:
        shirt_color = FLAGS.away_color
        opponent_shirt_color = FLAGS.home_color

      writer.writerow([
          event_type, start_date, start_time, end_date, end_time, timezone,
          home_away, game.opponent, arena, shirt_color.title(),
          opponent_shirt_color.title(), allow_rsvps, send_reminders,
          notes_comments
      ])

def main(argv):
  try:
    argv = FLAGS(argv)
  except gflags.FlagsError, e:
    print '%s\\nUsage: %s ARGS\\n%s' % (e, sys.argv[0], FLAGS)
    sys.exit(1)

  _precondition(FLAGS.sportszone_url, 'A Sportszone URL is required.')
  _precondition(FLAGS.league_id, 'A Sportszone league ID is required.')
  _precondition(FLAGS.team_id, 'A Sportszone team ID is required.')
  _precondition(FLAGS.season_id, 'A Sportszone season ID is required.')

  sz = sportszone.Sportszone(FLAGS.sportszone_url, FLAGS.league_id)
  games = sz.get_schedule(FLAGS.team_id, FLAGS.season_id)
  interpreter = translator.load(FLAGS.league_id)

  _write_csv(games, interpreter)

if __name__ == '__main__':
  main(sys.argv)
