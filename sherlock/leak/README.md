# Sherlock Quiz: answers are served to players

## Finding

The player web app (`https://play.sherlockquiz.com/?gid=<game>&tid=<team>`)
loads the whole game from a public, unauthenticated endpoint:

```
GET https://play-server.sherlockquiz.com/api/game/<gid>
```

The response (`{game, slider, teams, tours}`) contains every slide of the
game. Each question slide (`answer == 1`) carries an `answers` array with the
accepted answers, and the deck also contains the host's answer-reveal slides
(`type == 1`) that follow each question. Nothing requires a team id, a login,
or the game to be in progress; the data is also sitting in the browser's
IndexedDB and network tab for every player.

Other unauthenticated endpoints used by the app: `/api/game/<gid>/state`,
`/api/game/<gid>/settings`, `/api/result/<gid>`, `/api/games`.

## Impact

Any player can read every correct answer for the game before or during
play, with a single request or by opening the browser dev tools.

## Proof of concept

```
python3 leak.py 'https://play.sherlockquiz.com/?gid=4577&tid=2224'
```

Standard library only. Prints each tour's questions with their accepted
answers. Verified on game 4577 ("Песочные часы №9", 2026-09-16): 72 of 72
questions returned with answers
([output](../games/4577/output.txt), [report](../games/4577/leak.pdf)).

## Suggested fix

Do not send `answers` (or reveal slides) to player clients. Serve slides one
at a time as the host advances them, and check answers on the server, which
already receives them via `POST /api/answer/<gid>`.
