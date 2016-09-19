# create a table;

.headers on

DROP TABLE IF EXISTS asia;
CREATE TABLE asia (asia text, prob real);
INSERT INTO asia VALUES ('Y', 0.01);
INSERT INTO asia VALUES ('N', 0.99);

DROP TABLE IF EXISTS tub_asia;
CREATE TABLE tub_asia (tub text, asia text, prob real);
INSERT INTO tub_asia VALUES ('Y', 'Y', 0.05);
INSERT INTO tub_asia VALUES ('N', 'Y', 0.95);
INSERT INTO tub_asia VALUES ('Y', 'N', 0.01);
INSERT INTO tub_asia VALUES ('N', 'N', 0.99);

DROP TABLE IF EXISTS smoking;
CREATE TABLE smoking (smoking text, prob real);
INSERT INTO smoking VALUES ('Y', 0.50);
INSERT INTO smoking VALUES ('N', 0.50);

DROP TABLE IF EXISTS lung_smoking;
CREATE TABLE lung_smoking (lung text, smoking text, prob real);
INSERT INTO lung_smoking VALUES ('Y', 'Y', 0.1);
INSERT INTO lung_smoking VALUES ('N', 'Y', 0.9);
INSERT INTO lung_smoking VALUES ('Y', 'N', 0.01);
INSERT INTO lung_smoking VALUES ('N', 'N', 0.99);


DROP TABLE IF EXISTS bronc_smoking;
CREATE TABLE bronc_smoking (bronc text, smoking text, prob real);
INSERT INTO bronc_smoking VALUES ('Y', 'Y', 0.6);
INSERT INTO bronc_smoking VALUES ('N', 'Y', 0.4);
INSERT INTO bronc_smoking VALUES ('Y', 'N', 0.3);
INSERT INTO bronc_smoking VALUES ('N', 'N', 0.7);


DROP TABLE IF EXISTS either_lung_tub;
CREATE TABLE either_lung_tub (either text, lung text, tub, prob real);
INSERT INTO either_lung_tub VALUES ('Y', 'Y', 'Y', 1);
INSERT INTO either_lung_tub VALUES ('N', 'Y', 'Y', 0);
INSERT INTO either_lung_tub VALUES ('Y', 'Y', 'N', 1);
INSERT INTO either_lung_tub VALUES ('N', 'Y', 'N', 0);
INSERT INTO either_lung_tub VALUES ('Y', 'N', 'Y', 1);
INSERT INTO either_lung_tub VALUES ('N', 'N', 'Y', 0);
INSERT INTO either_lung_tub VALUES ('Y', 'N', 'N', 0);
INSERT INTO either_lung_tub VALUES ('N', 'N', 'N', 1);


DROP TABLE IF EXISTS xray_either;
CREATE TABLE xray_either (xray text, either text, prob real);
INSERT INTO xray_either VALUES ('Y', 'Y', 0.98);
INSERT INTO xray_either VALUES ('N', 'Y', 0.02);
INSERT INTO xray_either VALUES ('Y', 'N', 0.05);
INSERT INTO xray_either VALUES ('N', 'N', 0.95);

DROP TABLE IF EXISTS dysp_either_bronc;
CREATE TABLE dysp_either_bronc (dysp text, either text, bronc text, prob real);
INSERT INTO dysp_either_bronc VALUES ('Y', 'Y', 'Y', 0.90);
INSERT INTO dysp_either_bronc VALUES ('N', 'Y', 'Y', 0.10);
INSERT INTO dysp_either_bronc VALUES ('Y', 'Y', 'N', 0.70);
INSERT INTO dysp_either_bronc VALUES ('N', 'Y', 'N', 0.30);
INSERT INTO dysp_either_bronc VALUES ('Y', 'N', 'Y', 0.80);
INSERT INTO dysp_either_bronc VALUES ('N', 'N', 'Y', 0.20);
INSERT INTO dysp_either_bronc VALUES ('Y', 'N', 'N', 0.10);
INSERT INTO dysp_either_bronc VALUES ('N', 'N', 'N', 0.90);


## Joint probability of asia and tb
DROP VIEW tub;
CREATE VIEW IF NOT EXISTS tub AS SELECT tub_asia.tub as tub, SUM(tub_asia.prob*asia.prob) as prob FROM tub_asia, asia WHERE tub_asia.asia=asia.asia GROUP BY tub_asia.tub;

## Joint probability of smoking and lung
DROP VIEW lung;
CREATE VIEW IF NOT EXISTS lung AS SELECT lung_smoking.lung as lung, SUM(lung_smoking.prob*smoking.prob) as prob FROM lung_smoking, smoking WHERE lung_smoking.smoking=smoking.smoking GROUP BY lung_smoking.lung;

## Joint probability of smoking and bronc
DROP VIEW bronc;
CREATE VIEW IF NOT EXISTS bronc AS SELECT bronc_smoking.bronc as bronc, SUM(bronc_smoking.prob*smoking.prob) as prob FROM bronc_smoking, smoking WHERE bronc_smoking.smoking=smoking.smoking GROUP BY bronc_smoking.bronc;

DROP VIEW either;
CREATE VIEW IF NOT EXISTS either AS SELECT either_lung_tub.either as either, SUM(either_lung_tub.prob*lung.prob*tub.prob) as prob FROM either_lung_tub, lung, tub WHERE either_lung_tub.lung=lung.lung AND either_lung_tub.tub=tub.tub GROUP BY either_lung_tub.either;

DROP VIEW dysp;
CREATE VIEW IF NOT EXISTS dysp AS SELECT dysp_either_bronc.dysp as dysp, SUM(dysp_either_bronc.prob*either.prob*bronc.prob) as prob FROM dysp_either_bronc, either, bronc WHERE dysp_either_bronc.either=either.either AND dysp_either_bronc.bronc=bronc.bronc GROUP by dysp_either_bronc.dysp;
SELECT dysp.dysp, dysp.prob/SUM(dysp.prob) FROM dysp;


DROP VIEW xray;
CREATE VIEW IF NOT EXISTS xray AS SELECT xray_either.xray as xray, SUM(xray_either.prob*either.prob) as prob FROM xray_either, either WHERE xray_either.either=either.either GROUP by xray_either.xray;
SELECT xray.xray, xray.prob/SUM(xray.prob) FROM xray;


#### Not working


DROP VIEW dysp_either;
CREATE VIEW IF NOT EXISTS dysp_either AS SELECT dysp_either_bronc.dysp as dysp, dysp_either_bronc.either as either, SUM(dysp_either_bronc.prob*bronc.prob) as prob FROM dysp_either_bronc, bronc GROUP by dysp_either_bronc.dysp, dysp_either_bronc.either;
SELECT dysp_either.dysp, dysp_either.prob/SUM(dysp_either.prob) FROM dysp_either;

DROP VIEW either_post;
CREATE VIEW IF NOT EXISTS either_post AS SELECT either.either as either, SUM(either.prob*bronc.prob*dysp_either_bronc.prob) as prob FROM bronc, either, dysp_either_bronc WHERE dysp_either_bronc.either=either.either AND dysp_either_bronc.dysp= 'Y' AND bronc.bronc='Y' GROUP BY either.either;
SELECT either_post.either, either_post.prob/SUM(either_post.prob) FROM either_post;


