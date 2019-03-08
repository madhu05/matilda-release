import sqlite3
from matilda_release.db.sql_scripts import ddl, dmls

connection = "sqlite:////release_management.db"
print('connection:{}'.format(connection))
print('connected')


# scripts = ["C:\\Users\\divya\\Desktop\\Matilda\\matilda-release\\matilda_release\\db\\sql_scripts\\ddl\\release_management_create_db.sql",'C:\\Users\\divya\\Desktop\\Matilda\\matilda-release\\matilda_release\\db\\sql_scripts\\dmls\\1_release_management_platform.sql',
#      'C:\\Users\\divya\\Desktop\\Matilda\\matilda-release\\matilda_release\\db\\sql_scripts\\dmls\\2_release_management_operating_system.sql','C:\\Users\\divya\\Desktop\\Matilda\\matilda-release\\matilda_release\\db\\sql_scripts\\dmls\\3_release_management_project.sql',
#      'C:\\Users\\divya\\Desktop\\Matilda\\matilda-release\\matilda_release\\db\\sql_scripts\\dmls\\4_release_management_application.sql','C:\\Users\\divya\\Desktop\\Matilda\\matilda-release\\matilda_release\\db\\sql_scripts\\dmls\\5_release_management_frequency.sql',
#      'C:\\Users\\divya\\Desktop\\Matilda\\matilda-release\\matilda_release\\db\\sql_scripts\\dmls\\6_release_management_template.sql','C:\\Users\\divya\\Desktop\\Matilda\\matilda-release\\matilda_release\\db\\sql_scripts\\dmls\\7_release_management_status_type_cd.sql',
#      'C:\\Users\\divya\\Desktop\\Matilda\\matilda-release\\matilda_release\\db\\sql_scripts\\dmls\\9_release_management_release_type_cd.sql','C:\\Users\\divya\\Desktop\\Matilda\\matilda-release\\matilda_release\\db\\sql_scripts\\dmls\\10_release_management_vnf_node_type.sql',
#      'C:\\Users\\divya\\Desktop\\Matilda\\matilda-release\\matilda_release\\db\\sql_scripts\\dmls\\11_release_management_vnf_sites.sql','C:\\Users\\divya\\Desktop\\Matilda\\matilda-release\\matilda_release\\db\\sql_scripts\\dmls\\12_release_management_env_type_cd.sql']
# for script in scripts:
#     with open(script, 'r',encoding="utf8") as data:
#         query = data.read()
#         commads = query.split(';')
#         for command in commads:
#             connection.execute(command)


