import os
import subprocess
import re


def git_logs(repository_path):
    os.chdir(repository_path)
    result = str(subprocess.run(f'git log --reverse', capture_output=True, shell=True).stdout, 'utf-8')
    re_log = r'commit (.*)\nAuthor: (.*) <(.*)>\nDate:   (.*)\n\n    (.*)\n'
    matches = re.findall(re_log, result)
    return [{'id': match[0], 'name': match[1], 'email': match[2], 'date': match[3], 'message': match[4]} for match in matches]


def git_checkout_to_commit(repository_path, commit_id):
    print(repository_path)
    os.chdir(repository_path)
    subprocess.run(f'git checkout {commit_id}', shell=True)


def git_commit(repository_path, email, message, date):
    os.chdir(repository_path)
    subprocess.run('git add *', shell=True)
    subprocess.run(f'git commit -a -m "{message}" --date "{date}"', shell=True)


def git_init(repository_path):
    os.chdir(repository_path)
    subprocess.run('git init', shell=True)
