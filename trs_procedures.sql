-- CS4400: Introduction to Database Systems (Fall 2021)
-- Phase III: Stored Procedures & Views [v0] Tuesday, November 9, 2021 @ 12:00am EDT
-- Team __
-- Rachel Calder (rcalder3)
-- James DuBose (jdubose32)
-- Harini Narasimhan (hnarasimhan7)
-- Logan Gloster (lgloster3)
-- Directions:
-- Please follow all instructions for Phase III as listed on Canvas.
-- Fill in the team number and names and GT usernames for all members above.


-- ID: 1a
-- Name: register_customer
drop procedure if exists register_customer;
delimiter //
create procedure register_customer (
    in i_email varchar(50),
    in i_first_name varchar(100),
    in i_last_name varchar(100),
    in i_password varchar(50),
    in i_phone_number char(12),
    in i_cc_number varchar(19),
    in i_cvv char(3),
    in i_exp_date date,
    in i_location varchar(50)
) 
sp_main: begin
IF NOT EXISTS (SELECT Email, ccnumber from customer WHERE Email = i_email or ccnumber = i_cc_number)
then
IF NOT EXISTS (SELECT Email from accounts WHERE Email = i_email)
    then 
IF NOT EXISTS (SELECT Email, Phone_Number FROM clients WHERE Email = i_email or Phone_Number = i_phone_number)
    then 
IF NOT EXISTS (SELECT email, CCNumber  FROM customer WHERE Email = i_email or CCNumber = i_cc_number)

	Then 
    INSERT INTO accounts (Email, First_name, Last_name, Pass)
            VALUES    ( i_email,
                         i_first_name, i_last_name, i_password); 
    INSERT INTO Clients (Email, Phone_Number)
            VALUES     ( i_email,
                         i_phone_number);

INSERT INTO Customer (Email, CCNumber, Cvv, Exp_Date, Location)
            VALUES     ( i_email,
                         i_cc_number,
                         i_cvv, i_exp_date, i_location);
end if;
end if;
end if;
end if;

end //
delimiter ;


-- ID: 1b
-- Name: register_owner
drop procedure if exists register_owner;
delimiter //
create procedure register_owner (
    in i_email varchar(50),
    in i_first_name varchar(100),
    in i_last_name varchar(100),
    in i_password varchar(50),
    in i_phone_number char(12)
) 
sp_main: begin
IF NOT EXISTS (SELECT Email from owners WHERE Email = i_email)
then
IF NOT EXISTS (SELECT Email from accounts WHERE Email = i_email)
    then 
IF NOT EXISTS (SELECT Email, Phone_Number FROM clients WHERE Email = i_email or Phone_Number = i_phone_number)
	then
IF NOT EXISTS (SELECT email  FROM owners WHERE Email = i_email)
	Then
INSERT INTO accounts (Email, First_name, Last_name, Pass)
		VALUES    ( i_email,
                         i_first_name, i_last_name, i_password); 

 INSERT INTO Clients (Email, Phone_Number)
            VALUES     ( i_email,
                         i_phone_number);
 INSERT INTO owners (Email)
            VALUES     ( i_email);
end if;
end if;            
end if;
end if;


end //
delimiter ;


-- ID: 1c
-- Name: remove_owner
drop procedure if exists remove_owner;
delimiter //
create procedure remove_owner ( 
    in i_owner_email varchar(50)
)
sp_main: begin
IF not exists (SELECT owner_email FROM property WHERE owner_email = i_owner_email)
    then delete from review
        WHERE owner_email = i_owner_email;
delete from reserve
        WHERE owner_email = i_owner_email;
delete from owners_rate_customers
        WHERE owner_email = i_owner_email;
delete from Customers_Rate_Owners
        WHERE owner_email = i_owner_email;
delete from is_close_to
        WHERE owner_email = i_owner_email;
delete from amenity
        WHERE property_owner = i_owner_email;
delete from owners
        WHERE email = i_owner_email;

IF NOT EXISTS (SELECT email  FROM customer WHERE Email = i_owner_email)
    then delete from clients
        WHERE email = i_owner_email;
