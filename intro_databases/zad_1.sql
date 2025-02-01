--zadanie 1 
SELECT tytul FROM filmy
WHERE rok_produkcji BETWEEN 1998 AND 1999;

--zadanie 2
-- Wyświetl tytuły i ceny wypożyczenia filmów, których cena wypożyczenia przekracza 9 zł. Wynik uporządkuj
--rosnąco według ceny wypożyczenia.
SELECT tytul, cena FROM filmy
WHERE cena > 9
ORDER BY cena ASC;

--zadanie 3
SELECT nazwisko FROM klienci
WHERE imie = 'Jan';

--z4
SELECT imie, nazwisko FROM klienci
WHERE length(imie) > length(nazwisko);

--z5
SELECT nazwisko FROM aktorzy
WHERE imie IN ('Arnold', 'Tom', 'Jodie')
ORDER BY nazwisko;

--z6
SELECT DISTINCT(id_filmu) FROM kopie
WHERE czy_dostepna = 'T';

--z7
SELECT DISTINCT(id_kopii) FROM wypozyczenia
WHERE data_wypozyczenia BETWEEN '2005-07-15' AND '2005-07-22'
ORDER BY id_kopii;
--z8 Wyświetl identyfikatory i czas trwania wypożyczenia (w dniach) wszystkich kopii, które zostały wypożyczone na
--okres dłuższy niż 1 dzień.
SELECT id_kopii, ( data_zwrotu - data_wypozyczenia) AS "czas" FROM wypozyczenia
WHERE data_zwrotu - data_wypozyczenia > 1;
--z9
SELECT (UPPER(substring(imie,1,1)) || '. ' || nazwisko ) AS "aktor" FROM aktorzy;

--z10
SELECT tytul FROM "filmy"
ORDER BY LENGTH(tytul) ASC;
--z11
SELECT tytul, cena FROM filmy
ORDER BY rok_produkcji DESC
LIMIT 3;

--z12
SELECT imie, 
	SUBSTRING(imie,1,1) AS "pierwsza", 
	SUBSTRING(imie, LENGTH(imie), 1) AS "ostatnia" 
 FROM klienci;
 --z13
 SELECT DISTINCT(imie)
 FROM klienci
 WHERE 
 UPPER(SUBSTRING(imie,1,1)) = UPPER(SUBSTRING(imie, LENGTH(imie), 1));
 --z14
 SELECT tytul FROM filmy
 WHERE SUBSTRING(tytul, LENGTH(tytul)-1,1) = 'o';
 --z15
 SELECT LOWER(imie) || '.' || LOWER(nazwisko) || '@wsb.pl' FROM klienci;
 