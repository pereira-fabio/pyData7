# this was provided by the teacher

import difflib
import os
from gitpython import Repo
from typing import List, Dict, Generator, Iterable


def retrieving_file_from_specific_commit(repo: Repo, commit: str, path: str) -> str:
    """
    Function to return a file from a specific commit

    Parameters:
        repo (Repo): repository object
        commit (str): commit string
        path (str): path of the file to load

    Returns:
        the content of the file (str)
    """
    return repo.git.show("{}:{}".format(commit, path))


def list_of_commit_impacting_a_file(
    repo: Repo, path: str, before_commit: str = "HEAD"
) -> List[str]:
    """
    Function that returns the list of commit impacting a file

    Parameters:
        repo (Repo): repository object
        path (str): path of the file
        before_commit (str): optional parameter corresponding to a the last commit to consider

    Returns:
        the list of abbreviated commit
    """
    head = repo.head.commit.hexsha
    repo.head.reference = repo.commit(before_commit)
    result = repo.git.log("--follow", "--pretty=format:%h", path).splitlines("\n")
    repo.head.reference = head
    return result


def previous_commit_impacting_a_file(
    repo: Repo, path: str, before_commit: str = "HEAD"
) -> str:
    """
    Function that returns the last commit impacting a file

    Parameters:
        repo (Repo): repository object
        path (str): path of the file
        before_commit (str): optional parameter corresponding to a the last commit to consider

    Returns:
        abbreviated hash of the last commit
    """
    result = list_of_commit_impacting_a_file(repo, path, before_commit)
    if len(result) > 0:
        return result[0]
    else:
        return ""


def blame(repo: Repo, path: str, at_commit: str = "HEAD") -> Iterable[str]:
    """
    Function that returns the list of commits appearing within a git blame

    Parameters:
        repo (Repo): repository object
        path (str): path of the file
        at_commit (str): optional parameter corresponding to the last commit to consider

    Returns:
        list of abbreviated hash
    """
    return (commit[0].hexsha for commit in repo.blame(at_commit, path, True))


def blame_number_of_dev(repo: Repo, path: str, at_commit: str = "HEAD") -> int:
    """
    Function that returns the number of dev involved in a file at the current commit

    Parameters:
        repo (Repo): repository object
        path (str): path of the file
        at_commit (str): optional parameter corresponding to the last commit to consider

    Returns:
        number of devs currently involved on the current version of the file
    """
    return len({commit[0].author.email for commit in repo.blame(at_commit, path, True)})


def dev_history_of_a_file(
    repo: Repo, path: str, before_commit: str = "HEAD"
) -> Dict[str, int]:
    """
    Function that returns the developer history of a file before a given commit

    Parameters:
        repo (Repo): repository object
        path (str): path of the file
        before_commit (str): optional parameter corresponding to the last commit to consider

    Returns:
        a dictionary containing the following information:
            * numberOfDevs (int)
            * numberOfChanges (int)
            * numberOfCurrentDeveloper (int)
    """
    commits = list_of_commit_impacting_a_file(repo, path, before_commit)
    commits_size = len(commits)
    authors = len({repo.commit(commit).author.email for commit in commits})
    current_number_of_dev = blame_number_of_dev(repo, path, before_commit)
    return {
        "numberOfDevs": authors,
        "numberOfChanges": commits_size,
        "numberOfCurrentDev": current_number_of_dev,
    }


def delta_file(repo: Repo, path: str, before_commit: str = "HEAD") -> Dict[str, int]:
    """
    Function that returns the delta history of a file before a given commit

    Parameters:
        repo (Repo): repository object
        path (str): path of the file
        before_commit (str): optional parameter corresponding to the last commit to consider

    Returns:
        a dictionary containing the following information:
            * addedLines (int)
            * deletedLines (int)
    """
    commits = list_of_commit_impacting_a_file(repo, path, before_commit)
    files = [
        retrieving_file_from_specific_commit(repo, path, commit) for commit in commits
    ]
    new_file, old_file = None, None
    d = difflib.Differ()
    added, deleted = 0, 0
    for file in files:
        if new_file is None:
            new_file = file.splitlines(keepends=True)
        else:
            old_file = new_file
            new_file = file.splitlines(keepends=True)
            for line in d.compare(old_file, new_file):
                if line.startswith("+ "):
                    added += 1
                elif line.startswith("- "):
                    deleted += 1

    return {"addedLines": added, "deletedLines": added}


def list_of_modified_files(repo: Repo, commit: str) -> Iterable[str]:
    """
    Function that returns the list of files modified by a given commit

    Parameters:
        repo (Repo): repository object
        commit (str): commit hash

    Returns:
        iterable list of file (str)
    """
    current_commit = repo.commit(commit)
    previous_commit = current_commit.parents[0]
    diff_index = previous_commit.diff(current_commit)
    for diff in diff_index:
        if diff.change_type == "M":
            yield diff.b_path


def commit_message(repo: Repo, commit: str) -> str:
    """
    Function to retrieve the message going along a given commit

    Parameters:
        repo (Repo): repository object
        commit (str): commit hash

    Returns:
        commit message (str)
    """
    return repo.commit(commit).message


def commit_time(repo: Repo, commit: str) -> int:
    """
    Function to retrieve the epoch time of a commit

    Parameters:
        repo (Repo): repository object
        commit (str): commit hash

    Returns:
        commit time (int)
    """
    return repo.commit(commit).committed_date


def update_or_init_git_repo(url: str, dest: str) -> Repo:
    """
    Function to update or init a git repository

    Parameters:
        url (str): url of the git remote repository
        dest (str): destination folder

    Returns:
        Repo object
    """
    if os.path.isdir(dest):
        repo = Repo(dest)
        origin = repo.remotes.origin
    else:
        repo = Repo.init(os.path.join(dest))
        origin = repo.create_remote("origin", url)
        origin.fetch()
        repo.create_head("master", origin.refs.master).set_tracking_branch(
            origin.refs.master
        ).checkout()
    origin.pull()
    return repo
