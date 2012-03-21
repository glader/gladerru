delete core_relation
FROM
  `core_item` core_item1
  INNER JOIN `core_movie` ON (core_item1.name = `core_movie`.slug)
  INNER JOIN `core_relation` ON (core_item1.id = `core_relation`.item_b_id)
  INNER JOIN `core_item` ON (`core_relation`.item_a_id = `core_item`.id)
  INNER JOIN `core_relationtype` ON (`core_relation`.rel_type_id = `core_relationtype`.id)
WHERE
  (core_item1.type_id = 17)
  and core_relationtype.name='ACTOR';
  
delete core_relation
FROM
  `core_item` core_item1
  INNER JOIN `core_movie` ON (core_item1.name = `core_movie`.slug)
  INNER JOIN `core_relation` ON (core_item1.id = `core_relation`.item_b_id)
  INNER JOIN `core_item` ON (`core_relation`.item_a_id = `core_item`.id)
  INNER JOIN `core_relationtype` ON (`core_relation`.rel_type_id = `core_relationtype`.id)
WHERE
  (core_item1.type_id = 17)
  and core_relationtype.name='AUTHOR';
  
delete core_relation
FROM
  `core_item` core_item1
  INNER JOIN `core_movie` ON (core_item1.name = `core_movie`.slug)
  INNER JOIN `core_relation` ON (core_item1.id = `core_relation`.item_b_id)
  INNER JOIN `core_item` ON (`core_relation`.item_a_id = `core_item`.id)
  INNER JOIN `core_relationtype` ON (`core_relation`.rel_type_id = `core_relationtype`.id)
WHERE
  (core_item1.type_id = 17)
  and core_relationtype.name='BELONGS';
  
delete core_relation
FROM
  core_item core_item1
  INNER JOIN core_relation ON (core_item1.id = core_relation.item_b_id)
  INNER JOIN core_item ON (core_relation.item_a_id = core_item.id)
  INNER JOIN core_relationtype ON (core_relation.rel_type_id = core_relationtype.id)
  INNER JOIN `core_man` ON (core_item1.name = `core_man`.slug)
WHERE
  (core_relationtype.name = 'BELONGS');