alter table core_man 
modify column `hidden` tinyint(1) NOT NULL default '0',
modify column `comment_count` int(10) unsigned NOT NULL default '0';

insert into core_man
(title, slug, url, content, status, image)
select title, name, url, content, status, image
from core_item
where type_id=15;

update core_item set
type_id=52, url=concat('http://glader.ru/people/', name)
where type_id=15;

insert into core_man
(title, slug, url, content, status, image, is_photographer)
select title, name, url, content, status, image, 1
from core_item
where type_id=23;

update core_item set
type_id=52, url=concat('http://glader.ru/people/', name)
where type_id=23;