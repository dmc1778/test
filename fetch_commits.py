from asyncore import read
import json
from lib2to3.pgen2 import token
import os
import re
from urllib import request
import requests as r
import requests
import argparse
import sys
import random
import datetime
import time
from filter import read_txt
from requests.adapters import HTTPAdapter
from urllib3.util import Retry
from xml.dom import minidom 


# (0, nimashiri2012@gmail.com, 1, cse19922021@gmail.com, 2, nshiri@yorku.ca, 3, nshiri@cse.yorku.ca)
tokens = {0: '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', 1: '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',
          2: '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', 3: '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'}
tokens_status = {'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': True, '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': True,
                 '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': True, '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': True}


def requests_retry_session(
    retries=3,
    backoff_factor=0.3,
    status_forcelist=(500, 502, 504),
    session=None,
):
    session = session or requests.Session()
    retry = Retry(
        total=retries,
        read=retries,
        connect=retries,
        backoff_factor=backoff_factor,
        status_forcelist=status_forcelist,
    )
    adapter = HTTPAdapter(max_retries=retry)
    session.mount('http://', adapter)
    session.mount('https://', adapter)
    return session


retries = 10
#potential_commits = []
now = datetime.datetime.now()


def get_commits(githubUser, currentRepo, qm, page, amp, sh_string, last_com, page_number, branch_sha, potential_commits, current_token):

    #token = os.getenv('GITHUB_TOKEN', token)
    page_number += 1

    if page_number == 1:
        first_100_commits = "https://api.github.com/repos/" + githubUser + "/" + \
            currentRepo+"/commits" + qm + page + amp + sh_string + branch_sha
    else:
        first_100_commits = "https://api.github.com/repos/" + githubUser + \
            "/"+currentRepo+"/commits" + qm + page + amp + sh_string + last_com

    # response = r.get(first_100_commits, headers={'Authorization': 'token {}'.format(token)})

    t0 = time.time()

    response = requests_retry_session().get(first_100_commits, headers={
        'Authorization': 'token {}'.format(current_token)})
    if response.status_code != 200:
        tokens_status[current_token] = False
        current_token = select_access_token(current_token)
        response = requests_retry_session().get(first_100_commits, headers={
            'Authorization': 'token {}'.format(current_token)})

    if response.status_code != 200:
        tokens_status[current_token] = False
        current_token = select_access_token(current_token)
        response = requests_retry_session().get(first_100_commits, headers={
            'Authorization': 'token {}'.format(current_token)})

    if response.status_code != 200:
        tokens_status[current_token] = False
        current_token = select_access_token(current_token)
        response = requests_retry_session().get(first_100_commits, headers={
            'Authorization': 'token {}'.format(current_token)})

    if response.status_code != 200:
        tokens_status[current_token] = False
        current_token = select_access_token(current_token)
        response = requests_retry_session().get(first_100_commits, headers={
            'Authorization': 'token {}'.format(current_token)})

    first_100_commits = json.loads(response.text)

    if len(first_100_commits) == 1:
        return None
    for i, commit in enumerate(first_100_commits):
        #print('Total number of fetched commits: {}, page:{}, branch: {}'.format(i, page_number, branch_sha))

        _rule = r"(bug|Bug|defect|Defect|Fault|fault|fix|Fix|fixing|Fixing)"

        _match = re.findall(_rule, commit['commit']['message'])
        _date = commit['commit']['committer']['date']
        sdate = _date.split('-')
        if _match:
            print('got one!')
            _date = commit['commit']['committer']['date']
            sdate = _date.split('-')
            # if any(commit['html_url'] in s for s in commit_data) == False:
            potential_commits.append(commit['html_url'])
            # else:
            # print('Already Extracted')
    #   print('I found a relevant commit from:  {}'.format(int(sdate[0])))
    #   if ending_date is None:
    #     if int(sdate[0]) >= start_date and int(sdate[0]) <= now.year:
    #         print(len(potential_commits))

    #   else:
    #     if int(sdate[0]) >= start_date and int(sdate[0]) <= ending_date:
    #         print(len(potential_commits))
    #         potential_commits.append(commit['html_url'])

        if i == len(first_100_commits)-1:
            last_com = commit['sha']
            get_commits(githubUser, currentRepo, qm, page, amp, sh_string,
                        last_com, page_number, branch_sha, potential_commits, current_token)


def search_comit_data(c, commit_data):
    t = []

    for item in commit_data:
        temp = item.split('/')
        t.append('/' + temp[3] + '/' + temp[4] + '/')

    r_prime = c.split('/')
    x = '/' + r_prime[3] + '/' + r_prime[4] + '/'
    if any(x in s for s in t):
        return True
    else:
        return False


def select_access_token(current_token):
    x = ''
    if all(value == False for value in tokens_status.values()):
        for k, v in tokens_status.items():
            tokens_status[k] = True

    for k, v in tokens.items():
        if tokens_status[v] != False:
            x = v
            break
    current_token = x
    return current_token


