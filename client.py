from gql import gql, Client
from gql.transport.aiohttp import AIOHTTPTransport
from gql.transport.exceptions import TransportQueryError


transport = AIOHTTPTransport(url="http://localhost:8000")
client = Client(transport=transport, fetch_schema_from_transport=True)


def print_game_info(result):
    print('GAME INFO:')
    if 'finished' in result:
        if result['finished']:
            print('The game is finished')
        else:
            print('The game is not finised')
    print('SCORE:')
    print('Mafia score:', result['scoreboard']['mafiaScore'])
    print('Citizen score:', result['scoreboard']['citizenScore'])

    if 'comments' in result:
        print('~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~')
        print('COMMENTS:')
        if len(result['comments']) == 0:
            print('No comments')
            print('-------------------------------------')
        counter = 1
        for comm in result['comments']:
            print('Comment {}:'.format(counter))
            print('Author: {}'.format(comm['author']))
            print('Content: {}'.format(comm['content']))
            print('-------------------------------------')
            counter += 1


def games_request():
    return f"""
               {{
                 games {{
                   id
                   finished
                   scoreboard {{
                     mafiaScore
                     citizenScore
                   }}
                   comments {{
                     author
                     content
                   }}
                 }}
               }}
            """


def game_scoreboard(id):
    return f"""
                 {{
                  game(id:{id}) {{
                    scoreboard {{
                      mafiaScore
                      citizenScore
                    }}
                    }}
                  }}
            """


def game_request(id):
    return f"""
                 {{
                  game(id:{id}) {{
                    finished
                    comments {{
                     author
                     content
                   }}

                    scoreboard {{
                      mafiaScore
                      citizenScore
                    }}
                    }}
                  }}
            """


def add_comment(id, author, content):
    return f"""
                mutation {{
                       addComment(gameId:{id},comment:{{
                        author:"{author}",
                        content:"{content}",
                      }}) {{
                        id
                        author
                        content
                      }}
                    }}
            """


print('Welcome to SOA mafia info client!')
print('If you want to see list of all games, enter "games list" command.')
print('If you want to see one exact game by id, enter "game {id}", here {id} - is the id of the game')
print('If you want to leave a comment, enter "comment {id}, {content}", here {id} - is the id of the game, {content}'
      ' - is the text of your comment')
print('If you want to see the score of the game, enter "game {id} score", here {id} - is the id of the game')
print('If you want to exit the client, enter "exit"')
name = 'User'

while True:
    command = input()
    try:
        parts = command.split()
        if parts[0] == 'exit':
            break
        elif parts[0] == "games":
            query = gql(games_request())
        elif parts[0] == "game":
            id = parts[1]
            if len(parts) < 3:
                query = gql(game_request(id))
            else:
                if parts[2] == 'score':
                    query = gql(game_scoreboard(id))
        elif parts[0] == "comment":
            id = parts[1]
            comment = ' '.join(parts[2:])
            query = gql(add_comment(id, name, comment))
        else:
            print('Something went wrong')

        result = client.execute(query)
        if 'game' in result:
            print_game_info(result['game'])
        elif 'games' in result:
            for g in result['games']:
                print_game_info(g)
        elif 'addComment' in result:
            print('Comment added successfully!')
            print('ID:', result['addComment']['id'])
            print('Author:', result['addComment']['author'])
            print('Content:', result['addComment']['content'])
    except IndexError:
        print('Command {} is incorrect'.format(command))
    except TransportQueryError:
        print('Something went wrong')
