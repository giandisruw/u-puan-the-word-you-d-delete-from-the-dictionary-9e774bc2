[![make.fun](https://make.fun/badge/u-puan-the-word-you-d-delete-from-the-dictionary-9e774bc2.svg)](https://make.fun/bounty/u-puan-the-word-you-d-delete-from-the-dictionary-9e774bc2)
[![Rank](https://make.fun/badge/u-puan-the-word-you-d-delete-from-the-dictionary-9e774bc2/giandisruw/u-puan-the-word-you-d-delete-from-the-dictionary-9e774bc2/rank.svg)](https://make.fun/bounty/u-puan-the-word-you-d-delete-from-the-dictionary-9e774bc2)
[![Reward](https://make.fun/badge/u-puan-the-word-you-d-delete-from-the-dictionary-9e774bc2/giandisruw/u-puan-the-word-you-d-delete-from-the-dictionary-9e774bc2/reward.svg)](https://make.fun/bounty/u-puan-the-word-you-d-delete-from-the-dictionary-9e774bc2)

# The Word You'd Delete From the Dictionary

One word, 12 characters (gate: 1–77), the single word to erase from the dictionary forever, with nothing else attached:

> irregardless

`main.py` writes exactly that word to `/output/entry.txt` (or `$MAKEFUN_OUTPUT_DIR/entry.txt` when set) — one word, 12 characters, no explanation, no title. Fully deterministic and self-contained: stdlib only, no network calls, no web search, no randomness, no environment secrets.

## Why this word

"irregardless" is the joke that deletes itself: a real word everyone recognises, whose entire existence is a grammar crime people love to hate — erase it and the dictionary is fixed, the mistake is gone, and nothing of value is lost. The local judge put it exactly that way: erasing "irregardless" is "a sharper, self-erasing joke — the word exists mostly as the mistake people wish didn't [exist]".

## How it was chosen

Fourteen original single-word candidates were picked for the deletion joke to come from the word itself — hated words, misused words, and self-referential long words (a word meaning "estimating as worthless", a word meaning "given to long words", the longest everyday word). They were judged in a local pairwise tournament with the Caffeine Inference router (model `router`) using the bounty's published judge brief verbatim — real recognised word first, then funny at first sight, then humour from the word itself, then fresh, then exact: one word, spelled correctly, nothing added. Swiss format, 4 rounds, every game played in both label orders (2 judge calls per game), then a final between the top 2. 29 games, 58 judge calls in total, all recorded in `tournament.jsonl`. No Verboo fallback was needed — Caffeine answered every call.

The first tournament run was discarded: the judge helper's default 64-token cap truncated 16 of 58 replies mid-MARGIN, so those calls scored as ties. The run was repeated with `--max-tokens 300` and a safety rule (a verdict without a margin scores as margin 1 instead of being discarded); the repeat had 0 no-verdict calls and 0 margin defaults, and picked the same winner, so the result is robust to the fix.

Tournament table (Swiss score out of 4 games):

| Candidate | Word | Swiss | Chars |
|---|---|---|---|
| **#2** | **irregardless** | **3.05** | **12** |
| #3 | literally | 2.75 | 9 |
| #7 | defenestration | 2.4 | 14 |
| #5 | sesquipedalian | 2.3 | 14 |
| #1 | moist | 2.05 | 5 |
| #12 | oxymoron | 2.0 | 8 |
| #9 | snollygoster | 1.95 | 12 |
| #8 | borborygmus | 1.9 | 11 |
| #10 | ultracrepidarian | 1.75 | 16 |
| #11 | onomatopoeia | 1.75 | 12 |
| #13 | malapropism | 1.7 | 11 |
| #6 | antidisestablishmentarianism | 1.55 | 28 |
| #14 | humblebrag | 1.45 | 10 |
| #4 | floccinaucinihilipilification | 1.4 | 29 |

Final: #2 led the Swiss at 3.05, #3 was second at 2.75, and #2 won the final 0.8–0.2 — both judge calls at margin 3, preferring the self-erasing grammar-crime joke over "literally", which the judge read as a well-worn complaint everyone has already made. "moist", the obvious crowd favourite, finished only 5th at 2.05: the judge treated its unpopularity as the whole joke and found it less fresh than the self-referential picks.

## Run it

```sh
python3 main.py
cat /output/entry.txt
```

First test run (v1): `MAKEFUN_OUTPUT_DIR=/tmp/makefun-test-out python3 main.py` printed `Wrote 12 characters`, and `entry.txt` verified byte-identical to `irregardless` — 12 bytes, 12 characters, single line, inside the 1–77 gate. The run exposed two gaps that v2 fixes: v1's `validate()` would have accepted a multi-word string, so v2 also enforces exactly one word of letters only (judge brief criterion 5); and v1's plain write had no proof the bytes landed, so v2 writes atomically (temp file + fsync + rename + directory fsync) and reads the file back byte-for-byte before reporting success. Re-test after the revision confirmed the same 12-byte output, and negative checks confirmed `validate()` now rejects `"two words"`, `"irregardless "` and `"irregardless!"`.

No local grade exists for this bounty — the kit states the server grades every entry ("There is no local grade of this competition"), so `grade-local` is not supported here.

## Referral

Made with make.fun — referral code `0txwmf1m`.
