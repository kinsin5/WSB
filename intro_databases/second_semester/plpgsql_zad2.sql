--1.
ALTER TABLE filmy
ADD UNIQUE(id_filmu);

--2.
CREATE OR REPLACE FUNCTION dodaj_film(id INTEGER, tyt VARCHAR, 
	rok INTEGER, c REAL) RETURNS VOID AS
$$
BEGIN
	EXECUTE 
		FORMAT('INSERT INTO filmy (id_filmu, tytul, rok_produkcji, cena) 
				VALUES ($1, $2, $3, $4)') USING id, tyt, rok, c; 
EXCEPTION 
	WHEN UNIQUE_VIOLATION THEN
	EXECUTE
		FORMAT('INSERT INTO filmy (id_filmu, tytul, rok_produkcji, cena) 
				VALUES ((SELECT MAX(id_filmu) + 1 FROM filmy), $1, $2, $3)') USING tyt, rok, c; 
END;	
$$ LANGUAGE PLPGSQL;


SELECT dodaj_film(2, 'Film2', 1999, 1.99);

SELECT * FROM filmy;


CREATE OR REPLACE FUNCTION insert_into_table(table_name TEXT, id_val INT, name_val TEXT)
RETURNS VOID AS
$$
BEGIN
    EXECUTE FORMAT('INSERT INTO %I (id, name) VALUES ($1, $2)', table_name) USING id_val, name_val;
END;
$$ LANGUAGE plpgsql;


/*. Utwórz funkcję o nazwie DODAJ_FILM(id INTEGER, tyt VARCHAR, rok INTEGER, c
REAL), służącą do wprowadzania nowej krotki do relacji 
FILMY. W przypadku, gdy podczas
wykonania funkcji wystąpi wyjątek naruszenia 
ograniczenia integralnościowego UNIQUE,
automatycznie zmodyfikuj wartość identyfikatora nowego
filmu tak, aby była niepowtarzalna
(np. aktualna wartość maksymalna + 1). 
Przetestuj działanie funkcji.
*/