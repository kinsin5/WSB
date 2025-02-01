--1.
INSERT INTO filmy (id_filmu, tytul, rok_produkcji, cena)
VALUES 
(11, 'Komornik', 2005, 10.5);
--SELECT * FROM filmy;
--2.
DELETE FROM filmy 
WHERE rok_produkcji = 2005;
--SELECT * FROM filmy;
--3.
UPDATE filmy SET cena = cena + 0.5
WHERE rok_produkcji < 1980;
--SELECT * FROM filmy ORDER BY id_filmu ASC;
--4.
INSERT INTO filmy (id_filmu, tytul, rok_produkcji, cena)
VALUES 
(12, 'Nikofor', 2004, 9.5);
--SELECT * FROM filmy ORDER BY id_filmu ASC;
--5.
DELETE FROM filmy
	WHERE tytul IN (
	SELECT tytul FROM filmy
	EXCEPT
	SELECT DISTINCT(tytul) FROM filmy
	NATURAL JOIN obsada
);
--SELECT * FROM filmy ORDER BY id_filmu ASC;
--6.
UPDATE filmy SET cena = 5.0
WHERE tytul = 'Taksowkarz';
--SELECT * FROM filmy ORDER BY id_filmu ASC;