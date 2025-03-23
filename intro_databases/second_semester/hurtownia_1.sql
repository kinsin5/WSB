CREATE TABLE pora_rozmowy(
	id_pory SERIAL,
	przedzial_godziny VARCHAR,
	PRIMARY KEY (id_pory)
);

CREATE TABLE miejsce_rozmowy(
	id_miejsca SERIAL,
	strona_swiata VARCHAR,
	wojewodztwo VARCHAR,
	miasto VARCHAR,
	PRIMARY KEY(id_miejsca)
);

CREATE TABLE rozmowca(
	id_rozmowcy SERIAL,
	wiek INTEGER,
	przedzial_wieku VARCHAR,
	PRIMARY KEY(id_rozmowcy)
);
CREATE TABLE rozmowa_telefoniczna(
	id_rozmowy SERIAL,
	id_miejsca INT REFERENCES miejsce_rozmowy(id_miejsca),
	id_rozmowcy INTEGER REFERENCES rozmowca(id_rozmowcy),
	id_pory INTEGER REFERENCES pora_rozmowy(id_pory),
	czas_rozmowy REAL,
	PRIMARY KEY(id_rozmowy)
);

INSERT INTO miejsce_rozmowy 
VALUES
(1, 'Wschod', 'Lubelskie', 'Lublin'),
(2, 'Zachod', 'Wielkopolskie', 'Poznan');

INSERT INTO rozmowca 
VALUES
(1, 20, '18-20 lat'),
(2, 50, '45-65 lat');

INSERT INTO pora_rozmowy
VALUES
(1, '08:00-18:00'),
(2, '18:00=22:00');

INSERT INTO rozmowa_telefoniczna
VALUES
(1, 1, 1, 1, 50.4),
(2, 2, 2, 2, 114.5);

SELECT id_rozmowy, miasto, przedzial_wieku, czas_rozmowy FROM rozmowa_telefoniczna
NATURAL JOIN miejsce_rozmowy
NATURAL JOIN rozmowca;

/*-napisz funkcję która po wprowadzeniu miasta oraz przedziału wieku (lub godzin) podaje
średni czas trwania rozmowy tel.*/

CREATE OR REPLACE FUNCTION sr_rozmowy(mia VARCHAR, p_wieku VARCHAR)
RETURNS REAl AS
$$
DECLARE
	sr_rozmowy REAL;
BEGIN
	SELECT AVG(czas_rozmowy) INTO sr_rozmowy FROM rozmowa_telefoniczna
	NATURAL JOIN miejsce_rozmowy NATURAL JOIN rozmowca
	WHERE miejsce_rozmowy.miasto = mia 
	AND rozmowca.przedzial_wieku = p_wieku;
	RETURN sr_rozmowy;
END;
$$ LANGUAGE PLPGSQL;


SELECT sr_rozmowy('Lublin', '18-20 lat');


