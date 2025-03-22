--1.
CREATE TABLE piasek
	(
	id_ziarenka SERIAL,
	masa_ziarenka REAL,
	kolor_ziarenka VARCHAR(10)
);

INSERT INTO piasek (masa_ziarenka, kolor_ziarenka)
VALUES 
(0.05, 'fioletowy'),
(0.05, 'czarny'),
(0.02, 'zolty'),
(0.03, 'niebieski');

--2.
INSERT INTO piasek (masa_ziarenka, kolor_ziarenka)
SELECT masa_ziarenka, kolor_ziarenka FROM piasek;

SELECT COUNT(id_ziarenka) FROM piasek;

--3. Execution Time: 116.930 ms
EXPLAIN ANALYZE
SELECT kolor_ziarenka FROM piasek
WHERE id_ziarenka = 123456;

--4. Execution Time: 207.953 ms
EXPLAIN ANALYZE
SELECT COUNT(kolor_ziarenka) FROM piasek
WHERE id_ziarenka >= 50000 
	AND id_ziarenka < 50006;

--5. Execution Time: 106.692 ms
EXPLAIN ANALYZE
SELECT COUNT(id_ziarenka) FROM piasek
WHERE kolor_ziarenka = 'niebieski';
-- Execution Time: 359.212 ms
EXPLAIN ANALYZE
SELECT masa_ziarenka FROM piasek
WHERE masa_ziarenka = (
	SELECT MAX(masa_ziarenka) FROM piasek
);
--6. 
CREATE INDEX piasek_ind 
ON piasek(id_ziarenka);

--7.
--Czas zmienijszył się o 1916.89 raza
--SELECT ROUND(116.930/0.061, 2)
--Execution Time: 0.061 ms
EXPLAIN ANALYZE
SELECT kolor_ziarenka FROM piasek
WHERE id_ziarenka = 123456;

--8.Execution Time: 0.058 ms
-- Czas zmniejszył się o 3585.40 raza
--SELECT ROUND(207.953/0.058, 2)
EXPLAIN ANALYZE
SELECT COUNT(kolor_ziarenka) FROM piasek
WHERE id_ziarenka >= 50000 
	AND id_ziarenka < 50006;
--9.Execution Time: 332.757 ms nie uległ zmianie, nie
-- stworzyliśmy indexu dla masy_ziarenka
EXPLAIN ANALYZE
SELECT masa_ziarenka FROM piasek
WHERE masa_ziarenka = (
	SELECT MAX(masa_ziarenka) FROM piasek
);

DROP INDEX piasek_ind;

