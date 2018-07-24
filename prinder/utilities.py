import datetime

def time_delta(pull):
    return datetime.datetime.now(pull.created_at.tzinfo) - pull.created_at

def segregate_pr_by_repo(pull_requests):
    repos_pr = dict()
    for pull in pull_requests:
        repo_name = pull.repository.name.encode('utf-8')
        prs = repos_pr.get(repo_name, [])
        prs.append(pull)
        repos_pr[repo_name] = prs
    return repos_pr

def set_debug_level(logger, debug):
    if debug:
        logger.setLevel('DEBUG')
