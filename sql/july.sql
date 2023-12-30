SET NAMES utf8mb4;
SET FOREIGN_KEY_CHECKS = 0;

-- ----------------------------
-- Table structure for alembic_version
-- ----------------------------
DROP TABLE IF EXISTS `alembic_version`;
CREATE TABLE `alembic_version` (
  `version_num` varchar(32) NOT NULL,
  PRIMARY KEY (`version_num`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- ----------------------------
-- Table structure for chat
-- ----------------------------
DROP TABLE IF EXISTS `chat`;
CREATE TABLE `chat` (
  `id` varchar(32) NOT NULL COMMENT '主键标识',
  `create_time` datetime DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
  `update_time` datetime DEFAULT NULL COMMENT '更新时间',
  `delete_time` datetime DEFAULT NULL COMMENT '删除时间',
  `content` varchar(512) NOT NULL COMMENT '内容',
  `message_type` enum('INFO','TEXT','IMAGE') DEFAULT NULL COMMENT '类型',
  `user_id` varchar(32) NOT NULL COMMENT '用户标识',
  `room_id` varchar(32) NOT NULL COMMENT '房间号',
  `hole_id` varchar(32) DEFAULT NULL COMMENT '树洞标识',
  PRIMARY KEY (`id`),
  KEY `ix_chat_create_time` (`create_time`),
  KEY `ix_chat_hole_id` (`hole_id`),
  KEY `ix_chat_user_id` (`user_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- ----------------------------
-- Records of chat
-- ----------------------------
BEGIN;
INSERT INTO `chat` VALUES ('a3861ef371b64c5bb68a5c3abb43af67', '2023-12-20 14:25:26', NULL, NULL, '好看啊', 'TEXT', '1667e5003dac411b9668a43e1bdbe8cc', 'AFdSN8', 'fb922ebcd0c74476a709768deaa75f7a');
INSERT INTO `chat` VALUES ('c292f61bb5d64cfdab25fbb17d7ff656', '2023-12-20 14:25:04', NULL, NULL, 'https://img.yejiefeng.com/chat/3431d8dd60224aac8f8979622bffedfa', 'IMAGE', '1667e5003dac411b9668a43e1bdbe8cc', 'AFdSN8', 'fb922ebcd0c74476a709768deaa75f7a');
COMMIT;

-- ----------------------------
-- Table structure for comment
-- ----------------------------
DROP TABLE IF EXISTS `comment`;
CREATE TABLE `comment` (
  `id` varchar(32) NOT NULL COMMENT '主键标识',
  `create_time` datetime DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
  `update_time` datetime DEFAULT NULL COMMENT '更新时间',
  `delete_time` datetime DEFAULT NULL COMMENT '删除时间',
  `content` varchar(256) NOT NULL COMMENT '内容',
  `is_anon` tinyint(1) DEFAULT NULL COMMENT '是否匿名',
  `user_id` varchar(32) NOT NULL COMMENT '用户标识',
  `topic_id` varchar(32) NOT NULL COMMENT '话题标识',
  `comment_id` varchar(32) DEFAULT NULL COMMENT '父评论标识',
  `ip_belong` varchar(128) DEFAULT NULL COMMENT 'IP归属地',
  PRIMARY KEY (`id`),
  KEY `ix_comment_comment_id` (`comment_id`),
  KEY `ix_comment_create_time` (`create_time`),
  KEY `ix_comment_topic_id` (`topic_id`),
  KEY `ix_comment_user_id` (`user_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- ----------------------------
-- Records of comment
-- ----------------------------
BEGIN;
INSERT INTO `comment` VALUES ('014a94a2543e4fae9032276d5828eac1', '2023-12-18 16:29:51', NULL, NULL, '确实是蛮不错的！', 0, '1667e5003dac411b9668a43e1bdbe8cc', '816d5e68c6734f3197ef68ccb2c601c0', NULL, '四川');
INSERT INTO `comment` VALUES ('1e264dbc223d498ba06de8f7f83a63e5', '2023-12-29 12:54:18', NULL, NULL, '赞！', 0, '7301687ab38e4e73a0a9eb6c28bcdc3b', '1693d2c3018a42b3a6b26df468016048', NULL, NULL);
INSERT INTO `comment` VALUES ('2b9aba09812044859e0d85e11aa06021', '2023-12-17 22:59:12', NULL, NULL, '太可爱了吧！想偷回家去哈哈哈！', 0, '4e81a014c199449f9602ed264fb05663', '8bc105340e5443cd8e4860477e318197', NULL, '北京');
INSERT INTO `comment` VALUES ('2db6043dbb6f4023a5b32a43d7864e84', '2023-12-18 10:28:33', NULL, NULL, '那你可以试试看哈哈！', 0, '1667e5003dac411b9668a43e1bdbe8cc', '8bc105340e5443cd8e4860477e318197', '2b9aba09812044859e0d85e11aa06021', '浙江');
INSERT INTO `comment` VALUES ('50cc8ae7087e4671b96ef674053c1dae', '2023-12-29 12:49:13', NULL, NULL, '冲！', 0, '7301687ab38e4e73a0a9eb6c28bcdc3b', '998bfea4d7814c0986d8ff07d990be78', NULL, NULL);
INSERT INTO `comment` VALUES ('6eac2c4ac8434427814208b4444af9b3', '2023-12-18 16:59:58', NULL, NULL, '下次可以来玩', 0, '82e7c8c3bee2481589c80a66ab429aea', '816d5e68c6734f3197ef68ccb2c601c0', '014a94a2543e4fae9032276d5828eac1', NULL);
INSERT INTO `comment` VALUES ('b9f0792dd78d4408b7edb58c860c2158', '2023-12-20 15:44:51', NULL, NULL, '无限进步！', 0, '1667e5003dac411b9668a43e1bdbe8cc', 'fd2a612da9fe4d7ea18d4c29fd72d827', NULL, NULL);
INSERT INTO `comment` VALUES ('e64f9a03c6354f1ba597bb27e172e985', '2023-12-29 12:52:37', NULL, NULL, '漂亮', 0, '7301687ab38e4e73a0a9eb6c28bcdc3b', 'bcbb4da7f7c14e28af58894cfd765aa7', NULL, NULL);
COMMIT;

-- ----------------------------
-- Table structure for following
-- ----------------------------
DROP TABLE IF EXISTS `following`;
CREATE TABLE `following` (
  `id` varchar(32) NOT NULL COMMENT '主键标识',
  `create_time` datetime DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
  `update_time` datetime DEFAULT NULL COMMENT '更新时间',
  `delete_time` datetime DEFAULT NULL COMMENT '删除时间',
  `user_id` varchar(32) NOT NULL COMMENT '用户标识',
  `follow_user_id` varchar(32) NOT NULL COMMENT '被关注用户标识',
  PRIMARY KEY (`id`),
  KEY `ix_following_create_time` (`create_time`),
  KEY `ix_following_follow_user_id` (`follow_user_id`),
  KEY `ix_following_user_id` (`user_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- ----------------------------
-- Records of following
-- ----------------------------
BEGIN;
INSERT INTO `following` VALUES ('79b20ff8d48e4792a156daf60a97548e', '2023-12-18 12:56:20', NULL, NULL, '1667e5003dac411b9668a43e1bdbe8cc', '4e81a014c199449f9602ed264fb05663');
INSERT INTO `following` VALUES ('7fbcd57bf44447eba637277e503eb1af', '2023-12-29 12:49:52', NULL, NULL, '7301687ab38e4e73a0a9eb6c28bcdc3b', '1667e5003dac411b9668a43e1bdbe8cc');
INSERT INTO `following` VALUES ('dd8d4c0960b64e1b9699079c41656817', '2023-12-18 16:53:21', NULL, NULL, '82e7c8c3bee2481589c80a66ab429aea', '1667e5003dac411b9668a43e1bdbe8cc');
COMMIT;

-- ----------------------------
-- Table structure for hole
-- ----------------------------
DROP TABLE IF EXISTS `hole`;
CREATE TABLE `hole` (
  `id` varchar(32) NOT NULL COMMENT '主键标识',
  `create_time` datetime DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
  `update_time` datetime DEFAULT NULL COMMENT '更新时间',
  `delete_time` datetime DEFAULT NULL COMMENT '删除时间',
  `title` varchar(64) NOT NULL COMMENT '标题',
  `description` varchar(512) DEFAULT NULL COMMENT '描述',
  `poster` varchar(256) DEFAULT NULL COMMENT '海报',
  `room_id` varchar(32) NOT NULL COMMENT '房间号',
  `allowed_anon` tinyint(1) DEFAULT NULL COMMENT '是否可以匿名',
  `start_time` datetime NOT NULL COMMENT '开始时间',
  `end_time` datetime NOT NULL COMMENT '结束时间',
  PRIMARY KEY (`id`),
  KEY `ix_hole_create_time` (`create_time`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- ----------------------------
-- Records of hole
-- ----------------------------
BEGIN;
INSERT INTO `hole` VALUES ('6e202d5c4f01482aa223395d3292379d', '2023-12-17 12:56:30', NULL, NULL, '自然风光摄影基地', '摄影类爱好者的基地，在此可以分享自己的旅游时光和沿途的风景，和友人们一起讨论好玩的去处！', 'https://img.yejiefeng.com/hole/8e9534c039254d2c98f90f92ef70a5b8', 'D2hsaQ', 0, '2023-12-18 12:00:15', '2023-12-25 12:00:21');
INSERT INTO `hole` VALUES ('9b936457a5774c6cb46e0454a2c3eb6c', '2023-12-17 12:54:34', NULL, NULL, '美食探店博主玩家圈', '每个人都是美食探店的博主，你心中一定会有你最爱吃的那家店，或许是路口的一家地道的面馆，亦或许是一家环境典雅的西餐厅，分享你曾经的探店经历吧！', 'https://img.yejiefeng.com/hole/b1cee6f745dc4ec998adb163db15275e', 'S7YA7H', 0, '2023-12-01 00:00:00', '2023-12-31 12:00:17');
INSERT INTO `hole` VALUES ('e5074edf9f504a1b9e9b2ee39aa85c41', '2023-12-17 12:55:37', NULL, NULL, '萌宠总动员', '家有萌宠，不晒不行，快来把爱宠分享给大家看吧！猫猫狗狗最可爱了，在这里还能和朋友们分享养宠经验，洽谈和自己爱宠的生活点滴！', 'https://img.yejiefeng.com/hole/2fd1b2abf65f4fca9263edaf1f5b5465', 's77kSh', 0, '2023-12-31 00:00:11', '2024-05-31 12:00:21');
INSERT INTO `hole` VALUES ('fb922ebcd0c74476a709768deaa75f7a', '2023-12-17 12:58:29', NULL, NULL, '研发及计算机技术交流圈', '一个讨论软件研发、计算机科学、计算机网络等相关领域的交流圈，可以分享IT互联网发生的实时，也可以讨论CS技术的相关话题。管理员将定期保留清理和相关记录，文明互动，友谊至上！', 'https://img.yejiefeng.com/hole/b91f84e3d05d40658ec8914ef75d4f69', 'AFdSN8', 0, '2023-12-01 12:00:09', '2026-01-01 00:00:00');
INSERT INTO `hole` VALUES ('fcc194a1c7b045d98a4b9dd535bd5686', '2023-12-17 12:57:25', NULL, NULL, '天文摄影爱好者联盟', '聚集全国各地的天文爱好者，在此可以分享你拍到的浩瀚的星空和无尽的银河，也可以分享天文摄影中的经验，能有志同道合的人一起谈论天文奇观，何尝不是一件有趣的事呢？', 'https://img.yejiefeng.com/hole/9b822b35244148bdbe6bed2a7f9d85cb', 'amRXHM', 0, '2023-12-01 00:00:03', '2024-12-01 00:00:10');
COMMIT;

-- ----------------------------
-- Table structure for label
-- ----------------------------
DROP TABLE IF EXISTS `label`;
CREATE TABLE `label` (
  `id` varchar(32) NOT NULL COMMENT '主键标识',
  `create_time` datetime DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
  `update_time` datetime DEFAULT NULL COMMENT '更新时间',
  `delete_time` datetime DEFAULT NULL COMMENT '删除时间',
  `name` varchar(32) NOT NULL COMMENT '名称',
  `allowed_anon` tinyint(1) DEFAULT NULL COMMENT '是否可以匿名',
  `click_count` int(11) DEFAULT NULL COMMENT '点击次数',
  `priority` int(11) DEFAULT NULL COMMENT '优先级',
  PRIMARY KEY (`id`),
  KEY `ix_label_create_time` (`create_time`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- ----------------------------
-- Records of label
-- ----------------------------
BEGIN;
INSERT INTO `label` VALUES ('0f3dadc0d6724846a53254d7de77124e', '2023-12-17 12:50:04', '2023-12-18 14:52:37', NULL, '求助', 0, 4, 67);
INSERT INTO `label` VALUES ('15bec9dff19246ef90c6a13d1fc56daf', '2023-12-17 12:47:41', '2023-12-29 12:53:52', NULL, '美食探店', 0, 8, 99);
INSERT INTO `label` VALUES ('5683ad4d2a0b4c3f8aced7c2e3268e34', '2023-12-17 12:49:27', '2023-12-20 16:21:15', NULL, '工作', 0, 6, 68);
INSERT INTO `label` VALUES ('6e98d7faed8d4f2bbb54674a7cac9430', '2023-12-17 12:49:54', '2023-12-18 14:52:38', NULL, '学习', 0, 5, 69);
INSERT INTO `label` VALUES ('785c8cc53afd4151936d74ac52c177bc', '2023-12-17 12:49:39', '2023-12-20 16:21:14', NULL, '生活', 0, 11, 70);
INSERT INTO `label` VALUES ('7baf91cdcc864d5e8ee9c8b8fd786cad', '2023-12-17 12:46:46', '2023-12-29 12:50:51', NULL, '旅游攻略', 0, 7, 100);
INSERT INTO `label` VALUES ('7bee6d7d748f4970912dd06dabfe16f2', '2023-12-17 12:48:29', '2023-12-29 12:50:53', NULL, '晒自拍', 0, 9, 90);
INSERT INTO `label` VALUES ('a004f6e481634e0280fc7bedb625950a', '2023-12-17 12:48:58', '2023-12-29 12:52:26', NULL, '正能量', 0, 10, 80);
INSERT INTO `label` VALUES ('d6447512e6a84275b2e11c5c2db37155', '2023-12-17 12:50:23', '2023-12-18 14:52:36', NULL, '情感', 1, 4, 1);
COMMIT;

-- ----------------------------
-- Table structure for message
-- ----------------------------
DROP TABLE IF EXISTS `message`;
CREATE TABLE `message` (
  `id` varchar(32) NOT NULL COMMENT '主键标识',
  `create_time` datetime DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
  `update_time` datetime DEFAULT NULL COMMENT '更新时间',
  `delete_time` datetime DEFAULT NULL COMMENT '删除时间',
  `content` varchar(256) NOT NULL COMMENT '内容',
  `category` enum('COMMENT','FOLLOWING','STAR') DEFAULT NULL COMMENT '类型',
  `is_read` tinyint(1) DEFAULT NULL COMMENT '是否已读',
  `user_id` varchar(32) NOT NULL COMMENT '用户标识',
  `topic_id` varchar(32) DEFAULT NULL COMMENT '话题标识',
  `action_user_id` varchar(32) NOT NULL COMMENT '发起用户标识',
  `is_anon` tinyint(1) DEFAULT NULL COMMENT '是否匿名',
  PRIMARY KEY (`id`),
  KEY `ix_message_create_time` (`create_time`),
  KEY `ix_message_topic_id` (`topic_id`),
  KEY `ix_message_user_id` (`user_id`),
  KEY `ix_message_action_user_id` (`action_user_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- ----------------------------
-- Records of message
-- ----------------------------
BEGIN;
INSERT INTO `message` VALUES ('1884fdd86a0346a89333aaf92284698f', '2023-12-29 12:49:03', '2023-12-29 13:06:46', NULL, '收藏了你的话题', 'STAR', 1, '1667e5003dac411b9668a43e1bdbe8cc', '998bfea4d7814c0986d8ff07d990be78', '7301687ab38e4e73a0a9eb6c28bcdc3b', 0);
INSERT INTO `message` VALUES ('98a6633d487b4977bb984352b04b5178', '2023-12-18 16:29:51', NULL, NULL, '评论了你', 'COMMENT', 0, '82e7c8c3bee2481589c80a66ab429aea', '816d5e68c6734f3197ef68ccb2c601c0', '1667e5003dac411b9668a43e1bdbe8cc', 0);
INSERT INTO `message` VALUES ('9918c191ed374ca1a7c9d07f0e72e3c0', '2023-12-29 12:49:13', '2023-12-29 13:06:46', NULL, '评论了你', 'COMMENT', 1, '1667e5003dac411b9668a43e1bdbe8cc', '998bfea4d7814c0986d8ff07d990be78', '7301687ab38e4e73a0a9eb6c28bcdc3b', 0);
INSERT INTO `message` VALUES ('99576c7802d24fd18783d2338e54429a', '2023-12-18 12:56:20', NULL, NULL, '关注了你', 'FOLLOWING', 0, '4e81a014c199449f9602ed264fb05663', NULL, '1667e5003dac411b9668a43e1bdbe8cc', 0);
INSERT INTO `message` VALUES ('a39d8302527f416ea80ee025a88dc7ef', '2023-12-18 16:23:48', NULL, NULL, '收藏了你的话题', 'STAR', 0, '82e7c8c3bee2481589c80a66ab429aea', '816d5e68c6734f3197ef68ccb2c601c0', '1667e5003dac411b9668a43e1bdbe8cc', 0);
INSERT INTO `message` VALUES ('a7056dffb80948699115718654f99a4b', '2023-12-29 12:54:18', NULL, NULL, '评论了你', 'COMMENT', 0, '4e81a014c199449f9602ed264fb05663', '1693d2c3018a42b3a6b26df468016048', '7301687ab38e4e73a0a9eb6c28bcdc3b', 0);
INSERT INTO `message` VALUES ('c412503a010e488988f92811a4c09323', '2023-12-18 16:54:06', '2023-12-20 15:43:51', NULL, '关注了你', 'FOLLOWING', 1, '1667e5003dac411b9668a43e1bdbe8cc', NULL, '82e7c8c3bee2481589c80a66ab429aea', 0);
INSERT INTO `message` VALUES ('f2a14eba00994b2bb8fc4b8c9e7ca693', '2023-12-18 17:02:39', '2023-12-20 15:43:51', NULL, '评论了你', 'COMMENT', 1, '1667e5003dac411b9668a43e1bdbe8cc', '816d5e68c6734f3197ef68ccb2c601c0', '82e7c8c3bee2481589c80a66ab429aea', 0);
INSERT INTO `message` VALUES ('faee2242ebe343caa736a6e430a35d97', '2023-12-29 12:49:52', '2023-12-29 13:06:46', NULL, '关注了你', 'FOLLOWING', 1, '1667e5003dac411b9668a43e1bdbe8cc', NULL, '7301687ab38e4e73a0a9eb6c28bcdc3b', 0);
COMMIT;

-- ----------------------------
-- Table structure for star
-- ----------------------------
DROP TABLE IF EXISTS `star`;
CREATE TABLE `star` (
  `id` varchar(32) NOT NULL COMMENT '主键标识',
  `create_time` datetime DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
  `update_time` datetime DEFAULT NULL COMMENT '更新时间',
  `delete_time` datetime DEFAULT NULL COMMENT '删除时间',
  `user_id` varchar(32) NOT NULL COMMENT '用户标识',
  `topic_id` varchar(32) NOT NULL COMMENT '话题标识',
  PRIMARY KEY (`id`),
  KEY `ix_star_create_time` (`create_time`),
  KEY `ix_star_topic_id` (`topic_id`),
  KEY `ix_star_user_id` (`user_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- ----------------------------
-- Records of star
-- ----------------------------
BEGIN;
INSERT INTO `star` VALUES ('88d6ede747c344c69952d858d9c1afa5', '2023-12-20 15:44:21', NULL, NULL, '1667e5003dac411b9668a43e1bdbe8cc', 'fd2a612da9fe4d7ea18d4c29fd72d827');
INSERT INTO `star` VALUES ('a42a4643a3854a40be3165f9f6d6c58c', '2023-12-20 15:57:07', NULL, NULL, '1667e5003dac411b9668a43e1bdbe8cc', '998bfea4d7814c0986d8ff07d990be78');
INSERT INTO `star` VALUES ('b90b3545e56b4ca5886a30dd332c3a46', '2023-12-18 16:23:48', NULL, NULL, '1667e5003dac411b9668a43e1bdbe8cc', '816d5e68c6734f3197ef68ccb2c601c0');
INSERT INTO `star` VALUES ('e542b331de5b4c4d8e24b8ab7d0a7a13', '2023-12-29 12:49:03', NULL, NULL, '7301687ab38e4e73a0a9eb6c28bcdc3b', '998bfea4d7814c0986d8ff07d990be78');
INSERT INTO `star` VALUES ('e92922938ebb4337b8c48216c3512242', '2023-12-17 22:59:19', NULL, NULL, '1667e5003dac411b9668a43e1bdbe8cc', '8bc105340e5443cd8e4860477e318197');
COMMIT;

-- ----------------------------
-- Table structure for topic
-- ----------------------------
DROP TABLE IF EXISTS `topic`;
CREATE TABLE `topic` (
  `id` varchar(32) NOT NULL COMMENT '主键标识',
  `update_time` datetime DEFAULT NULL COMMENT '更新时间',
  `delete_time` datetime DEFAULT NULL COMMENT '删除时间',
  `title` varchar(64) DEFAULT NULL COMMENT '标题',
  `content` varchar(1024) NOT NULL COMMENT '内容',
  `is_anon` tinyint(1) DEFAULT NULL COMMENT '是否匿名',
  `click_count` int(11) DEFAULT NULL COMMENT '点击次数',
  `images` json DEFAULT NULL COMMENT '图片',
  `user_id` varchar(32) NOT NULL COMMENT '用户标识',
  `video_id` varchar(32) DEFAULT NULL COMMENT '视频标识',
  `create_time` datetime DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
  `ip_belong` varchar(128) DEFAULT NULL COMMENT 'IP归属地',
  `star_count` int(11) DEFAULT NULL COMMENT '收藏次数',
  `comment_count` int(11) DEFAULT NULL COMMENT '评论次数',
  PRIMARY KEY (`id`),
  KEY `ix_topic_user_id` (`user_id`),
  KEY `ix_topic_video_id` (`video_id`),
  KEY `ix_topic_create_time` (`create_time`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- ----------------------------
-- Records of topic
-- ----------------------------
BEGIN;
INSERT INTO `topic` VALUES ('1693d2c3018a42b3a6b26df468016048', '2023-12-29 12:54:18', NULL, NULL, '初心易得，始终难守', 0, 1, '[\"https://img.yejiefeng.com/topic/c337680144d34c8087106771970b2e36\"]', '4e81a014c199449f9602ed264fb05663', NULL, '2023-12-18 14:55:43', NULL, 0, 1);
INSERT INTO `topic` VALUES ('21282802075848a5b07f12b97a240556', '2023-12-18 14:24:37', NULL, NULL, '相约东极，在海上看日落日出，在山间看云卷云舒！', 0, 1, '[\"https://img.yejiefeng.com/topic/7758604c6fca4b2e85a7daaffd6df145\", \"https://img.yejiefeng.com/topic/ffae30416b7b44b1be06ba846327cbf2\", \"https://img.yejiefeng.com/topic/19b3822235fe43569fd1bd4e5252964c\", \"https://img.yejiefeng.com/topic/2de701094cbe41a3bbde6e9a3e42362a\", \"https://img.yejiefeng.com/topic/41e8aeacc7b14e8692e047f86e329e19\", \"https://img.yejiefeng.com/topic/8117fb4f20eb4fc184f8262b03c71b79\"]', '1667e5003dac411b9668a43e1bdbe8cc', NULL, '2023-12-18 14:24:15', '浙江', 0, 0);
INSERT INTO `topic` VALUES ('816d5e68c6734f3197ef68ccb2c601c0', '2023-12-20 16:08:52', NULL, NULL, '一个充满包容的城市，每个角色无论是何种职务，都有其容身之所，都有其发挥之处，这就是所谓的城市气场吧！', 0, 12, '[]', '82e7c8c3bee2481589c80a66ab429aea', 'a7b3070351474f7e97bee50ba9aac168', '2023-12-18 15:16:19', '上海', 1, 2);
INSERT INTO `topic` VALUES ('8ad12c6d0cb7494d9e1261e89faa2092', '2023-12-18 14:47:11', NULL, NULL, '无论人生上到哪一层台阶，阶下有人在仰望你，阶上亦有人在俯视你，你抬头自卑，低头自得，唯有平视，才能看见真实的自己。', 0, 3, '[]', '1667e5003dac411b9668a43e1bdbe8cc', NULL, '2023-12-18 14:18:21', NULL, 0, 0);
INSERT INTO `topic` VALUES ('8bc105340e5443cd8e4860477e318197', '2023-12-18 14:21:34', NULL, NULL, '分享两只爱玩逗猫棒的喵喵！', 0, 83, '[\"https://img.yejiefeng.com/topic/0035dafd65434b4580c54202e3896f57\", \"https://img.yejiefeng.com/topic/bf24087c3629479b8eb5d928cd2656c0\", \"https://img.yejiefeng.com/topic/dd02efb5acb343bd8704f9f562facea0\", \"https://img.yejiefeng.com/topic/4e3c63fcd7874e24a2894986bd468b52\"]', '1667e5003dac411b9668a43e1bdbe8cc', NULL, '2023-12-17 16:20:50', '上海', 1, 2);
INSERT INTO `topic` VALUES ('998bfea4d7814c0986d8ff07d990be78', '2023-12-29 12:49:13', NULL, NULL, '准备发布V2版本，一个里程碑版本，开源真的需要花费很大的精力去做，因为致力于把一个产品做到最好，并不是一件容易的事情。', 0, 4, '[]', '1667e5003dac411b9668a43e1bdbe8cc', NULL, '2023-12-18 16:51:39', NULL, 2, 1);
INSERT INTO `topic` VALUES ('b677676e34c04705a0471c32a052e742', '2023-12-18 14:21:30', NULL, NULL, '可以拿居老师来做手机壁纸不？', 0, 4, '[\"https://img.yejiefeng.com/topic/f58fad3e82a24fb78b92c15f8f986d22\"]', '1667e5003dac411b9668a43e1bdbe8cc', NULL, '2023-12-18 13:27:07', NULL, 0, 0);
INSERT INTO `topic` VALUES ('bcbb4da7f7c14e28af58894cfd765aa7', '2023-12-29 12:56:59', NULL, NULL, '上海三件套之东方之珠，九十年代的设计，看着还是如此的现代。', 0, 5, '[\"https://img.yejiefeng.com/topic/9248a8939b97472ab6e9e7f8dce00ad9\"]', '7301687ab38e4e73a0a9eb6c28bcdc3b', NULL, '2023-12-29 12:48:48', NULL, 0, 1);
INSERT INTO `topic` VALUES ('fd2a612da9fe4d7ea18d4c29fd72d827', '2023-12-29 12:50:25', NULL, NULL, '这个世界上没有无用的齿轮，能够决定其用途的只有齿轮自身。', 1, 8, '[]', '1667e5003dac411b9668a43e1bdbe8cc', NULL, '2023-12-18 14:27:33', NULL, 1, 1);
COMMIT;

-- ----------------------------
-- Table structure for topic_label_rel
-- ----------------------------
DROP TABLE IF EXISTS `topic_label_rel`;
CREATE TABLE `topic_label_rel` (
  `id` varchar(32) NOT NULL COMMENT '主键标识',
  `create_time` datetime DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
  `update_time` datetime DEFAULT NULL COMMENT '更新时间',
  `delete_time` datetime DEFAULT NULL COMMENT '删除时间',
  `topic_id` varchar(32) NOT NULL COMMENT '话题标识',
  `label_id` varchar(32) NOT NULL COMMENT '标签标识',
  PRIMARY KEY (`id`),
  KEY `ix_topic_label_rel_create_time` (`create_time`),
  KEY `ix_topic_label_rel_label_id` (`label_id`),
  KEY `ix_topic_label_rel_topic_id` (`topic_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- ----------------------------
-- Records of topic_label_rel
-- ----------------------------
BEGIN;
INSERT INTO `topic_label_rel` VALUES ('291e5492acf14dc6be6f847e5fec5bb0', '2023-12-18 15:16:19', NULL, NULL, '816d5e68c6734f3197ef68ccb2c601c0', 'a004f6e481634e0280fc7bedb625950a');
INSERT INTO `topic_label_rel` VALUES ('3e8ad2fde169497983d8473ffe476f58', '2023-12-18 16:51:39', NULL, NULL, '998bfea4d7814c0986d8ff07d990be78', '6e98d7faed8d4f2bbb54674a7cac9430');
INSERT INTO `topic_label_rel` VALUES ('5a2ec3ca597244dfa799ecb10aa29559', '2023-12-18 15:01:18', NULL, NULL, '254668fd6dca4a1a96c746e6aa8e89e3', '785c8cc53afd4151936d74ac52c177bc');
INSERT INTO `topic_label_rel` VALUES ('66b4fa14a33047c0a0920d953117d7e9', '2023-12-18 15:16:19', NULL, NULL, '816d5e68c6734f3197ef68ccb2c601c0', '785c8cc53afd4151936d74ac52c177bc');
INSERT INTO `topic_label_rel` VALUES ('700490f094de44288ebe47f0713b4a72', '2023-12-29 12:48:48', NULL, NULL, 'bcbb4da7f7c14e28af58894cfd765aa7', '7baf91cdcc864d5e8ee9c8b8fd786cad');
INSERT INTO `topic_label_rel` VALUES ('786db0f401d64eb999f78390fc47a7f8', '2023-12-18 15:01:18', NULL, NULL, '254668fd6dca4a1a96c746e6aa8e89e3', '6e98d7faed8d4f2bbb54674a7cac9430');
INSERT INTO `topic_label_rel` VALUES ('868a1011787d44aabb45b750dbcbf571', '2023-12-18 14:24:15', NULL, NULL, '21282802075848a5b07f12b97a240556', '785c8cc53afd4151936d74ac52c177bc');
INSERT INTO `topic_label_rel` VALUES ('8847fbca88fc4e749b8e23b291c8b3bc', '2023-12-18 14:27:33', NULL, NULL, 'fd2a612da9fe4d7ea18d4c29fd72d827', 'd6447512e6a84275b2e11c5c2db37155');
INSERT INTO `topic_label_rel` VALUES ('8da1532aca0f42de9c43cdb0edb3e1ae', '2023-12-18 15:01:18', NULL, NULL, '254668fd6dca4a1a96c746e6aa8e89e3', 'a004f6e481634e0280fc7bedb625950a');
INSERT INTO `topic_label_rel` VALUES ('995d771a5eff4f448cb0a7427c9bdefb', '2023-12-18 14:24:15', NULL, NULL, '21282802075848a5b07f12b97a240556', '7bee6d7d748f4970912dd06dabfe16f2');
INSERT INTO `topic_label_rel` VALUES ('9d7e34c735fe41b4b5de9cb42a71a997', '2023-12-17 16:20:50', NULL, NULL, '8bc105340e5443cd8e4860477e318197', '785c8cc53afd4151936d74ac52c177bc');
INSERT INTO `topic_label_rel` VALUES ('a55618d32f61423ca16e13f8ed7c1eea', '2023-12-18 14:55:43', NULL, NULL, '1693d2c3018a42b3a6b26df468016048', 'a004f6e481634e0280fc7bedb625950a');
INSERT INTO `topic_label_rel` VALUES ('bf7309514a6644c8b0731287c0281d4e', '2023-12-18 15:16:19', NULL, NULL, '816d5e68c6734f3197ef68ccb2c601c0', '6e98d7faed8d4f2bbb54674a7cac9430');
INSERT INTO `topic_label_rel` VALUES ('c74aea7c926048308ab04f362e549dbc', '2023-12-18 16:51:39', NULL, NULL, '998bfea4d7814c0986d8ff07d990be78', '5683ad4d2a0b4c3f8aced7c2e3268e34');
INSERT INTO `topic_label_rel` VALUES ('f5635df5882d4f918060d6a6c6154bf8', '2023-12-18 14:24:15', NULL, NULL, '21282802075848a5b07f12b97a240556', '7baf91cdcc864d5e8ee9c8b8fd786cad');
COMMIT;

-- ----------------------------
-- Table structure for user
-- ----------------------------
DROP TABLE IF EXISTS `user`;
CREATE TABLE `user` (
  `id` varchar(32) NOT NULL COMMENT '主键标识',
  `create_time` datetime DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
  `update_time` datetime DEFAULT NULL COMMENT '更新时间',
  `delete_time` datetime DEFAULT NULL COMMENT '删除时间',
  `openid` varchar(64) NOT NULL COMMENT '微信openid',
  `nickname` varchar(32) DEFAULT NULL COMMENT '昵称',
  `avatar` varchar(256) DEFAULT NULL COMMENT '头像',
  `poster` varchar(256) DEFAULT NULL COMMENT '封面',
  `signature` varchar(64) DEFAULT NULL COMMENT '个性签名',
  `gender` enum('MAN','WOMAN','UN_KNOW') DEFAULT NULL COMMENT '性别',
  `city` varchar(128) DEFAULT NULL COMMENT '城市',
  `province` varchar(128) DEFAULT NULL COMMENT '省份',
  `country` varchar(128) DEFAULT NULL COMMENT '国家',
  `is_admin` tinyint(1) DEFAULT NULL COMMENT '是否为管理员',
  `remark` varchar(64) DEFAULT NULL COMMENT '备注',
  `ip_belong` varchar(128) DEFAULT NULL COMMENT 'IP归属地',
  PRIMARY KEY (`id`),
  UNIQUE KEY `openid` (`openid`),
  KEY `ix_user_create_time` (`create_time`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- ----------------------------
-- Records of user
-- ----------------------------
BEGIN;
INSERT INTO `user` VALUES ('1667e5003dac411b9668a43e1bdbe8cc', '2023-12-17 13:35:35', '2023-12-18 13:25:43', NULL, 'o7yGX4kanSwICk6R3Mes1U9hNY_0', '仓鼠不怕猫咪', 'https://img.yejiefeng.com/avatar/ba507f9068b04e96986efada47322812', 'https://img.yejiefeng.com/poster/d91a7d41ff0f480e8e8a471158a66c45', '左脑编程，右脑写诗', 'MAN', '', '', '', 1, NULL, '芬兰');
INSERT INTO `user` VALUES ('4e81a014c199449f9602ed264fb05663', '2023-12-17 13:00:07', NULL, NULL, 'o37HjWxF3fVLwe2UFweR7SWJd5R', 'wiki', 'https://img.yejiefeng.com/avatar/sb9gew0d8-c4d4-11e9-ss4a-14csa9s53b11', NULL, '爱生活，爱自然', 'WOMAN', '绍兴', '浙江', '中国', 0, NULL, '浙江');
INSERT INTO `user` VALUES ('7301687ab38e4e73a0a9eb6c28bcdc3b', '2023-12-29 12:45:28', '2023-12-29 12:56:36', NULL, 'o7yGX4ou0MpbtcgSZK2KCdGIEefp', '可可西里', 'https://img.yejiefeng.com/avatar/65189e5cb2f6470ab6645cd2f0b5071a', NULL, NULL, 'MAN', '', '', '', 0, NULL, NULL);
INSERT INTO `user` VALUES ('82e7c8c3bee2481589c80a66ab429aea', '2023-12-17 13:01:34', NULL, NULL, 'oScas2xF3fVLWvsd2gbR7SffEVn', 'Eve', 'https://img.yejiefeng.com/avatar/dw2cew0d8-4t6u-gh8s-sca2-1sd2a9s5sd22', NULL, '我想要两颗西柚', 'MAN', '杭州', '浙江', '中国', 0, NULL, '上海');
COMMIT;

-- ----------------------------
-- Table structure for video
-- ----------------------------
DROP TABLE IF EXISTS `video`;
CREATE TABLE `video` (
  `id` varchar(32) NOT NULL COMMENT '主键标识',
  `create_time` datetime DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
  `update_time` datetime DEFAULT NULL COMMENT '更新时间',
  `delete_time` datetime DEFAULT NULL COMMENT '删除时间',
  `src` varchar(256) NOT NULL COMMENT '地址',
  `cover` varchar(256) DEFAULT NULL COMMENT '封面',
  `width` int(11) DEFAULT NULL COMMENT '宽度',
  `height` int(11) DEFAULT NULL COMMENT '高度',
  `duration` int(11) DEFAULT NULL COMMENT '时长',
  `size` int(11) DEFAULT NULL COMMENT '大小',
  `user_id` varchar(32) NOT NULL COMMENT '用户标识',
  `video_status` enum('REVIEWING','NORMAL','VIOLATION') DEFAULT NULL COMMENT '状态',
  PRIMARY KEY (`id`),
  KEY `ix_video_create_time` (`create_time`),
  KEY `ix_video_user_id` (`user_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- ----------------------------
-- Records of video
-- ----------------------------
BEGIN;
INSERT INTO `video` VALUES ('a7b3070351474f7e97bee50ba9aac168', '2023-12-18 15:16:18', NULL, NULL, 'https://img.yejiefeng.com/video/46f9e2b59c144ce38628aaefe841fab2', 'https://img.yejiefeng.com/video-cover/de31290556774409801906662cebcf55', 1280, 720, 9, 1836354, '1667e5003dac411b9668a43e1bdbe8cc', 'NORMAL');
COMMIT;

SET FOREIGN_KEY_CHECKS = 1;
