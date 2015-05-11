# Sportszone Schedule Exporter

## Overview

This tool scrapes schedule data from a Sportszone instance and exports it into a CSV suitable for uploading to Team Cowboy.

I've included a flagfile that can be used with the Greater Seattle Hockey League that contains the base URL, league ID, and arena map. Use it by specifying `--flagfile=gshl.flags` in your command line.

## Example

In most cases you will execute the exporter with a URL and a file containing a map of Sportszone and Team Cowboy arena names (e.g. [gshl.flags](gshl.flags)). The URL should be to a Sportszone schedule, e.g. [Amazon's winter 2014/2015 season](http://www.gshockey.com/site/3333/page.asp?Site=9941&page=Teams&LeagueID=9941&SeasonID=39&DivisionID=100&TeamID=470&Section=Schedule). Specifically, the URL must have values for LeagueID, TeamID, and SeasonID in its query parameters.

You can pass the arena names via the command line, but I find it more convenient to put them in a file that can be referenced by `--flagfile`, e.g. arenas.flags:

```
--arena_map=Castle=Castle Ice Arena
--arena_map=Kent=Kent Valley Ice Center
```

With these attributes we can run the exporter:

```
$ exporter --url="http://www.gshockey.com/site/3333/page.asp?Site=9941&page=Teams&LeagueID=9941&SeasonID=39&DivisionID=100&TeamID=470&Section=Schedule"
           --flagfile=arenas.flags
```

This will generate a file named schedule.csv in the current directory (this can be modified with the `--output_file` flag).

```
$ head -n5 schedule.csv
Event Type      Start Date      Start Time      End Date        End Time        Timezone ID     Home or Away    Opponent/Event Title    Location Name   Shirt Color     Opponent Shirt Color    Allow RSVPs     Send Reminders  Notes/Comments
game    2014-10-02      11:00 PM        2014-10-03      12:00 AM        US/Pacific      Home    Shockers        Castle Ice Arena        White   Black   Yes     Yes
game    2014-10-09      09:35 PM        2014-10-09      10:35 PM        US/Pacific      Home    GLY Construction        Castle Ice Arena        White   Black   Yes     Yes
game    2014-10-14      09:35 PM        2014-10-14      10:35 PM        US/Pacific      Away    Mustangs 2      Castle Ice Arena        Black   White   Yes     Yes
game    2014-10-21      09:50 PM        2014-10-21      10:50 PM        US/Pacific      Away    Acme    Lynnwood Ice Center     Black   White   Yes     Yes
```

## Usage

```
$ exporter --help 
A script that generates a CSV file of games to import into Team Cowboy.
flags:
    
./exporter:
  --arena_map: A map from Sportszone to Team Cowboy arena names.;
    repeat this option to specify a list of values
    (default: '[]')
  --away_color: The color of the away jerseys.
    (default: 'Black')
  -?,--[no]help: show this help
  --[no]helpshort: show usage only for this module
  --[no]helpxml: like --help, but generates XML output
  --home_color: The color of the home jerseys.
    (default: 'White')
  --league_id: The Sportszone league ID.
    (an integer)
  --output_file: The output file.
    (default: 'schedule.csv')
  --season_id: The Sportszone season ID.
    (an integer)
  --sportszone_url: The base Sportszone URL.
  --team_id: The Sportszone team ID.
    (an integer)
  --url: The URL of a schedule page.
    
gflags:
  --flagfile: Insert flag definitions from the given file into the command line.
    (default: '')
  --undefok: comma-separated list of flag names that it is okay to specify on
    the command line even if the program does not define a flag with that name.
    IMPORTANT: flags in this list that have arguments MUST use the --flag=value
    format.
    (default: '')
```