def extractCommits(c):
    current_token = tokens[0]
    # for root, dir, files in os.walk('./repos_phase1_uniques'):
    #     for file in files:
    #         current_file = os.path.join(root, file)
    #         #curren_commit = os.path.join('./commits', file)
    #         data = read_txt(current_file)

    #         # commit_data = read_txt(curren_commit)

    #         for j, c in enumerate(data):
    x = []
    # if search_comit_data(c, commit_data) == False:
    potential_commits = []
    #print('Repo {0}/{1}/{2} The token is '.format(j, len(data), current_token))
    r_prime = c.split('/')

    qm = '?'
    page = 'per_page='+str(100)
    amp = '&'
    sh_string = "sha="

    branchLink = "https://api.github.com/repos/{0}/{1}/branches".format(
        r_prime[3], r_prime[4])

    t0 = time.time()
    response = requests_retry_session().get(
        branchLink, headers={'Authorization': 'token {}'.format(current_token)})
    if response.status_code != 200:
        tokens_status[current_token] = False
        current_token = select_access_token(current_token)
        response = requests_retry_session().get(
            branchLink, headers={'Authorization': 'token {}'.format(current_token)})

    if response.status_code != 200:
        tokens_status[current_token] = False
        current_token = select_access_token(current_token)
        response = requests_retry_session().get(
            branchLink, headers={'Authorization': 'token {}'.format(current_token)})

    if response.status_code != 200:
        tokens_status[current_token] = False
        current_token = select_access_token(current_token)
        response = requests_retry_session().get(
            branchLink, headers={'Authorization': 'token {}'.format(current_token)})

    if response.status_code != 200:
        tokens_status[current_token] = False
        current_token = select_access_token(current_token)
        response = requests_retry_session().get(
            branchLink, headers={'Authorization': 'token {}'.format(current_token)})

    branches = json.loads(response.text)

    # if branches != []:
    try:
        selected_branch = random.choice(branches)
        branch_sha = selected_branch['commit']['sha']

        page_number = 0

        first_100_commits = "https://api.github.com/repos/" + \
            r_prime[3] + "/"+r_prime[4]+"/commits" + \
            qm + page + amp + sh_string + branch_sha

        t0 = time.time()

        response = requests_retry_session().get(first_100_commits, headers={
            'Authorization': 'token {}'.format(current_token)})
        if response.status_code != 200:
            tokens_status[current_token] = False
            current_token = select_access_token(current_token)
            response = requests_retry_session().get(first_100_commits, headers={
                'Authorization': 'token {}'.format(current_token)})

        if response.status_code != 200:
            tokens_status[current_token] = False
            current_token = select_access_token(current_token)
            response = requests_retry_session().get(first_100_commits, headers={
                'Authorization': 'token {}'.format(current_token)})

        if response.status_code != 200:
            tokens_status[current_token] = False
            current_token = select_access_token(current_token)
            response = requests_retry_session().get(first_100_commits, headers={
                'Authorization': 'token {}'.format(current_token)})

        if response.status_code != 200:
            tokens_status[current_token] = False
            current_token = select_access_token(current_token)
            response = requests_retry_session().get(first_100_commits, headers={
                'Authorization': 'token {}'.format(current_token)})

        first_100_commits = json.loads(response.text)

        if len(first_100_commits) >= 100:
            last_com = first_100_commits[-1]['sha']
            get_commits(r_prime[3], r_prime[4], qm, page, amp, sh_string, last_com,
                        page_number, branch_sha, potential_commits, current_token)

            
            if not os.path.isdir('./'+r_prime[4]):
                os.makedirs('./'+r_prime[4])

            with open('./'+r_prime[4]+'/'+'buggy_commits.txt', 'a') as f:
            #with open('./'+r_prime[4]+file, 'a') as f:
                for item in potential_commits:
                    f.write("%s\n" % item)
        else:
            _rule = r"(bug|Bug|defect|Defect|Fault|fault|fix|Fix|fixing|Fixing)"

            try:
                temp = []
                for i, com in enumerate(first_100_commits):
                    #print('Total number of fetched commits: {}, page:{}, branch: {}'.format(i, page_number, branch_sha))
                    _match = re.findall(_rule, com['commit']['message'])
                    if _match:
                        x = requests_retry_session().get(com['url'])
                        x = json.loads(x.text)
                        print('got one!')
                        # if any(com['html_url'] in s for s in commit_data) == False:
                        temp.append(com['html_url'])
                        # else:
                        #print('Already Extracted')
            except Exception as e:
                print(e)

            if not os.path.isdir('./'+r_prime[4]):
                os.makedirs('./'+r_prime[4])

            with open('./'+r_prime[4]+'/'+'buggy_commits.txt', 'a') as f:
                for item in temp:
                    f.write("%s\n" % item)
    except Exception as e:
        print(e)
# 13915
# if __name__ == "__main__":

  # main()
