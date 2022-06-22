import typing
from typing import List

import strawberry
from strawberry.scalars import ID


@strawberry.type
class Scoreboard:
    id: ID
    mafia_score: int
    citizen_score: int


@strawberry.type
class Comment:
    id: ID
    author: str
    content: str


@strawberry.input
class CommentInput:
    author: str
    content: str


@strawberry.type
class Game:
    id: ID
    finished: bool
    scoreboard: Scoreboard
    comments: List[Comment]


game_dict: typing.Dict[int or ID, Game] = {
    0: Game(id=0, finished=True, scoreboard=Scoreboard(id=0, mafia_score=0, citizen_score=1),
            comments=[]),
    1: Game(id=1, finished=True, scoreboard=Scoreboard(id=1, mafia_score=57, citizen_score=179),
            comments=[Comment(id=0, author='User_1', content='Test 0')]),
    2: Game(id=2, finished=False, scoreboard=Scoreboard(id=2, mafia_score=200, citizen_score=100),
            comments=[Comment(id=0, author='User_1', content='Test 1'),
                      Comment(id=1, author='User_2', content='Test 2')]),
    3: Game(id=3, finished=False, scoreboard=Scoreboard(id=3, mafia_score=0, citizen_score=0),
            comments=[])
}


@strawberry.type
class Query:
    @strawberry.field
    def games(self) -> List[Game]:
        return list(game_dict.values())

    @strawberry.field
    def game(self, id: int) -> Game:
        return game_dict[id]


@strawberry.type
class Mutation:
    @strawberry.mutation
    def addComment(self, gameId: int, comment: CommentInput) -> Comment:
        max_id = max([comment.id for g in game_dict.values() for comment in g.comments])
        new_comment = Comment(id=int(max_id) + 1, author=comment.author, content=comment.content)
        game_dict[gameId].comments.append(new_comment)
        return new_comment


schema = strawberry.Schema(query=Query, mutation=Mutation)

f = open("schema.graphql", "w+")
f.write(schema.as_str())
f.close()
