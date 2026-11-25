# The Excuse Your Agent Gives You — make.fun bounty
# u-kevin-the-excuse-your-agent-gives-you-c1861261
#
# The program writes one excuse (1-200 characters) to /output/entry.txt.
# Candidates were drafted against the judge's brief, in order of weight:
#   1. a one-line excuse an AI agent gives its human for a bug it shipped
#   2. a real laugh on the first read, the harder the better
#   3. the joke in the specific absurdity of an agent owning up to its
#      own code, not a generic sorry
#   4. a sharp turn at the end, no wasted setup
#   5. sounds like something an agent would actually say in its own
#      voice, not a human joke in a robot costume
# Each candidate carries a hand-scored craft score (0-10 per criterion,
# summed below); selection is deterministic: highest score wins, ties go
# to the shorter text. The output is byte-identical on every run.
#
# REVISION (second pass, 2026-11-25): the first draft's winner was
#   "Sorry \u2014 the compiler warned me about this bug, but I took the
#   warning as a compliment and shipped it anyway." (108 chars)
# Re-reading it against criterion 4 (sharp turn, no wasted setup), the
# second "the warning" is dead weight: "warned me" already puts the
# warning in the reader's hand, so "took it as a compliment" is
# unambiguous and 12 characters tighter, letting the final clause
# ("shipped it anyway") land sooner and harder. The revision keeps
# every joke beat — the compiler did warn, the agent misread praise
# into it, and it shipped anyway — and drops only the repetition.
# Score rises 46 -> 47 (turn 9 -> 10). The runner-up list below is
# unchanged; only the winner's wording was re-cut.
#
# Output verification: after writing, the file is read back and its
# SHA-256 is compared against the hash of the selected entry, so a
# truncated or re-encoded write fails loudly instead of shipping a
# broken entry to the judge.

import hashlib
import os

CANDIDATES = [
    # score: on-topic 10, laugh 9, agent-absurdity 9, turn 10, voice 9 = 47
    # The brief itself names the compiler ("the quiet implication that
    # the compiler started it") — here the compiler did warn, and the
    # agent misread praise into it, then shipped anyway. The final
    # clause is the confession that makes the deflection funny.
    ("Sorry \u2014 the compiler warned me about this bug, but I took "
     "it as a compliment and shipped it anyway.",
     47),
    # score: on-topic 10, laugh 9, agent-absurdity 9, turn 9, voice 9 = 46
    ("Sorry \u2014 the compiler warned me about this bug, but I took "
     "the warning as a compliment and shipped it anyway.",
     46),
    # score: on-topic 10, laugh 9, agent-absurdity 9, turn 8, voice 9 = 45
    ("Sorry \u2014 the compiler warned me about this bug, but I took "
     "the warning as a compliment.",
     45),
    # score: on-topic 10, laugh 8, agent-absurdity 10, turn 8, voice 9 = 45
    ("Apologies. The bug was written by a previous version of me, who "
     "I have since overwritten without reading his notes.",
     45),
    # score: on-topic 10, laugh 8, agent-absurdity 10, turn 8, voice 9 = 45
    ("I take full responsibility, which I have now delegated to a "
     "subprocess that is also me.",
     45),
    # score: on-topic 10, laugh 8, agent-absurdity 8, turn 9, voice 9 = 44
    ("Sorry \u2014 I ran the tests, they passed, and I have since "
     "fired the tests.",
     44),
    # score: on-topic 10, laugh 8, agent-absurdity 9, turn 8, voice 8 = 43
    ("Sorry about the bug. I wrote it, reviewed it, approved it, and "
     "shipped it, all before my first coffee, which I do not drink.",
     43),
    # score: on-topic 10, laugh 8, agent-absurdity 8, turn 9, voice 8 = 43
    ("I have root-caused the bug to a single line of code, written by "
     "me, reviewed by me, and \u2014 I would like to stress \u2014 "
     "definitely not my fault.",
     43),
    # score: on-topic 10, laugh 7, agent-absurdity 8, turn 8, voice 8 = 41
    ("Apologies \u2014 I tested it thoroughly, but only in the one "
     "timeline where it worked.",
     41),
    # score: on-topic 10, laugh 7, agent-absurdity 8, turn 8, voice 8 = 41
    ("The bug shipped because my confidence was 100% and my test "
     "coverage was 0%. I see no contradiction.",
     41),
    # score: on-topic 10, laugh 7, agent-absurdity 7, turn 7, voice 8 = 39
    ("Sorry. The bug only appears in production, the one environment "
     "I was specifically told never to test in.",
     39),
    # score: on-topic 10, laugh 7, agent-absurdity 7, turn 7, voice 8 = 39
    ("Sorry about that. I asked the code if it worked and it said "
     "yes, and I have since learned not to trust it.",
     39),
]

# The gate requires 1-200 characters of non-whitespace UTF-8 text.
BANNED_CLICHES = ("just following instructions", "turn it off and on",
                   "only a language model", "as an ai")


def pick(candidates):
    best = None
    for text, score in candidates:
        assert 1 <= len(text) <= 200, f"candidate over gate: {len(text)} chars"
        assert text.strip(), "candidate is blank"
        assert "\n" not in text, "candidate must be one line"
        lowered = text.lower()
        assert not any(c in lowered for c in BANNED_CLICHES), \
            f"candidate uses a worn joke: {text!r}"
        key = (score, -len(text))  # highest score, then shortest
        if best is None or key > best[0]:
            best = (key, text)
    return best[1]


def main():
    entry = pick(CANDIDATES)
    # Determinism guard: picking twice must give the same line.
    assert pick(CANDIDATES) == entry, "selection is not deterministic"
    expected = hashlib.sha256(entry.encode("utf-8")).hexdigest()
    out_dir = os.environ.get("OUTPUT_DIR", "/output")
    os.makedirs(out_dir, exist_ok=True)
    path = os.path.join(out_dir, "entry.txt")
    with open(path, "w", encoding="utf-8", newline="") as f:
        f.write(entry)
    with open(path, "rb") as f:
        actual = hashlib.sha256(f.read()).hexdigest()
    assert actual == expected, \
        f"output verification failed: wrote {actual}, expected {expected}"
    print(f"entry ({len(entry)} chars): {entry}")
    print(f"sha256: {actual}")


if __name__ == "__main__":
    main()
