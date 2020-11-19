try:
    import requests

except ImportError as imp_err:
    print('\n---{{{ Failed - ' + format(imp_err) + ' }}}---\n')


class GitApi(object):

    def __init__(self, url=None, password=None, owner=None, access_token=None):
        self.url = f"{url}{owner}/repos"
        self.password = password
        self.owner = owner
        self.access_token = access_token
        try:
            self.oSession = requests.get(self.url, headers={'Authorization': "Token " + self.access_token}).json()
            # Todo: a debug purpose to be removed
            # print(self.oSession)
        except requests.exceptions.BaseHTTPError as e:
            print(e)

    def get_total_repo(self):
        """
        This function to return the total of repository under project
        """
        # print('Number of repositories of project is %s' % len(self.session))
        iRepo = len(self.oSession)
        print('Number of repositories of project is %s' % iRepo)
        return iRepo

    def get_total_issue(self):
        """
        This function is return the total of issue for all repositories of project
        """
        iTotal_open_issue = 0
        for repo_info in self.oSession:
            # update the iTotal_open_issue
            iTotal_open_issue += repo_info['open_issues']
        return iTotal_open_issue

    def get_most_watcher_repo(self):
        """
        This function is return the name of repository which has the most watcher in project
        """
        most_watcher_repo = None
        biggest_watcher = -1
        for repo_info in self.oSession:
            # update the most_watcher_repo if watchers_count is more then old
            if biggest_watcher < repo_info['watchers_count']:
                biggest_watcher = repo_info['watchers_count']
                most_watcher_repo = repo_info['name']

        return most_watcher_repo

    def get_sorted_lst(self, bReverse=True, sort_key='updated_at', bShow=True):
        """
        This function is return the list of sorted repository

        :param bReverse: bReverse = True if descending, else accesnding
        :param sort_key: key that we want to sort (default is based on updated time of repositories)
        :return: list of sorted repository
        """
        self.oSession.sort(key=lambda x: x[sort_key], reverse=bReverse)
        lst_sorted_repos = [repo['name'] for repo in self.oSession]
        if bShow:
            for repo in self.oSession:
                print('{}:{}:{}'.format(repo['name'], sort_key, repo[sort_key]))

        return lst_sorted_repos
