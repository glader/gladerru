INSERT INTO `core_photo`
(id,slug,title,content,`status`,`date_created`,
  `author_id`, `post_id`, `rider_id`, `photographer_id`,`place`,
  `comment_count`,`image`,`last_comment_date`,`rating`, `tags_str`)
  
SELECT
RIGHT(p.name, 6), p.name, p.title, p.content, p.status, p.date_created,
p.author_id, rel.item_a_id, NULL, NULL, NULL,
p.comment_count, p.image, p.last_comment_date, p.rating, p.tags_str
FROM core_item p
LEFT JOIN core_relation rel ON rel.item_b_id=p.id and rel.rel_type_id=1
WHERE p.type_id=49;


INSERT INTO `core_photo_tags`
(photo_id, tag_id)
SELECT
right(p.name, 6), tag_id
FROM core_item p
join core_item_tags tag ON p.id=tag.item_id
WHERE p.type_id=49;


INSERT INTO `core_photo_favorites`
(photo_id, profile_id)
SELECT
right(p.name, 6), profile_id
FROM core_item p
join core_item_favorites  f ON p.id=f.item_id
WHERE p.type_id=49;

update core_comment c
join core_item p on c.object_id=p.id
set c.object_id=right(p.name, 6), c.content_type_id=39
where p.type_id=49;

update core_itemvote c
join core_item p on c.object_id=p.id
set c.object_id=right(p.name, 6), c.content_type_id=39
where p.type_id=49;



INSERT INTO `core_photo`
(id,slug,title,content,`status`,`date_created`,
  `author_id`, `post_id`, `rider_id`, `photographer_id`,`place`,
  `comment_count`,`image`,`last_comment_date`,`rating`, `tags_str`)

SELECT
NULL, p.name, p.title, p.content, p.status, p.date_created,
if(p.author_id, p.author_id, 1), NULL, NULL, NULL, NULL,
p.comment_count, p.image, p.last_comment_date, p.rating, p.tags_str
FROM core_item p
WHERE p.type_id=22;


INSERT INTO `core_photo_tags`
(photo_id, tag_id)
SELECT
core_photo.id, tag_id
FROM core_item p
join core_item_tags tag ON p.id=tag.item_id
join core_photo on p.name=core_photo.slug
WHERE p.type_id=22;


INSERT INTO `core_photo_favorites`
(photo_id, profile_id)
SELECT
core_photo.id, profile_id
FROM core_item p
join core_item_favorites  f ON p.id=f.item_id
join core_photo on p.name=core_photo.slug
WHERE p.type_id=22;


update core_comment c
join core_item p on c.object_id=p.id
join core_photo on p.name=core_photo.slug
set c.object_id=core_photo.id, c.content_type_id=39
where p.type_id=22 and c.content_type_id=16;

update core_itemvote c
join core_item p on c.object_id=p.id
join core_photo on p.name=core_photo.slug
set c.object_id=core_photo.id, c.content_type_id=39
where p.type_id=22 and c.content_type_id=16;


update
 core_relation
 INNER JOIN core_item ON (core_relation.item_a_id=core_item.id)
 INNER JOIN core_item core_item1 ON (core_relation.item_b_id=core_item1.id)
 INNER JOIN core_man ON (core_man.slug=core_item.name)
 INNER JOIN core_relationtype ON (core_relation.rel_type_id=core_relationtype.id)
 INNER JOIN core_photo ON (core_photo.slug=core_item1.name)

set core_photo.rider_id=core_man.id

WHERE core_relationtype.name='ACTOR';

update
 core_relation
 INNER JOIN core_item ON (core_relation.item_a_id=core_item.id)
 INNER JOIN core_item core_item1 ON (core_relation.item_b_id=core_item1.id)
 INNER JOIN core_man ON (core_man.slug=core_item.name)
 INNER JOIN core_relationtype ON (core_relation.rel_type_id=core_relationtype.id)
 INNER JOIN core_photo ON (core_photo.slug=core_item1.name)

set core_photo.photographer_id=  core_man.id

WHERE core_relationtype.name='AUTHOR';