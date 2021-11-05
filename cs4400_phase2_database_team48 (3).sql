-- CS4400: Introduction to Database Systems (Fall 2021)
-- Phase II: Create Table & Insert Statements [v0] Thursday, October 14, 2021 @ 2:00pm EDT

-- Team 48
-- Gabe DuBose (jdubose32)
-- Rachel Calder (rcalder3)
-- Logan Gloster (lgloster3)
-- Harini Narasimhan (hnarasimhan7)

-- Directions:
-- Please follow all instructions for Phase II as listed on Canvas.
-- Fill in the team number and names and GT usernames for all members above.
-- Create Table statements must be manually written, not taken from an SQL Dump file.
-- This file must run without error for credit.

-- ------------------------------------------------------
-- CREATE TABLE STATEMENTS AND INSERT STATEMENTS BELOW
-- ------------------------------------------------------

DROP DATABASE IF EXISTS phase2;
CREATE DATABASE IF NOT EXISTS phase2;
USE phase2;

create table account (
	email varchar(50) not null,
    fname varchar(100),
    lname varchar(100),
    password varchar(50),
    primary key (email)
);

insert into account values ('mmoss1@travelagency.com', 'Mark', 'Moss', 'password1');
insert into account values ('asmith@travelagency.com', 'Aviva', 'Smith', 'password2');
insert into account values ('mscott22@gmail.com', 'Michael', 'Scott', 'password3');
insert into account values ('arthurread@gmail.com', 'Arthur', 'Read', 'password4');
insert into account values ('jwayne@gmail.com', 'John', 'Wayne', 'password5');
insert into account values ('gburdell3@gmail.com', 'George', 'Burdell', 'password6');
insert into account values ('mj23@gmail.com', 'Michael', 'Jordan', 'password7');
insert into account values ('lebron6@gmail.com', 'Lebron', 'James', 'password8');
insert into account values ('msmith5@gmail.com', 'Michael', 'Smith', 'password9');
insert into account values ('ellie2@gmail.com', 'Ellie', 'Johnson', 'password10');
insert into account values ('scooper3@gmail.com', 'Sheldon', 'Cooper', 'password11');
insert into account values ('mgeller5@gmail.com', 'Monica', 'Geller', 'password12');
insert into account values ('cbing10@gmail.com', 'Chandler', 'Bing', 'password13');
insert into account values ('hwmit@gmail.com', 'Howard', 'Wolowitz', 'password14');
insert into account values ('swilson@gmail.com', 'Samantha', 'Wilson', 'password16');
insert into account values ('aray@tiktok.com', 'Addison', 'Ray', 'password17');
insert into account values ('cdemilio@tiktok.com', 'Charlie', 'Demilio', 'password18');
insert into account values ('bshelton@gmail.com', 'Blake', 'Shelton', 'password19');
insert into account values ('lbryan@gmail.com', 'Luke', 'Bryan', 'password20');
insert into account values ('tswift@gmail.com', 'Taylor', 'Swift', 'password21');
insert into account values ('jseinfeld@gmail.com', 'Jerry', 'Seinfeld', 'password22');
insert into account values ('maddiesmith@gmail.com', 'Madison', 'Smith', 'password23');
insert into account values ('johnthomas@gmail.com', 'John', 'Thomas', 'password24');
insert into account values ('boblee15@gmail.com', 'Bob', 'Lee', 'password25');

create table admin (
	email varchar(50) not null,
    constraint admin_fk1 foreign key (email) references account (email),
    primary key (email)
);

insert into admin values ('mmoss1@travelagency.com');
insert into admin values ('asmith@travelagency.com');

create table client (
	phone_number varchar(50),
    email varchar(50) not null,
	primary key (email),
    constraint client_fk2 foreign key (email) references account (email),
    unique (phone_number)
);

