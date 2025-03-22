--WYZWALACZE
/*1. Utwórz relację AKTORZY_OPERACJE(data DATE, oper VARCHAR(100)), która posłuży
do śledzenia operacji wykonywanych przez użytkownika. */
CREATE TABLE AKTORZY_OPERACJE (
	data TIMESTAMP,
	oper VARCHAR(100)
)
DROP TABLE AKTORZY_OPERACJE;
/*2  Utwórz wyzwalacz reagujący na operacje wprowadzania i usuwania krotek z relacji
AKTORZY. Czas i rodzaj każdej operacji wykonywanej na relacji AKTORZY powinien
być zapisywany w relacji AKTORZY_OPERACJE. Przetestuj działanie wyzwalacza.
W rozwiązaniu zamieść wszystkie polecenie potrzebne do utworzenia wyzwalacza. */

CREATE OR REPLACE FUNCTION trig_procedure() RETURNS TRIGGER AS 
$$
BEGIN
	INSERT INTO aktorzy_operacje
	VALUES (now(), TG_OP);
RETURN NEW;
END;
$$ LANGUAGE PLPGSQL;

CREATE TRIGGER trigger_aktorzy
BEFORE INSERT OR DELETE ON aktorzy
FOR EACH ROW EXECUTE PROCEDURE trig_procedure();

SELECT * FROM aktorzy_operacje;

INSERT INTO aktorzy(id_aktora, imie, nazwisko)
VALUES (50, 'Jan', 'Kowalski');

DELETE FROM aktorzy
WHERE id_aktora = 50;
/* 3. Usuń wyzwalacz i procedurę wyzwalacza */

DROP TRIGGER trigger_aktorzy
ON aktorzy;

DROP FUNCTION trig_procedure();