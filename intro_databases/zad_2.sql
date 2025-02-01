--z1
SELECT id_kopii, tytul FROM kopie
NATURAL JOIN filmy 
ORDER BY id_kopii;
--z2 
SELECT DISTINCT(tytul) FROM filmy
NATURAL JOIN kopie 
WHERE czy_dostepna = 'T';
--z3
SELECT id_kopii FROM kopie
NATURAL JOIN filmy 
WHERE rok_produkcji = 1984;
--z4
SELECT data_wypozyczenia, data_zwrotu, nazwisko FROM wypozyczenia 
NATURAL JOIN klienci 
--z5
SELECT nazwisko, tytul FROM filmy AS "f"
NATURAL JOIN kopie 
NATURAL JOIN wypozyczenia 
NATURAL JOIN klienci;
--z6
SELECT tytul, rok_produkcji FROM filmy
NATURAL JOIN kopie 
NATURAL JOIN wypozyczenia 
NATURAL JOIN klienci 
WHERE nazwisko = 'Kowalski';
--z7 --subquery
SELECT nazwisko FROM wypozyczenia
NATURAL JOIN klienci 
WHERE data_wypozyczenia = (
	SELECT MIN(data_wypozyczenia) FROM wypozyczenia
); 
--z7 -- without subquery
SELECT nazwisko FROM wypozyczenia
NATURAL JOIN klienci
ORDER BY data_wypozyczenia ASC
LIMIT 1;
--z8
SELECT nazwisko FROM obsada
NATURAL JOIN aktorzy 
NATURAL JOIN filmy 
WHERE tytul = 'Terminator';

--z9
SELECT tytul FROM obsada
NATURAL JOIN aktorzy 
NATURAL JOIN filmy 
WHERE nazwisko = 'De Niro';

--z10
SELECT tytul FROM wypozyczenia 
NATURAL JOIN kopie
NATURAL JOIN filmy
WHERE (data_zwrotu - data_wypozyczenia) = (
 SELECT MAX((data_zwrotu - data_wypozyczenia)) FROM wypozyczenia
);
--z11 2005-07-15, ‘2005-07-20’.
SELECT DISTINCT(nazwisko) FROM wypozyczenia
NATURAL JOIN klienci
NATURAL JOIN kopie
NATURAL JOIN filmy
WHERE data_wypozyczenia BETWEEN '2005-07-15' AND '2005-07-20';
--z12
SELECT DISTINCT(tytul) FROM wypozyczenia
NATURAL JOIN kopie 
NATURAL JOIN filmy
WHERE data_wypozyczenia BETWEEN '2005-07-15' AND '2005-07-25';
--z13 --NATURAL JOIN
SELECT klienci.imie, klienci.nazwisko, aktorzy.nazwisko FROM klienci
CROSS JOIN aktorzy
WHERE klienci.imie = aktorzy.imie;
--z13 --NORMAL INNTER JOIN
SELECT klienci.imie, klienci.nazwisko, aktorzy.nazwisko FROM klienci
JOIN aktorzy ON klienci.imie = aktorzy.imie;
