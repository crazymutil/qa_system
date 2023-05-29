from datetime import datetime

import timeago
def number_split(num):
    """
    数字格式化
    :param num:12345678
    :return:12，345，678
    """
    "{:,}千位符格式化"
    return '{:,}'.format(int(num))


def dt_format_show(dt):
    """
    日期和时间格式化显示
    :param dt: datetime 时间
    :return:
    """
    now = datetime.now()
    return timeago.format(dt, now, 'zh_CN')
