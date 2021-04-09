DROP DATABASE IF EXISTS SportsEventer;
CREATE DATABASE SportsEventer;
USE SportsEventer;

CREATE TABLE Events(
  event_id INT PRIMARY KEY auto_increment,
  created_by VARCHAR(40) NOT NULL,
  sport VARCHAR(15),
  people_participating INT,
  people_needed INT,
  date_time VARCHAR(50),
  location VARCHAR(150),
  price FLOAT,
  description VARCHAR(300)
);

CREATE TABLE Users(
  user_id int Primary Key not null auto_increment,
  email tinytext not null,
  username tinytext not null,
  pwd tinytext not null
);
