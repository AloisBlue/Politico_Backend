userstable = """CREATE TABLE if not exists Users(
user_id SERIAL PRIMARY KEY,
firstname varchar (50) NOT NULL,
lastname varchar (50) NOT NULL,
othername varchar (50) NOT NULL,
email varchar(40) NOT NULL UNIQUE,
phoneNumber varchar (20) NOT NULL,
passportUrl varchar (255) NOT NULL,
password_hash varchar(64) NOT NULL,
confirmed boolean DEFAULT 'f',
confirmed_on TIMESTAMP NULL,
isAdmin boolean DEFAULT 'f'
);"""
partiestable = """CREATE TABLE if not exists Parties(
party_id SERIAL PRIMARY KEY,
name varchar (50) NOT NULL,
hqAddress varchar (50) NOT NULL,
logoUrl varchar (150) NOT NULL
);"""
officetable = """CREATE TABLE if not exists Offices(
office_id SERIAL PRIMARY KEY,
name varchar (50) NOT NULL,
type varchar (50) NOT NULL
);"""
queries = [userstable, partiestable, officetable]

# administrator
admin = """INSERT INTO Users(email, firstname, lastname, othername, phonenumber, passporturl, password_hash, confirmed, isadmin) VALUES('anonymousnewblue@gmail.com', 'Alois', 'Mburu', 'Admin', '0791999232', 'https://miro.medium.com/fit/c/240/240/1*hiAQNjsT30LuqlZRmpdJkQ.jpeg', '$2b$12$ql6PgHM9PXnhW2Lh2RyeY.t.OZelCSttKw0Dhdy1SLLvn3RxS.JHq', TRUE, TRUE);"""
