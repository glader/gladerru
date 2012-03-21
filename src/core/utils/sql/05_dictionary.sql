SET NAMES utf8;

CREATE TABLE `core_word` (
  `id` INTEGER(11) NOT NULL AUTO_INCREMENT,
  `title` VARCHAR(100) COLLATE utf8_general_ci NOT NULL,
  `slug` VARCHAR(100) COLLATE utf8_general_ci NOT NULL,
  `abstract` LONGTEXT NOT NULL,
  `content` LONGTEXT,
  `type` VARCHAR(10) COLLATE utf8_general_ci NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `title` (`title`),
  UNIQUE KEY `slug` (`slug`))ENGINE=MyISAM;

COMMIT;

/* Data for the `core_word` table  (Records 1 - 96) */
INSERT INTO `core_word` (`id`, `title`, `slug`, `abstract`, `content`, `type`) VALUES 
  (1, 'Cab', 'cab', 'Сокращенное от <:ItemLink item=\'switch\' title=\'switch\':> <:Itemlink item=\'fs\' title=\'frontside\':>. Обычно имеется в виду вращение на 360 градусов. Назван в честь легенды скейтбординга Steve Caballero.', NULL, 'common'),
  (2, 'Ван-эйти', '180', 'Вращение на 180 в любую сторону (англ one-eighty)', NULL, 'common'),
  (3, 'Кант', 'kant', 'Железная полоска по краю доски. Именно благодаря ей доска режет снег.', NULL, 'common'),
  (4, 'Tailbone', 'tailbone', 'Выпрямление задней ноги при взятии греба', NULL, 'common'),
  (5, 'Nosebone', 'nosebone', 'Выпрямление передней ноги при взятии греба', NULL, 'common'),
  (6, 'Передняя рука/нога', 'front', 'Ну что тут сказать, передняя она и есть передняя. У <:ItemLink item=\'regular\' title=\'регуляра\':> - левая, у <:ItemLink item=\'goofy\' title=\'гуфи\':> - правая.', NULL, 'common'),
  (7, 'Double', 'double', 'В названии трюка - означает, что райдер за время полета берет два греба по очереди', NULL, 'common'),
  (8, 'Double handed', 'doubleh', 'В названии трюка - означает, что райдер берет два греба одновременно', NULL, 'common'),
  (9, 'Halfcab', 'halfcab', '<:ItemLink item=\'switch\' title=\'Switch\':> <:ItemLink item=\'fs\' title=\'frontside\':> 180', NULL, 'common'),
  (10, '4x4', '4x4', 'Стандарт монтажа креплений, который на сегодняшний день поддерживают все фирмы, за исключением <:ItemLink item=\'burton\':>, четыре втулки с резьбой расположены по углам квадрата. ', NULL, 'common'),
  (11, '3D', '3d', 'Фирменный стандарт креплений фирмы <:ItemLink item=\'burton\':>, три втулки по сторонам равностороннего треугольника. ', NULL, 'common'),
  (12, 'Baseplate', 'baseplate', 'Основная часть крепления, к которой прикрепляются все остальные детали. Выпускают из металла и/или пластика. ', NULL, 'common'),
  (13, 'Binding disc', 'bindingdisc', 'Деталь в средней части платформы крепления, которая позволяет устанавливать крепление под разными углами относительно оси доски. ', NULL, 'common'),
  (14, 'Поймать кант', 'catch_kant', 'Упасть из-за слишком сильного опускания нижнего по склону канта (и зарезания его в снег).', '<:ImageLink item=\'pilnaja20070401_img_0007\':>', 'common'),
  (15, 'Bs', 'bs', 'Backside rotation. Вращение, при котором райдер после первых 90 градусов летит спиной к приземлению. Для <:ItemLink item=\'regular\' title=\'регуляра\':> - по часовой стрелке, для <:ItemLink item=\'goofy\' title=\'гуфи\':> - против.', NULL, 'common'),
  (16, 'Fs', 'fs', 'Frontside rotation. Вращение, при котором райдер после первых 90 градусов летит лицом к приземлению. Для <:ItemLink item=\'regular\' title=\'регуляра\':> - против часовой стрелки, для <:ItemLink item=\'goofy\' title=\'гуфи\':> - по часовой стрелке.', NULL, 'common'),
  (17, 'Goofy', 'goofy', 'Райдер, в основном катающийся правой ногой вперед.', NULL, 'common'),
  (18, 'Regular', 'regular', 'Райдер, катающийся в основном левой ногой вперед.', NULL, 'common'),
  (19, 'Air-to-Fakie', 'airtofakie', 'Любой трюк в пайпе, когда подъезжаешь к стене передом, прыгаешь без поворота и приземляешься в <:ItemLink item=\'fakie\':>.', NULL, 'common'),
  (20, 'Fakie', 'fakie', 'Приземление трюка не в своей стойке', NULL, 'common'),
  (21, 'Switch', 'switch', 'SwitchStance. Заход на прыжок или просто езда не в своей стойке', NULL, 'common'),
  (22, 'Alley-oop', 'alleyoop', 'Этот термин описывает любое вращение в пайпе в так называемом \"uphill\"-направлении: т. е., если ты едешь лицом к стене - вращаешься в <:ItemLink item=\'bs\' title=\'backside\':>, если спиной - во <:ItemLink item=\'fs\' title=\'frontside\':>.', NULL, 'common'),
  (23, 'Backside wall', 'backsidewall', 'В <:ItemLink item=\'halfpipe\' title=\'пайпе\':> \"задняя\" стена - это та стена, к которой ты находишься спиной.', NULL, 'common'),
  (24, 'Frontside wall', 'frontsidewall', 'В пайпе, \"передняя\" стена - это та стена, к которой ты находишься лицом.', NULL, 'common'),
  (25, 'Spin', 'spin', 'Вращение вокруг вертикальной оси. Все базовые трюки - <:ItemLink item=\'fs180\' title=\'fs180\':>, <:ItemLink item=\'bs180\' title=\'bs180\':> и тд. относятся к этой категории.', NULL, 'common'),
  (26, 'Flip', 'flip', 'Вращение вокруг горизонтальной оси, то есть через голову. Например <:ItemLink item=\'backflip\' title=\'backflip\':>, <:ItemLink item=\'sideroll\' title=\'sideroll\':>', NULL, 'common'),
  (27, 'Powder', 'powder', 'Спежевыпавший снег, пухляк. Мечта сноубордиста.', NULL, 'common'),
  (28, 'Sintered', 'sintered', 'Технология изготовления <:ItemLink item=\'base\' title=\'скользяка\':> путем спекания полиэтилена с различными добавками.', 'Подробности читайте в статье <:ItemLink item=\'board_inner\':>', 'common'),
  (29, 'Extruded', 'extruded', 'Технология изготовления <:ItemLink item=\'base\' title=\'скользяка\':> путем выдавливания и проката между двумя валиками расплавленной полиэтиленовой массы.', 'Подробности читайте в статье <:ItemLink item=\'board_inner\':>', 'common'),
  (30, 'Base (база)', 'base', 'Скользящая поверхность. Нижняя часть сноуборда, которая скользит по снегу', 'Подробности читайте в статье <:ItemLink item=\'board_inner\':>', 'common'),
  (31, 'Смывка', 'base_cleaner', 'Специальный растворитель для очистки <:ItemLink item=\'base\' title=\'скользяка\':> от грязи перед нанесением парафина.', 'Подробнее смотрите в статье <:ItemLink item=\'grinding\':>', 'common'),
  (32, 'Мембрана', 'membrana', 'Специальная ткань, пропускающая пар и не пропускающая воду и ветер', '<table border=\'0\' width=\'100%\'><tr><td vlaign=\'top\'>\n<div class=\'para\'>У каждой мембранной ткани есть два показателя: </div>\n\n<div class=\'para\'>Первый - водонепроницаемость. Измеряется в мм водного столба - какой столб воды надо \"поставить\" на ткань, чтобы она начала протекать. Ориентировочно: базовый уровень - 3 000 мм, средний - 8 000 мм , хороший - 20 000мм и более.</div>\n\n<div class=\'para\'>Второй - паропроницаемость. Измеряется в количестве испаренной воды, пропускаемом поверхностью за определенное время. Ориентировочно: базовый уровень - 3 000 г/м2/24 часа, средний - 5 000 г/м2/24 часа, хороший - 8 и более.</div>\n\n<div class=\'para\'>Подробности читайте в статье <:ItemLink item=\'membrana_full\':></div>\n</td><td vlaign=\'top\'><:ImageLink item=\'membrana_scheme\':></td></tr></table>\n', 'common'),
  (33, 'Gore-Tex', 'goretex', 'Одна из товарных марок <:ItemLink item=\'membrana\' title=\'мембранных тканей\':>', NULL, 'common'),
  (34, 'Фрирайд (freeride)', 'freeride', 'Стиль катания, в основном в горах, вне трасс. Цель - проехать там, где никто/мало кто катался, по глубокому нетронутому снегу.', 'Подробности читайте в статье <:ItemLink item=\'snowstyles\':>', 'common'),
  (35, 'Фристайл (freestyle)', 'freestyle', 'Стиль катания, в основном прыжки с трамплинов и карнизов. Цель - полетать повыше и покрасивее.', 'Подробности читайте в статье <:ItemLink item=\'snowstyles\':>, список трюков фристайла приведен <:ItemLink item=\'tricks\' title=\'здесь\':>', 'common'),
  (36, 'Карвинг (freecarv)', 'carving', 'Стиль катания, в основном по подготовленным трассам. Цель - максимальная скорость.', 'Подробности читайте в статье <:ItemLink item=\'snowstyles\':>', 'common'),
  (37, 'Джиббинг (jibbing)', 'jibbing', 'Стиль катания по всему кроме снега.', 'Подробности читайте в статье <:ItemLink item=\'snowstyles\':>', 'common'),
  (38, 'Хафпайп (halfpipe)', 'halfpipe_dict', 'U-образная полутруба из снега, в которой райдеры гоняют от одной стороны к другой, что бы прыгнуть и выполнить крутой трюк. См \"<:ItemLink item=\'halfpipe\':>\". ', NULL, 'common'),
  (39, 'Backcountry', 'backcountry', 'Стиль катания, смысл которого - забраться туда, где нет подъемников, подготовленных трасс и прочих признаков цивилизации.', 'Бывает backcountry-<:ItemLink item=\'freeride\' title=\'фрирайд\':> - катание по диким горам, и backcountry-<:ItemLink item=\'freestyle\' title=\'фристайл\':> - строительство там <:ItemLink item=\'build_big\' title=\'трамплинов\':> и прыжки с них.', 'common'),
  (40, 'Inverted', 'inverted', 'Любой трюк, в котором доска оказывается выше головы райдера', NULL, 'common'),
  (41, 'Бипер', 'beeper', 'Радио-маяк, позволяющий найти райдера, погребенного под лавиной. См. статью <:ItemLink item=\'trackers\':>.', NULL, 'common'),
  (42, 'Лавинный щуп', 'schup_dict', 'Предназначен для обнаружения райдера, попавшего в лавину. См. статью <:ItemLink item=\'avalancheprobes\':>', NULL, 'common'),
  (43, 'Доска', 'board', '1) Сноуборд. Подробнее см. <:ItemLink item=\'board_inner\':><br>\n2) Пласт снега, который срывается со склона и образует лавину. Подробнее см. <:ItemLink item=\'avalanchetracks\':>', NULL, 'common'),
  (44, 'Andrecht', 'andrecht', '<:ItemLink item=\'bs\':> <:ItemLink item=\'handplant\' title=\'handplant\':> на задней руке с <:ItemLink item=\'grab\' title=\'грэбом\':> передней рукой', NULL, 'common'),
  (45, 'Грэб (grab)', 'grab', 'Захват доски. В основном выполняется для красоты и стильности трюков, но и помогает устойчивым вращениям, предотвращает расколбас в воздухе.', NULL, 'common'),
  (46, 'Handplant', 'handplant', 'Трюк, при котором райдер как бы опирается вытянутой рукой на <:ItemLink item=\'lip\' title=\'lip\':>, при этом доска находится у него над головой.', NULL, 'common'),
  (47, 'Lip', 'lip', 'Верхняя грань <:ItemLink item=\'halfpipe\' title=\'хафпайпа\':>, где заканчивается стена', NULL, 'common'),
  (48, 'Ассиметричный боковой вырез', 'asymmetricalsidecut', 'Профиль бокового выреза доски, при котором радиус выреза в передней части доски и в задней различаются. При сдвинутом ассиметричном вырезе центр переднего радиуса сдвинут назад по отношению к центру заднего радиуса.', NULL, 'common'),
  (49, 'Молоток', 'hammer', 'Если <:ItemLink item=\'freeride\' title=\'фрирайдер\':>, успев набрать хорошую скорость, падает вперед, его по инерции несколько раз переворачивает через голову, причем иногда не тормозит, а даже разгоняется. При этом из-за центробежной силы все конечности раскидываются в разные стороны и собрать их нет никакой возможности. Это и есть молоток.', NULL, 'common'),
  (50, 'Гляциология', 'glaciology', 'Наука по изучению снега', NULL, 'common'),
  (51, 'Эффективная длина канта', 'effective_edge', 'Длина канта в той части, которая непосредственно касается снега в повороте.', '<:ImageLink item=\'effect_edge\':>', 'common'),
  (52, 'Закладные', 'fixing', 'Гайки, вставляемые в доску на этапе изготовления, для установки <:ItemLink item=\'bindings\' title=\'креплений\':>.', '<div class=\'para\'>Если во время катания, а особенно прыжков у вас прокручиваются крепления, возможно, болты креплений длиннее, чем закладные. Попробуйте снять крепления и завинтить болты до упора. Если они остаются торчать больше, чем толщина диска, желательно их слегка укоротить. Купите подходящую к болтам гайку, навинтите так, чтобы из гайки выглядывал небольшой фрагмент болта, и отпилите его ножовкой по металлу. После этого снимите гайку (без гайки мы испортите нарезку болта). И так же с остальными.</div>\n\n<div class=\'para\'>Если вы опасаетесь, что болты будут выкручиваться из закладных, зайдите в любой автомагазин и попросите \"синий фиксатор для резьбы\". Стоит недорого, есть везде, маленького тюбика хватит надолго. Только не просите красный. После него болты на морозе могут и не отвернуться вообще.</div>\n\n<div class=\'para\'>См также <:ItemLink item=\'board_inner\':>.</div>', 'common'),
  (53, 'Крепления (bindings)', 'bindings', 'Жестко устанавливаются на доску и удерживают ботинки райдера во время катания. См. статью <:ItemLink item=\'bindings_detailed\':>.', NULL, 'common'),
  (54, 'Asymmetrical sidecut', 'asymmetricalsidecut_eng', 'См. <:ItemLink item=\'asymmetricalsidecut\':>.', NULL, 'common'),
  (55, 'Backside', 'backside', 'У сноубода - сторона у пяток. У сноубордиста - спина.', NULL, 'common'),
  (56, 'Bail', 'bail', 'Падение, уборка. \"He bailed and landed on his head\" - он упал и приземлился на голову.', NULL, 'common'),
  (57, 'Banked slalom', 'bankedslalom', 'Слалом, в котором ворота установлены на противоположных уклонах. Впервые был проведен в Mount Baker, Вашингтон, где трасса была проложена по дну и стенкам оврага.', NULL, 'common'),
  (58, 'Baseless bindings', 'baselessbindings', '<:ItemLink item=\'bindings\' title=\'Крепления\':> без <:ItemLink item=\'baseplate\' title=\'базы\':>. Ботинки стоят прямо на доске, максимально близко к снегу. Одни говорят, что такие крепления позволяют им лучще \"чувствовать\" поверхность под доской, следовательно, лучше управлять ей. Другие считают, что это глупый маркетинговый трюк.', NULL, 'common'),
  (59, 'Bevel', 'bevel', 'Угол, на который заточены <:ItemLink item=\'kant\' title=\'канты\':> сноуборда. Доски для <:ItemLink item=\'carving\' title=\'карвинга\':> имеют больший угол заточки, чем <:ItemLink item=\'halfpipe\' title=\'пайповые\':>. См статью <:ItemLink item=\'grinding\':>.', NULL, 'common'),
  (60, 'Blindside', 'blindside', 'Любое вращение, в котором райдер летит спиной к приземлению и должен смотреть через плечо. Такой трюк считается сложнее. Например, \n<:ItemLink item=\'bs\' title=\'backside\':> <:ItemLink item=\'alleyoop\' title=\'alley oop\':> в <:ItemLink item=\'halfpipe\' title=\'пайпе\':> обычно сложнее, чем <:ItemLink item=\'fs\' title=\'frontside\':>, потому что он выполняется в blintside. ', NULL, 'common'),
  (61, 'Boned', 'boned', 'Это слово означает впечатление от трюка или стиля. То есть если кто-то \"boned out a <:ItemLink item=\'method\':>\", значит он так взял греб и создал такое впечатление, будто его руки или ноги могут вытягиваться просто невероятно. \"Bone\" в описании трюка означает выпрямление одной или обеих ног. ', NULL, 'common'),
  (62, 'Bonk', 'bonk', 'Удар доской по чему-либо кроме снега.', NULL, 'common'),
  (63, 'Bust', 'bust', 'То же, что и \"сделал\", но с бОльшим выражением. \"He busted a huge air over that tree.\" - он фиганул со здоровенного трамплина и перелетел через это дерево.', NULL, 'common'),
  (64, 'Caballerial', 'caballerial', 'См <:ItemLink item=\'cab\':>.', NULL, 'common'),
  (65, 'Весовой прогиб', 'camber', 'Когда сноуборд кладут на ровную поверхность, его центр возвышается над ней, соприкасаются только нос и хвост. Этот изгиб предназначен для правильного распределения веса, то есть равномерного прижимания доски к снегу по всей длине. Прогиб равен расстоянию между серединой базы и поверхностью, на которой покоится доска. Если прогиб отсутствует, значит либо доску неправильно хранили, либо на ней невероятно много ездили.', NULL, 'common'),
  (66, 'Camber', 'camber_eng', 'См <:ItemLink item=\'camber\':>.', NULL, 'common'),
  (67, 'Cap', 'cap', 'Конструкция сноуборда, при которой верхний лист загибается к <:ItemLink item=\'kant\' title=\'кантам\':>.', 'Увеличивает торсионную жесткость, облегчает доску, упрощает и улучшает внешний вид, потому что не требует боковых вставок. Но уменьшает прочность.', 'common'),
  (68, 'Centered stance', 'centeredstance', 'Установка креплений таким образом, что расстояние между передним реплением и носом доски равно расстоянию между задним креплением и хвостом. Позволяет ехать на доске носом или хвостом с одинаковым успехом. См <:ItemLink item=\'stances\':>', NULL, 'common'),
  (69, 'Chatter', 'chatter', 'Лишнее дрожание сноуборда. Обычно возникает на большой скорости или в резких поворотах. Рейсеры обычно стараются уменьшить дрожание, чтобы лучше контролировать доску.', NULL, 'common'),
  (70, 'Coping', 'coping', 'Грань стены <:ItemLink item=\'halfpipe\' title=\'пайпа\':>.', NULL, 'common'),
  (71, 'Corkscrew', 'corkscrew', 'Очень быстрое и резкое вращение. Еще используется для описания любого вращения со смещеннйо осью.', NULL, 'common'),
  (72, 'Педаль газа', 'gazpedal', 'Накладка под носком ботинка на базе <:ItemLink item=\'bindings\' title=\'крепления\':>, небходимая для точной передачи усилия от стопы к переднему канту. См. статью <:ItemLink item=\'bindings_detailed\':>.', NULL, 'common'),
  (73, 'Ратрак', 'ratrack', 'Специальный трактор, предназначенный для передвижения по крутым склонам, формирования трасс, изготовления фигур из снега и т.д. Подробнее смотрите в <:ItemLink item=\'ratracks\' title=\'статье о ратраках\':>.', NULL, 'common'),
  (74, 'Шейпер', 'shaper', 'Человек, который умеет строить сноубордические парки. Очень ответственная должность - от его работы зависит здоровье райдеров.', NULL, 'common'),
  (75, 'FIS', 'fis', 'Всемирная лыжная федерация. Подгребла под себя часть сноубордических соревнований.', NULL, 'common'),
  (76, 'SBX', 'sbx', 'Snowboardcross. См <:ItemLink item=\'snowsporttypes\':>.', NULL, 'common'),
  (77, 'HP', 'hp', 'Соревнования в <:ItemLink item=\'halfpipe\' title=\'халфпайпе\':>. См <:ItemLink item=\'snowsporttypes\':>.', NULL, 'common'),
  (78, 'PGS', 'pgs', 'Параллельный гигантский слалом. См <:ItemLink item=\'snowsporttypes\':>.', NULL, 'common'),
  (79, 'PSL', 'psl', 'Параллельный слалом. См <:ItemLink item=\'snowsporttypes\':>.', NULL, 'common'),
  (80, 'GS', 'gs', 'Гигантский слалом. См <:ItemLink item=\'snowsporttypes\':>.', NULL, 'common'),
  (81, 'BA', 'ba', 'Big Air. Соревнования по фристайлу на трамплине. Судится сложность <:ItemLink item=\'tricks\' title=\'трюка\':>, стиль и общее впечатление. См <:ItemLink item=\'snowsporttypes\':>.', NULL, 'common'),
  (82, 'Олли (ollie)', 'ollie', 'Способ запрыгивания на препятствие. Подпрыгивая, сначала понимаете нос доски, загружая хвост. Хвост пружинит и подбрасывает вас вверх.', NULL, 'common'),
  (83, 'Баттер (butter)', 'butter', 'Переход в <:ItemLink item=\'switch\' title=\'switch\':> прямо на <:ItemLink item=\'kicker\' title=\'кикере\':> или непосредственно перед ним.', NULL, 'common'),
  (84, 'Кикер', 'kicker', 'Та часть <:ItemLink item=\'build_big\' title=\'трамплина\':>, с которой прыгает райдер', NULL, 'common'),
  (85, 'Уборка', 'fall', 'Падение, обычно с неприятными последствиями. \"Он так убрался на биг-эйре, что в тот день больше не прыгал\".', NULL, 'common'),
  (86, 'FRS', 'frs', 'Family Radio Service (FRS) - стандарт, принятый в США для использования средств связи в развлекательных целях. Используются частоты 462,5625 - 462,7125 МГц (шаг 0,025, каналы 1-7) и 467,5625 - 467,7125 МГц (шаг 0,025, каналы 8-14). Разрешенная мощность передатчика <:ItemLink item=\'radio\' title=\'радиостанции\':> составляет 0,5 Вт.', NULL, 'common'),
  (87, 'GMRS', 'gmrs', 'General Mobile Radio Service (GMRS) - принятый в США стандарт <:ItemLink item=\'radio\' title=\'радиосвязи\':> с разрешенной мощностью передатчика более 1 Вт. Используются как частототная сетка <:ItemLink item=\'frs\':>, так и частоты 462,5750-462,7250 МГц (шаг 0,025, 15-22 каналы). На каналах 8-14 (FRS) передача ведется с мощностью 0,5 Вт, на остальных - 1 Вт (в некоторых моделях 2 или 3 Вт).', NULL, 'common'),
  (88, 'Step-up', 'stepup', '1) Трамплин, у которого приземление находится выше <:ItemLInk item=\'kicker\' title=\'кикера\':> (обычно в <:ItemLink item=\'backcountry\' title=\'backcountry\':> <:ItemLink item=\'freestyle\' title=\'фристайле\':>).<br>\n2) <:ItemLink item=\'funbox\' title=\'Funbox\':>, имеющий \"ступеньку\" вверх', NULL, 'common'),
  (89, 'Shifty', 'shifty', 'Трюк во <:ItemLink item=\'freestyle\' title=\'фристайле\':>, когда райдер в полете скручивается, как бы смотря на свои пятки.', NULL, 'common'),
  (90, 'Лавина (avalanche)', 'avalanche', 'Огромная масса снега, срывающаяся со склона и катящаяся вниз с огромной скоростью. Лавины погребают людей, сносят здания, повреждают дороги. Попадание в лавину чаще всего приводит к смертельному исходу. Подробнее см. \"<:ItemLink item=\'avalanchetracks\':>\".', '<div class=\'para\'>Сходящая лавина:</div>\n<div class=\'centered\'>\n<object width=\"425\" height=\"350\"><param name=\"movie\" value=\"http://www.youtube.com/v/6qVwIuznFW0\"></param><param name=\"wmode\" value=\"transparent\"></param><embed src=\"http://www.youtube.com/v/6qVwIuznFW0\" type=\"application/x-shockwave-flash\" wmode=\"transparent\" width=\"425\" height=\"350\"></embed></object>\n</div>', 'common'),
  (91, 'Cork', 'cork', 'Вращение, при котором доска проходит на одном уровне с головой райдера.', 'Пример:<br>\n<:ImageLink item=\'rice_img_003\':>', 'common'),
  (92, 'Экстрим', 'extreme', 'Деятельность человека, компетентность и навыки которого ниже уровня, при котором эта деятельность становится безопасной.', NULL, 'common'),
  (93, 'Pretzel', 'pretzel', 'Крутка в противоположную сторону на сходе с перилы', 'Например, <:ItemLink item=\'boardslide\' title=\'boardslide\':> pretzel - это boardslide bs 270 out', 'jib'),
  (94, 'Revert', 'revert', 'Крутка в ту же сторону на сходе, что и при заходе на перилу', 'Например, boardslide revert - это boardslide fs 270 out', 'jib'),
  (95, 'Целина', 'snowfield', 'Большое поле пухлого глубокого снега с уклоном, достаточным для катания. Мечта <:Itemlink item=\'freeride\' title=\'фрирайдера\':>.', NULL, 'common'),
  (96, 'TTR', 'ttr', 'Ticket To Ride - самая известная и уважаемая организация, проводящая контесты среди сноубордистов.', NULL, 'common');

COMMIT;


update core_item set type_id=52, url="/terms" where name="full_dictionary";
update core_item set type_id=52, url="/tricks" where name="tricks";