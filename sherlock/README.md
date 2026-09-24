# Sherlock Quiz

Player app: `https://play.sherlockquiz.com/?gid=<game>&tid=<team>`.

## Protocol

- `GET https://play-server.sherlockquiz.com/api/game/<gid>` returns the whole
  game (`{game, slider, teams, tours}`), unauthenticated. Slide types: 1 info,
  2 text, 3 image, 4 audio, 5 video; question slides have `answer == 1`.
- Other unauthenticated endpoints: `/api/game/<gid>/state`,
  `/api/game/<gid>/settings`, `/api/result/<gid>`, `/api/games`.
- Live state over socket.io: client emits `joinRooms {gameId, teamId}`,
  server pushes `state {sid, t, ts, ls}`.
- Answers are submitted with
  `POST /api/answer/<gid> {team_id, slide_id, answer, tour}`.

## Findings

- [leak/](leak/README.md) - correct answers are served to players.

## Games

| gid | Date | Name | Artifacts |
|-----|------|------|-----------|
| 4577 | 2026-09-16 | Песочные часы №9 | [games/4577/](games/4577/) |
