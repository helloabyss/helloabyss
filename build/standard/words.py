#!/usr/bin/env python3
"""Turn a HeyGen create_speech result (saved as JSON) into the engine's words.json.

    python3 words.py speech.json ../<episode>/words.json
Drops the <start>/<end> markers; keeps each word's start/end seconds exactly as returned."""
import json, sys
r = json.load(open(sys.argv[1]))
w = [dict(w=x["word"], s=x["start"], e=x["end"]) for x in r["word_timestamps"] if not x["word"].startswith("<")]
json.dump(dict(dur=round(r["duration"], 3), words=w), open(sys.argv[2], "w"))
print(len(w), "words,", round(r["duration"], 2), "s")
