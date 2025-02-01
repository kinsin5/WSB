--1.
SELECT tytul FROM filmy
WHERE cena = (
	SELECT MAX(cena) FROM filmy
);
--2.
SELECT nazwisko FROM wypozyczenia
NATURAL JOIN klienci
WHERE wypozyczenia.data_wypozyczenia = (
	SELECT MIN(data_wypozyczenia) FROM wypozyczenia
);
--3.
SELECT tytul FROM filmy
WHERE id_filmu IN (
	SELECT id_filmu FROM kopie
	WHERE czy_dostepna = 'T'
);
--4.
SELECT tytul FROM filmy
WHERE cena > (
	SELECT cena FROM filmy
	WHERE tytul = 'Frantic'
);
--5.
SELECT tytul FROM filmy
WHERE cena > (
	SELECT MAX(cena) FROM filmy
	WHERE LENGTH(tytul) = 6
)
