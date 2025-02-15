/*
 Navicat Premium Dump SQL

 Source Server         : 118.89.171.26
 Source Server Type    : MySQL
 Source Server Version : 50742 (5.7.42)
 Source Host           : 118.89.171.26:3306
 Source Schema         : botpy

 Target Server Type    : MySQL
 Target Server Version : 50742 (5.7.42)
 File Encoding         : 65001

 Date: 15/02/2025 11:05:38
*/

SET NAMES utf8mb4;
SET FOREIGN_KEY_CHECKS = 0;

-- ----------------------------
-- Table structure for chat
-- ----------------------------
DROP TABLE IF EXISTS `chat`;
CREATE TABLE `chat`  (
  `chat_id` bigint(20) NOT NULL AUTO_INCREMENT COMMENT '聊天编号',
  `user_openid` varchar(255) CHARACTER SET utf8 COLLATE utf8_general_ci NULL DEFAULT NULL COMMENT '用户编号',
  `name` text CHARACTER SET utf8 COLLATE utf8_general_ci NULL COMMENT '聊天名称（默认第一句话）',
  PRIMARY KEY (`chat_id`) USING BTREE
) ENGINE = InnoDB AUTO_INCREMENT = 31 CHARACTER SET = utf8 COLLATE = utf8_general_ci ROW_FORMAT = Dynamic;

-- ----------------------------
-- Table structure for message
-- ----------------------------
DROP TABLE IF EXISTS `message`;
CREATE TABLE `message`  (
  `message_id` bigint(20) NOT NULL AUTO_INCREMENT COMMENT '消息编号',
  `chat_id` bigint(20) NULL DEFAULT NULL COMMENT '聊天id',
  `role` varchar(255) CHARACTER SET utf8 COLLATE utf8_general_ci NULL DEFAULT NULL COMMENT '角色',
  `content` longtext CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL COMMENT '消息',
  `create_time` timestamp NULL DEFAULT CURRENT_TIMESTAMP COMMENT '消息创建时间',
  PRIMARY KEY (`message_id`) USING BTREE,
  INDEX `message_chat_id`(`chat_id`) USING BTREE,
  CONSTRAINT `message_chat_id` FOREIGN KEY (`chat_id`) REFERENCES `chat` (`chat_id`) ON DELETE SET NULL ON UPDATE CASCADE
) ENGINE = InnoDB AUTO_INCREMENT = 86 CHARACTER SET = utf8 COLLATE = utf8_general_ci ROW_FORMAT = Dynamic;

SET FOREIGN_KEY_CHECKS = 1;
