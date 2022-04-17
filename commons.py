import math
import os.path
import time
import inspect
import datetime
from datetime import datetime, timedelta
import logging
from enum import Enum
from typing import Union


def init_logging(log_file='.log'):
    logging.basicConfig(format='%(asctime)s %(levelname)s {%(module)s} [%(funcName)s] %(message)s',
                        datefmt='%Y-%m-%d,%H:%M:%S', level=logging.INFO, filename=log_file)


class LogType(Enum):
    warn = 1
    error = 2
    info = 3


def print_and_log_statement(message, logging_type=LogType.info, line_no=''):
    message = message + " (line " + line_no + " )"
    print(message)
    if logging_type is LogType.error:
        logging.error(message)
    elif logging_type is LogType.warn:
        logging.warning(message)
    else:
        logging.info(message)


def get_tuple_index_values_as_list(tuple_list: list, idx: int, return_as="LIST"):
    """
        In list of tuples get only the values of specified index
        eg. get idx at 2 [(1,2,3,5),('hey','yoyo','cool','nay']
        will return [3,'cool']
        We assume all tuple sizes are uniform
        PrintAndLogMsg(inspect.currentframe().f_code.co_name)
        Return Types:
            - LISTSTR: encapuslates values as string and return list
            - LIST
            - STR
            - STRENC
    """
    values_at_idx = []
    # make sure the tuple size > idx
    if len(tuple_list[0]) > idx:
        for row in tuple_list:
            if return_as == 'LISTSTR':
                # useful for string encapsulation of integer IDs
                values_at_idx.append(str(row[idx]))
            else:
                values_at_idx.append(row[idx])
        if return_as == 'LISTSTR':
            return values_at_idx
        if return_as == 'LIST':
            return values_at_idx
        elif return_as == 'STR':  # string with no encaps on values handy for integers
            # eg: csv string: "1,2,4,6,9"
            return ','.join("{0}".format(w) for w in values_at_idx)
        elif return_as == 'STRENC':  # string encapsulated values
            # eg: csv string: "'1','2','4','6','9'"
            # repr_str = ",".join(repr(w) for w in dup_serial_numbers)
            return ','.join("'{0}'".format(w) for w in values_at_idx)
        else:
            return False
    else:
        return False


def purge_empties_in_dict(my_dict, exceptions=None):
    if exceptions is None:
        exceptions = []
    for k, v in my_dict.items():
        if (k is None or v is None) and k not in exceptions:
            my_dict.pop(k)
    return my_dict


def line_info():
    f = inspect.currentframe()
    i = inspect.getframeinfo(f.f_back)
    return f"line {i.lineno} -> def {i.function}() -> {i.filename}"


def dict_to_list(dict_object):
    if type(dict_object) is dict:
        return [dict_object]
    else:
        return dict_object


def get_time_now(fmt='%H:%M%:%S', minutes_offset=0):
    return get_todays_date(fmt, minutes_offset)


def get_todays_date(fmt='%Y-%m-%d', minutes_offset=0):
    dt = datetime.now()
    if minutes_offset != 0:
        dt = dt + timedelta(minutes=minutes_offset)
        # if str(time_delta)[0] == '-':
        #     dt = dt - datetime.timedelta(time_delta)
        # else:
        #     dt = dt + datetime.timedelta(time_delta)
    return dt.strftime(fmt)


def stringify(value, escape=False):
    if escape:
        value = value.replace("'", "\\'")
    return f"'{value}'"


def get_quarterly_id(yyyy, mm, dd):
    # dt = datetime.now()
    year = yyyy
    # useful if wanting to compare years in past or future
    # if int(yyyy) != year:
    #     year = yyyy
    # yyyy / mm /dd
    cmp_date = datetime(int(yyyy), int(mm), int(dd))
    if (cmp_date >= datetime(int(year), 1, 1)) and (cmp_date <= datetime(int(year), 3, 31)):
        return 1
    elif (cmp_date >= datetime(int(year), 4, 1)) and (cmp_date <= datetime(int(year), 6, 30)):
        return 2
    elif (cmp_date >= datetime(int(year), 7, 1)) and (cmp_date <= datetime(int(year), 9, 30)):
        return 3
    elif (cmp_date >= datetime(int(year), 10, 1)) and (cmp_date <= datetime(int(year), 12, 31)):
        return 4


def get_calender_months():
    return ["Unknown",
            "January",
            "February",
            "March",
            "April",
            "May",
            "June",
            "July",
            "August",
            "September",
            "October",
            "November",
            "December"]


def _convert_unix_timestamp_to_readable_date(unix_time, dt_format='%Y-%m-%d', return_nothing_on_err=True):
    the_date = ''
    is_err = False
    try:
        the_date = datetime.fromtimestamp(unix_time).strftime(dt_format)
    except ValueError:
        the_date = "ERR"
        is_err = True
        # if return_nothing_on_err:
        #     return None
        # else:
        #     return False
    finally:
        if is_err:
            if return_nothing_on_err:
                return None
            else:
                return the_date
        else:
            return the_date


