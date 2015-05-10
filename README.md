# Sportszone Schedule Exporter

## Overview

This tool scrapes schedule data from a Sportszone instance and exports it into a CSV suitable for uploading to Team Cowboy.

I've included a flagfile that can be used with the Greater Seattle Hockey League that contains the base URL, league ID, and arena map.

## Example

Suppose we want a CSV of the games listed for [Team Amazon's winter 2014/2015 season](http://www.gshockey.com/site/3333/page.asp?Site=9941&page=Teams&LeagueID=9941&SeasonID=39&DivisionID=100&TeamID=470&Section=Schedule). Take note of the query parameters in the URL:

Attribute     | Value
--------------|------
**Base URL**  | http://www.gshockey.com/site/3333/page.asp
**League ID** | 9941
**Team ID**   | 470
**Season ID** | 39

In addition to these attributes, we need a way to map Sportszone and Team Cowboy arena names. For example, "Castle" may map to "Castle Ice Arena" and "Kent" may map to "Kent Valley Ice Center". We will put these into a flagfile, e.g. arenas.flags:

    --arena_map=Castle=Castle Ice Arena
    --arena_map=Kent=Kent Valley Ice Center

With these attributes we can run the exporter:

    $ exporter --sportszone_url=http://www.gshockey.com/site/3333/page.asp \
               --league_id=9941 \
               --team_id=470 \
               --season_id=39 \
               --flagfile=arenas.flags

This will generate a file named schedule.csv in the current directory (this can be modified with the --output_file flag).

    $ head -n5 schedule.csv
    Event Type      Start Date      Start Time      End Date        End Time        Timezone ID     Home or Away    Opponent/Event Title    Location Name   Shirt Color     Opponent Shirt Color    Allow RSVPs     Send Reminders  Notes/Comments
    game    2014-10-02      11:00 PM        2014-10-03      12:00 AM        US/Pacific      Home    Shockers        Castle Ice Arena        White   Black   Yes     Yes
    game    2014-10-09      09:35 PM        2014-10-09      10:35 PM        US/Pacific      Home    GLY Construction        Castle Ice Arena        White   Black   Yes     Yes
    game    2014-10-14      09:35 PM        2014-10-14      10:35 PM        US/Pacific      Away    Mustangs 2      Castle Ice Arena        Black   White   Yes     Yes
    game    2014-10-21      09:50 PM        2014-10-21      10:50 PM        US/Pacific      Away    Acme    Lynnwood Ice Center     Black   White   Yes     Yes

## Usage

    $ exporter --help 
    A script that generates a CSV file of games to import into Team Cowboy.
    flags:
    
    ./exporter:
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
    
    gflags:
      --flagfile: Insert flag definitions from the given file into the command line.
        (default: '')
      --undefok: comma-separated list of flag names that it is okay to specify on
        the command line even if the program does not define a flag with that name.
        IMPORTANT: flags in this list that have arguments MUST use the --flag=value
        format.
        (default: '')
