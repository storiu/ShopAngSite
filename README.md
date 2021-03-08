# Overview
Copy one repository to another replacing with a new git user name.(using global user configuration)

# How it works?
Github contribution graph is calculated based on the commit, pull request, code review and created issue count on a specific date.

The only way to add contribution on a past day is adding a repository which has commits signed in that day.

The aim of this repository is to clone someone else's repository copying commits one by one with a configured github user id and email.

We start with a repository to clone.

How does this script copy commits? (What is behind the hood)

1. Make an empty repository.
2. Git check out to the first commit of the repository to clone.
3. Copy all project files to the newly made repository. (excluding `.git` directory)
4. Create a git commit. Provide a commit date in a past time.
5. Git check out one commit ahead of the repository to clone.
6. Continue step 3, 4 until all the commits are passed.

Additional feature: This cli can find "empty contribution" date and make 1 ~ 3 commits with that date. 

All the above operation is done by the `main.py` with some minor config changes.

## Changing git user configuration
Refer this [link](https://git-scm.com/book/en/v2/Customizing-Git-Git-Configuration).
```bash
$ git config --global user.name "John Doe"
$ git config --global user.email johndoe@example.com
```
Replace `John Doe` and `johndoe@example.com` with your github connected account name and email.

# Requirement
* git
* python 3.6+

# Usage
* Assume git and git bash is already installed and I recommend using git bash for all the cli operations.

```bash
$ py main.py --help
Copy one repository to another replacing the git user name.

optional arguments:
  -h, --help            show this help message and exit
  --src SRC             original repository path (required)
  --dst DST             destination directory. should be an empty directory. (required)
  --fill FILL           fill non contribution dates
  --user USER           github user name to search contribution
  --startdate STARTDATE
                        github contribution skip date e.g: 2015-08-15
```

* Select a repository from your local drive or clone one from github, bitbucket or gitlab.
* Configure git user settings. (skip this step if it is already configured) You can check with this command. 
```bash
$ git config --list | grep user
```
* Run the cli with arguments.

```bash
py main.py --src </path/to/original-repository> --dst </path/to/new-repository> [--fill fill --user <username> --startdate <startdate>]
```


This cli makes 1 ~ 3 commits for no contribution dates with the provided repository when the argument `fill`, `user`, `startdate` is given.

Example:
```bash
py main.py --src e:/git_repository/auto-mart-original --dst e:/git_repository/auto-mart --fill fill --user triaton --startdate 2015-02-03
```
