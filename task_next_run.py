import sys
import datetime


def main():
    """
    This is a program for calculating when a scheduled task
    will next be run. The current time is provided as an argument
    and the schedule configuration is passed to stdin and follows
    the following structure:

       MM:HH command

    An asterisk can be used in place of minutes and/or hours which
    indicates that the task will run for all values of that field.

    Examples:
       Run a task every day at 01:30.
         30 1 /path_to_task
       Run a task at 45 minutes past every hour.
         45 * /path_to_task
       Run a task every minute.
         * * /path_to_task
       Run a task every minute from 19:00 upto and including 19:59.
         * 19 /path_to_task

    Output shows the time when the task will next be run and whether
    it will be today or tomorrow.

    Example output with an argument of 10:20:
       1:30 tomorrow - /path_to_task
       16:45 today - /path_to_task
    """
    # Check for correct number of arguments
    if len(sys.argv) != 2:
        print "Usage: task_next_run HH:MM"
        sys.exit()

    current_time = check_time_argument(sys.argv[1])

    for config_line in sys.stdin:
        config_line = check_config_line(config_line)
        next_run_time = calculate_task_next_run_time(current_time, config_line)
        print format_next_task_run_line(config_line, next_run_time)

def check_time_argument(time_argument):
    """
    Check for valid time provided as argument and return
    dictionary with hour and minute values.
    """
    try:
        parsed_time = datetime.datetime.strptime(time_argument, "%H:%M")
    except ValueError:
        print "Error: Incorrect time provided, must follow HH:MM pattern."
        sys.exit()

    current_time = dict()
    # Retrieve current time as hours and minutes
    # for later comparison with scheduled times.
    current_time['hour'] = int(parsed_time.hour)
    current_time['minute'] = int(parsed_time.minute)

    return current_time

def check_config_line(config_line):
    """
    Check configuration line is valid and return dictionary with
    hour, minute and command elements.
    """
    line = config_line.rstrip('\n') # Remove trailing new line
    line = line.split(' ') # Elements are space seperated

    if len(line) != 3:
        print 'Incorrectly formatted schedule configuration.\nHH MM /path_to_task'
        sys.exit()

    split_line = dict()
    split_line['minute'] = line[0]
    split_line['hour'] = line[1]
    split_line['command'] = line[2]

    return split_line

def calculate_task_next_run_time(current_time, scheduled):
    """
    Determine when a task will next be run and whether it
    will be today or tomorrow
    """
    if scheduled['minute'] == '*':
        if scheduled['hour'] == '*':
            return today(current_time['hour'], current_time['minute'])
        else:
            if int(scheduled['hour']) == current_time['hour']:
                return today(current_time['hour'], current_time['minute'])
            else:
                if int(scheduled['hour']) > current_time['hour']:
                    return today(scheduled['hour'], minute=0)
                else:
                    return tomorrow(scheduled['hour'], minute=0)
    elif scheduled['hour'] == '*':
        if int(scheduled['minute']) >= current_time['minute']:
            return today(current_time['hour'], scheduled['minute'])
        else:
            if current_time['hour'] == 23:
                return tomorrow(0, scheduled['minute'])
            else:
                return today(current_time['hour'] + 1, scheduled['minute'])
    elif int(scheduled['hour']) == current_time['hour']:
        if int(scheduled['minute']) >= current_time['minute']:
            return today(scheduled['hour'], scheduled['minute'])
        else:
            return tomorrow(scheduled['hour'], scheduled['minute'])
    else:
        if int(scheduled['hour']) > current_time['hour']:
            return today(scheduled['hour'], scheduled['minute'])
        else:
            return tomorrow(scheduled['hour'], scheduled['minute'])

def today(hour, minute):
    run_time = dict()
    run_time['today'] = True
    set_time(run_time, hour, minute)
    return run_time

def tomorrow(hour, minute):
    run_time = dict()
    run_time['today'] = False
    set_time(run_time, hour, minute)
    return run_time

def set_time(run_time, hour, minute):
    run_time['hour'] = hour
    run_time['minute'] = minute
    return run_time

def format_next_task_run_line(config_line, next_run_time):
    """
    Print the time a command will next be run.
    """
    formatted_hour = "{0:0>2}".format(next_run_time['hour'])
    formatted_minute = "{0:0>2}".format(next_run_time['minute'])
    formatted_time = str(formatted_hour) + ':' + str(formatted_minute)
    run_on_day = 'today' if next_run_time['today'] else  'tomorrow'
    return formatted_time + ' ' + run_on_day + ' - ' + config_line['command']

if __name__ == '__main__':
    main()
