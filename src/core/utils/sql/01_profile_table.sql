drop table if exists core_profile;

CREATE TABLE `core_profile` (
  `id` int(11) NOT NULL auto_increment,
  `name` varchar(250) default NULL,
  `user_id` int(11) default NULL,
  `date_created` datetime NOT NULL,
  `date_changed` datetime NOT NULL,
  `title` varchar(250) default NULL,
  `content` longtext,
  `status` varchar(50) default 'pub',
  `avatar` tinyint(1) default '0',
  `bindings` varchar(250) default NULL,
  `birthday` datetime default NULL,

  `board` varchar(250) default NULL,
  `boots` varchar(250) default NULL,
  `clothes` varchar(250) default NULL,
  `city` varchar(250) default NULL,
  `country` varchar(250) default NULL,
  `email` varchar(75) default NULL,
  `equip` varchar(250) default NULL,
  `gender` varchar(1) default NULL,
  `icq` varchar(50) default NULL,
  `interests` longtext,
  `is_moderator` tinyint(1) NOT NULL default '0',
  `last_visit` datetime default NULL,
  `mountains` varchar(250) default NULL,
  `rating` double NOT NULL default '0',
  `riding_style` varchar(250) default NULL,
  `stance` varchar(50) default NULL,

  `comment_count` int(10) unsigned NOT NULL default '0',
  `favorites_count` int(10) unsigned NOT NULL default '0',
  `pic_count` int(10) unsigned NOT NULL default '0',
  `pub_post_count` int(10) unsigned NOT NULL default '0',
  `unread_comment_count` int(10) unsigned NOT NULL default '0',
  `unread_post_count` int(10) unsigned NOT NULL default '0',

  PRIMARY KEY  (`id`),
  UNIQUE KEY `name` (`name`),
  KEY `site_item_user_id` (`user_id`)
) ENGINE=MyISAM DEFAULT CHARSET=utf8;

insert into `core_profile`
(id, `name`,user_id, date_created,date_changed,
  title,content,`status`,`avatar`,  `bindings`,  `birthday`,  `board`,  `boots`
  ,`clothes`,  `city`,  `country`,  `email`,  `equip`,  `gender`,  `icq`,  `interests`,
  `is_moderator`,  `last_visit`,  `mountains`, `rating`,  `riding_style`,  `stance`)
  select
  id, `name`,user_id, date_created,date_changed,
  title,content,`status`,`avatar`,  `bindings`,  `birthday`,  `board`,  `boots`
  ,`clothes`,  `city`,  `country`,  `email`,  `equip`,  `gender`,  `icq`,  `interests`,
  `is_moderator`,  `last_visit`,  `mountains`, `rating`,  `riding_style`,  `stance`
from core_item where type_id=50 and name like 'user%';

update core_profile set `name`=RIGHT( `name`, CHAR_LENGTH(`name`)-5);

update
  `core_relation`
  INNER JOIN `core_item` ON (`core_relation`.item_a_id = `core_item`.id)
  INNER JOIN `core_item` core_item1 ON (`core_relation`.item_b_id = core_item1.id)

set core_item1.user_id = `core_item`.user_id

WHERE
  (`core_relation`.rel_type_id = 2) AND
  (`core_item`.type_id = 50);


alter table core_item change column user_id author_id INT(11) NULL;

delete from core_item where type_id=50;

alter table core_itemvote add column `user_id` int(11) default NULL after profile_id;

update core_profile, `core_itemvote`
set core_itemvote.user_id=core_profile.user_id
where core_itemvote.profile_id =core_profile.id;

alter table core_itemvote drop column profile_id;

update core_profile, `core_uservisit`
set core_uservisit.user_id=core_profile.user_id
where core_uservisit.user_id =core_profile.id;


drop table if exists core_count;


delete core_relation from core_relation
left join `core_item`
on core_relation.item_a_id=`core_item`.id
where `core_item`.id is null;

delete core_relation from core_relation
left join `core_item`
on core_relation.item_b_id=`core_item`.id
where `core_item`.id is null;