insert into client values ('555-123-4567', 'mscott22@gmail.com');
insert into client values ('555-234-5678', 'arthurread@gmail.com');
insert into client values ('555-345-6789', 'jwayne@gmail.com');
insert into client values ('555-456-7890', 'gburdell3@gmail.com');
insert into client values ('555-567-8901', 'mj23@gmail.com');
insert into client values ('555-678-9012', 'lebron6@gmail.com');
insert into client values ('555-789-0123', 'msmith5@gmail.com');
insert into client values ('555-890-1234', 'ellie2@gmail.com');
insert into client values ('678-123-4567', 'scooper3@gmail.com');
insert into client values ('678-234-5678', 'mgeller5@gmail.com');
insert into client values ('678-345-6789', 'cbing10@gmail.com');
insert into client values ('678-456-7890', 'hwmit@gmail.com');
insert into client values ('770-123-4567', 'swilson@gmail.com');
insert into client values ('770-234-5678', 'aray@tiktok.com');
insert into client values ('770-345-6789', 'cdemilio@tiktok.com');
insert into client values ('770-456-7890', 'bshelton@gmail.com');
insert into client values ('770-567-8901', 'lbryan@gmail.com');
insert into client values ('770-678-9012', 'tswift@gmail.com');
insert into client values ('770-789-0123', 'jseinfeld@gmail.com');
insert into client values ('770-890-1234', 'maddiesmith@gmail.com');
insert into client values ('404-770-5555', 'johnthomas@gmail.com');
insert into client values ('404-678-5555', 'boblee15@gmail.com');

create table customer (
	credit_card_number varchar(16),
    email varchar(50) not null,
    exp_date date,
    cvv varchar(3),
    current_location varchar(50),
	primary key (email),
    unique (credit_card_number),
    constraint customer_fk3 foreign key (email) references account (email)
);
 
insert into customer values ('6518555974461660', 'scooper3@gmail.com', '2024-02-28', '551', null);
insert into customer values ('2328567043101965', 'mgeller5@gmail.com', '2024-03-31', '644', null);
insert into customer values ('8387952398279291', 'cbing10@gmail.com', '2023-02-28', '201', null);
insert into customer values ('6558859698525299', 'hwmit@gmail.com', '2023-04-30', '102', null);
insert into customer values ('9383321241981836', 'swilson@gmail.com', '2022-08-31', '455', null);
insert into customer values ('3110266979495605', 'aray@tiktok.com', '2022-08-31', '744', null);
insert into customer values ('2272355540784744', 'cdemilio@tiktok.com', '2025-02-28', '606', null);
insert into customer values ('9276763978834273', 'bshelton@gmail.com', '2023-09-30', '862', null);
insert into customer values ('4652372688643798', 'lbryan@gmail.com', '2023-05-31', '258', null);
insert into customer values ('5478842044367471', 'tswift@gmail.com', '2024-12-31', '857', null);
insert into customer values ('3616897712963372', 'jseinfeld@gmail.com', '2022-06-30', '295', null);
insert into customer values ('9954569863556952', 'maddiesmith@gmail.com', '2022-07-31', '794', null);
insert into customer values ('7580327437245356', 'johnthomas@gmail.com', '2025-10-31', '269', null);
insert into customer values ('7907351371614248', 'boblee15@gmail.com', '2021-11-30', '858', null);
        
create table owner (
	email varchar(50) not null,
	primary key (email),
    constraint owner_fk4 foreign key (email) references client (email)
);

insert into owner values ('mscott22@gmail.com');
insert into owner values ('arthurread@gmail.com');
insert into owner values ('jwayne@gmail.com');
insert into owner values ('gburdell3@gmail.com');
insert into owner values ('mj23@gmail.com');
insert into owner values ('lebron6@gmail.com');
insert into owner values ('msmith5@gmail.com');
insert into owner values ('ellie2@gmail.com');
insert into owner values ('scooper3@gmail.com');
insert into owner values ('mgeller5@gmail.com');
insert into owner values ('cbing10@gmail.com');
insert into owner values ('hwmit@gmail.com');

create table airport (
	airport_id varchar(3) not null,
    airport_name varchar(50),
    street varchar(50),
    city varchar(50),
    state varchar(50),
    zip varchar(5),
    time_zone varchar(50),
    primary key (airport_id),
    unique (street, city, state, zip),
    unique (airport_name)
);

