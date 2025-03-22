--1.
ALTER TABLE filmy
ADD UNIQUE(id_filmu);

--2.
CREATE OR REPLACE FUNCTION dodaj_film(id INTEGER, tyt VARCHAR, 
	rok INTEGER, c REAL) RETURNS VOID AS
$$
DECLARE
	new_id INTEGER;
BEGIN
	EXECUTE 
		FORMAT('INSERT INTO filmy (id_filmu, tytul, rok_produkcji, cena) 
				VALUES ($1, $2, $3, $4)') USING id, tyt, rok, c; 
EXCEPTION 
	WHEN UNIQUE_VIOLATION THEN
	SELECT MAX(id_filmu) + 1 INTO new_id FROM filmy;
	EXECUTE
		FORMAT('INSERT INTO filmy (id_filmu, tytul, rok_produkcji, cena) 
				VALUES ($1, $2, $3, $4)') USING new_id, tyt, rok, c; 
END;	
$$ LANGUAGE PLPGSQL;


SELECT dodaj_film(2, 'Film3', 1999, 1.99);

SELECT * FROM filmy;



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