delete from accounts
        WHERE email = i_owner_email;

end if;
end if;


end //
delimiter ;


-- ID: 2a
-- Name: schedule_flight
drop procedure if exists schedule_flight;
delimiter //
create procedure schedule_flight (
    in i_flight_num char(5),
    in i_airline_name varchar(50),
    in i_from_airport char(3),
    in i_to_airport char(3),
    in i_departure_time time,
    in i_arrival_time time,
    in i_flight_date date,
    in i_cost decimal(6, 2),
    in i_capacity int,
    in i_current_date date
)
sp_main: begin
If not exists (select flight_num, airline_name from flight where flight_num = i_flight_num and airline_name = i_airline_name)
and (i_from_airport != i_to_airport) and (i_flight_date > i_current_date)
	then INSERT INTO flight (Flight_Num, Airline_Name, From_Airport, To_Airport, Departure_Time, Arrival_Time, Flight_Date, Cost, Capacity)
            VALUES    (i_flight_num, i_airline_name, i_from_airport, i_to_airport, i_departure_time, 
            i_arrival_time, i_flight_date, i_cost, i_capacity);
end if;
end //
delimiter ;


-- ID: 2b
-- Name: remove_flight
drop procedure if exists remove_flight;
delimiter //
create procedure remove_flight ( 
    in i_flight_num char(5),
    in i_airline_name varchar(50),
    in i_current_date date
) 
sp_main: begin
if (select Flight_Date from Flight where Flight_Num = i_flight_num and airline_name = i_airline_name) > i_current_date
then delete from Book where Flight_Num = i_flight_num and airline_name = i_airline_name;
delete from Flight where Flight_Num = i_flight_num and airline_name = i_airline_name; 
end if;

end //
delimiter ;


-- ID: 3a
-- Name: book_flight
drop procedure if exists book_flight;
delimiter //
create procedure book_flight (
    in i_customer_email varchar(50),
    in i_flight_num char(5),
    in i_airline_name varchar(50),
    in i_num_seats int,
    in i_current_date date
)
sp_main: begin
#if the number of seats for the flight in question can be booked given the capacity
If  i_num_seats < (select ((select capacity from flight where flight_num = i_flight_num and airline_name = i_airline_name)-count(num_seats)) 
from (select b.customer, b.flight_num, b.airline_name, b.num_seats, b.was_cancelled, f.capacity, f.flight_date
from ((select * from book) b join (select * from flight) f on b.Flight_num = f.flight_num and b.airline_name = f.airline_name) 
where b.flight_num = i_flight_num and b.airline_name = i_airline_name and b.was_cancelled = 0) as c)
Then
#if the flight date is in the future
If Exists (select * from flight where flight_date > i_current_date and flight_num = i_flight_num and 
airline_name = i_airline_name)
Then
# if the flight in question has been booked and it has not been cancelled, update the count with the seats
If Exists (select b.customer, b.flight_num, b.airline_name, b.num_seats, b.was_cancelled, f.capacity, f.flight_date
from ((select * from book) b join (select * from flight) f on b.Flight_num = f.flight_num and b.airline_name = f.airline_name) 
where f.flight_date > i_current_date and b.flight_num = i_flight_num and 
b.airline_name = i_airline_name and b.customer = i_customer_email and was_cancelled = 0)
	then
update book set num_seats = (num_seats + i_num_seats) where customer =
i_customer_email and flight_num = i_flight_num and airline_name = i_airline_name and was_cancelled = 0;
else
#if the customer does not have a 
IF not exists (select b.customer, b.flight_num, b.airline_name, b.num_seats, b.was_cancelled, f.capacity, f.flight_date
from ((select * from book) b left outer join (select * from flight) f on b.Flight_num = f.flight_num and b.airline_name = f.airline_name) 
where b.was_cancelled = 0 and b.customer = i_customer_email and f.flight_date = (select flight_date from flight 
where flight_date > i_current_date and flight_num = i_flight_num and 
airline_name = i_airline_name))
Then
insert into Book (Customer, Flight_Num, Airline_Name, Num_Seats, Was_Cancelled)
values (i_customer_email, i_flight_num, i_airline_name, i_num_seats, 0);
end if;
end if;
end if;
end if;

