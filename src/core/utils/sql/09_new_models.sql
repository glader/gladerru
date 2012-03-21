truncate table core_movie;

insert into core_movie
	(    title, slug, content, status, url, cover,
	torrent, teaser, has_songs, year, rating, hidden )
select  title, name, content, status, url, image,
	torrent, youtube, if(length(tracklist)>0, 1, 0), year, rating, 0
from core_item where type_id=17;

// производители фильмов
update
core_relation r
join core_item iss ON r.item_a_id=iss.id AND iss.type_id=19
join core_studio studio on iss.name=studio.slug
join core_item im ON r.item_b_id=im.id AND im.type_id=17
join core_movie movie on im.name=movie.slug
SET movie.studio_id=studio.id
WHERE r.rel_type_id=2

// райдеры в фильмах
insert into core_man2movie
select NULL, man.id, movie.id, 'actor'
FROM core_relation r
join core_item ir ON r.item_a_id=ir.id AND ir.type_id=27
join core_man man on ir.name=man.slug
join core_item im ON r.item_b_id=im.id AND im.type_id=17
join core_movie movie on im.name=movie.slug
WHERE r.rel_type_id=3;

// музыка из фильмов
update
core_song s
join core_item im ON s.item_id=im.id
join core_movie movie on im.name=movie.slug

SET s.movie_id=movie.id

// Комментарии к фильмам
UPDATE
core_comment c
join core_item i on c.object_id=i.id and content_type_id=16
join core_movie m on i.name=m.slug
set c.object_id=m.id, c.content_type_id=37

// Комментарии к райдерам
UPDATE
core_comment c
join core_item i on c.object_id=i.id and content_type_id=16
join core_man m on i.name=m.slug
set c.object_id=m.id, c.content_type_id=35