--1.
SELECT nazwisko FROM aktorzy
UNION
SELECT nazwisko FROM klienci
ORDER BY nazwisko ASC;
--2.
SELECT tytul FROM filmy
NATURAL JOIN obsada
NATURAL JOIN aktorzy
WHERE nazwisko = 'De Niro'
INTERSECT
SELECT tytul FROM filmy
NATURAL JOIN obsada
NATURAL JOIN aktorzy
WHERE nazwisko = 'Reno';
--3.
SELECT tytul FROM filmy
NATURAL JOIN kopie
NATURAL JOIN wypozyczenia
NATURAL JOIN klienci
WHERE nazwisko = 'Nowak'
INTERSECT
SELECT tytul FROM filmy
NATURAL JOIN kopie
NATURAL JOIN wypozyczenia
NATURAL JOIN klienci
WHERE nazwisko = 'Kowalski';
--4.
SELECT tytul FROM filmy
NATURAL JOIN kopie
NATURAL JOIN wypozyczenia
NATURAL JOIN klienci
WHERE nazwisko = 'Kowalski'
EXCEPT
SELECT tytul FROM filmy
NATURAL JOIN kopie
NATURAL JOIN wypozyczenia
NATURAL JOIN klienci
WHERE nazwisko = 'Nowak';
--5.
SELECT nazwisko FROM aktorzy
NATURAL JOIN obsada
NATURAL JOIN filmy
WHERE tytul = 'Terminator'
EXCEPT
SELECT nazwisko FROM aktorzy
NATURAL JOIN obsada
NATURAL JOIN filmy
WHERE tytul = 'Ghostbusters';



