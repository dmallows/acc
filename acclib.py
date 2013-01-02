import os
import itertools
import operator
import datetime
import decimal
import re
import subprocess

def _git(*args, stdout=subprocess.PIPE):
    return subprocess.check_call(('git',) + args, stdout=stdout)

def git_init():
    _git('init')

def git_add(*files):
    _git('add', *files)

def git_commit(msg, files=[]):
    if files:
        _git('commit', '-m', msg, *files)
    else:
        _git('commit', '-a', '-m', msg)

def is_account():
    return os.path.isfile('.acc')

def mk_account():
    assert not acc.is_account()
    git_init()
    with open('.acc', 'w'):
        pass
    git_add('.acc')
    git_commit('Initialized repo')

def read_account_line(line):
    line = line.split(None, 2)
    date = datetime.datetime.strptime(line[0], '%Y-%m-%d').date()
    amt = decimal.Decimal(line[1])
    name = line[2]
    return date, amt, name

def show_account_line(line):
    date, amt, name = line
    return " ".join((
        date.strftime('%Y-%m-%d'),
        str(amt),
        name))

rstrip = operator.methodcaller('rstrip')
fst = operator.itemgetter(0)
third = operator.itemgetter(2)

def read_account(filename):
    try:
        with open(filename) as account_file:
            return list(map(read_account_line, map(rstrip, account_file)))
    except IOError:
        return []

def write_account(data, filename):
    with open(filename, 'w') as account_file:
        for line in map(show_account_line, data):
            print(line, file=account_file)

def partition_account(account, xs):
    a, b = itertools.tee(xs)
    match = itertools.compress(account, a)
    b = map(operator.not_, b)
    nomatch = itertools.compress(account, b)
    return list(match), list(nomatch)

def partition_account_on_name(account, regex):
    regex = re.compile(regex, re.IGNORECASE)
    matches = map(regex.search, map(third, account))
    return partition_account(account, matches)

def merge_accounts(a, b):
    return sorted(itertools.chain(a, b))

#a1 = read_account('hsbc')
#
#a1.sort(key=fst)
#
#
#aldi_re = re.compile('aldi stores', re.IGNORECASE)
#
#match = lambda x: bool(aldi_re.search(x[2]))
#
#ins, outs = partition_account(a1, map(match, a1))
#
#
#write_account(merge_accounts(ins, ins), 'aldi')
#
