userstable = """CREATE TABLE if not exists Users(
user_id SERIAL PRIMARY KEY,
firstname varchar (50) NOT NULL,
lastname varchar (50) NOT NULL,
othername varchar (50) NOT NULL,
email varchar(40) NOT NULL UNIQUE,
phoneNumber varchar (20) NOT NULL,
passportUrl varchar (255) NOT NULL,
password_hash varchar(64) NOT NULL,
isAdmin boolean DEFAULT 'f'
);"""
partiestable = """CREATE TABLE if not exists Parties(
party_id SERIAL PRIMARY KEY,
name varchar (50) NOT NULL,
hqAddress varchar (50) NOT NULL,
logoUrl varchar (150) NOT NULL
);"""
queries = [userstable, partiestable]
