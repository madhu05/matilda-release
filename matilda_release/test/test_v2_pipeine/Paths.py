<<<<<<< HEAD
#!/usr/bin/python
import subprocess

file_names = ['1_release_management_platform.sql',
              '2_release_management_operating_system.sql',
              '3_release_management_project.sql',
              '4_release_management_application.sql',
              '5_release_management_frequency.sql',
              '6_release_management_template.sql',
              '7_release_management_status_type_cd.sql',
              '8_release_management_status_cd.sql',
              '9_release_management_release_type_cd.sql',
              '10_release_management_vnf_node_type.sql',
              '11_release_management_vnf_sites.sql',
              '12_release_management_env_type_cd.sql',
              '13_release_management_milestone_status_cd.sql']


def path():
    command = 'find'
    directory = '/var/lib/jenkins/workspace'
    flag = '-iname'
    file_paths = []
    for files in file_names:
        args = [command, directory, flag, files]
        process = subprocess.run(args, stdout=subprocess.PIPE)
        path = process.stdout.decode().strip('\n')
        file_paths.append(path)
    return file_paths
=======
def path():
    print('started')
    scripts = ['matilda-release\\matilda_release\\db\\ sql_scripts\\dmls\\1_release_management_platform.sql',
               'matilda-release\\matilda_release\\db\\ sql_scripts\\dmls\\2_release_management_operating_system.sql',
               'matilda-release\\matilda_release\\db\\ sql_scripts\\dmls\\3_release_management_project.sql',
               'matilda-release\\matilda_release\\db\\ sql_scripts\\dmls\\4_release_management_application.sql',
               'matilda-release\\matilda_release\\db\\ sql_scripts\\dmls\\5_release_management_frequency.sql',
               'matilda-release\\matilda_release\\db\\ sql_scripts\\dmls\\6_release_management_template.sql',
               'matilda-release\\matilda_release\\db\\ sql_scripts\\dmls\\7_release_management_status_type_cd.sql',
               'matilda-release\\matilda_release\\db\\ sql_scripts\\dmls\\8_release_management_status_cd.sql',
               'matilda-release\\matilda_release\\db\\ sql_scripts\\dmls\\9_release_management_release_type_cd.sql',
               'matilda-release\\matilda_release\\db\\ sql_scripts\\dmls\\10_release_management_vnf_node_type.sql',
               'matilda-release\\matilda_release\\db\\ sql_scripts\\dmls\\11_release_management_vnf_sites.sql',
               'matilda-release\\matilda_release\\db\\ sql_scripts\\dmls\\12_release_management_env_type_cd.sql',
               'matilda-release\\matilda_release\\db\\ sql_scripts\\dmls\\13_release_management_milestone_status_cd.sql']
    return scripts





>>>>>>> test