end //
delimiter ;

-- ID: 3b
-- Name: cancel_flight_booking
drop procedure if exists cancel_flight_booking;
delimiter //
create procedure cancel_flight_booking ( 
    in i_customer_email varchar(50),
    in i_flight_num char(5),
    in i_airline_name varchar(50),
    in i_current_date date
)
sp_main: begin
if exists (select Customer from Book where Customer = i_customer_email and Flight_Num = i_flight_num)
and (select Flight_Date from Flight where Flight_Num = i_flight_num) > i_current_date
then update Book set Was_Cancelled = 1 where Customer = i_customer_email and i_flight_num = Flight_Num;
end if;
end //
delimiter ;


-- ID: 3c
-- Name: view_flight
create or replace view view_flight (
    flight_id,
    flight_date,
    airline,
    destination,
    seat_cost,
    num_empty_seats,
    total_spent
) as

select  F.Flight_Num as 'Flight ID',
        F.Flight_Date as 'Date',
        F.Airline_Name as 'Airline',
        F.To_Airport as 'Destination',
        F.Cost as 'Seat Cost',
        Capacity - IFNULL(rem_seats,0)  as 'Number of Empty Seats',
        IFNULL(Num_Seats,0)*Cost - (cost*IFNULL(act_seats,0)) as 'Total Money' from
        (select    Flight_Num,
                        Flight_Date,
                        Airline_Name,
                        To_Airport,
                        Cost,
                        Capacity from Flight) as F
            left outer join
				(select Flight_Num, airline_name, sum(Num_Seats* Was_cancelled*.8) as act_seats, sum(Num_seats) 
        as num_seats, sum(Num_Seats*(1-was_cancelled)) as rem_seats from Book group by Flight_Num, airline_name) as N
            on F.Flight_Num = N.Flight_Num and F.airline_name = n.airline_name;

-- ID: 4a
-- Name: add_property
drop procedure if exists add_property;
delimiter //
create procedure add_property (
    in i_property_name varchar(50),
    in i_owner_email varchar(50),
    in i_description varchar(500),
    in i_capacity int,
    in i_cost decimal(6, 2),
    in i_street varchar(50),
    in i_city varchar(50),
    in i_state char(2),
    in i_zip char(5),
    in i_nearest_airport_id char(3),
    in i_dist_to_airport int
) 
sp_main: begin
if not exists (select Street, City, State, Zip from Property where
Street = i_street and
City = i_city and
State = i_state and
Zip = i_zip) 
then
if not exists (select Property_Name, Owner_Email from Property where
I_property_name = Property_Name and i_owner_email = Owner_Email) 
then 
insert into Property values (i_property_name, i_owner_email, i_description, i_capacity, i_cost, i_street, i_city, i_state, i_zip);
if exists (select Airport_Id from Airport where Airport_Id = i_nearest_airport_id) and i_dist_to_airport is not null
then
insert into Is_Close_To values (i_property_name, i_owner_email, i_nearest_airport_id, i_dist_to_airport);
end if;
end if;
end if;

  
end //
delimiter ;


-- ID: 4b
-- Name: remove_property
drop procedure if exists remove_property;
delimiter //
create procedure remove_property (
    in i_property_name varchar(50),
    in i_owner_email varchar(50),
    in i_current_date date
)
sp_main: begin
if not exists (select Property_Name from Reserve where Property_Name = i_property_name
and Owner_Email = i_owner_email and Was_Cancelled = 0
and Start_Date < i_current_date 
and End_Date > i_current_date)
then
delete from Amenity where Property_Name = i_property_name and Property_owner = i_owner_email;
delete from Is_Close_To where Property_Name = i_property_name and Owner_Email = i_owner_email;
delete from Reserve where Property_Name = i_property_name and Owner_Email = i_owner_email;
delete from Property where Property_Name = i_property_name and Owner_Email = i_owner_email;
end if;

    
end //
delimiter ;


