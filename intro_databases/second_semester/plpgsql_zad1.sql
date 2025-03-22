--1.
CREATE FUNCTION cena_brutto(c real) RETURNS REAL AS $$
DECLARE 
	brutto REAL;
BEGIN
	brutto := c + (c * 0.23);
	RETURN brutto;
END;
$$ LANGUAGE PLPGSQL;

SELECT tytul, cena, 
	cena_brutto(cena) AS "cena brutto" 
	FROM filmy;

--2. 
CREATE FUNCTION opis_filmu(id INTEGER) RETURNS VARCHAR AS $$
DECLARE
	opis_film RECORD;
	filmy_kursor CURSOR FOR 
		SELECT 
		imie, nazwisko FROM filmy
		NATURAL JOIN obsada
		NATURAL JOIN aktorzy
		WHERE id_filmu = id;
	imie_a aktorzy.imie%TYPE;
	nazwisko_a aktorzy.nazwisko%TYPE;
	aktorzy VARCHAR;
BEGIN 
	aktorzy := '';
	SELECT * INTO opis_film FROM filmy 
	NATURAL JOIN obsada
	NATURAL JOIN aktorzy
	WHERE id_filmu = id;
	OPEN filmy_kursor;
	LOOP
	 FETCH filmy_kursor INTO imie_a, nazwisko_a;
	 EXIT WHEN NOT FOUND;
	 aktorzy := aktorzy || imie_a || ' ' || nazwisko_a 
	 || ', ' ;
	END LOOP;
	CLOSE filmy_kursor;
	
	RETURN 
	'Film "' || opis_film.tytul ||
	'" zostal nakrecony w roku ' ||
	 opis_film.rok_produkcji 
	 || ' przy udziale aktorow: ' 
	 || LEFT(aktorzy, LENGTH(aktorzy) - 2) || '.';
	 
END;

$$ LANGUAGE PLPGSQL;

DROP FUNCTION opis_filmu
SELECT opis_filmu(1);