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
