import time

from sakailib import SakaiAuth
from sakailib.exceptions import NoSuchItem


def parse_time(time_str: str):
    """
    parse time displayed on page to timestamp
    :param time_str: time displayed on page
    :return: timestamp
    """
    if 'am' in time_str or 'pm' in time_str:
        mon, day_plus_comma, year, hr_plus_min, am_pm = time_str.split(' ')
        if len(day_plus_comma) == 2:
            day_plus_comma = '0' + day_plus_comma
        if len(hr_plus_min) == 4:
            hr_plus_min = '0' + hr_plus_min
        am_pm = am_pm.upper()
        time_str = ' '.join([mon, day_plus_comma, year, hr_plus_min, am_pm])
        format = '%b %d, %Y %I:%M %p'
    elif '上午' in time_str or '下午' in time_str:
        time_str = time_str.replace('上午', 'AM ').replace('下午', 'PM ')
        year_month_day, am_pm, hr_plus_min = time_str.split(' ')
        if len(hr_plus_min) == 4:
            hr_plus_min = '0' + hr_plus_min
        time_str = ' '.join([year_month_day, am_pm, hr_plus_min])
        format = '%Y-%m-%d %p %I:%M'
    else:
        raise ValueError('Unknown time format')
    return time.mktime(time.strptime(time_str, format))


def main():
    sid = input('Enter SID: ')
    pwd = input('Enter password: ')
    sakai = SakaiAuth(sid, pwd)
    print('Login successful')
    sites = sakai.get_sites_list()
    assignments = list()
    for site in sites:
        try:
            for a in site.assignment_list():
                s = a['status']
                st = parse_time(a['start_date'])
                dt = parse_time(a['due_date'])
                nt = time.time()
                if 'Not Started' in s or 'Draft' in s or '进行中' in s or '尚未提交' in s:  # unfinished assignments
                    if st <= nt:  # has started
                        if dt > nt:  # not due
                            assignments.append([site._name, a['title'], dt])
        except NoSuchItem:
            pass
    assignments.sort(key=lambda _assignment: _assignment[2])
    for assignment in assignments:
        print(' | '.join(assignment[:2] + [time.ctime(assignment[2])]))


if __name__ == '__main__':
    main()
