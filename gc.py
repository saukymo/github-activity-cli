# coding: utf-8

import configparser
from xtermcolor import colorize
from github import Github
from multiprocessing.dummy import Pool as ThreadPool

cf = configparser.ConfigParser()
cf.read('config.ini')


def get_repo_contributions(repo):
    contribution = repo.get_stats_commit_activity()
    return contribution or [[0 for _ in range(7)] for week in range(52)]

def get_color(commit):
    if commit == 0:
        return None
    commit = commit_list.index(commit)
    commit = int(int((commit / top) * part + 1) * (top / part))
    color = str(hex(15 - commit))[-1]
    return int('0x%s%sff%s%s' % (color, color, color, color), 16)

username = cf.get('account', 'username')
password = cf.get('account', 'password')

client = Github(username, password)
user = client.get_user()
repos = user.get_repos()

pool = ThreadPool(processes=16)
results = pool.map(get_repo_contributions, repos)

pool.close()
pool.join()

# for repo in repos:
#     contribution = repo.get_stats_commit_activity()
#     if contribution is None:
#         print(repo.name)
#         continue
year_contributions = [[0 for _ in range(7)] for week in range(52)]
for contribution in results:
    year_contributions = [[a + b for a, b in zip(x, y.days)] for x, y in zip(year_contributions, contribution)]

commit_set = set()
for week in year_contributions:
    for day in week:
        commit_set.add(day)

commit_list = sorted(list(commit_set))
top = len(commit_list)
part = 5

for days in range(7):
    for week in year_contributions:
        print(colorize("  ", rgb=0, bg=get_color(week[days])), end='')
    print()

# commit_list = [_ for _ in range(16)]
# top = len(commit_list)
# part = 5
# for commit in range(top):
# 	if commit == 0:
# 		print(colorize(" ", rgb=0), end='')
# 	else:
# 		print(colorize(u"\u25A1", rgb=get_color(commit)), end='')
# print()