insert into airport values ('ATL', 'Atlanta Hartsfield Jackson Airport', '6000 N Terminal Pkwy', 'Atlanta', 'GA', '30320','EST');
insert into airport values ('JFK', 'John F Kennedy International Airport', '455 Airport Ave', 'Queens', 'NY', '11430', 'EST');
insert into airport values ('LGA', 'Laguardia Airport', '790 Airport St', 'Queens', 'NY', '11371','EST');
insert into airport values ('LAX', 'Lost Angeles International Airport', '1 World Way', 'Los Angeles', 'CA', '90045','PST');
insert into airport values ('SJC', 'Norman Y. Mineta San Jose International Airport', '1702 Airport Blvd', 'San Jose', 'CA', '95110','PST');
insert into airport values ('ORD', "O'Hare International Airport", "10000 W O'Hare Ave", 'Chicago', 'IL', '60666','CST');
insert into airport values ('MIA', 'Miami International Airport', '2100 NW 42nd Ave', 'Miami', 'FL', '33126','EST');
insert into airport values ('DFW', 'Dallas International Airport', '2400 Aviation DR', 'Dallas', 'TX', '75261','CST');

create table airline (
	airline_name varchar(50) not null,
    rating decimal(2,1),
    primary key (airline_name)
);

insert into airline values ('Delta Airlines', '4.7');
insert into airline values ('Southwest Airlines', '4.4');
insert into airline values ('American Airlines', '4.6');
insert into airline values ('United Airlines', '4.2');
insert into airline values ('JetBlue Airways', '3.6');
insert into airline values ('Spirit Airlines', '3.3');
insert into airline values ('WestJet', '3.9');
insert into airline values ('Interjet', '3.7');

create table flight (
	airline varchar(50) not null,
    flight_number varchar(5) not null,
    departure_time time,
	departure_date date,
    arrival_time time,
    cost_per_seat decimal(12,2),
    capacity integer,
    airport_from varchar(3),
    airport_to varchar(3),
    primary key (flight_number, airline),
    constraint flight_fk5 foreign key (airline) references airline (airline_name),
    constraint flight_fk6 foreign key (airport_from) references airport (airport_id),
    constraint flight_fk7 foreign key (airport_to) references airport (airport_id)
);

insert into flight values ('Delta Airlines', '1', '10:00:00', '2021-10-18', '12:00:00', '400.00', '150', 'ATL', 'JFK');
insert into flight values ('Southwest Airlines', '2', '10:30:00', '2021-10-18', '14:30:00', '350.00', '125', 'ORD', 'MIA');
insert into flight values ('American Airlines', '3', '13:00:00', '2021-10-18', '16:00:00', '350.00', '125', 'MIA', 'DFW');
insert into flight values ('United Airlines', '4', '16:30:00', '2021-10-18', '18:30:00', '400.00', '100', 'ATL', 'LGA');
insert into flight values ('JetBlue Airways', '5', '11:00:00', '2021-10-19', '13:00:00', '400.00', '130', 'LGA', 'ATL');
insert into flight values ('Spirit Airlines', '6', '12:30:00', '2021-10-19', '21:30:00', '650.00', '140', 'SJC', 'ATL');
insert into flight values ('WestJet', '7', '13:00:00', '2021-10-19', '16:00:00', '700.00', '100', 'LGA', 'SJC');
insert into flight values ('Interjet', '8', '19:30:00', '2021-10-19', '21:30:00', '350.00', '125', 'MIA', 'ORD');
insert into flight values ('Delta Airlines', '9', '08:00:00', '2021-10-20', '10:00:00', '375.00', '150', 'JFK', 'ATL');
insert into flight values ('Delta Airlines', '10', '09:15:00', '2021-10-20', '18:15:00', '700.00', '110', 'LAX', 'ATL');
insert into flight values ('Southwest Airlines', '11', '12:07:00', '2021-10-20', '19:07:00', '600.00', '95', 'LAX', 'ORD');
insert into flight values ('United Airlines', '12', '15:35:00', '2021-10-20', '17:35:00', '275.00', '115', 'MIA', 'ATL');

