DROP TABLE IF EXISTS core_region;

CREATE TABLE `core_region` (
  `id` int(11) NOT NULL auto_increment,
  `title` varchar(250) NOT NULL,
  `order` int(10) unsigned NOT NULL,
  PRIMARY KEY  (`id`)
) ENGINE=MyISAM DEFAULT CHARSET=utf8;

INSERT INTO `core_region` (`id`, `title`, `order`) VALUES 
  (1,'Россия',99),
  (2,'Москва и Московская обл.',1),
  (3,'Питер и Ленинградская обл.',2),
  (4,'Центральная Россия',3),
  (5,'Урал',4),
  (6,'Мурманск',5),
  (7,'Кавказ',6),
  (8,'Сибирь',7),
  (9,'Дальний Восток',8);

DROP TABLE IF EXISTS core_district;

CREATE TABLE `core_district` (
  `id` int(11) NOT NULL auto_increment,
  `title` varchar(250) NOT NULL,
  PRIMARY KEY  (`id`)
) ENGINE=MyISAM DEFAULT CHARSET=utf8;

INSERT INTO core_district (title)
SELECT title FROM core_item WHERE type_id=2;

DROP TABLE IF EXISTS core_mountain;

CREATE TABLE `core_mountain` (
  `id` int(11) NOT NULL auto_increment,
  `name` varchar(250) default NULL,
  `title` varchar(250) default NULL,
  `content` longtext,
  `status` varchar(50) default NULL,
  `address` varchar(200) default NULL,
  `district_id` int(11) default NULL,
  `hidden` tinyint(1) NOT NULL default '0',
  `image` varchar(100) default NULL,
  `last_comment_date` datetime default NULL,
  `lifts` longtext,
  `light` varchar(50) default NULL,
  `latitude` varchar(20) default NULL,
  `longitude` varchar(20) default NULL,
  `longest` varchar(50) default NULL,
  `nightwork` varchar(50) default NULL,
  `overfall` varchar(50) default NULL,
  `pistelength` varchar(50) default NULL,
  `pistes` varchar(50) default NULL,
  `rating` double NOT NULL,
  `region_id` int(11) NOT NULL,
  `root_tag_id` int(11) default NULL,
  `service` longtext,
  `snow` varchar(50) default NULL,
  `tel` varchar(250) default NULL,
  `url` varchar(250) default NULL,
  `webcam` varchar(250) default NULL,
  `work_time` longtext,
  PRIMARY KEY  (`id`),
  UNIQUE KEY `name` (`name`),
  KEY `core_mountain_district_id` (`district_id`),
  KEY `core_mountain_region_id` (`region_id`),
  KEY `core_mountain_root_tag_id` (`root_tag_id`)
) ENGINE=MyISAM DEFAULT CHARSET=utf8;


INSERT into core_mountain (
  `name`,`title`,`content`,`status`,`address`,`hidden`,`image`,`last_comment_date`,
  `lifts`,`light`,`latitude`,`longitude`,`nightwork`,
  `overfall`,`pistelength`,`pistes`,`rating`,
  `service`,`snow`,`tel`,`url`, region_id)
SELECT   `name`,`title`,`content`,`status`,`address`,`hidden`,`image`,`last_comment_date`,
  `lifts`,`light`,`latitude`,`longitude`,`nightwork`,
  `overfall`,`pistelength`,`pistes`,`rating`,
  `service`,`snow`,`tel`,`url`, 1
FROM `core_item` c
WHERE c.type_id=16;

UPDATE core_mountain m 
JOIN core_item i on m.name=i.name
LEFT JOIN core_relation r on r.item_b_id=i.id and rel_type_id=11
LEFT JOIN core_item d ON r.item_a_id=d.id AND d.type_id=2
LEFT JOIN core_district ON core_district.title=d.title
SET m.district_id=core_district.id
WHERE core_district.id IS NOT NULL;

INSERT INTO core_itemtype VALUES (52, 'REDIRECT', 'Редирект', 'redirect_t');

update core_item set type_id=52, url=concat('http://glader.ru/mountains/', name) where type_id=16;