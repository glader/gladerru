alter table core_item
add column is_question INT(1) default '0',
add column best_answer_id INT(2) default '0',
add column ask_for_answer_amount INT(1) default '0';

INSERT INTO core_tag VALUES (Null, 'question', 'Вопрос', 1, Null, Null, 10, 0);