create table attractions (
	nearest_airport varchar(3) not null,
	attraction_name varchar(50) not null,
    primary key (nearest_airport, attraction_name),
    constraint attractions_fk8 foreign key (nearest_airport) references airport (airport_id)
);

insert into attractions values ('ATL', 'The Coke Factory');
insert into attractions values ('ATL', 'The Georgia Aquarium');
insert into attractions values ('JFK', 'The Statue of Liberty');
insert into attractions values ('JFK', 'The Empire State Building');
insert into attractions values ('LGA', 'The Statue of Liberty');
insert into attractions values ('LGA', 'The Empire State Building');
insert into attractions values ('LAX', 'Lost Angeles Lakers Stadium');
insert into attractions values ('LAX', 'Los Angeles Kings Stadium');
insert into attractions values ('SJC', 'Winchester Mystery House');
insert into attractions values ('SJC', 'San Jose Earthquakes Soccer Team');
insert into attractions values ('ORD', 'Chicago Blackhawks Stadium');
insert into attractions values ('ORD', 'Chicago Bulls Stadium');
insert into attractions values ('MIA', 'Crandon Park Beach');
insert into attractions values ('MIA', 'Miami Heat Basketball Stadium');
insert into attractions values ('DFW', 'Texas Longhorns Stadium');
insert into attractions values ('DFW', 'The Original Texas Roadhouse');

create table property (
	owner_email varchar(50) not null,
    property_name varchar(50) not null,
    street varchar(50),
    city varchar(50),
    state varchar(50),
    zip integer,
    capacity int,
	cost int,
    description varchar(300),
    primary key (property_name, owner_email),
    unique (street, city, state, zip),
    constraint property_fk9 foreign key (owner_email) references owner (email)
);

insert into property values ('scooper3@gmail.com', 'Atlanta Great Property', '2nd St', 'ATL', 'GA', '30008', '4', '600', 'This is right in the middle of Atlanta near many attractions!');
insert into property values ('gburdell3@gmail.com', 'House near Georgia Tech', 'North Ave', 'ATL', 'GA', '30008', '3', '275', 'Super close to bobby dodde stadium!');
insert into property values ('cbing10@gmail.com', 'New York City Property', '123 Main St', 'NYC', 'NY', '10008', '2', '750', 'A view of the whole city. Great property!');
insert into property values ('mgeller5@gmail.com', 'Statue of Libery Property', '1st St', 'NYC', 'NY', '10009', '5', '1000', 'You can see the statue of liberty from the porch');
insert into property values ('arthurread@gmail.com', 'Los Angeles Property', '10th St', 'LA', 'CA', '90008', '3', '700', null);
insert into property values ('arthurread@gmail.com', 'LA Kings House', 'Kings St', 'La', 'CA', '90011', '4', '750', 'This house is super close to the LA kinds stadium!');
insert into property values ('arthurread@gmail.com', 'Beautiful San Jose Mansion', 'Golden Bridge Pkwt', 'San Jose', 'CA', '90001', '12', '900', 'Huge house that can sleep 12 people. Totally worth it!');
insert into property values ('lebron6@gmail.com', 'LA Lakers Property', 'Lebron Ave', 'LA', 'CA', '90011', '4', '850', 'This house is right near the LA lakers stadium. You might even meet Lebron James!');
insert into property values ('hwmit@gmail.com', 'Chicago Blackhawks House', 'Blackhawks St', 'Chicago', 'IL', '60176', '3', '775', 'This is a great property!');
insert into property values ('mj23@gmail.com', 'Chicago Romantic Getaway', '23rd Main St', 'Chicago', 'IL', '60176', '2', '1050', 'This is a great property!');
insert into property values ('msmith5@gmail.com', 'Beautiful Beach Property', '456 Beach Ave', 'Miami', 'FL', '33101', '2', '975', 'You can walk out of the house and be on the beach!');
insert into property values ('ellie2@gmail.com', 'Family Beach House', '1132 Beach Ave', 'Miami', 'FL', '33101', '6', '850', 'You can literally walk onto the beach and see it from the patio!');
insert into property values ('mscott22@gmail.com', 'Texas Roadhouse', '17th Street', 'Dallas', 'TX', '75043', '3', '450', 'This property is right in the center of Dallas, Texas!');
insert into property values ('mscott22@gmail.com', 'Texas Longhorns House', '1125 Longhorns Way', 'Dallas', 'TX', '75001', '10', '600', 'You can walk to the longhorns stadium from here!');