def date_time_converter(run_date, dt_fmt='%Y-%m-%d'):
    rd = tuple
    try:
        if not run_date or len(str(run_date)) < 3:
            print("Error Empty Date Value!")
            return False, False
        if run_date is not None and int(run_date) > 100:
            readable_dt = _convert_unix_timestamp_to_readable_date(int(run_date), dt_fmt)
            rd = (run_date, readable_dt)
        else:
            # valid date string return as is
            rd = (run_date, run_date)
    except ValueError as e:
        # eg: '2018-10-09T16:43:07'
        # sometimes the date is formatted like this 2019-08-24T03:51:43
        try:
            time_split = str(run_date).split('T')
            dt_string = time_split[0]
            readable_dt = dt_string
            run_date = time.mktime(datetime.strptime(dt_string, "%Y-%m-%d").timetuple())
            rd = (run_date, readable_dt)
        except Exception as e:
            print(f"ERR: {e}")
            print(f"run date == {run_date}")
            return False, False
    except Exception as e:
        print(f"ERR: {e} {run_date}")
        print(f"run date == {run_date}")
        return False, False
        # run_date, readable_dt
    return rd


def append_file_ext(file_name: str, extension: str):
    ext = os.path.splitext(file_name)[1]
    if ext == extension:
        return file_name
    else:
        return file_name + "." + extension


def get_progress(size, count):
    r = range(1, 100)
    for n in r:
        if math.floor(size * (n / 100)) == count:
            return n
    return 0


