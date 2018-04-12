#!/usr/bin/python3.5
# -*- coding: utf-8 -*-
# bot: @omomdobot

from telegram.ext import Updater, MessageHandler, Filters, \
    CommandHandler, ConversationHandler
from telegram import ReplyKeyboardMarkup
import omdb
import json
import re


def regex_movie(title_year):

    p = re.compile('(.+), ?(\d{4}\Z)')

    try:

        try:

            title = p.search(title_year).group(1)
            year = p.search(title_year).group(2)
        except:

            title = title_year
            year = None

        return (title, year)
    except:

        return """Hey! You got the wrong syntax! Think about it.

You can also press /stop if you want to."""


def regex_season(title_season_year):

    p = re.compile('(.*) s(\d+)(, ?(\d{4}))?')

    try:

        try:

            title = p.search(title_season_year).group(1)
            season = p.search(title_season_year).group(2)
            year = p.search(title_season_year).group(4)
        except:

            title = p.search(title_season_year).group(1)
            season = p.search(title_season_year).group(2)
            year = None

        return (title, season, year)
    except:

        return """Hey! You got the wrong syntax! Think about it.

You can also press /stop if you want to."""


def regex_episode(title_season_episode_year):

    p = re.compile('(.*) (s(\d+)e(\d+))(, ?(\d{4}))?')

    try:

        try:

            title = p.search(title_season_episode_year).group(1)
            season = p.search(title_season_episode_year).group(3)
            episode = p.search(title_season_episode_year).group(4)
            year = p.search(title_season_episode_year).group(6)
        except:

            title = p.search(title_season_episode_year).group(1)
            season = p.search(title_season_episode_year).group(2)
            episode = season = \
                p.search(title_season_episode_year).group(3)
            year = None
        return (title, season, episode, year)
    except:

        return """Hey! You got the wrong syntax! Think about it.

You can also press /stop if you want to."""


def convert(my_json):

    return json.loads(my_json.decode('utf8'))


def movie_search(bot, update):

    cont = regex_movie(update.message.text)
    if len(cont) > 2:
        update.message.reply_text(cont)
        return 1

    title = cont[0]
    year = cont[1]

    if not year:

        res = omdb.request(t=title, apikey='1debb7dc', plot='full',
                           detail='full')
    else:

        res = omdb.request(t=title, y=year, apikey='1debb7dc',
                           plot='full', detail='full')

    json_content = convert(res.content)

    if 'Error' in json_content:
        update.message.reply_text("""I can't find anything. I think this movie doesn't exist.
Let's find out where the mistake was done.
Make sure you've sent me a message in the right format.
Maybe you've selected the wrong title/year.
Maybe you have sent me a sticker, didn't you?
Try to insert/remove 'The' in the beginning of the title.

You can also press /stop if you want to.""")
        return 1

    if json_content['Type'] == 'movie':

        if json_content['Production'] == 'N/A':
            json_content['Production'] = ''
        else:
            json_content['Country'] += ', '

        update.message.reply_text('''%s, %s
%s%s

Released:
%s

Runtime:
%s

Director:
%s

Actors:
%s


  %s

IMDb
%s

Rated:
%s



You can go back to menu. Press /search.'''
                                  % (
            json_content['Title'],
            json_content['Year'],
            json_content['Country'],
            json_content['Production'],
            json_content['Released'],
            json_content['Runtime'],
            json_content['Director'],
            json_content['Actors'],
            json_content['Plot'],
            json_content['Ratings'][0]['Value'],
            json_content['Rated'],
            ))
        update.message.reply_photo(json_content['Poster'])
    else:
        update.message.reply_photo("""I'm sorry, I can't find any movie.
Make sure you have send the right title and year or press /stop."""
                                   )
    return ConversationHandler.END


def series_search(bot, update):
    cont = regex_movie(update.message.text)

    if len(cont) > 2:
        update.message.reply_text(cont)
        return 1

    title = cont[0]
    year = cont[1]

    if not year:
        res = omdb.request(t=title, apikey='1debb7dc', plot='full',
                           detail='full')
    else:
        res = omdb.request(t=title, y=year, apikey='1debb7dc',
                           plot='full', detail='full')

    json_content = convert(res.content)

    if 'Error' in json_content:
        update.message.reply_text("""I can't find anything. I think these series don't exist.
Let's find out where the mistake was done.
Make sure you've sent me a message in the right format.
Maybe you've selected the wrong title/year.
Maybe you have sent me a sticker, didn't you?
Try to insert/remove 'The' in the beginning of the title.

You can also press /stop if you want to.""")
        return 1

    if json_content['Type'] == 'series':

        update.message.reply_text('''%s, %s
%s
%s seasons

First episode:
%s

Runtime:
%s

Actors:
%s

  %s

IMDb
%s

Rated:
%s



You can go back to menu. Press /search.'''
                                  % (
            json_content['Title'],
            json_content['Year'],
            json_content['Country'],
            json_content['totalSeasons'],
            json_content['Released'],
            json_content['Runtime'],
            json_content['Actors'],
            json_content['Plot'],
            json_content['Ratings'][0]['Value'],
            json_content['Rated'],
            ))
        update.message.reply_photo(json_content['Poster'])
    else:

        update.message.reply_text("""I'm sorry, I can't find any series with this title.
Make sure you have send the right title and year or press /stop."""
                                  )

    return ConversationHandler.END


