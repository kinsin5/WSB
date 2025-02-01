--1.
SELECT rok_produkcji, AVG(cena) AS "avg" FROM filmy
GROUP BY rok_produkcji
ORDER BY rok_produkcji DESC;
--2.
SELECT MAX(cena) AS "max" FROM filmy;
--3.
SELECT COUNT(id_filmu) AS "count" FROM filmy
WHERE rok_produkcji = 1984;
--4.
SELECT COUNT(id_klienta) AS "count" FROM wypozyczenia
NATURAL JOIN kopie
NATURAL JOIN filmy
WHERE tytul = 'Taksowkarz';
--5.
SELECT ROUND(AVG(JULIANDAY(data_zwrotu) - JULIANDAY(data_wypozyczenia)),1) AS "round"   FROM wypozyczenia
NATURAL JOIN kopie
NATURAL JOIN filmy
WHERE tytul = 'Ronin';
--6.
SELECT 
	tytul, 
	ROUND(MIN(JULIANDAY(data_zwrotu) - JULIANDAY(data_wypozyczenia)),1) AS "min",   
	ROUND(MAX(JULIANDAY(data_zwrotu) - JULIANDAY(data_wypozyczenia)),1) AS "max",
	ROUND(AVG(JULIANDAY(data_zwrotu) - JULIANDAY(data_wypozyczenia)),1) AS "sre",
	COUNT(wypozyczenia.id_klienta) AS "razy"
 FROM wypozyczenia
NATURAL JOIN kopie
NATURAL JOIN filmy
GROUP BY tytul
ORDER BY razy DESC, tytul ASC;
--7.
SELECT imie, nazwisko, COUNT(wypozyczenia.id_klienta) AS "count" FROM klienci
NATURAL JOIN wypozyczenia
GROUP BY imie, nazwisko;
--8.
SELECT nazwisko, COUNT(aktorzy.id_aktora) AS "filmy" FROM aktorzy
NATURAL JOIN obsada
GROUP BY nazwisko
HAVING filmy > 1;
--9.
SELECT nazwisko, SUM(cena) AS "kwota" FROM klienci
NATURAL JOIN wypozyczenia
NATURAL JOIN kopie
NATURAL JOIN filmy
GROUP BY nazwisko;