-- ID: 5a
-- Name: reserve_property
drop procedure if exists reserve_property;
delimiter //
create procedure reserve_property (
    in i_property_name varchar(50),
    in i_owner_email varchar(50),
    in i_customer_email varchar(50),
    in i_start_date date,
    in i_end_date date,
    in i_num_guests int,
    in i_current_date date
)
sp_main: begin
IF NOT EXISTS (SELECT owner_email, customer, property_name from reserve WHERE owner_email = i_owner_email AND customer = i_customer_email  AND property_name = i_property_name)
THEN
if not exists (select customer from reserve where i_end_date >= Start_Date and end_Date >= i_start_date and customer=i_customer_email)
THEN
if(i_start_date > i_current_date)
Then
if not exists (select Property_Name, num_guests, was_cancelled
from reserve where i_end_date >= Start_Date and end_Date >= i_start_date and Property_Name = i_property_name and was_cancelled = 0) 
and i_num_guests <= (select capacity from property where Property_Name = i_property_name)
then
INSERT INTO Reserve (Property_Name, Owner_Email, Customer, Start_Date, End_Date, Num_Guests, Was_Cancelled)
VALUES
(i_property_name, i_owner_email, i_customer_email, i_start_date, i_end_date, i_num_guests, 0);
else
if (Select i_num_guests <= (select 
(select capacity from property where Property_Name = i_property_name) - 
(select (sum(Num_Guests*(1-was_cancelled))) from (select Property_Name, num_guests, was_cancelled
from reserve where i_end_date >= Start_Date and end_Date >= i_start_date) as N
Left outer join
(Select property_name as prop, capacity from property) as P
On P.prop = N.property_name group by Property_name having Property_Name = i_property_name) as difference))
THEN INSERT INTO Reserve (Property_Name, Owner_Email, Customer, Start_Date, End_Date, Num_Guests, Was_Cancelled)
VALUES
(i_property_name, i_owner_email, i_customer_email, i_start_date, i_end_date, i_num_guests, 0);
end if;
end if;
end if;
end if;
end if;


end //
delimiter ;


-- ID: 5b
-- Name: cancel_property_reservation
drop procedure if exists cancel_property_reservation;
delimiter //
create procedure cancel_property_reservation (
    in i_property_name varchar(50),
    in i_owner_email varchar(50),
    in i_customer_email varchar(50),
    in i_current_date date
)
sp_main: begin
UPDATE RESERVE
SET WAS_CANCELLED = 1
WHERE owner_email = i_owner_email AND customer = i_customer_email  
AND property_name = i_property_name AND was_cancelled = 0 and start_date > i_current_date;


end //
delimiter ;


-- ID: 5c
-- Name: customer_review_property
drop procedure if exists customer_review_property;
delimiter //
create procedure customer_review_property (
    in i_property_name varchar(50),
    in i_owner_email varchar(50),
    in i_customer_email varchar(50),
    in i_content varchar(500),
    in i_score int,
    in i_current_date date
)
sp_main: begin
IF EXISTS(SELECT* from reserve where owner_email = i_owner_email
AND customer = i_customer_email  
AND property_name = i_property_name
AND i_current_date >= start_date AND was_cancelled = 0)
THEN
IF NOT EXISTS (SELECT owner_email, customer, property_name from review
 WHERE owner_email = i_owner_email
 AND customer = i_customer_email  
 AND property_name = i_property_name)
THEN INSERT INTO Review (Property_Name, Owner_Email, Customer, Content, Score)
VALUES
(i_property_name, i_owner_email, i_customer_email, i_content, i_score);
end if;
end if;
    
end //
delimiter ;


-- ID: 5d
-- Name: view_properties
create or replace view view_properties (
    property_name, 
    average_rating_score, 
    description, 
    address, 
    capacity, 
    cost_per_night
) as

Select prop.property_name as property_name, average_rating_score, Descr as 'Description', concat(street, ', ' ,city, ', ' , state, ', ', zip) as concatonated_address, capacity, cost
from (Select * from property) as prop left outer join 
(Select sum(score)/count(score) as average_rating_score, property_name from review group by property_name)
as rev on prop.property_name = rev.property_name;