create table amenities (
	property varchar(50) not null,
    owner_email varchar(50) not null,
    amenity_name varchar(50) not null,
    primary key (amenity_name, owner_email, property),
    constraint amenities_fk10 foreign key (property) references property (property_name),
    constraint amenities_fk11 foreign key (owner_email) references owner (email)
);

insert into amenities values ('Atlanta Great Property', 'scooper3@gmail.com', 'A/C & Heating');
insert into amenities values ('Atlanta Great Property', 'scooper3@gmail.com', 'Pets allowed');
insert into amenities values ('Atlanta Great Property', 'scooper3@gmail.com', 'Wifi & TV');
insert into amenities values ('Atlanta Great Property', 'scooper3@gmail.com', 'Washer and Dryer');
insert into amenities values ('House near Georgia Tech', 'gburdell3@gmail.com', 'Wifi & TV');
insert into amenities values ('House near Georgia Tech', 'gburdell3@gmail.com', 'Washer and Dryer');
insert into amenities values ('House near Georgia Tech', 'gburdell3@gmail.com', 'Full Kitchen');
insert into amenities values ('New York City Property', 'cbing10@gmail.com', 'A/C & Heating');
insert into amenities values ('New York City Property', 'cbing10@gmail.com', 'Wifi & TV');
insert into amenities values ('Statue of Libery Property', 'mgeller5@gmail.com', 'A/C & Heating');
insert into amenities values ('Statue of Libery Property', 'mgeller5@gmail.com', 'Wifi & TV');
insert into amenities values ('Los Angeles Property', 'arthurread@gmail.com', 'A/C & Heating');
insert into amenities values ('Los Angeles Property', 'arthurread@gmail.com', 'Pets allowed');
insert into amenities values ('Los Angeles Property', 'arthurread@gmail.com', 'Wifi & TV');
insert into amenities values ('LA Kings House', 'arthurread@gmail.com', 'A/C & Heating');
insert into amenities values ('LA Kings House', 'arthurread@gmail.com', 'Wifi & TV');
insert into amenities values ('LA Kings House', 'arthurread@gmail.com', 'Washer and Dryer');
insert into amenities values ('LA Kings House', 'arthurread@gmail.com', 'Full Kitchen');
insert into amenities values ('Beautiful San Jose Mansion', 'arthurread@gmail.com', 'A/C & Heating');
insert into amenities values ('Beautiful San Jose Mansion', 'arthurread@gmail.com', 'Pets allowed');
insert into amenities values ('Beautiful San Jose Mansion', 'arthurread@gmail.com', 'Wifi & TV');
insert into amenities values ('Beautiful San Jose Mansion', 'arthurread@gmail.com', 'Washer and Dryer');
insert into amenities values ('Beautiful San Jose Mansion', 'arthurread@gmail.com', 'Full Kitchen');
insert into amenities values ('LA Lakers Property', 'lebron6@gmail.com', 'A/C & Heating');
insert into amenities values ('LA Lakers Property', 'lebron6@gmail.com', 'Wifi & TV');
insert into amenities values ('LA Lakers Property', 'lebron6@gmail.com', 'Washer and Dryer');
insert into amenities values ('LA Lakers Property', 'lebron6@gmail.com', 'Full Kitchen');
insert into amenities values ('Chicago Blackhawks House', 'hwmit@gmail.com', 'A/C & Heating');
insert into amenities values ('Chicago Blackhawks House', 'hwmit@gmail.com', 'Wifi & TV');
insert into amenities values ('Chicago Blackhawks House', 'hwmit@gmail.com', 'Washer and Dryer');
insert into amenities values ('Chicago Blackhawks House', 'hwmit@gmail.com', 'Full Kitchen');
insert into amenities values ('Chicago Romantic Getaway', 'mj23@gmail.com', 'A/C & Heating');
insert into amenities values ('Chicago Romantic Getaway', 'mj23@gmail.com', 'Wifi & TV');
insert into amenities values ('Beautiful Beach Property', 'msmith5@gmail.com', 'A/C & Heating');
insert into amenities values ('Beautiful Beach Property', 'msmith5@gmail.com', 'Wifi & TV');
insert into amenities values ('Beautiful Beach Property', 'msmith5@gmail.com', 'Washer and Dryer');
insert into amenities values ('Family Beach House', 'ellie2@gmail.com', 'A/C & Heating');
insert into amenities values ('Family Beach House', 'ellie2@gmail.com', 'Pets allowed');
insert into amenities values ('Family Beach House', 'ellie2@gmail.com', 'Wifi & TV');
insert into amenities values ('Family Beach House', 'ellie2@gmail.com', 'Washer and Dryer');
insert into amenities values ('Family Beach House', 'ellie2@gmail.com', 'Full Kitchen');
insert into amenities values ('Texas Roadhouse', 'mscott22@gmail.com', 'A/C & Heating');
insert into amenities values ('Texas Roadhouse', 'mscott22@gmail.com', 'Pets allowed');
insert into amenities values ('Texas Roadhouse', 'mscott22@gmail.com', 'Wifi & TV');
insert into amenities values ('Texas Roadhouse', 'mscott22@gmail.com', 'Washer and Dryer');
insert into amenities values ('Texas Longhorns House', 'mscott22@gmail.com', 'A/C & Heating');
insert into amenities values ('Texas Longhorns House', 'mscott22@gmail.com', 'Pets allowed');
insert into amenities values ('Texas Longhorns House', 'mscott22@gmail.com', 'Wifi & TV');
insert into amenities values ('Texas Longhorns House', 'mscott22@gmail.com', 'Washer and Dryer');
insert into amenities values ('Texas Longhorns House', 'mscott22@gmail.com', 'Full Kitchen');

