alter table core_item add column `skill_id` int(11) default NULL;

UPDATE core_item set skill_id=5 WHERE id=2222;
UPDATE core_item set skill_id=1 WHERE id=2442;
UPDATE core_item set skill_id=1 WHERE id=2453;
UPDATE core_item set skill_id=1 WHERE id=2475;
UPDATE core_item set skill_id=1 WHERE id=2507;
UPDATE core_item set skill_id=1 WHERE id=2586;
UPDATE core_item set skill_id=1 WHERE id=3816;
UPDATE core_item set skill_id=1 WHERE id=3870;
UPDATE core_item set skill_id=2 WHERE id=2079;
UPDATE core_item set skill_id=3 WHERE id=2204;
UPDATE core_item set skill_id=1 WHERE id=2346;
UPDATE core_item set skill_id=2 WHERE id=2412;
UPDATE core_item set skill_id=2 WHERE id=2413;
UPDATE core_item set skill_id=1 WHERE id=2415;
UPDATE core_item set skill_id=2 WHERE id=3064;
UPDATE core_item set skill_id=1 WHERE id=3323;

INSERT INTO `core_skill` (`id`, `title`, `slug`, `description`, `image`) VALUES 
  (1, 'Новичок', 'newbie', '<div class=\'para\'>Итак, вы решили заняться сноубордингом. Неважно, подговорили вас друзья, или вы увидели захватывающие трюки в каком-нибудь <a href=\"/content/snow_films.htm\" style=\"\">фильме</a>. И теперь вы хотели бы узнать - а с чего, собственно, начать? Вот вам примерная последовательность действий по вхождению в замечательный мир сноубординга:</div>\r\n\r\n<ol><li>Если есть возможность, договоритесь с другом-сноубордистом, что он поможет вам в первый раз. Учиться в одиночку достаточно сложно, со стороны ваши ошибки лучше видны.</li>\r\n<li>Определитесь, какая сторона у вас ведущая. Проще всего найти скользкую поверхность, типа линолеума, разбежаться и проскользить по ней. Какой ногой вперед вы будете скользить, та и есть ведущая. Если левая - вы \"регуляр\", если правая - \"гуфи\".</li>\r\n<li><a href=\"/content/gearing.htm\" style=\"\">Оденьтесь</a> с учетом того, что вы будете много и активно двигаться, а также основательно валяться по снегу. Поэтому лучше взять что-нибудь непромокаемое.</li>\r\n<li>Если у вас есть знакомый сноубордер, а у него есть защита (особенно шорты), выпросите на пару дней. Не пожалеете.</li>\r\n<li>Обязательно прочтите, поймите и запомните <a href=\"/content/whitekodex.htm\" style=\"\">Белый кодекс</a>. Не надо увеличивать число недоумков на склоне.</li>\r\n<li>Придя на ближайший ГЛК, зайдите в прокат и попросите подобрать себе что-нибудь подходящее. Попросите подогнать крепления для себя. Не надо покупать себе снарягу, не будучи уверенным, что вы и дальше будете кататься.</li>\r\n<li>Если не договорились с другом, возьмите на пару часов инструктора. Они есть на каждой горке.</li>\r\n<li>Выполните <a href=\"/content/training.htm\" style=\"\">разогревающую зарядку</a></li>\r\n<li>Проделайте <a href=\"/content/firststeps.htm\" style=\"\">первые упражнения</a></li>\r\n\r\n<li>Если понравилось, <a href=\"/content/howtobuy.htm\" style=\"\">идите в магазин за своей снарягой</a></li>\r\n<li><a href=\"/content/stances.htm\" style=\"\">Подгоните крепления</a> под себя</li>\r\n<li>Еще раз проделайте первые упражнения</li>\r\n<li>Научитесь <a href=\"/content/usebugels.htm\" style=\"\">подниматься на подъемнике</a></li>\r\n<li>Катайтесь в свое удовольствие</li>\r\n</ol>\r\n\r\n<div class=\'para\'>Все незнакомые слова смотрите в <a href=\"/terms\" style=\"\">словарике</a>.</div>\r\n', 'data/skills/newbie.jpg'),
  (2, 'Начинающий сноубордист', 'beginner', NULL, NULL),
  (3, 'Джиббинг', 'jibbing', NULL, NULL),
  (4, 'Карвинг', 'carving', NULL, NULL),
  (5, 'Фристайл', 'freestyle', NULL, NULL),
  (6, 'Фрирайд', 'freeride', NULL, NULL),
  (7, 'Продвинутый джиббинг', 'advanced_jibbing', NULL, NULL),
  (8, 'Пайповый фристайл', 'halfpipe_freestyle', NULL, NULL),
  (9, 'Продвинутый фристайл', 'advanced_freestyle', NULL, NULL),
  (10, 'Беккантри фристайл', 'backcountry_freestyle', NULL, NULL),
  (11, 'Продвинутый фристайл', 'advanced_freeride', NULL, NULL),
  (12, 'Физкультура', 'physical_culture', NULL, NULL),
  (13, 'Первая помощь', 'first_aid', NULL, NULL),
  (14, 'Фото', 'photo', NULL, NULL);

COMMIT;

