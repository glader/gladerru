drop table if exists core_comment;

CREATE TABLE `core_comment` (
  `id` int(11) NOT NULL auto_increment,
  `author_id` int(11) default NULL,
  `date_created` datetime NOT NULL,
  `content` longtext,
  `status` varchar(50) default 'pub',
  `hidden` tinyint(1) default '0',
  `order` varchar(255) default NULL,
  `rating` double NOT NULL default '0',
  
  `object_id` int(11) NOT NULL,
  `content_type_id` int(11) default NULL,
    
  PRIMARY KEY  (`id`),
  KEY `author_id` (`author_id`)  
) ENGINE=MyISAM DEFAULT CHARSET=utf8;

insert into core_comment (
  `id`,  `author_id`, `date_created`,  `content`, `status`,
  `hidden` , `order` , `rating`,  `object_id`, `content_type_id`)
  select
  cast(RIGHT( c.`name`, CHAR_LENGTH(c.`name`)-8) as unsigned),
  c.`author_id`, c.`date_created`,  c.`content`, c.`status`,
  c.`hidden` , c.`order` , c.`rating`,  i.id, 16
from `core_item` c
join core_relation r on r.item_b_id=c.id and r.rel_type_id=1
join core_item i on r.item_a_id=i.id
where c.type_id=47;

DELETE FROM core_item where type_id=47;

delete core_relation from core_relation
left join `core_item`
on core_relation.item_a_id=`core_item`.id
where `core_item`.id is null;

delete core_relation from core_relation
left join `core_item`
on core_relation.item_b_id=`core_item`.id
where `core_item`.id is null;