from datetime import datetime
from datetime import timedelta
import random
import argparse
import gitUtils
import fileUtils
import contributions

# original_repository_path = 'E:/git_history/golang-test-original'
# new_repository_path = 'E:/git_history/golang-test'


def add_rand_time(d):
    rand_hours = random.randint(1, 4)
    rand_minutes = random.randint(1, 59)
    rand_seconds = random.randint(1, 59)
    return d+timedelta(hours=rand_hours, minutes=rand_minutes, seconds=rand_seconds)


def start_git_copy(src, dst, fill, username, start_date):
    empty_contribution_dates = None
    if fill is not None and username is not None:
        empty_contribution_dates = contributions.get_empty_contribution_dates(username, start_date)
        if start_date is not None:
            start_date = datetime.strptime(start_date, '%Y-%m-%d')
            empty_contribution_dates = list(filter(lambda x: x > start_date, empty_contribution_dates))
            i = 0
            temp = list(())
            while i < len(empty_contribution_dates):
                temp.append(empty_contribution_dates[i])
                i += random.randint(1, 4)
            empty_contribution_dates.clear()
            empty_contribution_dates.extend(temp)
    gitUtils.git_checkout_to_commit(src, 'master')
    log_data = gitUtils.git_logs(src)
    fileUtils.reset_directory(dst)
    gitUtils.git_init(dst)
    daily_log_cnt = 10
    last_log_date = None
    log_counter = 0
    total_log_count = 0 if empty_contribution_dates is None else len(empty_contribution_dates)
    for log in log_data:
        print(f'processing {log["id"]}')
        gitUtils.git_checkout_to_commit(src, log['id'])
        fileUtils.remove_files(dst)
        fileUtils.copy_files(src, dst)
        if empty_contribution_dates is None:
            gitUtils.git_commit(dst, log['email'], log['message'], log['date'])
        else:
            if log_counter >= total_log_count:
                print('ran out of empty contribution date')
                exit(0)
            if last_log_date is None or daily_log_cnt <= 0:
                last_log_date = empty_contribution_dates[log_counter]
                log_counter += 1
                daily_log_cnt = random.randint(1, 10)
            last_log_date = add_rand_time(last_log_date)
            s_log_date = last_log_date.strftime('%c')
            gitUtils.git_commit(dst, log['email'], log['message'], s_log_date)
            daily_log_cnt -= 1


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='''
Copy one repository to another replacing the git user name.
    ''')
    parser.add_argument('--src', help='original repository path', required=True)
    parser.add_argument('--dst', help='destination directory', required=True)
    parser.add_argument('--fill', help='fill non contribution dates', required=False)
    parser.add_argument('--user', help='github user name to search contribution', required=False)
    parser.add_argument('--startdate', help='github contribution skip date e.g: 2015-08-15', required=False)
    args = parser.parse_args()

    start_git_copy(args.src, args.dst, args.fill, args.user, args.startdate)