-- ID: 5e
-- Name: view_individual_property_reservations
drop procedure if exists view_individual_property_reservations;
delimiter //
create procedure view_individual_property_reservations (
    in i_property_name varchar(50),
    in i_owner_email varchar(50)
)
sp_main: begin
    drop table if exists view_individual_property_reservations;
    create table view_individual_property_reservations (
        property_name varchar(50),
        start_date date,
        end_date date,
        customer_email varchar(50),
        customer_phone_num char(12),
        total_booking_cost decimal(6,2),
        rating_score int,
        review varchar(500)
    ) as
select R.Property_name, start_date, end_date, customer as Customer_email, Phone_number as Customer_phone_num, 
(((end_date-start_date)*cost)-(R.was_cancelled*.80*((end_date-start_date)*cost))) as Total_booking_cost, Score as Rating_score, content as Review  
from 
(select Z.property_name, Z.customer, Z.start_date, Z.end_date, Z.was_cancelled, Z.phone_number, Rev.content,
Rev.score  from ((select * from (select * from reserve where property_name = i_property_name and owner_email = i_owner_email) a left outer join 
(Select cust1.email, client1.phone_number from (select * from customer) as 
cust1 left outer join (select * from clients) as client1 on cust1.email = client1.email) as b on a.customer = b.email) as Z 
left outer join (select * from review) as Rev on Rev.customer = Z.email)) as R left outer join
(select property_name, cost from property) as P on R.Property_name = P.property_name;




end //
delimiter ;


-- ID: 6a
-- Name: customer_rates_owner
drop procedure if exists customer_rates_owner;
delimiter //
create procedure customer_rates_owner (
    in i_customer_email varchar(50),
    in i_owner_email varchar(50),
    in i_score int,
    in i_current_date date
)
sp_main: begin
if exists (select * from Reserve where Customer = i_customer_email and owner_email = i_owner_email)
then
if not exists (select * from Customers_Rate_Owners where Owner_Email = i_owner_email and Customer = i_customer_email)
and (select End_Date from Reserve where Owner_Email = i_owner_email and Customer = i_customer_email) < i_current_date
and (select Was_Cancelled from Reserve where Owner_Email = i_owner_email and Customer = i_customer_email) = 0
then insert into Customers_Rate_Owners values (i_customer_email, i_owner_email, i_score);
end if;
end if;

end //
delimiter ;


-- ID: 6b
-- Name: owner_rates_customer
drop procedure if exists owner_rates_customer;
delimiter //
create procedure owner_rates_customer (
    in i_owner_email varchar(50),
    in i_customer_email varchar(50),
    in i_score int,
    in i_current_date date
)
sp_main: begin
if exists (select * from Reserve where Customer = i_customer_email and owner_email = i_owner_email)
then
if not exists (select * from Owners_rate_customers where Owner_Email = i_owner_email and Customer = i_customer_email)
and (select End_Date from Reserve where Owner_Email = i_owner_email and Customer = i_customer_email) < i_current_date
and (select Was_Cancelled from Reserve where Owner_Email = i_owner_email and Customer = i_customer_email) = 0
then insert into Owners_rate_customers values (i_owner_email, i_customer_email, i_score);
end if;
end if;


end //
delimiter ;


-- ID: 7a
-- Name: view_airports
create or replace view view_airports (
    airport_id, 
    airport_name, 
    time_zone, 
    total_arriving_flights, 
    total_departing_flights, 
    avg_departing_flight_cost
) as
-- TODO: replace this select query with your solution    
select airport_id, 
airport_name, time_zone, IFNULL(total_arriving_flights,0) as total_arriving_flights, IFNULL(total_departing_flights,0) as total_departing_flights, 
avg_departing_flight_cost from ((((select 
airport_id, 
airport_name, time_zone
from airport) air
left outer join 
(select from_airport, count(from_airport) as total_departing_flights from flight group by from_airport) as r
on r.from_airport = air.airport_id) 
left outer join 
(select to_airport, count(to_airport) as total_arriving_flights from flight group by to_airport) as z
on z.to_airport = air.airport_id) left outer join 
(select from_airport, avg(cost) as avg_departing_flight_cost from flight group by from_airport) as g
on g.from_airport = air.airport_id);


