use release_management;

set foreign_key_checks = 0;

SET SQL_SAFE_UPDATES=0;

delete from service_fields;

truncate service_fields;

alter table service_fields auto_increment = 1;

delete from actions;

truncate actions;

alter table actions auto_increment = 1;

delete from service;

truncate service;

alter table service auto_increment = 1;

set foreign_key_checks = 1;

SET SQL_SAFE_UPDATES=1;

commit;