def seasons_search(bot, update):

    cont = regex_season(update.message.text)

    if len(cont) > 3:
        update.message.reply_text(cont)
        return 1

    series = cont[0]
    seas = cont[1]
    year = cont[2]

    episodes = []

    if not year:
        res = omdb.request(t=series, apikey='1debb7dc', detail='full',
                           season=seas)
    else:
        res = omdb.request(t=series, y=year, apikey='1debb7dc',
                           plot='full', detail='full')
    json_content = convert(res.content)

    if 'Error' in json_content:
        update.message.reply_text("""I can't find anything. I think this season doesn't exist.
Let's find out where the mistake have done.
Make sure you've sent me a message in the right format.
Maybe you've selected the wrong year/season.
Maybe you have sent me a sticker, didn't you?
Try to insert/remove 'The' in the beginning of the title.

You can also press /stop if you want to.""")

    for i in range(len(json_content['Episodes'])):

        episodes.append('''Episode %s:
  %s'''
                        % (json_content['Episodes'][i]['Episode'],
                        json_content['Episodes'][i]['Title']))

    update.message.reply_text('''%s
Season %s

%s



You can go back to menu. Press /search.'''
                              % (json_content['Title'],
                              json_content['Season'],
                              '''

'''.join(episodes)))
    return ConversationHandler.END


def episode_search(bot, update):

    cont = regex_episode(update.message.text)

    if len(cont) > 4:
        update.message.reply_text(cont)
        return 1

    series = cont[0]
    seas = cont[1]
    epi = cont[2]
    year = cont[3]
    print (series, seas, epi, year)
    if not year:
        res = omdb.request(
            t=series,
            apikey='1debb7dc',
            plot='full',
            detail='full',
            season=seas,
            episode=epi,
            )
    else:
        res = omdb.request(
            t=series,
            y=year,
            apikey='1debb7dc',
            plot='full',
            detail='full',
            season=seas,
            episode=epi,
            )
    json_content = convert(res.content)
    if 'Error' in json_content:
        update.message.reply_text("""I can't find anything. I think this episode doesn't exist.
Let's find out where the mistake have done.
Make sure you've sent me a message in the right format.
Maybe you've selected the wrong year/season/episode.
Maybe you have sent me a sticker, didn't you?
Try to insert/remove 'The' in the beginning of the title.

You can also press /stop if you want to.""")
        return 1
    elif json_content['Type'] == 'episode':

        update.message.reply_text('''%s
Season %s, Episode %s
%s

Released:
%s

Director:
%s

Actors:
%s

  %s

IMDb
%s

Rated:
%s



You can go back to menu. Press /search.
'''
                                  % (
            json_content['Title'],
            json_content['Season'],
            json_content['Episode'],
            json_content['Country'],
            json_content['Released'],
            json_content['Director'],
            json_content['Actors'],
            json_content['Plot'],
            json_content['Ratings'][0]['Value'],
            json_content['Rated'],
            ))

    return ConversationHandler.END


def movie(bot, update):
    update.message.reply_text('''I can help you find information about certain movie. Send me the movie title.
You can also send the release year but this is not required.

Please, send message in format "Movie title, Year" or "Movie title"
For example: "Black Panther"''')
    return 1


def series(bot, update):
    update.message.reply_text('''I can help you find information about certain series. Send me the series title.
You can also send the release year but this is not required.

Please, send message in this format "Series title, Year" or "Series title"
For example: "The Flash"''')
    return 1


def season(bot, update):
    update.message.reply_text('''I can help you find information about any season of certain series.
Send me the series title and number of season.
You can also send the release year but this is not required.

Please, send message in this format "Series title s#, Year" or "Series title, s#"
For example: "Friends s5"''')
    return 1


def episode(bot, update):
    update.message.reply_text('''I can help you find information about any episode of certain series.
Send me the series title, season and number of episode.
You can also send the release year but this is not required.

Please, send message in this format "Series title s#e#, Year" or "Series title s#e#"
For example: "Friends s5e16"''')
    return 1


def start(bot, update):
    update.message.reply_text("Hi! I can help you find \
    information about any movie or series.\nPress /search to start."
                              )


reply_keyboard = [['/movie', '/series'], ['/season', '/episode']]

markup = ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=True)


def search(bot, update):
    update.message.reply_text('What are you looking for?',
                              reply_markup=markup)


def stop(bot, update):
    update.message.reply_text('Ha-ha. Ok. Bye.')
    return ConversationHandler.END


def main():
    updater = Updater('570091828:AAGzIwTpMozBhxnoBc5OJTpaPtdPy91QBew')

    movie_conv = \
        ConversationHandler(entry_points=[CommandHandler('movie',
                            movie)],
                            states={1: [MessageHandler(Filters.text,
                            movie_search)]},
                            fallbacks=[CommandHandler('stop', stop)])

    series_conv = \
        ConversationHandler(entry_points=[CommandHandler('series',
                            series)],
                            states={1: [MessageHandler(Filters.text,
                            series_search)]},
                            fallbacks=[CommandHandler('stop', stop)])

    season_conv = \
        ConversationHandler(entry_points=[CommandHandler('season',
                            season)],
                            states={1: [MessageHandler(Filters.text,
                            seasons_search)]},
                            fallbacks=[CommandHandler('stop', stop)])

    episode_conv = \
        ConversationHandler(entry_points=[CommandHandler('episode',
                            episode)],
                            states={1: [MessageHandler(Filters.text,
                            episode_search)]},
                            fallbacks=[CommandHandler('stop', stop)])

    dp = updater.dispatcher
    dp.add_handler(CommandHandler('start', start))
    dp.add_handler(CommandHandler('search', search))
    dp.add_handler(movie_conv)
    dp.add_handler(series_conv)
    dp.add_handler(season_conv)
    dp.add_handler(episode_conv)

    updater.start_polling()

    updater.idle()


if __name__ == '__main__':
    main()


