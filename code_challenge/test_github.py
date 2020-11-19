from code_challenge.base.github_api import GitApi

if __name__ == '__main__':
    print('Question - 2')
    git_repo = GitApi(url='https://api.github.com/users/', owner='SeleniumHQ',
                      access_token='05c9d370a91d79aa7a1cc63eb66bb4032ef9bc84')
    # For debug - print the number of repository
    git_repo.get_total_repo()
    # answer point a
    print('a. Total open issues across all repositories are %s' % git_repo.get_total_issue())
    # answer b. Sort the repositories by date updated in descending order.
    print('b. Sort the repositories by date updated in descending order.')

    print(git_repo.get_sorted_lst(bShow=True))
    print('Note b. There is an issue that the updated date returned by api does not match with one on '
          'https://github.com/SeleniumHQ or it is different meaning')

    # answer c
    print('c. The most watchers repository is %s' % git_repo.get_most_watcher_repo())


