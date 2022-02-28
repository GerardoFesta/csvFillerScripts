import sys
import collections

last_tag = None
commits_per_tag = collections.defaultdict(set)


for line in sys.stdin:
    line = line.strip()
    if not line:
        continue
    commit, _, refs = line.partition(" ")
    if refs.startswith("tag:"):
        last_tag = refs.split(", ")[0]
    commits_per_tag[last_tag].add(commit)


for last_tag, commits in sorted(
    commits_per_tag.items(),
    key=lambda pair: len(pair[1]),
    reverse=True,
):
    print(last_tag, commits)
