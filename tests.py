import unittest
from task_next_run import check_time_argument, check_config_line, calculate_task_next_run_time, format_next_task_run_line

class testProgrammingChallenge(unittest.TestCase):

    def setUp(self):
        pass

    def test_check_time_argument(self):
        assert check_time_argument('22:00') == {'hour': 22, 'minute': 00}

    def test_check_config_line(self):
        input_case = '30 1 /bin/run_me_daily'
        expected_output = {'minute':'30', 'hour':'1', 'command':'/bin/run_me_daily'}
        assert check_config_line(input_case) == expected_output

        input_case = '45 * /bin/run_me_hourly'
        expected_output = {'minute':'45', 'hour':'*', 'command':'/bin/run_me_hourly'}
        assert check_config_line(input_case) == expected_output

        input_case = '05 * /bin/run_me_hourly_2'
        expected_output = {'minute':'05', 'hour':'*', 'command':'/bin/run_me_hourly_2'}
        assert check_config_line(input_case) == expected_output

        input_case = '* * /bin/run_me_every_minute'
        expected_output = {'minute':'*', 'hour':'*', 'command':'/bin/run_me_every_minute'}
        assert check_config_line(input_case) == expected_output

        input_case = '* 19 /bin/run_me_sixty_times_at_19'
        expected_output = {'minute':'*', 'hour':'19', 'command':'/bin/run_me_sixty_times_at_19'}
        assert check_config_line(input_case) == expected_output

        input_case = '* 5 /bin/run_me_sixty_times_at_5'
        expected_output = {'minute':'*', 'hour':'5', 'command':'/bin/run_me_sixty_times_at_5'}
        assert check_config_line(input_case) == expected_output

        input_case = '* 10 /bin/run_me_sixty_times_at_10'
        expected_output = {'minute':'*', 'hour':'10', 'command':'/bin/run_me_sixty_times_at_10'}
        assert check_config_line(input_case) == expected_output

        input_case = '05 16 /bin/run_me_daily_2'
        expected_output = {'minute':'05', 'hour':'16', 'command':'/bin/run_me_daily_2'}
        assert check_config_line(input_case) == expected_output

        input_case = '55 16 /bin/run_me_daily_3'
        expected_output = {'minute':'55', 'hour':'16', 'command':'/bin/run_me_daily_3'}
        assert check_config_line(input_case) == expected_output

        input_case = '25 19 /bin/run_me_daily_4'
        expected_output = {'minute':'25', 'hour':'19', 'command':'/bin/run_me_daily_4'}
        assert check_config_line(input_case) == expected_output

        input_case = '0 * /bin/run_me_hourly_3'
        expected_output = {'minute':'0', 'hour':'*', 'command':'/bin/run_me_hourly_3'}
        assert check_config_line(input_case) == expected_output

    def test_calculate_task_next_run_time(self):

        """
        scheduled minute equals '*' cases
        """
        input_time = {'hour':10, 'minute':05}

        input_schedule = {'hour':'*', 'minute':'*'}
        expected_next_run = {'today':True, 'hour':10, 'minute':5}
        assert calculate_task_next_run_time(input_time, input_schedule) == expected_next_run

        input_schedule = {'hour':'10', 'minute':'*'}
        expected_next_run = {'today':True, 'hour':10, 'minute':5}
        assert calculate_task_next_run_time(input_time, input_schedule) == expected_next_run

        input_schedule = {'hour':'11', 'minute':'*'}
        expected_next_run = {'today':True, 'hour':'11', 'minute':0}
        assert calculate_task_next_run_time(input_time, input_schedule) == expected_next_run

        input_schedule = {'hour':'09', 'minute':'*'}
        expected_next_run = {'today':False, 'hour':'09', 'minute':0}
        assert calculate_task_next_run_time(input_time, input_schedule) == expected_next_run

        """
        scheduled hour equals '*' cases
        """
        input_time = {'hour':10, 'minute':05}

        input_schedule = {'hour':'*', 'minute':'05'}
        expected_next_run = {'today':True, 'hour':10, 'minute':'05'}
        assert calculate_task_next_run_time(input_time, input_schedule) == expected_next_run

        input_schedule = {'hour':'*', 'minute':'55'}
        expected_next_run = {'today':True, 'hour':10, 'minute':'55'}
        assert calculate_task_next_run_time(input_time, input_schedule) == expected_next_run

        input_time = {'hour':23, 'minute':05}

        input_schedule = {'hour':'*', 'minute':'04'}
        expected_next_run = {'today':False, 'hour':0, 'minute':'04'}
        assert calculate_task_next_run_time(input_time, input_schedule) == expected_next_run

        input_time = {'hour':21, 'minute':05}

        input_schedule = {'hour':'*', 'minute':'04'}
        expected_next_run = {'today':True, 'hour':22, 'minute':'04'}
        assert calculate_task_next_run_time(input_time, input_schedule) == expected_next_run

        """
        scheduled hour equals current hour cases
        """
        input_time = {'hour':10, 'minute':05}

        input_schedule = {'hour':'10', 'minute':'06'}
        expected_next_run = {'today':True, 'hour':'10', 'minute':'06'}
        assert calculate_task_next_run_time(input_time, input_schedule) == expected_next_run

        input_schedule = {'hour':'10', 'minute':'04'}
        expected_next_run = {'today':False, 'hour':'10', 'minute':'04'}
        assert calculate_task_next_run_time(input_time, input_schedule) == expected_next_run

        """
        scheduled hour different from current hour cases
        """
        input_time = {'hour':10, 'minute':05}

        input_schedule = {'hour':'22', 'minute':'00'}
        expected_next_run = {'today':True, 'hour':'22', 'minute':'00'}
        assert calculate_task_next_run_time(input_time, input_schedule) == expected_next_run

        input_schedule = {'hour':'09', 'minute':'00'}
        expected_next_run = {'today':False, 'hour':'09', 'minute':'00'}
        assert calculate_task_next_run_time(input_time, input_schedule) == expected_next_run

    def test_print_next_task_run_line(self):
        schedule = {'minute':'30', 'hour':'1', 'command':'/bin/run_me_daily'}
        run_time = {'today':False, 'hour': '1', 'minute':'30'}
        expected_output = '01:30 tomorrow - /bin/run_me_daily'

        assert format_next_task_run_line(schedule, run_time) == expected_output

if __name__ == '__main__':
    unittest.main()
