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

--2. bez aktorów
DROP FUNCTION opis_filmu;

CREATE FUNCTION opis_filmu(id INTEGER) RETURNS VARCHAR AS $$
DECLARE
	opis_film RECORD;
BEGIN 
	SELECT * INTO opis_film FROM filmy 
	NATURAL JOIN obsada
	NATURAL JOIN aktorzy
	WHERE id_filmu = id;
	RETURN 
	'Film "' || opis_film.tytul ||
	'" zostal nakrecony w roku ' ||
	 opis_film.rok_produkcji 
	 || ' przy udziale akrotorow: ';
END;

$$ LANGUAGE PLPGSQL;

CREATE FUNCTION opis_filmu(id INTEGER) RETURNS VARCHAR AS $$
DECLARE
	opis_film RECORD;
	filmy_kursor CURSOR FOR SELECT id_filmu, 
		id_aktora FROM filmy
		NATURAL JOIN obsada
		NATURAL JOIN aktorzy;
	id_f filmy.id_filmu%TYPE;
	id_a aktorzy.id_aktora%TYPE;
	aktorzy VARCHAR;
BEGIN 
	aktorzy := '';
	SELECT * INTO opis_film FROM filmy 
	NATURAL JOIN obsada
	NATURAL JOIN aktorzy
	WHERE id_filmu = id;
	OPEN filmy_kursor;
	LOOP
	 FETCH filmy_kursor INTO id_f, id_a;
	 EXIT WHEN NOT FOUND;
	 aktorzy := aktorzy || id_a || ', ' ;
	END LOOP;
	CLOSE filmy_kursor;
	
	RETURN 
	'Film "' || opis_film.tytul ||
	'" zostal nakrecony w roku ' ||
	 opis_film.rok_produkcji 
	 || ' przy udziale akrotorow: ' 
	 || aktorzy;
	 
END;

$$ LANGUAGE PLPGSQL;


SELECT opis_filmu(1);

SELECT * FROM filmy 
NATURAL JOIN obsada
NATURAL JOIN aktorzy
WHERE id_filmu = 1;