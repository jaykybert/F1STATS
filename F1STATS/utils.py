import datetime
import re


def date_format(d):
    """ Format the date appropriately for output.

    :param d: String Date - I.E. 2019-12-31
    :return: String Date - I.E. Tuesday 31 December, 2019
    """
    dt = datetime.datetime.strptime(d, '%Y-%m-%d')
    return dt.strftime('%A %d %B, %Y')


def return_datetime(d):
    """ Return the datetime object of the passed date.

    :param d: String Date - I.E 2019-12-31
    :return: Datetime Date in the same format.
    """
    return datetime.datetime.strptime(d, '%Y-%m-%d')


def current_date():
    """ Return the current date (and time).

    :return: Current datetime object.
    """
    return datetime.datetime.now()


def total_seconds(time):
    """ Get a lap time in the form of seconds.

     :param time: Lap time - I.E. 1:27.809
     :return: The lap time in seconds."""

    """ I used a regular expression for this due to the (very unlikely) possibility
     that a lap is 10 minutes or more, otherwise string slicing would work. """
    lap_regex = re.compile(r'(\d+):(\d\d).(\d\d\d)')

    mo = lap_regex.search(time)

    mins = int(mo.group(1))
    secs = int(mo.group(2))
    milli = int(mo.group(3))
    mins *= 60
    milli /= 1000

    return mins + secs + milli
