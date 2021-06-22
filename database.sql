DROP DATABASE IF EXISTS SportsEventer;
CREATE DATABASE SportsEventer;
USE SportsEventer;

CREATE TABLE Events(
  event_id             INT PRIMARY KEY auto_increment,
  created_by           VARCHAR(40) NOT NULL,
  sport                VARCHAR(15),
  people_participating INT,
  people_needed        INT,
  event_date           VARCHAR(50),
  event_time           VARCHAR(30),
  location             VARCHAR(150),
  price                FLOAT,
  description          VARCHAR(300)
);

CREATE TABLE Users(
  user_id          INT PRIMARY KEY NOT NULL auto_increment,
  email            VARCHAR(60) NOT NULL,
  username         VARCHAR(40) NOT NULL,
  pwd              VARCHAR(300) NOT NULL,
  confirmed        BOOL DEFAULT 0
);

CREATE TABLE UsersEvents(
  id          INT PRIMARY KEY NOT NULL auto_increment,
  event_id    INT NOT NULL,
  FOREIGN KEY(event_id) REFERENCES Events(event_id),
  user_id     INT NOT NULL,
  FOREIGN KEY(user_id) REFERENCES Users(user_id)
);
