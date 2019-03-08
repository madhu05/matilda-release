use release_management;

-- INSERT INTO release_management.frequency (frequency_cd, frequency_description, dag_usage, comments, cron_expression) VALUES (1, 'None', 'None', 'Don’t schedule, use for exclusively “externally triggered” DAGs', null);
INSERT INTO frequency (frequency_cd, frequency_description, dag_usage, comments, cron_expression) VALUES (1, 'once', '@once', 'Schedule once and only once', null);
# INSERT INTO frequency (frequency_cd, frequency_description, dag_usage, comments, cron_expression) VALUES (2, 'hourly', '@hourly', 'Run once an hour at the beginning of the hour', '0 * * * *');
# INSERT INTO frequency (frequency_cd, frequency_description, dag_usage, comments, cron_expression) VALUES (3, 'daily', '@daily', 'Run once a day at midnight', '0 0 * * *');
# INSERT INTO frequency (frequency_cd, frequency_description, dag_usage, comments, cron_expression) VALUES (4, 'weekly', '@weekly', 'Run once a week at midnight on Sunday morning', '0 0 * * 0');
# INSERT INTO frequency (frequency_cd, frequency_description, dag_usage, comments, cron_expression) VALUES (5, 'monthly', '@monthly', 'Run once a month at midnight of the first day of the month', '0 0 1 * *');
# INSERT INTO frequency (frequency_cd, frequency_description, dag_usage, comments, cron_expression) VALUES (6, 'yearly', '@yearly', 'Run once a year at midnight of January 1', '0 0 1 1 *');
commit