-- ID: 7b
-- Name: view_airlines
create or replace view view_airlines (
    airline_name, 
    rating, 
    total_flights, 
    min_flight_cost
) as
-- TODO: replace this select query with your solution
select airl.airline_name as airline_name, rating, total_flights, min_flight_cost from (((select
airline_name,
rating
from airline) airl
left outer join
(select airline_name, count(airline_name) as total_flights from flight group by airline_name) as r
on r.airline_name = airl.airline_name)
left outer join
(select airline_name, min(cost) as min_flight_cost from flight group by airline_name) as g
on g.airline_name = airl.airline_name);


-- ID: 8a
-- Name: view_customers
create or replace view view_customers (
    customer_name, 
    avg_rating, 
    location, 
    is_owner, 
    total_seats_purchased
) as
-- TODO: replace this select query with your solution
-- view customers
select concat(first_name, ' ', last_name) as 'Customer Name' , average_rating, Location, isowner, total_seats as total_seats_purchased from
(select cust2.email, average_rating, total_seats, isowner, Location from(
select cust1.email, average_rating, total_seats, Location from (
select email, CASE WHEN total_seats IS NULL THEN 0 ELSE total_seats END total_seats, Location from 
((select * from customer) as cust
left join 
(Select sum(num_seats) as total_seats, Customer 
from Book group by Customer) as seat on cust.email = seat.Customer)) as cust1 left outer join
(Select sum(score)/count(score) as average_rating, Customer as email from Owners_Rate_Customers group by Customer) as scre on cust1.email = scre.email) as cust2
left join (SELECT customer.email,
       IF(owners.email IS NULL, 0, 1) as isowner
FROM customer
LEFT JOIN owners ON (customer.email = owners.email)) as cust3 on cust2.email = cust3.email) as cust4 join (select * from accounts) as cust5 on cust4.email = cust5.email;


-- ID: 8b
-- Name: view_owners
create or replace view view_owners (
    owner_name, 
    avg_rating, 
    num_properties_owned, 
    avg_property_rating
) as
-- TODO: replace this select query with your solution
select DISTINCT (concat(First_Name,' ', Last_Name)) as Owner_name,  avg_rating, IFNULL(properties_owned,0), avg_property_rating from (select * from (select * from (select * from  ((select * from owners) own left outer join (select Prop.property_name, Rev.avg_property_rating, Prop.owner_email
from ((select * from property) as prop left outer join 
(select sum(Score)/count(Score) as avg_property_rating, owner_email as owne  
from Review group by owner_email) rev 
on rev.owne = prop.owner_email)) as tot on own.email = tot.owner_email)) as al left outer join 
(select owner_email as owner1, (sum(Score)/count(Score)) as avg_rating from Customers_Rate_Owners group by Owner_email) as avg1 
on al.email = avg1.owner1) w left outer join (select email as em, first_name, last_name from accounts) as x on w.email = x.em) as total2
left outer join (select owner_email as irr, count(owner_email) as properties_owned from property group by owner_email) as count1 on
total2.owner_email = count1.irr;


-- ID: 9a
-- Name: process_date
drop procedure if exists process_date;
delimiter //
create procedure process_date ( 
    in i_current_date date
)
sp_main: begin

update Customer
inner join (select DISTINCT b.customer, b.flight_num, b.was_cancelled, state, b.airline_name, f.flight_date from ((select * from Book) as B
join (select Book.Customer, t.State, t.Flight_Num, t.flight_date from
(select Airport.State, Flight.Flight_Num, Flight.Flight_date
from Flight join Airport on Airport.Airport_ID = Flight.To_Airport
where Flight.To_Airport = Airport.Airport_ID) as t
join Book on Book.Flight_Num = t.Flight_Num where was_cancelled = 0) as f on f.customer = B.customer) WHERE was_cancelled = 0
and i_current_date = Flight_date)as temp on Customer.Email = temp.Customer
set Customer.Location = temp.State
where temp.Customer = Customer.Email and temp.was_cancelled = 0;
end //
delimiter ;