class Progressor:
    """ USAGE:
        progress = commons.Progressor(size=max_records, Label='progress bar')
        for idx, row in enumerate(rows):
            # do some processing here ...
            progress.update(idx)
    """
    def __init__(self, size: int, label: str, start=False):
        self.has_zero_index = True
        self.first_time_thru = True
        self.total_size = size
        self.subject = label
        self.prog_timer = ProcTimer(start_timer=True)
        self.time_remaining_lbl = ''
        if start:
            self.start()

    def start(self):
        self.prog_timer.start_lap()

    def stop(self):
        self.prog_timer.stop_lap()

    def total_time(self):
        return self.prog_timer.get_total_duration()

    def _get_progress_number(self, count):
        r = range(1, 100)
        for n in r:
            if math.floor(self.total_size * (n / 100)) == count:
                return n
        return 0

    def _print_progress_bar(self, iteration, prefix='', suffix='', decimals=0, length=100, fill='█', printEnd="\r"):
        """
        Call in a loop to create terminal progress bar
        src: https://stackoverflow.com/a/34325723
        @params:
            iteration   - Required  : current iteration (Int)
            prefix      - Optional  : prefix string (Str)
            suffix      - Optional  : suffix string (Str)
            decimals    - Optional  : positive number of decimals in percent complete (Int)
            length      - Optional  : character length of bar (Int)
            fill        - Optional  : bar fill character (Str)
            printEnd    - Optional  : end character (e.g. "\r", "\r\n") (Str)
        """
        percent = ("{0:." + str(decimals) + "f}").format(100 * (iteration / float(self.total_size)))
        filledLength = int(length * iteration // self.total_size)
        bar = fill * filledLength + '-' * (length - filledLength)
        print(f'\r{prefix} |{bar}| {percent}% {suffix}', end=printEnd)
        # Print New Line on Complete
        if iteration == self.total_size:
            print(' ')

    def update(self, done):
        self.prog_timer.stop_lap()
        progress = 1
        lapped_secs = self.prog_timer.get_lap_time(raw_seconds=True)
        secs_remain = (self.total_size - done) * lapped_secs
        t_running_secs = self.prog_timer.get_elapsed_time(raw_seconds=True)
        if self.first_time_thru:
            print(f"Start {self.subject} {self.total_size} rows ...")
            self.first_time_thru = False
            # check if we start at 0 index
            if done == 0:
                self.has_zero_index = True
            else:
                self.has_zero_index = False
        if self.has_zero_index:
            done = done + 1
        if done == self.total_size:
            self.time_remaining_lbl = ''
            print(f"... Completed {self.subject} rows ({self.prog_timer.get_total_duration()})\n")
            progress = 0
        else:
            progress = self._get_progress_number(done)
            if progress in [1, 3, 5, 10, 15, 20, 25, 30, 35, 40, 45, 50, 55, 60, 65, 70, 75, 80, 85, 87, 89, 90, 92, 95,
                            96, 97, 98, 99]:
                # secs_remain = lapped_secs * left
                if secs_remain > 0.09:
                    t_remain = "-" + self.prog_timer.get_nice_time_format(secs_remain, digital_format=True)
                    t_running = self.prog_timer.get_nice_time_format(t_running_secs, digital_format=True)
                    self.time_remaining_lbl = "[ " + t_remain + " / " + t_running + " ]"
                    # finished with showing progress bar
            if done >= (self.total_size - 3):
                self.time_remaining_lbl = '                                             '
            if CONFIG.SHOW_PROGRESSOR:
                self._print_progress_bar(done + 1, suffix=str(self.time_remaining_lbl))
                # print(str(p_time))
            # self.time_list.append(remaining_secs)
        if progress > 0:
            self.prog_timer.start_lap()


class Day(Enum):
    Sunday = 'Sunday'
    Monday = 'Monday'
    Tuesday = 'Tuesday'
    Wednesday = 'Wednesday'
    Thursday = 'Thursday'
    Friday = 'Friday'
    Saturday = 'Saturday'
    _weekend = [Saturday, Sunday]
    _sunday_to_thursday = [Sunday, Monday, Tuesday, Wednesday, Thursday]
    _work_week = [Monday, Tuesday, Wednesday, Thursday, Friday]
    _every_day = [Monday, Tuesday, Wednesday, Thursday, Friday, Saturday, Sunday]

    @staticmethod
    def BetweenSundayAndThursday():
        return [Day._sunday_to_thursday.value][0]

    @staticmethod
    def WorkWeek():
        return [Day._work_week.value][0]

    @staticmethod
    def Weekend():
        return [Day._weekend][0]

    @staticmethod
    def Everyday():
        return [Day._every_day][0]


class SkedTime:
    def __init__(self, skip_time_checks=False):
        # freeze current time at constructor
        self.current_time = get_time_now('%H:%M')
        # useful for running all scripts without checking time
        self.skip_time_checks = skip_time_checks

    def is_in_(self, times_list: list) -> bool:
        if self.skip_time_checks:
            return True
        for time_str in times_list:
            if self.is_(time_str):
                return True
        return False

    def is_(self, time_str: str) -> bool:
        if self.skip_time_checks:
            return True
            # eg. if time is at "15:15"
        system_hour: Union[str, int]
        system_minute: Union[str, int]
        system_hour, system_minute = str(self.current_time).split(":")
        time_values = time_str.split(":")
        sked_hour: Union[str, int]
        sked_minute: Union[str, int]
        if len(time_values) == 2:
            sked_hour, sked_minute = time_values
            if sked_hour == '':
                sked_hour = 0
        elif len(time_values) == 1:
            sked_hour = time_values[0]
            sked_minute = 0
        else:
            raise ValueError("Value entered cannot be parsed as time")
        if int(system_hour) == int(sked_hour) and int(system_minute) == int(sked_minute):
            return True
        else:
            return False


class ProcTimer:
    def __init__(self, start_timer=True):
        self._time_stop = 0.0
        self._time_start = 0.0
        self._lap_start = 0.0
        self._lap_stop = 0.0
        if start_timer:
            self.start_timer()

    def start_timer(self):
        self._time_start = float(time.perf_counter())

    def stop_timer(self):
        self._time_stop = float(time.perf_counter())

    def start_lap(self):
        self._lap_start = float(time.perf_counter())

    def stop_lap(self):
        self._lap_stop = float(time.perf_counter())

    def get_elapsed_time(self, raw_seconds=False):
        time_now = float(time.perf_counter())
        return self.get_duration(self._time_start, time_now, raw_seconds)

    def get_lap_time(self, raw_seconds=False):
        return self.get_duration(self._lap_start, self._lap_stop, raw_seconds)

    def get_total_duration(self):
        self.stop_timer()
        dur = self.get_duration(self._time_start, self._time_stop)
        return dur

    def get_duration(self, start_time, end_time, get_raw_seconds=False):
        duration_secs = round(end_time - start_time, 0)
        # take seconds to 3 decimal places if seconds less than 1
        # if 1.0 > duration_secs > 0.0:
        if duration_secs == 0.0:
            duration_secs = round(end_time - start_time, 3)
        if get_raw_seconds:
            return abs(duration_secs)
        else:
            return self.get_nice_time_format(abs(duration_secs))

    def get_nice_time_format(self, duration_secs, digital_format=False):
        if duration_secs > 60.0:  # if over 1 minute
            hrs_label = ""
            digital_hrs = "00:"
            if duration_secs >= 3600:
                hrs_label = "%Hhrs "
                digital_hrs = "%H:"
            return_time = time.strftime(hrs_label + '%Mmins %Ssecs', time.gmtime(duration_secs))
            if digital_format:
                return_time = time.strftime(digital_hrs + '%M:%S', time.gmtime(duration_secs))
        else:
            return_time = f"{round(duration_secs, 2)} second(s)"
            if digital_format:
                return_time = f"00:00:{round(duration_secs, 2)}"
        return return_time

    def get_end_time_msg(self):
        dur = self.get_total_duration()
        return f"Finished in {dur}"

    def print_end_time_msg(self, append_custom_message=None):
        print(self.get_end_time_msg())
        if append_custom_message is not None:
            print(str(append_custom_message))
