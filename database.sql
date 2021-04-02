DROP DATABASE IF EXISTS SportsEventer;
CREATE DATABASE SportsEventer;
USE SportsEventer;

CREATE TABLE Events(
  id INT PRIMARY KEY auto_increment,
  sport VARCHAR(15),
  people_participating INT,
  people_needed INT,
  date_time VARCHAR(50),
  location VARCHAR(150),
  price FLOAT,
  description VARCHAR(300)
);

CREATE TABLE Users(
  id int Primary Key not null auto_increment,
  email tinytext not null,
  username tinytext not null,
  pwd tinytext not null
);
