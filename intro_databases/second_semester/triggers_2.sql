/*Na potrzeby zadań utwórz tablice pracownicy(id_pracownika, imie, nazwisko, miasto, pensja)
1. Utwórz w języku PL/pgSQL funkcję PIT(dochód REAL) służącą do wyliczania należnego podatku
dochodowego od osób fizycznych według skali podatkowej. Obliczenia powinny odbywać się według
następującego algorytmu:
- jeżeli "dochód"<= 85528 zł, to podatek należny wynosi 18% z "dochód" minus 556,02 zł
- jeżeli "dochód" > 85528 zł, to podatek należny wynosi 14839 zł plus 32% z ("dochód" - 85528 zł)
Następnie sprawdź działanie funkcji PIT() na tabeli pracownicy:
select nazwisko, pensja, pit(pensja) from pracownicy; */

INSERT INTO pracownicy (id_pracownika, imie, nazwisko, miasto, pensja)
VALUES 
(6, 'Jan', 'Kowalski', 'Warszawa', 90000);

SELECT * FROM pracownicy;

CREATE OR REPLACE FUNCTION pit(dochod REAL)
RETURNS REAL AS
$$
DECLARE
	podatek REAL;
BEGIN
	IF dochod > 85528 THEN
		podatek := 14839 + (dochod - 85528) * 0.32;
	ELSE
		podatek := (dochod - 556.02) * 0.18;
	END IF;
	RETURN podatek;
END;
$$ LANGUAGE PLPGSQL;

SELECT nazwisko, pensja, pit(pensja) FROM pracownicy;




/* */