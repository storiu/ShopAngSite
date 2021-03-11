from urllib import request
import re
from datetime import datetime


def get_years(username):
    user_page_result = str(request.urlopen(f'https://github.com/{username}').read(), 'utf8')
    return re.findall(r'year-link-(\d+)', user_page_result)


def get_year_contributions(username, year):
    contributions_raw_html = str(request.urlopen(f'https://github.com/users/{username}/contributions?from={year}-12-01&to={year}-12-31').read(), 'utf8')
    daily_contributions_raw = re.findall(r'<rect.+data-count="\d+" data-date=".+" data-level=.*></rect>', contributions_raw_html)
    result = []
    for daily_contribution_raw in daily_contributions_raw:
        match = re.match(r'<rect.+data-count="(\d+)" data-date="(.+)" data-level=.*></rect>', daily_contribution_raw)
        count = int(match[1])
        date = datetime.strptime(match[2], '%Y-%m-%d')
        result.append({'date': date, 'count': count})
    return result


def get_empty_contribution_dates(username, start_date):
    years = get_years(username)
    start_year = int(re.match(r'(\d+)-\d+-\d+', start_date)[1])
    first_available_year = int(years[-1])
    if start_year < first_available_year:
        years = [*[str(y) for y in range(start_year, first_available_year)], *years]
    contributions = []
    today = datetime.now()
    for year in years:
        year_contributions = get_year_contributions(username, year)
        empty_contributions = filter(lambda x: x['count'] == 0 and x['date'].weekday() != 6 and x['date'] < today and not (x['date'].month == 1 and x['date'].day <= 10), year_contributions)
        empty_contribution_dates = map(lambda x: x['date'], empty_contributions)
        contributions.extend(empty_contribution_dates)
    
    return contributions