create table owner_rates (
	owner_email varchar(50) not null,
    customer_email varchar(50) not null,
    score decimal(2,1),
    primary key (owner_email, customer_email),
    constraint rates_fk12 foreign key (owner_email) references owner (email),
    constraint rates_fk13 foreign key (customer_email) references customer (email)
);

insert into owner_rates values ('gburdell3@gmail.com', 'swilson@gmail.com', '5');
insert into owner_rates values ('cbing10@gmail.com', 'aray@tiktok.com', '5');
insert into owner_rates values ('mgeller5@gmail.com', 'bshelton@gmail.com', '3');
insert into owner_rates values ('arthurread@gmail.com', 'lbryan@gmail.com', '4');
insert into owner_rates values ('arthurread@gmail.com', 'tswift@gmail.com', '4');
insert into owner_rates values ('lebron6@gmail.com', 'jseinfeld@gmail.com', '1');
insert into owner_rates values ('hwmit@gmail.com', 'maddiesmith@gmail.com', '2');

create table owner_is_rated_by (
	owner_email varchar(50) not null,
    customer_email varchar(50) not null,
    score decimal(2,1),
    primary key (owner_email, customer_email),
    constraint owner_is_rated_by_fk14 foreign key (owner_email) references owner (email),
    constraint owner_is_rated_by_fk15 foreign key (customer_email) references customer (email)
);

