ALTER TABLE core_mountain ADD COLUMN has_ratrack TINYINT(1) default '0',
	ADD COLUMN oldschool TINYINT(1) default '0',
	ADD COLUMN prices MEDIUMTEXT default NULL,
	ADD COLUMN snowpark MEDIUMTEXT default NULL;
    