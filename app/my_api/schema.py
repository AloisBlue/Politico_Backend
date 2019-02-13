userstable = """CREATE TABLE if not exists Users(
user_id SERIAL PRIMARY KEY,
firstname varchar (50) NOT NULL,
lastname varchar (50) NOT NULL,
othername varchar (50) NOT NULL,
email varchar(40) NOT NULL UNIQUE,
phoneNumber varchar (20) NOT NULL,
passportUrl varchar (255) NOT NULL,
password_hash varchar(128) NOT NULL,
isAdmin boolean DEFAULT 'f'
);"""
queries = [userstable]