insert into owner_is_rated_by values ('gburdell3@gmail.com', 'swilson@gmail.com', '5');
insert into owner_is_rated_by values ('cbing10@gmail.com', 'aray@tiktok.com', '5');
insert into owner_is_rated_by values ('mgeller5@gmail.com', 'bshelton@gmail.com', '4');
insert into owner_is_rated_by values ('arthurread@gmail.com', 'lbryan@gmail.com', '4');
insert into owner_is_rated_by values ('arthurread@gmail.com', 'tswift@gmail.com', '3');
insert into owner_is_rated_by values ('lebron6@gmail.com', 'jseinfeld@gmail.com', '2');
insert into owner_is_rated_by values ('hwmit@gmail.com', 'maddiesmith@gmail.com', '5');

create table reservations (
	owner_email varchar(50) not null,
    reserved_property varchar(50) not null,
    customer_email varchar(50) not null,
    start_date date,
    end_date date,
    number_of_guests integer,
    primary key (owner_email, customer_email, reserved_property),
    constraint reservations_fk16 foreign key (owner_email) references owner (email),
    constraint reservations_fk17 foreign key (reserved_property) references property (property_name),
    constraint reservations_fk18 foreign key (customer_email) references customer (email)
);

insert into reservations values ('gburdell3@gmail.com', 'House near Georgia Tech', 'swilson@gmail.com', '2021-10-19', '2021-10-25', '3');
insert into reservations values ('cbing10@gmail.com', 'New York City Property', 'aray@tiktok.com', '2021-10-18', '2021-10-23', '2');
insert into reservations values ('cbing10@gmail.com', 'New York City Property', 'cdemilio@tiktok.com', '2021-10-24', '2021-10-30', '2');
insert into reservations values ('mgeller5@gmail.com', 'Statue of Libery Property', 'bshelton@gmail.com', '2021-10-18', '2021-10-22', '4');
insert into reservations values ('arthurread@gmail.com', 'Los Angeles Property', 'lbryan@gmail.com', '2021-10-19', '2021-10-25', '2');
insert into reservations values ('arthurread@gmail.com', 'Beautiful San Jose Mansion', 'tswift@gmail.com', '2021-10-19', '2021-10-22', '10');
insert into reservations values ('lebron6@gmail.com', 'LA Lakers Property', 'jseinfeld@gmail.com', '2021-10-19', '2021-10-24', '4');
insert into reservations values ('hwmit@gmail.com', 'Chicago Blackhawks House', 'maddiesmith@gmail.com', '2021-10-19', '2021-10-23', '2');
insert into reservations values ('mj23@gmail.com', 'Chicago Romantic Getaway', 'aray@tiktok.com', '2021-11-01', '2021-11-07', '2');
insert into reservations values ('msmith5@gmail.com', 'Beautiful Beach Property', 'cbing10@gmail.com', '2021-10-18', '2021-10-25', '2');
insert into reservations values ('ellie2@gmail.com', 'Family Beach House', 'hwmit@gmail.com', '2021-10-18', '2021-10-28', '5');

create table reviews (
	owner_email varchar(50) not null,
    property_name varchar(50) not null,
    customer_email varchar(50) not null,
    content varchar(500),
    score decimal(2,0),
    primary key (owner_email, customer_email, property_name),
    constraint reviews_fk19 foreign key (owner_email) references owner (email),
    constraint reviews_fk20 foreign key (property_name) references property (property_name),
    constraint reviews_fk21 foreign key (customer_email) references customer (email)
);

insert into reviews values ('gburdell3@gmail.com', 'House near Georgia Tech', 'swilson@gmail.com', '"This was so much fun. I went and saw the coke factory, the falcons play, GT play, and the Georgia aquarium. Great time! Would highly recommend!', '5');
insert into reviews values ('cbing10@gmail.com', 'New York City Property', 'aray@tiktok.com', 'This was the best 5 days ever! I saw so much of NYC!', '5');
insert into reviews values ('mgeller5@gmail.com', 'Statue of Libery Property', 'bshelton@gmail.com', 'This was truly an excellent experience. I really could see the Statue of Liberty from the property!', '4');
insert into reviews values ('arthurread@gmail.com', 'Los Angeles Property', 'lbryan@gmail.com', 'I had an excellent time!', '4');
insert into reviews values ('arthurread@gmail.com', 'Beautiful San Jose Mansion', 'tswift@gmail.com', 'We had a great time, but the house wasn\'t fully cleaned when we arrived', '3');
insert into reviews values ('lebron6@gmail.com', 'LA Lakers Property', 'jseinfeld@gmail.com', 'I was disappointed that I did not meet lebron james', '2');
insert into reviews values ('hwmit@gmail.com', 'Chicago Blackhawks House', 'maddiesmith@gmail.com', 'This was awesome! I met one player on the chicago blackhawks!', '5');

