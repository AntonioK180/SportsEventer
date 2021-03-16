USE SportsEventer;

CREATE TABLE Users(
	id int Primary Key not null auto_increment,
	email tinytext not null,
	username tinytext not null,
	pwd tinytext not null
);

CREATE TABLE Event(
	id int Primary Key not null auto_increment,
	user_id int not null,
	sport enum('Football', 'Tennis', 'Basketball', 'Volleyball', 'Table Tennis'),
	people_part int,
	people_needed int,
	event_date datetime,
	location_lat double(7, 4),
	location_lng double(7, 4),
	price double(8, 2),
	description mediumtext,
	FOREIGN_KEY (user_id) REFERENCES Users(id),
	CHECK (people_part > 0),
	CHECK (people_needed >= 0),
	CHECK (price >= 0)
);
