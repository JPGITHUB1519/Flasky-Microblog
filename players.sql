/*
Navicat PGSQL Data Transfer

Source Server         : PostgreSQL 9.5
Source Server Version : 90505
Source Host           : localhost:5432
Source Database       : tournament
Source Schema         : public

Target Server Type    : PGSQL
Target Server Version : 90505
File Encoding         : 65001

Date: 2017-01-03 11:52:57
*/


-- ----------------------------
-- Table structure for players
-- ----------------------------
DROP TABLE IF EXISTS "public"."players";
CREATE TABLE "public"."players" (
"idplayer" int4 DEFAULT nextval('players_idplayer_seq'::regclass) NOT NULL,
"name" text COLLATE "default",
"nationality" text COLLATE "default"
)
WITH (OIDS=FALSE)

;

-- ----------------------------
-- Records of players
-- ----------------------------
INSERT INTO "public"."players" VALUES ('1', 'Magnus', 'nor');
INSERT INTO "public"."players" VALUES ('2', 'Fabiano', 'usa');
INSERT INTO "public"."players" VALUES ('3', 'Vladimir', 'rus');
INSERT INTO "public"."players" VALUES ('4', 'Maxime', 'fra');
INSERT INTO "public"."players" VALUES ('5', 'Wesley', 'usa');
INSERT INTO "public"."players" VALUES ('6', 'Sergey', 'rus');
INSERT INTO "public"."players" VALUES ('7', 'Levon', 'arm');
INSERT INTO "public"."players" VALUES ('8', 'Viswanathan', 'ind');
INSERT INTO "public"."players" VALUES ('9', 'Hikaru', 'usa');
INSERT INTO "public"."players" VALUES ('10', 'Anish', 'ned');
INSERT INTO "public"."players" VALUES ('11', 'Pendyala', 'ind');
INSERT INTO "public"."players" VALUES ('12', 'Shakhriyar', 'aze');
INSERT INTO "public"."players" VALUES ('13', 'Ian', 'rus');
INSERT INTO "public"."players" VALUES ('14', 'Pavel', 'ukr');
INSERT INTO "public"."players" VALUES ('15', 'Veselin', 'bul');
INSERT INTO "public"."players" VALUES ('16', 'Liren', 'chn');

-- ----------------------------
-- Alter Sequences Owned By 
-- ----------------------------

-- ----------------------------
-- Primary Key structure for table players
-- ----------------------------
ALTER TABLE "public"."players" ADD PRIMARY KEY ("idplayer");