create table bookings (
	customer_email varchar(50) not null,
    airline varchar(50) not null,
    flight_number varchar(50) not null,
    number_of_seats integer,
    primary key (customer_email, airline, flight_number),
    constraint bookings_fk22 foreign key (customer_email) references customer (email),
    constraint bookings_fk23 foreign key (airline) references airline (airline_name),
    constraint bookings_fk24 foreign key (flight_number) references flight (flight_number)
);

insert into bookings values ('swilson@gmail.com', 'JetBlue Airways', '5', '3');
insert into bookings values ('aray@tiktok.com', 'Delta Airlines', '1', '2');
insert into bookings values ('bshelton@gmail.com', 'United Airlines', '4', '4');
insert into bookings values ('lbryan@gmail.com', 'WestJet', '7', '2');
insert into bookings values ('tswift@gmail.com', 'WestJet', '7', '2');
insert into bookings values ('jseinfeld@gmail.com', 'WestJet', '7', '4');
insert into bookings values ('maddiesmith@gmail.com', 'Interjet', '8', '2');
insert into bookings values ('cbing10@gmail.com', 'Southwest Airlines', '2', '2');
insert into bookings values ('hwmit@gmail.com', 'Southwest Airlines', '2', '5');

create table is_close_to (
	property_name varchar(50) not null,
    owner_email varchar(50) not null,
    airport_id varchar(3) not null,
    distance int,
    primary key (property_name, owner_email, airport_id),
    constraint is_close_to_fk25 foreign key (property_name) references property (property_name),
    constraint is_close_to_fk26 foreign key (owner_email) references owner (email),
    constraint is_close_to_fk27 foreign key (airport_id) references airport (airport_id)
);

insert into is_close_to values ('Atlanta Great Property', 'scooper3@gmail.com', 'ATL', '12');
insert into is_close_to values ('House near Georgia Tech', 'gburdell3@gmail.com', 'ATL', '7');
insert into is_close_to values ('New York City Property', 'cbing10@gmail.com', 'JFK', '10');
insert into is_close_to values ('Statue of Libery Property', 'mgeller5@gmail.com', 'JFK', '8');
insert into is_close_to values ('New York City Property', 'cbing10@gmail.com', 'LGA', '25');
insert into is_close_to values ('Statue of Libery Property', 'mgeller5@gmail.com', 'LGA', '19');
insert into is_close_to values ('Los Angeles Property', 'arthurread@gmail.com', 'LAX', '9');
insert into is_close_to values ('LA Kings House', 'arthurread@gmail.com', 'LAX', '12');
insert into is_close_to values ('Beautiful San Jose Mansion', 'arthurread@gmail.com', 'SJC', '8');
insert into is_close_to values ('Beautiful San Jose Mansion', 'arthurread@gmail.com', 'LAX', '30');
insert into is_close_to values ('LA Lakers Property', 'lebron6@gmail.com', 'LAX', '6');
insert into is_close_to values ('Chicago Blackhawks House', 'hwmit@gmail.com', 'ORD', '11');
insert into is_close_to values ('Chicago Romantic Getaway', 'mj23@gmail.com', 'ORD', '13');
insert into is_close_to values ('Beautiful Beach Property', 'msmith5@gmail.com', 'MIA', '21');
insert into is_close_to values ('Family Beach House', 'ellie2@gmail.com', 'MIA', '19');
insert into is_close_to values ('Texas Roadhouse', 'mscott22@gmail.com', 'DFW', '8');
insert into is_close_to values ('Texas Longhorns House', 'mscott22@gmail.com', 'DFW', '17');






