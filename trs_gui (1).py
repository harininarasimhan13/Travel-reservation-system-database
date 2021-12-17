#!/usr/bin/env python3

#importing modules
from __future__ import print_function
import tkinter as tk
from tkinter import Entry, ttk
from tkinter import *
from datetime import date, datetime, timedelta 
import mysql.connector
from mysql.connector import errorcode
from mysql.connector import (connection)
from tkinter import messagebox

#connect to mysql server
cnx = mysql.connector.connect(
    host="127.0.0.1",
    user="root",
    password="strawberry1331$",
    database="travel_reservation_service",
    port=3306
)
cursor = cnx.cursor(buffered=True)

#define fonts
Header_Font=("Arial", 15)
main_font=("Arial", 20)
Header_Font2=("Arial", 30)
Subfont = ("Arial", 20)


#Define Driver Class
class ReservationService(tk.Tk):
	#init ReservationService with variable positional and key arguments
	def __init__(self, *args, **kwargs):
		#init class Tk with variable positional and key arguments
		tk.Tk.__init__(self, *args, **kwargs)
		#create container for frames
		container = tk.Frame(self)
		container.pack(side="top", fill="both", expand = True)
		container.grid_rowconfigure(0, weight = 1)
		container.grid_columnconfigure(0, weight = 1)
		#initialize empty dictionary for frames
		self.title("Go2 ~ Travel Reservation Service")
		self.frames = {}
		self.geometry("2000x800")
		#store user login
		self.user_login={"email": tk.StringVar()}
		#iterate through each page in tuple and add to self.frames dictionary
		#when a new page is made, add class name to this tuple
		for P in (LoginPage, CustomerHome, LoginErrorPage, BookFlight, 
			ReserveProperty, RegisterCustomer, RegistrationType, RegisterOwner, AdminHome, 
			LoginOption, OwnerHome, CancelFlight, CancelPropertyReservation, ReviewProperty, 
            RateOwner, AddFlight, RemoveFlight, ViewAirports, ViewAirlines, ViewCustomers, 
            ViewOwners, AddProperty, RemoveProperty, RateCustomer, ManageAccount, RemoveAccount):
			frame = P(container, self)
			self.frames[P] = frame
			frame.grid(row = 0, column = 0, sticky = "nswe")
		self.show_frame(LoginPage)
		#define function to show current frame
	def show_frame(self, cont):
		frame = self.frames[cont]
		frame.tkraise()


#Login Associated Pages

#Login Page
class LoginPage(tk.Frame):
	def __init__(self, parent, controller):
		tk.Frame.__init__(self, parent)
		self.controller = controller
		#set color
		LoginPage.configure(self, bg = '#00A7E1')
		#Login Page Header
		header = tk.Label(self, text="Welcome to Go2 Travel Services", font = Header_Font2, bg = '#00A7E1', fg="white")
		header.grid(row = 0, column = 0, padx = 10, pady = 10)
		sub_header = tk.Label(self, text="Go2 Anywhere...", font = Subfont, bg = '#00A7E1', fg="white")
		sub_header.grid(row = 1, column = 0, padx = 10, pady = 10)
		#Email Prompt
		email_prompt = tk.Label(self, text = "Email", font = main_font, bg = '#00A7E1', fg="white")
		email_prompt.grid(row = 2, column = 1, padx = 10, pady = 10)
		#Email Input box
		input_email = Entry(self, textvariable=self.controller.user_login["email"], highlightbackground = "#FFA630")
		input_email.grid(row = 2, column = 2)
		#Password Prompt
		password_prompt = tk.Label(self, text = "Password", font = main_font, bg = '#00A7E1', fg="white")
		password_prompt.grid(row = 3, column = 1, padx = 10, pady = 10)
		#Password Input Prompt
		input_password = Entry(self, highlightbackground = "#FFA630")
		input_password.grid(row = 3, column = 2)
		#SQL Query to check if user email is in accounts with the provided password
		def check_login(i_email, i_password):
			check_valid = (f"select Email from Accounts where '{i_email}' = Email and '{i_password}' = Pass")
			check_owner = (f"select Email from Owners where '{i_email}' = Email")
			check_customer = (f"select Email from Customer where '{i_email}' = Email")
			check_admin = (f"select Email from Admins where '{i_email}' = Email")
			#declar variable to hold login type
			valid = 0
			owner = 0
			customer = 0
			admin = 0
			cursor.execute(check_valid)
			for user in cursor:
				valid += 1
			cursor.execute(check_owner)
			for user in cursor:
				owner += 1
			cursor.execute(check_customer)
			for user in cursor:
				customer += 1
			cursor.execute(check_admin)
			for user in cursor:
				admin += 1
			#check login type
			#check if customer
			if valid !=0 and customer != 0 and owner == 0:
				controller.show_frame(CustomerHome)
			#check if owner
			elif valid !=0 and owner != 0 and customer == 0:
				controller.show_frame(OwnerHome)
			#check if admin
			elif valid !=0 and admin != 0:
				controller.show_frame(AdminHome)
			#check if owner and customer
			elif valid !=0 and customer !=0 and owner != 0:
				controller.show_frame(LoginOption)
			if valid == 0:
				controller.show_frame(LoginErrorPage)	
		#Login Button
		login = tk.Button(self, text = "Log in", highlightbackground = "#00A7E1", height = 1, width = 18,
			command = lambda : check_login(self.controller.user_login["email"].get(), input_password.get()))
		login.grid(row = 4, column = 2, padx = 10, pady = 10)
		#Register new customer
		register_label = tk.Label(self, text = "Not a Customer?",
			font = main_font, bg = '#00A7E1', fg="white")
		register_label.grid(row = 6, column = 0, padx = 10, pady = 10)
		register_button = tk.Button(self, text = "Register Here", highlightbackground = "#00A7E1",
			command = lambda : controller.show_frame(RegistrationType))
		register_button.grid(row = 7, column = 0)

#Login Error Page # might get rid of later
class LoginErrorPage(tk.Frame):
	def __init__(self, parent, controller):
		tk.Frame.__init__(self, parent)
		#Error Message
		header = tk.Label(self, text = "The login infortmation you have provided is invalid")
		header.grid(row = 0, column = 4, padx = 10, pady = 10)
		try_again = tk.Button(self, text = "Try Again", command = lambda : controller.show_frame(LoginPage))
		try_again.grid(row = 2, column = 4, padx = 10, pady = 10)

#Login Option Page
class LoginOption(tk.Frame):
	def __init__(self, parent, controller):
		tk.Frame.__init__(self, parent)
		self.controller = controller
		#set page color
		LoginOption.configure(self, bg = '#00A7E1')
		#As if user wants to go to customer home or login home
		header = tk.Label(self, text = "Would you like to go to Customer Home or Owner Home?", 
			font = Header_Font2, bg = '#00A7E1', fg="white")
		header.grid(column = 1, row = 0, padx = 10, pady = 10)
		#define customer login button
		login_as_customer = tk.Button(self, text = "Go to Customer Home", height = 15, width = 30,
			highlightbackground = "#FFA630", font = main_font, command = lambda : controller.show_frame(CustomerHome))
		login_as_customer.grid(column = 1, row = 1, padx = 10, pady = 10)
		#define owner login button
		login_as_owner = tk.Button(self, text = "Go to Owner Home", height = 15, width = 30,
			highlightbackground = "#FFA630", font = main_font, command = lambda : controller.show_frame(OwnerHome))
		login_as_owner.grid(column = 3, row = 1, padx = 10, pady = 10)


#Home Pages

#Owner Home Page
class OwnerHome(tk.Frame):
	def __init__(self, parent, controller):
		tk.Frame.__init__(self, parent)
		#set page color
		LoginOption.configure(self, bg = '#00A7E1')
		#make header
		header = tk.Label(self, text = "Welcome Owner!", font = Header_Font2, bg = '#00A7E1', fg="white")
		header.grid(column = 0, row = 0, padx = 10, pady = 10)
		#Add property button
		add_property_button = tk.Button(self, text = "Add Property",
			height = 4, width = 20, highlightbackground = "#FFA630", 
                command = lambda : controller.show_frame(AddProperty))
		add_property_button.grid(column = 1, row = 3, padx = 10, pady = 10)
		#Remove property button
		remove_property_button = tk.Button(self, text = "View and Remove Properties", 
			height = 4, width = 20, highlightbackground = "#FFA630", 
                command = lambda : controller.show_frame(RemoveProperty))
		remove_property_button.grid(column = 1, row = 4, padx = 10, pady = 10)
		#Rate customers button
		rate_customers_button = tk.Button(self, text = "Rate Customer", 
			height = 4, width = 20, highlightbackground = "#FFA630", 
				command = lambda : controller.show_frame(RateCustomer))
		rate_customers_button.grid(column = 1, row = 5, padx = 10, pady = 10)
		#Manage account
		manage_account_button = tk.Button(self, text = "Manage Account", 
			height = 4, width = 20, highlightbackground = "#FFA630",
			command = lambda : controller.show_frame(ManageAccount))
		manage_account_button.grid(column = 1, row = 6, padx = 10, pady = 10)
		#Logout button
		logout = tk.Button(self, text = "Log out", width = 10, highlightbackground = "#00A7E1",
			command = lambda : controller.show_frame(LoginPage))
		logout.grid(row = 8, column = 0, padx = 10, pady = 10)

#Admin Home Page
class AdminHome(tk.Frame):
	def __init__(self, parent, controller):
		tk.Frame.__init__(self, parent)
		#set page color
		AdminHome.configure(self, bg = '#00A7E1')
		#set header
		header = tk.Label(self, text = "Welcome Admin!", font = Header_Font2, 
			bg = '#00A7E1', fg="white")
		header.grid(column = 0, row = 0, padx = 10, pady = 10)
		#schedule flight
		shcedule_flight_button = tk.Button(self, text = "Add Flight", 
			height = 4, width = 20, highlightbackground = "#FFA630", 
            command = lambda : controller.show_frame(AddFlight))
		shcedule_flight_button.grid(column = 1, row = 1, padx = 10, pady = 10)
		#remove flight
		remove_flight_button = tk.Button(self, text = "View and Remove Flight", 
			height = 4, width = 20, highlightbackground = "#FFA630", 
            command = lambda : controller.show_frame(RemoveFlight))
		remove_flight_button.grid(column = 2, row = 1, padx = 10, pady = 10)
		#view airports
		view_airports_button = tk.Button(self, text = "View Airports", 
			height = 4, width = 20, highlightbackground = "#FFA630", 
                command = lambda : controller.show_frame(ViewAirports))
		view_airports_button.grid(column = 3, row = 1, padx = 10, pady = 10)
		#view airlines
		view_airlines_button = tk.Button(self, text = "View Airlines", 
			height = 4, width = 20, highlightbackground = "#FFA630", 
                command = lambda : controller.show_frame(ViewAirlines))
		view_airlines_button.grid(column = 4, row = 1, padx = 10, pady = 10)

		#view owners
		view_owners_button = tk.Button(self, text = "View Owners",
			height = 4, width = 20, highlightbackground = "#FFA630", 
                command = lambda : controller.show_frame(ViewOwners))
		view_owners_button.grid(column = 1, row = 3, padx = 10, pady = 10)
		#view customers
		view_customers_button = tk.Button(self, text = "View Customers",
			height = 4, width = 20, highlightbackground = "#FFA630", 
                command = lambda : controller.show_frame(ViewCustomers))
		view_customers_button.grid(column = 2, row = 3, padx = 10, pady = 10)
		#logout button
		logout = tk.Button(self, text = "Log out", width = 10, highlightbackground = "#00A7E1",
			command = lambda : controller.show_frame(LoginPage))
		logout.grid(row = 8, column = 0, padx = 10, pady = 10)

#Customer Home Page
class CustomerHome(tk.Frame):
	def __init__(self, parent, controller):
		tk.Frame.__init__(self, parent)
		#set page color
		CustomerHome.configure(self, bg = '#00A7E1')
		#Page header
		header = tk.Label(self, text = "Customer Home", font = Header_Font2, bg = '#00A7E1', fg="white")
		header.grid(row = 0, column = 0, padx = 10, pady = 10)
		#Book Flight Button
		book_flight_button = tk.Button(self, text = "Book a Flight", height = 4, width = 25,
			highlightbackground = "#FFA630", command = lambda : controller.show_frame(BookFlight))
		book_flight_button.grid(row = 1, column = 1, padx = 10, pady = 10)
		#Cancel Flight Button
		cancel_flight_button = tk.Button(self, text = "View and Cancel Flights", height = 4, width = 25, 
			highlightbackground = "#FFA630", command = lambda : controller.show_frame(CancelFlight))
		cancel_flight_button.grid(row = 1, column = 2, padx = 10, pady = 10)
		#Book Property Button
		reserve_property_button = tk.Button(self, text = "Reserve Property", height = 4, width = 25,
			highlightbackground = "#FFA630", command = lambda : controller.show_frame(ReserveProperty))
		reserve_property_button.grid(row = 2, column = 1, padx = 10, pady = 10)
		#Cancel Property Booking Button
		cancel_property_button = tk.Button(self, text = "View and Cancel Property Reservations", height = 4, width = 25,
			highlightbackground = "#FFA630", command = lambda : controller.show_frame(CancelPropertyReservation))
		cancel_property_button.grid(row = 2, column = 2, padx = 10, pady = 10)
		#Review Property Button
		review_property_button = tk.Button(self, text = "Review Property", height = 4, width = 25, 
			highlightbackground = "#FFA630", command = lambda : controller.show_frame(ReviewProperty))
		review_property_button.grid(row = 3, column = 1, padx = 10, pady = 10)
		#Rate Owner Button
		rate_owner_button = tk.Button(self, text = "Rate Owner", height = 4, width = 25, 
			highlightbackground = "#FFA630", command = lambda : controller.show_frame(RateOwner))
		rate_owner_button.grid(row = 3, column = 2, padx = 10, pady = 10)
		#Log out Button
		logout = tk.Button(self, text = "Log out", width = 10, highlightbackground = "#00A7E1",
			command = lambda : controller.show_frame(LoginPage))
		logout.grid(row = 8, column = 0, padx = 10, pady = 10)



#buttons on customer home page


#View and Book Flights
class BookFlight(tk.Frame):
	def __init__(self, parent, controller):
		tk.Frame.__init__(self, parent)
		self.controller = controller
		#set page color
		BookFlight.configure(self, bg = '#00A7E1')
		#add header and home button
		header = tk.Label(self, text = "Flight Information", font = Header_Font2, bg = '#00A7E1', fg="white")
		header.grid(row = 0, column = 1, padx = 10, pady = 10)
		home_button = tk.Button(self, text = "Return to Home", highlightbackground = "#00A7E1",
			command = lambda : controller.show_frame(CustomerHome))
		home_button.grid(row = 0, column = 0, padx = 10, pady = 10)

		#initialize empty list to store flight info tuples
		flights = []
		view_flights = ("select * from Flight;")
		cursor.execute(view_flights)
		for (Flight_Num, Airline_Name, From_Airport, To_Airport, Departure_Time, Arrival_Time, Flight_Date, Cost, Capacity) in cursor:
			Flight_Num = Flight_Num
			Airline_Name = Airline_Name
			From_Airport = From_Airport
			To_Airport = To_Airport
			Departure_Time = Departure_Time
			Arrival_Time = Arrival_Time
			Flight_Date = Flight_Date
			Cost = Cost
			Capacity = Capacity
			flight_info = (str(Flight_Num), str(Airline_Name), str(From_Airport), str(To_Airport), str(Departure_Time), str(Arrival_Time), str(Flight_Date), str(Cost), str(Capacity))
			flights.append(flight_info)

		def refresh():
			#clear current entries
			tree.delete(*tree.get_children())
			#SQL query to view booked flights
			flights = []
			view_flights = ("select * from Flight;")
			cursor.execute(view_flights)
			for (Flight_Num, Airline_Name, From_Airport, To_Airport, Departure_Time, Arrival_Time, Flight_Date, Cost, Capacity) in cursor:
				Flight_Num = Flight_Num
				Airline_Name = Airline_Name
				From_Airport = From_Airport
				To_Airport = To_Airport
				Departure_Time = Departure_Time
				Arrival_Time = Arrival_Time
				Flight_Date = Flight_Date
				Cost = Cost
				Capacity = Capacity
				flight_info = (str(Flight_Num), str(Airline_Name), str(From_Airport), str(To_Airport), str(Departure_Time), str(Arrival_Time), str(Flight_Date), str(Cost), str(Capacity))
				flights.append(flight_info)
			for flight in flights:
				tree.insert('', tk.END, values = flight)
			
		refresh_button = tk.Button(self, text = "Refresh", highlightbackground = "#00A7E1", 
			command = lambda : refresh())
		refresh_button.grid(row = 0, column = 3, padx = 10, pady = 10)

		columns = ('Flight_Num', 'Airline_Name', 'From_Airport', 'To_Airport', 'Departure_Time', 'Arrival_Time', 'Flight_Date', 'Cost', 'Capacity')
		tree = ttk.Treeview(self, columns = columns, show = 'headings', height = 10)
		tree.grid(row = 1, column = 1, columnspan=100)

		tree.column('Flight_Num', width = 125)
		tree.heading('Flight_Num', text = 'Flight Number')
		tree.column('Airline_Name', width = 125)
		tree.heading('Airline_Name', text = 'Airline')
		tree.column('From_Airport',  width = 125)
		tree.heading('From_Airport', text = 'Departing From')
		tree.column('To_Airport', width = 125)
		tree.heading('To_Airport', text = 'Destination')
		tree.column('Departure_Time', width = 125)
		tree.heading('Departure_Time', text = 'Departure Time')
		tree.column('Arrival_Time', width = 125)
		tree.heading('Arrival_Time', text = 'Arrival Time')
		tree.column('Flight_Date', width = 125)
		tree.heading('Flight_Date', text = 'Departure Date')
		tree.column('Cost', width = 125)
		tree.heading('Cost', text = 'Cost Per Seat')
		tree.column('Capacity', width = 125)
		tree.heading('Capacity', text = 'Capacity')
		for flight in flights:
			tree.insert('', tk.END, values = flight)

		#add scrollbar
		scrollbar = ttk.Scrollbar(self, orient = tk.VERTICAL, command = tree.yview)
		tree.configure(yscroll=scrollbar.set)
		scrollbar.grid(row = 2, column = 101, rowspan = 2, sticky = 'ns')

		#set up confirmation windows
		#flight selected
		flight_selected_lable = tk.Label(self, text = "Flight", bg = '#00A7E1', fg="white", font = main_font)
		flight_selected_lable.grid(row = 4, column = 1, padx = 10, pady = 10, columnspan = 2)
		flight_selected = Entry(self, highlightbackground = "#FFA630")
		flight_selected.grid(row = 4, column = 2, padx = 10, pady = 10)
		#airline selected
		airline_selected_label = tk.Label(self, text = "Airline", bg = '#00A7E1', fg="white", font = main_font)
		airline_selected_label.grid(row = 5, column = 1, padx = 10, pady = 10, columnspan = 2)
		airline_selected = Entry(self, highlightbackground = "#FFA630")
		airline_selected.grid(row = 5, column = 2, padx = 10, pady = 10)
		#number of seats
		num_seat_label = tk.Label(self, text = "Seats", bg = '#00A7E1', fg="white", font = main_font)
		num_seat_label.grid(row = 6, column = 1, padx = 10, pady = 10, columnspan = 2)
		num_seats = Entry(self, highlightbackground = "#FFA630")
		num_seats.grid(row = 6, column = 2, padx = 10, pady = 10)
		num_seats.insert(END, 'Number of Seats')
		#current date
		current_date_label = tk.Label(self, text = "Today", bg = '#00A7E1', fg="white", font = main_font)
		current_date_label.grid(row = 7, column = 1, padx = 10, pady = 10, columnspan = 2)
		current_date = Entry(self, highlightbackground = "#FFA630")
		current_date.grid(row = 7, column = 2, padx = 10, pady = 10)
		current_date.insert(END, 'yyyy-mm-dd')

		#Get selected info
		def item_selected(event):
			for selected_item in tree.selection():
				#get selected row as list
				item = tree.item(selected_item)
				#delete whatever is currently in entry window and fill with selected data
				flight_selected.delete(0, 'end')
				flight_selected.insert(END, str(item['values'][0]))
				airline_selected.delete(0, 'end')
				airline_selected.insert(END, str(item['values'][1]))

		tree.grid(row = 2, column = 1, sticky='nsew')
		#set action for double clicking 		
		tree.bind('<Double-1>', item_selected)

		#define functon to book flight
		def book_flight(i_flight_num, i_airline_name, i_num_seats, i_current_date):
			current_customer = self.controller.user_login["email"].get()
			book = (f"call book_flight('{current_customer}', '{i_flight_num}', '{i_airline_name}', '{i_num_seats}', '{i_current_date}')")
			check_booking = (f"select Customer from Book where Customer = '{current_customer}' and Flight_Num = '{i_flight_num}' and Was_Cancelled = 0;")
			try:
				cursor.execute(book)
				cnx.commit()
				cursor.execute(check_booking)
				#check to see if booking was successful
				booking_valid = 0
				for booking in cursor:
					booking_valid += 1
				if booking_valid != 0:
					messagebox.showinfo("showinfo", "Flight has been booked. Please confirm fight details in 'View and Cancel Flights'")
				else:
					messagebox.showwarning("showwarning", "Your reservation was unsuccessful. Please check your information.")
			except:
				messagebox.showwarning("showwarning", "Your reservation was unsuccessful. Please check your information.")
		#Confirm reservation button
		book_button = tk.Button(self, text = "Confirm Reservation", highlightbackground = "#00A7E1", 
			command = lambda : book_flight(flight_selected.get(), airline_selected.get(), num_seats.get(), current_date.get()))
		book_button.grid(row = 10, column = 2, padx = 10, pady = 10)

#View and Reserve Properties Page
class ReserveProperty(tk.Frame):
	def __init__(self, parent, controller):
		tk.Frame.__init__(self, parent)
		self.controller = controller
		#set page color
		ReserveProperty.configure(self, bg = '#00A7E1')
		#add header and home button
		header = tk.Label(self, text = "Properties Information", font = Header_Font2, bg = '#00A7E1', fg="white")
		header.grid(row = 0, column = 1, padx = 10, pady = 10)
		home_button = tk.Button(self, text = "Return to Home", highlightbackground = "#00A7E1",
			command = lambda : controller.show_frame(CustomerHome))
		home_button.grid(row = 0, column = 0, padx = 10, pady = 10)

		#initialize empty list to store properties info tuples
		properties = []
		#SQL view to view all available flight
		view_properties = ("select * from view_properties;")
		cursor.execute(view_properties)
		for (property_name, average_rating, description, address, capacity, cost_per_night) in cursor:
			property_name = property_name
			average_rating = average_rating
			description = description
			address = address
			capacity = capacity
			cost_per_night = cost_per_night
			properties_info = (str(property_name), str(average_rating), str(description), str(address), str(capacity), str(cost_per_night))
			properties.append(properties_info)
		
		def refresh():
			#clear current entries
			tree.delete(*tree.get_children())
			#SQL query to view booked flights
			properties = []
			#SQL view to view all available flight
			view_properties = ("select * from view_properties;")
			cursor.execute(view_properties)
			for (property_name, average_rating, description, address, capacity, cost_per_night) in cursor:
				property_name = property_name
				average_rating = average_rating
				description = description
				address = address
				capacity = capacity
				cost_per_night = cost_per_night
				properties_info = (str(property_name), str(average_rating), str(description), str(address), str(capacity), str(cost_per_night))
				properties.append(properties_info)
			for property in properties:
				tree.insert('', tk.END, values = property)
			
		refresh_button = tk.Button(self, text = "Refresh", highlightbackground = "#00A7E1", 
			command = lambda : refresh())
		refresh_button.grid(row = 1, column = 0, padx = 10, pady = 10)

		#create table to show properties
		columns = ('property_name', 'average_rating', 'description', 'address', 'capacity', 'cost_per_night')
		tree = ttk.Treeview(self, columns = columns, show = 'headings', height=10)
		tree.grid(row = 1, column = 2, columnspan=100)
		tree.column('property_name', width = 175)
		tree.heading('property_name', text = 'Property')
		tree.column('average_rating', width = 60)
		tree.heading('average_rating', text = 'Rating')
		tree.column('description', width = 525)
		tree.heading('description', text = 'Description')
		tree.column('address', width = 300)
		tree.heading('address', text = 'Address')
		tree.column('capacity', width = 50)
		tree.heading('capacity', text = 'Capacity')
		tree.column('cost_per_night', width = 100)
		tree.heading('cost_per_night', text = 'Cost Per Night')
		for property in properties:
			tree.insert('', tk.END, values = property)
		
		#set up confirmation windows
		#property selected
		property_selected_lable = tk.Label(self, text = "Property", bg = '#00A7E1', fg="white", font = main_font)
		property_selected_lable.grid(row = 4, column = 1, padx = 10, pady = 10, columnspan = 9)
		selected_property = Entry(self, highlightbackground = "#FFA630")
		selected_property.grid(row = 4, column = 2, padx = 10, pady = 10)
		#Start Date
		start_date_label = tk.Label(self, text="Start Date", bg = '#00A7E1', fg="white", font = main_font)
		start_date_label.grid(row = 5, column = 1, padx = 10, pady = 10, columnspan = 8)
		start_date = Entry(self, highlightbackground = "#FFA630")
		start_date.grid(row = 5, column = 2, padx = 10, pady = 10)
		start_date.insert(END, "yyyy-mm-dd")
		#End Date
		end_date_label = tk.Label(self, text="End Date", bg = '#00A7E1', fg="white", font = main_font)
		end_date_label.grid(row = 6, column = 1, padx = 10, pady = 10, columnspan = 8)
		end_date = Entry(self, highlightbackground = "#FFA630")
		end_date.grid(row = 6, column = 2, padx = 10, pady = 10)
		end_date.insert(END, "yyyy-mm-dd")
		#Number of guests
		num_guests_label = tk.Label(self, text = "Guests", bg = '#00A7E1', fg="white", font = main_font)
		num_guests_label.grid(row = 7, column = 1, padx = 10, pady = 10, columnspan = 8)
		num_guests = Entry(self, highlightbackground = "#FFA630")
		num_guests.grid(row = 7, column = 2, padx = 10, pady = 10)
		num_guests.insert(END, "Number of Guests")
		#Input current date
		today_date_label = tk.Label(self, text = "Today", bg = '#00A7E1', fg="white", font = main_font)
		today_date_label.grid(row = 8, column = 1, padx = 10, pady = 10, columnspan = 8)
		today_date = Entry(self, highlightbackground = "#FFA630")
		today_date.grid(row = 8, column = 2, padx = 10, pady = 10)
		today_date.insert(END, "Enter Today's Date")

		#get selected row and owner for property
		def item_selected(event):
			for selected_item in tree.selection():
				#get selected row as list
				item = tree.item(selected_item)
				#delete whatever is currently in entry window
				selected_property.delete(0, 'end')
				#display property selected in proper entry window
				selected_property.insert(END, str(item['values'][0]))
			get_owner = (f"select Owner_Email from Property where '{selected_property.get()}' = Property_Name")
			cursor.execute(get_owner)
			for owner in cursor:
				property_owner = str(owner[0])
				return property_owner	
	
		#set action for double clicking 		
		tree.bind('<Double-1>', item_selected)
		#place table on page
		tree.grid(row = 2, column = 1, sticky='nsew')

		#add scrollbar
		scrollbar = ttk.Scrollbar(self, orient = tk.VERTICAL, command = tree.yview)
		tree.configure(yscroll=scrollbar.set)
		scrollbar.grid(row = 2, column = 101, rowspan = 2, sticky = 'ns')

		#define function to reserve property
		def reserve_property(i_property_name, i_start_date, i_end_date, i_num_guests, i_current_date):
			current_customer = self.controller.user_login["email"].get()
			#get property owner
			get_owner = (f"select Owner_Email from Property where '{selected_property.get()}' = Property_Name")
			property_owner = ''
			cursor.execute(get_owner)
			for owner in cursor:
				property_owner += str(owner[0])
			#reserve property
			reserve = (f"call reserve_property('{i_property_name}', '{property_owner}', '{current_customer}', '{i_start_date}', '{i_end_date}', '{i_num_guests}', '{i_current_date}');")
			#check if reservation was successful
			reservation_check = (f"select Property_Name from Reserve where '{i_property_name}' = Property_Name and '{property_owner}' = Owner_Email and '{current_customer}' = Customer and '{i_start_date}' = Start_Date")
			try:
				cursor.execute(reserve)
				cnx.commit()
				cursor.execute(reservation_check)
				review_valid = 0
				for review in cursor:
					review_valid += 1
				if review_valid != 0:
					messagebox.showinfo("showinfo", "Your submission was successful")
				else:
					messagebox.showwarning("showwarning", "Your submission was unsuccessful. Please check your information.")
			except:
				messagebox.showwarning("showwarning", "Your submission was unsuccessful. Please check your information.")

		#Confirm reservation button
		reserve_button = tk.Button(self, text = "Confirm Reservation", highlightbackground = "#00A7E1", 
			command = lambda : reserve_property(selected_property.get(), start_date.get(), end_date.get(), num_guests.get(), today_date.get()))
		reserve_button.grid(row = 10, column = 2, padx = 10, pady = 10)

class CancelFlight(tk.Frame):
	def __init__(self, parent, controller):
		tk.Frame.__init__(self, parent)
		self.controller = controller
		#set page color
		CancelFlight.configure(self, bg = '#00A7E1')
		#add header and home button and Define return to home button
		header = tk.Label(self, text = "View and Cancel Flights", font = Header_Font2, bg = '#00A7E1', fg="white")
		header.grid(row = 0, column = 1, padx = 10, pady = 10)
		home_button = tk.Button(self, text = "Return to Home", highlightbackground = "#00A7E1",
			command = lambda : controller.show_frame(CustomerHome))
		home_button.grid(row = 0, column = 0, padx = 10, pady = 10)

		#create table to show booked Flights
		columns = ('Customer', 'Flight_Num', 'Airline_Name', 'Num_Seats', 'Was_Cancelled')
		tree = ttk.Treeview(self, columns = columns, show = 'headings', height=10)
		tree.grid(row = 1, column = 2, columnspan=100)
		tree.column('Customer', width = 175)
		tree.heading('Customer', text = 'Customer')
		tree.column('Flight_Num', width = 100)
		tree.heading('Flight_Num', text = 'Flight Number')
		tree.column('Airline_Name', width = 150)
		tree.heading('Airline_Name', text = 'Airline')
		tree.column('Num_Seats', width = 75)
		tree.heading('Num_Seats', text = 'Seats')
		tree.column('Was_Cancelled', width = 100)
		tree.heading('Was_Cancelled', text = 'Cancelled')

		#function to view booked flights
		def view_booked_flights():
			#clear current entries
			tree.delete(*tree.get_children())
			current_customer = self.controller.user_login["email"].get()
			#SQL query to view booked flights
			get_booked_flights = (f"select Customer, Flight_Num, Airline_Name, Num_seats, Was_Cancelled from Book where '{current_customer}' = Customer")
			cursor.execute(get_booked_flights)
			flights = []
			for (Customer, Flight_Num, Airline_Name, Num_Seats, Was_Cancelled) in cursor:
				Customer = Customer
				Flight_Num = Flight_Num
				Airline_Name = Airline_Name
				Num_Seats = Num_Seats
				Was_Cancelled = Was_Cancelled
				booked_flights = (str(Customer), str(Flight_Num), str(Airline_Name), str(Num_Seats), str(Was_Cancelled))
				flights.append(booked_flights)
			for flight in flights:
				tree.insert('', tk.END, values = flight)
		#place table on page
		tree.grid(row = 2, column = 1, sticky='nsew')
		#add scrollbar
		scrollbar = ttk.Scrollbar(self, orient = tk.VERTICAL, command = tree.yview)
		tree.configure(yscroll=scrollbar.set)
		scrollbar.grid(row = 2, column = 101, rowspan = 2, sticky = 'ns')
		#View booked flights button
		booked_flights_button = tk.Button(self, text = "View Your Flights", highlightbackground = "#00A7E1", 
			command = lambda : view_booked_flights())
		booked_flights_button.grid(row = 1, column = 3, padx = 10, pady = 10)

		#define cancel flight function
		def cancel_flight(i_current_date):
			for selected_item in tree.selection():
				item = tree.item(selected_item)
				customer_email = str(item['values'][0])
				flight_number = str(item['values'][1])
				airline_name = str(item['values'][2])
				was_cancelled = int(item['values'][3])
				#sql procedure to cancel flight
			cancel_booked_flight = (f"call cancel_flight_booking('{customer_email}', '{flight_number}', '{airline_name}', '{i_current_date}')")
			#check to see if flight was cancelled
			check_cancellation = (f"select Customer, Flight_Num from Book where Customer = '{customer_email}' and Flight_Num = '{flight_number}' and Was_Cancelled = 1")
			try:
				cursor.execute(cancel_booked_flight)
				cnx.commit()
				cursor.execute(check_cancellation)
				review_valid = 0
				for review in cursor:
					review_valid += 1
				if review_valid != 0:
					messagebox.showinfo("showinfo", "Your submission was successful")
				else:
					messagebox.showwarning("showwarning", "Your submission was unsuccessful. Please check your information.")
			except:
				messagebox.showwarning("showwarning", "Your submission was unsuccessful. Please check your information.")

		#get current date
		current_date_label = tk.Label(self, text = "Today", bg = '#00A7E1', fg="white", font = main_font)
		current_date_label.grid(column = 2, row = 5, padx = 10, pady = 10)
		current_date = Entry(self, highlightbackground = "#FFA630")
		current_date.grid(column = 3, row = 5, padx = 10, pady = 10)
		current_date.insert(END, 'yyyy-mm-dd')
		#cancel flight button
		cancel_flight_button = tk.Button(self, text = "Cancel Selected Flight", highlightbackground = "#00A7E1", 
			command = lambda : cancel_flight(current_date.get()))
		cancel_flight_button.grid(column = 3, row = 6, padx = 10, pady = 10)		

class CancelPropertyReservation(tk.Frame):
	def __init__(self, parent, controller):
		tk.Frame.__init__(self, parent)
		self.controller = controller
		#set page color
		CancelPropertyReservation.configure(self, bg = '#00A7E1')
		#Define return to home button
		#add header and home button
		header = tk.Label(self, text = "View and Cancel Reservation", font = Header_Font2, bg = '#00A7E1', fg="white")
		header.grid(row = 0, column = 1, padx = 10, pady = 10)
		home_button = tk.Button(self, text = "Return to Home", highlightbackground = "#00A7E1",
			command = lambda : controller.show_frame(CustomerHome))
		home_button.grid(row = 0, column = 0, padx = 10, pady = 10)

		#create table to show reserved property
		columns = ('Customer', 'Property_Name', 'Owner_Email', 'Start_Date', 'End_Date', 'Num_Guests', 'Was_Cancelled')
		tree = ttk.Treeview(self, columns = columns, show = 'headings', height=10)
		tree.grid(row = 1, column = 2, columnspan=100)
		tree.column('Customer', width = 150)
		tree.heading('Customer', text = 'Customer')
		tree.column('Property_Name', width = 200)
		tree.heading('Property_Name', text = 'Property')
		tree.column('Owner_Email', width = 150)
		tree.heading('Owner_Email', text = 'Owner Email')
		tree.column('Start_Date', width = 100)
		tree.heading('Start_Date', text = 'Start Date')
		tree.column('End_Date', width = 100)
		tree.heading('End_Date', text = 'End Date')
		tree.column('Num_Guests', width = 75)
		tree.heading('Num_Guests', text = 'Guests')
		tree.column('Was_Cancelled', width = 100)
		tree.heading('Was_Cancelled', text = 'Cancelled')

		#function to view and select reserved properties
		def view_reserved_property():
			current_customer = self.controller.user_login["email"].get()
			#clear current entries
			tree.delete(*tree.get_children())
			#SQL query to view booked flights
			get_reserved_property = (f"select Customer, Property_Name, Owner_Email, Start_Date, End_Date, Num_Guests, Was_Cancelled from Reserve where '{current_customer}' = Customer")
			cursor.execute(get_reserved_property)
			properties = []
			for (Customer, Property_Name, Owner_Email, Start_Date, End_Date, Num_Guests, Was_Cancelled) in cursor:
				Customer = Customer
				Property_Name = Property_Name
				Owner_Email = Owner_Email
				Start_Date = Start_Date
				End_Date = End_Date
				Num_Guests = Num_Guests
				Was_Cancelled = Was_Cancelled
				reserved_properties = (str(Customer), str(Property_Name), str(Owner_Email), str(Start_Date), str(End_Date), str(Num_Guests), str(Was_Cancelled))
				properties.append(reserved_properties)
			for property in properties:
				tree.insert('', tk.END, values = property)

		#place table on page
		tree.grid(row = 2, column = 1, sticky='nsew')
		#add scrollbar
		scrollbar = ttk.Scrollbar(self, orient = tk.VERTICAL, command = tree.yview)
		tree.configure(yscroll=scrollbar.set)
		scrollbar.grid(row = 2, column = 101, rowspan = 2, sticky = 'ns')
		#View booked flights button
		booked_flights_button = tk.Button(self, text = "View Your Reservations", highlightbackground = "#00A7E1", 
			command = lambda : view_reserved_property())
		booked_flights_button.grid(row = 1, column = 3, padx = 10, pady = 10)

		#define cancel reservation function
		def cancel_reservation(i_current_date):
			for selected_item in tree.selection():
				item = tree.item(selected_item)
				customer_email = str(item['values'][0])
				property_name = str(item['values'][1])
				owner_email = str(item['values'][2])
				was_cancelled = int(item['values'][6])
				#sql procedure to cancel flight
			cancel_reserved_property = (f"call cancel_property_reservation('{property_name}', '{owner_email}', '{customer_email}', '{i_current_date}')")
			#check to see if property was cancelled
			check_cancellation = (f"select Customer, Property_Name from Reserve where Customer = '{customer_email}' and Property_Name = '{property_name}' and Was_Cancelled = 1")
			try:
				cursor.execute(cancel_reserved_property)
				cnx.commit()
				cursor.execute(check_cancellation)
				review_valid = 0
				for review in cursor:
					review_valid += 1
				if review_valid != 0:
					messagebox.showinfo("showinfo", "Your submission was successful")
				else:
					messagebox.showwarning("showwarning", "Your submission was unsuccessful. Please check your information.")
			except:
				messagebox.showwarning("showwarning", "Your submission was unsuccessful. Please check your information.")

		#get current date
		current_date_label = tk.Label(self, text = "Today", bg = '#00A7E1', fg="white", font = main_font)
		current_date_label.grid(column = 2, row = 5, padx = 10, pady = 10)
		current_date = Entry(self, highlightbackground = "#FFA630")
		current_date.grid(column = 3, row = 5, padx = 10, pady = 10)
		current_date.insert(END, 'yyyy-mm-dd')
		#cancel flight button
		cancel_reserved_property = tk.Button(self, text = "Cancel Selected Reservation", highlightbackground = "#00A7E1", 
			command = lambda : cancel_reservation(current_date.get()))
		cancel_reserved_property.grid(column = 3, row = 6, padx = 10, pady = 10)


class ReviewProperty(tk.Frame):
	def __init__(self, parent, controller):
		tk.Frame.__init__(self, parent)
		self.controller = controller
		#set page color
		ReviewProperty.configure(self, bg = '#00A7E1')
		#Define return to home button
		#add header and home button
		header = tk.Label(self, text = "Review Property", font = Header_Font2, bg = '#00A7E1', fg="white")
		header.grid(row = 0, column = 1, padx = 10, pady = 10)
		home_button = tk.Button(self, text = "Return to Home", highlightbackground = "#00A7E1",
			command = lambda : controller.show_frame(CustomerHome))
		home_button.grid(row = 0, column = 0, padx = 10, pady = 10)

		#create table to show reserved property
		columns = ('Customer', 'Property_Name', 'Owner_Email', 'Start_Date', 'End_Date', 'Num_Guests', 'Was_Cancelled')
		tree = ttk.Treeview(self, columns = columns, show = 'headings', height=10)
		tree.grid(row = 1, column = 2, columnspan=100)
		tree.column('Customer', width = 150)
		tree.heading('Customer', text = 'Customer')
		tree.column('Property_Name', width = 200)
		tree.heading('Property_Name', text = 'Property')
		tree.column('Owner_Email', width = 150)
		tree.heading('Owner_Email', text = 'Owner Email')
		tree.column('Start_Date', width = 100)
		tree.heading('Start_Date', text = 'Start Date')
		tree.column('End_Date', width = 100)
		tree.heading('End_Date', text = 'End Date')
		tree.column('Num_Guests', width = 75)
		tree.heading('Num_Guests', text = 'Guests')
		tree.column('Was_Cancelled', width = 100)
		tree.heading('Was_Cancelled', text = 'Cancelled')

		#function to view and select reserved properties
		def view_reserved_property():
			#clear current entries
			current_customer = self.controller.user_login["email"].get()
			tree.delete(*tree.get_children())
			#SQL query to view booked flights
			get_reserved_property = (f"select Customer, Property_Name, Owner_Email, Start_Date, End_Date, Num_Guests, Was_Cancelled from Reserve where '{current_customer}' = Customer")
			cursor.execute(get_reserved_property)
			properties = []
			for (Customer, Property_Name, Owner_Email, Start_Date, End_Date, Num_Guests, Was_Cancelled) in cursor:
				Customer = Customer
				Property_Name = Property_Name
				Owner_Email = Owner_Email
				Start_Date = Start_Date
				End_Date = End_Date
				Num_Guests = Num_Guests
				Was_Cancelled = Was_Cancelled
				reserved_properties = (str(Customer), str(Property_Name), str(Owner_Email), str(Start_Date), str(End_Date), str(Num_Guests), str(Was_Cancelled))
				properties.append(reserved_properties)
			for property in properties:
				tree.insert('', tk.END, values = property)

		#place table on page
		tree.grid(row = 2, column = 1, sticky='nsew')
		#add scrollbar
		scrollbar = ttk.Scrollbar(self, orient = tk.VERTICAL, command = tree.yview)
		tree.configure(yscroll=scrollbar.set)
		scrollbar.grid(row = 2, column = 101, rowspan = 2, sticky = 'ns')
		#View booked flights button
		booked_flights_button = tk.Button(self, text = "View Your Reservations", highlightbackground = "#00A7E1", 
			command = lambda : view_reserved_property())
		booked_flights_button.grid(row = 1, column = 3, padx = 10, pady = 10)

		#define review property
		def review_property(i_content, i_score, i_current_date):
			for selected_item in tree.selection():
				item = tree.item(selected_item)
				customer_email = str(item['values'][0])
				property_name = str(item['values'][1])
				owner_email = str(item['values'][2])
				#sql procedure to review property
			review_property = (f"call customer_review_property('{property_name}', '{owner_email}', '{customer_email}', '{i_content}', '{i_score}', '{i_current_date}')")
			check_cancellation = (f"select Customer, Owner_Email from Review where Customer = '{customer_email}' and Owner_Email = '{owner_email}'")
			try:
				cursor.execute(review_property)
				cnx.commit()
				cursor.execute(check_cancellation)
				review_valid = 0
				for review in cursor:
					review_valid += 1
				if review_valid != 0:
					messagebox.showinfo("showinfo", "This property has been reviewed.")
				else:
					messagebox.showwarning("showwarning", "Your submission was unsuccessful. Please check your information.")
			except:
				messagebox.showwarning("showwarning", "Your submission was unsuccessful. Please check your information.")

		#Comment Box
		property_review = Entry(self, highlightbackground = "#FFA630", width = 75)
		property_review.grid(column = 2, row = 5, padx = 10, pady = 10)
		property_review.insert(END, 'Comments')

		#Leave Rating
		rating = Entry(self, highlightbackground = "#FFA630", width = 10)
		rating.grid(column = 2, row = 6)
		rating.insert(END, 'Rating (1-5)')

		#get current date
		current_date = Entry(self, highlightbackground = "#FFA630")
		current_date.grid(column = 3, row = 7, padx = 10, pady = 10)
		current_date.insert(END, 'Confirm Date: yyyy-mm-dd')
		#cancel flight button
		cancel_reserved_property = tk.Button(self, text = "Submit Review", highlightbackground = "#00A7E1", 
			command = lambda : review_property(property_review.get(), rating.get(), current_date.get()))
		cancel_reserved_property.grid(column = 3, row = 8, padx = 10, pady = 10)	

class RateOwner(tk.Frame):
	def __init__(self, parent, controller):
		tk.Frame.__init__(self, parent)
		self.controller = controller
		#set page color
		RateOwner.configure(self, bg = '#00A7E1')
		#Define return to home button
		#add header and home button
		header = tk.Label(self, text = "Rate Owner", font = Header_Font2, bg = '#00A7E1', fg="white")
		header.grid(row = 0, column = 1, padx = 10, pady = 10)
		home_button = tk.Button(self, text = "Return to Home", highlightbackground = "#00A7E1",
			command = lambda : controller.show_frame(CustomerHome))
		home_button.grid(row = 0, column = 0, padx = 10, pady = 10)

		#get current date
		current_date = Entry(self, highlightbackground = "#FFA630")
		current_date.grid(column = 3, row = 1, padx = 10, pady = 10)
		current_date.insert(END, 'Confirm Date: yyyy-mm-dd')

		#create table to show properties stayed at previously
		columns = ('Customer', 'Property_Name', 'Owner_Email')
		tree = ttk.Treeview(self, columns = columns, show = 'headings', height=10)
		tree.grid(row = 1, column = 2, columnspan=100)
		tree.column('Customer', width = 150)
		tree.heading('Customer', text = 'Customer')
		tree.column('Property_Name', width = 200)
		tree.heading('Property_Name', text = 'Property')
		tree.column('Owner_Email', width = 150)
		tree.heading('Owner_Email', text = 'Owner Email')

		#function to view and select reserved properties
		def view_reserved_property(i_current_date):
			current_customer = self.controller.user_login["email"].get()
			#clear current entries
			tree.delete(*tree.get_children())
			#SQL query to view booked flights
			get_reserved_property = (f"select Customer, Property_Name, Owner_Email from Reserve where '{current_customer}' = Customer and '{i_current_date}' > End_Date")
			cursor.execute(get_reserved_property)
			properties = []
			for (Customer, Property_Name, Owner_Email) in cursor:
				Customer = Customer
				Property_Name = Property_Name
				Owner_Email = Owner_Email
				reserved_properties = (str(Customer), str(Property_Name), str(Owner_Email))
				properties.append(reserved_properties)
			for property in properties:
				tree.insert('', tk.END, values = property)

		#place table on page
		tree.grid(row = 2, column = 1, sticky='nsew')
		#add scrollbar
		scrollbar = ttk.Scrollbar(self, orient = tk.VERTICAL, command = tree.yview)
		tree.configure(yscroll=scrollbar.set)
		scrollbar.grid(row = 2, column = 101, rowspan = 2, sticky = 'ns')
		#View stayed at properties
		previous_rentals_button = tk.Button(self, text = "View Owners and Properties", highlightbackground = "#00A7E1", 
			command = lambda : view_reserved_property(current_date.get()))
		previous_rentals_button.grid(row = 1, column = 4, padx = 10, pady = 10)

		#define rate owner
		def review_owner(i_score, i_current_date):
			for selected_item in tree.selection():
				item = tree.item(selected_item)
				customer_email = str(item['values'][0])
				property_name = str(item['values'][1])
				owner_email = str(item['values'][2])
				#sql procedure to review property
			review_owner = (f"call customer_rates_owner('{customer_email}', '{owner_email}', '{i_score}', '{i_current_date}')")
			check_review = (f"select Customer, Owner_Email from Customers_Rate_Owners where Customer = '{customer_email}' and Owner_Email = '{owner_email}'")
			try:
				cursor.execute(review_owner)
				cnx.commit()
				cursor.execute(check_review)
				review_valid = 0
				for review in cursor:
					review_valid += 1
				if review_valid != 0:
					messagebox.showinfo("showinfo", "Your submission was successful")
				else:
					messagebox.showwarning("showwarning", "Your submission was unsuccessful. Please check your information.")
			except:
				messagebox.showwarning("showwarning", "Your submission was unsuccessful. Please check your information.")

		#Leave Rating
		rating = Entry(self, highlightbackground = "#FFA630", width = 15)
		rating.grid(column = 2, row = 8)
		rating.insert(END, 'Rating (1-5)')
		
		#rate owner button
		rate_owner = tk.Button(self, text = "Submit Rating", highlightbackground = "#00A7E1", 
			command = lambda : review_owner(rating.get(), current_date.get()))
		rate_owner.grid(column = 3, row = 8, padx = 10, pady = 10)



#buttons associated with admin home

#add flight page
class AddFlight(tk.Frame):
	def __init__(self, parent, controller):
		tk.Frame.__init__(self, parent)
		#set page color
		AddFlight.configure(self, bg = '#00A7E1')
		#Define return to home button
		#add header and home button
		header = tk.Label(self, text = "Add Flight", font = Header_Font2, bg = '#00A7E1', fg="white")
		header.grid(row = 0, column = 1, padx = 10, pady = 10)
		home_button = tk.Button(self, text = "Return to Home", highlightbackground = "#00A7E1",
			command = lambda : controller.show_frame(AdminHome))
		home_button.grid(row = 0, column = 0, padx = 10, pady = 10)

        #Define fields
		#flight number field
		flight_num_label = tk.Label(self, text = "Flight Number", bg = '#00A7E1', fg="white", font = main_font)
		flight_num_label.grid(row = 1, column = 1, padx = 10, pady = 10)
		flight_num = Entry(self, highlightbackground = "#FFA630")
		flight_num.grid(row = 1, column = 2, padx = 10, pady = 10)
		#Airline field
		airline_lable = tk.Label(self, text = "Airline", bg = '#00A7E1', fg="white", font = main_font)
		airline_lable.grid(row = 2, column = 1, padx = 10, pady = 10)
		airline = Entry(self, highlightbackground = "#FFA630")
		airline.grid(row = 2, column = 2, padx = 10, pady = 10)
		#from airport field
		from_airport_lable = tk.Label(self, text = "Departing From", bg = '#00A7E1', fg="white", font = main_font)
		from_airport_lable.grid(row = 3, column = 1, padx = 10, pady = 10)
		from_airport = Entry(self, highlightbackground = "#FFA630")
		from_airport.grid(row = 3, column = 2, padx = 10, pady = 10)
		#to airport field
		to_airport_lable = tk.Label(self, text = "Destination", bg = '#00A7E1', fg="white", font = main_font)
		to_airport_lable.grid(row = 4, column = 1, padx = 10, pady = 10)
		to_airport = Entry(self, highlightbackground = "#FFA630")
		to_airport.grid(row = 4, column = 2, padx = 10, pady = 10)
		#departure time field
		departure_time_lable = tk.Label(self, text = "Departure Time", bg = '#00A7E1', fg="white", font = main_font)
		departure_time_lable.grid(row = 5, column = 1, padx = 10, pady = 10)
		departure_time = Entry(self, highlightbackground = "#FFA630")
		departure_time.grid(row = 5, column = 2, padx = 10, pady = 10)
		#arrival time field
		arrival_time_label = tk.Label(self, text = "Arrival Time", bg = '#00A7E1', fg="white", font = main_font)
		arrival_time_label.grid(row = 6, column = 1, padx = 10, pady = 10)
		arrival_time = Entry(self, highlightbackground = "#FFA630")
		arrival_time.grid(row = 6, column = 2, padx = 10, pady = 10)
		#flight date field
		flight_date_label = tk.Label(self, text = "Date", bg = '#00A7E1', fg="white", font = main_font)
		flight_date_label.grid(row = 7, column = 1, padx = 10, pady = 10)
		flight_date = Entry(self, highlightbackground = "#FFA630")
		flight_date.grid(row = 7, column = 2, padx = 10, pady = 10)
		#cost field
		cost_label = tk.Label(self, text = "Cost", bg = '#00A7E1', fg="white", font = main_font)
		cost_label.grid(row = 8, column = 1, padx = 10, pady = 10)
		cost = Entry(self, highlightbackground = "#FFA630")
		cost.grid(row = 8, column = 2, padx = 10, pady = 10)
		#capacity field
		capacity_label = tk.Label(self, text = "Capacity", bg = '#00A7E1', fg="white", font = main_font)
		capacity_label.grid(row = 9, column = 1, padx = 10, pady = 10)
		capacity = Entry(self, highlightbackground = "#FFA630")
		capacity.grid(row = 9, column = 2, padx = 10, pady = 10)
        #current date field
		current_date_label = tk.Label(self, text = "Today", bg = '#00A7E1', fg="white", font = main_font)
		current_date_label.grid(row = 10, column = 1, padx = 10, pady = 10)
		current_date = Entry(self, highlightbackground = "#FFA630")
		current_date.grid(row = 10, column = 2, padx = 10, pady = 10)

        #define function to add flight
		def add_flight(flight_num, airline, from_airport, to_airport, departure_time, arrival_time, flight_date, cost, capacity, current_date):
			add_flight = (f"call schedule_flight('{flight_num}', '{airline}', '{from_airport}', '{to_airport}', '{departure_time}', '{arrival_time}', '{flight_date}', '{cost}', '{capacity}', '{current_date}')")
			check_flight = (f"select Flight_Num from Flight where Flight_Num = '{flight_num}' and Airline_Name = '{airline}' and Flight_Date = '{flight_date}' and From_Airport = '{from_airport}' and To_Airport = '{to_airport}' and Departure_Time = '{departure_time}' and Arrival_Time = '{arrival_time}' and Flight_Date = '{flight_date}' and Cost = '{cost}' and Capacity = '{capacity}';")
			try:
				cursor.execute(add_flight)
				cnx.commit()
				cursor.execute(check_flight)
				valid = 0
				for review in cursor:
					valid += 1
				if valid != 0:
					messagebox.showinfo("showinfo", "Flight is scheduled")
				else:
					messagebox.showwarning("showwarning", "Your submission was unsuccessful. Please check the information provided.")
			except:
				messagebox.showwarning("showwarning", "Your submission was unsuccessful. Please check the information provided.")

		#add flight button
		add_flight_button = tk.Button(self, text = "Add Flight", highlightbackground = "#00A7E1",
			command = lambda : add_flight(flight_num.get(), airline.get(), from_airport.get(), to_airport.get(), departure_time.get(), arrival_time.get(), flight_date.get(), cost.get(), capacity.get(), current_date.get()))
		add_flight_button.grid(row = 11, column = 1)

#remove flight page
class RemoveFlight(tk.Frame):
	def __init__(self, parent, controller):
		tk.Frame.__init__(self, parent)
		#set page color
		RemoveFlight.configure(self, bg = '#00A7E1')
		#add header and home button
		header = tk.Label(self, text = "View and Remove Flights", font = Header_Font2, bg = '#00A7E1', fg="white")
		header.grid(row = 0, column = 1, padx = 10, pady = 10)
		home_button = tk.Button(self, text = "Return to Home", highlightbackground = "#00A7E1",
			command = lambda : controller.show_frame(AdminHome))
		home_button.grid(row = 0, column = 0, padx = 10, pady = 10)

		#initialize empty list to store properties info tuples
		flights = []
		#SQL view to view all available flight
		view_flights = ("select Flight_Num, Airline_Name from Flight;")
		cursor.execute(view_flights)
		for (flight_num, airline) in cursor:
			flight_num = flight_num
			airline = airline
			flights_info = (str(flight_num), str(airline))
			flights.append(flights_info)
		#create table to show flights
		columns = ('flight_num', 'airline')
		tree = ttk.Treeview(self, columns = columns, show = 'headings', height=10)
		tree.grid(row = 1, column = 2, columnspan=100)
		tree.column('flight_num', width = 100)
		tree.heading('flight_num', text = 'Flight Number')
		tree.column('airline', width = 100)
		tree.heading('airline', text = 'Airline')
		for flight in flights:
			tree.insert('', tk.END, values = flight)

		#Input current date
		today_date_label = tk.Label(self, text = "Today", bg = '#00A7E1', fg="white", font = main_font)
		today_date_label.grid(row = 9, column = 1, padx = 10, pady = 10, columnspan = 8)
		today_date = Entry(self, highlightbackground = "#FFA630")
		today_date.grid(row = 9, column = 3, padx = 10, pady = 10)
		today_date.insert(END, "Enter Today's Date")

		#function to view flights
		def view_flights():
			#clear current entries
			tree.delete(*tree.get_children())
			#SQL query to view booked flights
			get_flights = (f"select Flight_Num, Airline_Name from Flight;")
			cursor.execute(get_flights)
			flights = []
			for (Flight_Num, Airline_Name) in cursor:
				Flight_Num = Flight_Num
				Airline_Name = Airline_Name
				current_flights = (str(Flight_Num), str(Airline_Name))
				flights.append(current_flights)
			for flight in flights:
				tree.insert('', tk.END, values = flight)
		#place table on page
		tree.grid(row = 2, column = 1, sticky='nsew')
		#add scrollbar
		scrollbar = ttk.Scrollbar(self, orient = tk.VERTICAL, command = tree.yview)
		tree.configure(yscroll=scrollbar.set)
		scrollbar.grid(row = 2, column = 101, rowspan = 2, sticky = 'ns')
		#View booked flights button
		view_flights_button = tk.Button(self, text = "View Flights", highlightbackground = "#00A7E1", 
			command = lambda : view_flights())
		view_flights_button.grid(row = 1, column = 3, padx = 10, pady = 10)

        #define cancel flight function
		def cancel_flight(i_current_date):
			for selected_item in tree.selection():
				item = tree.item(selected_item)
				flight_num = str(item['values'][0])
				airline = str(item['values'][1])
			#sql procedure to cancel flight
			cancel_flight = (f"call remove_flight('{flight_num}', '{airline}', '{i_current_date}')")
			#check to see if flight was cancelled
			check_cancellation = (f"select Flight_Num, Airline_Name from Flight where Flight_Num = '{flight_num}' and Airline_Name = '{airline}';")
			try:
				cursor.execute(cancel_flight)
				cnx.commit()
				cursor.execute(check_cancellation)
				valid = 0
				for flight in cursor:
					valid += 1
				if valid == 0:
					messagebox.showinfo("showinfo", "Your submission was successful")
				else:
					messagebox.showwarning("showwarning", "Your submission was unsuccessful. Please check your information.")
			except:
				messagebox.showwarning("showwarning", "Your submission was unsuccessful. Please check your information.")
		#cancel flight button
		cancel_flight_button = tk.Button(self, text = "Remove Selected Flight", highlightbackground = "#00A7E1", 
			command = lambda : cancel_flight(today_date.get()))
		cancel_flight_button.grid(column = 3, row = 6, padx = 10, pady = 10)

#view airports page
class ViewAirports(tk.Frame):
	def __init__(self, parent, controller):
		tk.Frame.__init__(self, parent)
		#set page color
		ViewAirports.configure(self, bg = '#00A7E1')
		#add header and home button
		header = tk.Label(self, text = "View Airports", font = Header_Font2, bg = '#00A7E1', fg="white")
		header.grid(row = 0, column = 1, padx = 10, pady = 10)
		home_button = tk.Button(self, text = "Return to Home", highlightbackground = "#00A7E1",
			command = lambda : controller.show_frame(AdminHome))
		home_button.grid(row = 0, column = 0, padx = 10, pady = 10)

		#create table to show flights
		columns = ('airport_id', 'airport_name', 'time_zone', 'total_arriving_flights', 'total_departing_flights', 'avg_departing_flight_cost')
		tree = ttk.Treeview(self, columns = columns, show = 'headings', height=10)
		tree.grid(row = 1, column = 2, columnspan=100)
		tree.column('airport_id', width = 100)
		tree.heading('airport_id', text = 'Airport ID')
		tree.column('airport_name', width = 325)
		tree.heading('airport_name', text = 'Airport')
		tree.column('time_zone', width = 100)
		tree.heading('time_zone', text = 'Time Zone')
		tree.column('total_arriving_flights', width = 150)
		tree.heading('total_arriving_flights', text = 'Total Arriving Flights')
		tree.column('total_departing_flights', width = 150)
		tree.heading('total_departing_flights', text = 'Total Departing Flights')
		tree.column('avg_departing_flight_cost', width = 200)
		tree.heading('avg_departing_flight_cost', text = 'Average Departing Cost')
		#place table on page
		tree.grid(row = 2, column = 1, sticky='nsew')
		#add scrollbar
		scrollbar = ttk.Scrollbar(self, orient = tk.VERTICAL, command = tree.yview)
		tree.configure(yscroll=scrollbar.set)
		scrollbar.grid(row = 2, column = 101, rowspan = 2, sticky = 'ns')

		def refresh():
			#clear current entries
			tree.delete(*tree.get_children())
			#SQL query to view booked flights
			view_airports = ("select * from view_airports;")
			cursor.execute(view_airports)
			airports = []
			for (airport_id, airport_name, time_zone, total_arriving_flights, total_departing_flights, avg_departing_flight_cost) in cursor:
				airport_id = airport_id
				airport_name = airport_name
				time_zone = time_zone
				total_arriving_flights = total_arriving_flights
				total_departing_flights = total_departing_flights
				avg_departing_flight_cost = avg_departing_flight_cost
				airport_info = (str(airport_id), str(airport_name), str(time_zone), str(total_arriving_flights), str(total_departing_flights), str(avg_departing_flight_cost))
				airports.append(airport_info)
			for airport in airports:
				tree.insert('', tk.END, values = airport)
		refresh_button = tk.Button(self, text = "Refresh", highlightbackground = "#00A7E1", 
			command = lambda : refresh())
		refresh_button.grid(row = 0, column = 3, padx = 10, pady = 10)

#view owners page
class ViewOwners(tk.Frame):
	def __init__(self, parent, controller):
		tk.Frame.__init__(self, parent)
		#set page color
		ViewOwners.configure(self, bg = '#00A7E1')
		#add header and home button
		header = tk.Label(self, text = "Owners", font = Header_Font2, bg = '#00A7E1', fg="white")
		header.grid(row = 0, column = 1, padx = 10, pady = 10)
		home_button = tk.Button(self, text = "Return to Home", highlightbackground = "#00A7E1",
			command = lambda : controller.show_frame(AdminHome))
		home_button.grid(row = 0, column = 0, padx = 10, pady = 10)

		#initialize empty list to store properties info tuples
		owners = []
		#SQL view to view all airlines
		view_owners = ("select * from view_owners;")
		cursor.execute(view_owners)
		for (owner_name, avg_rating, num_properties, avg_property_rating) in cursor:
			owner_name = owner_name
			avg_rating = avg_rating
			num_properties = num_properties
			avg_property_rating = avg_property_rating
			owners_info = (str(owner_name), str(avg_rating), str(num_properties), str(avg_property_rating))
			owners.append(owners_info)
		#create table to show airlines
		columns = ('owner_name', 'avg_rating', 'num_properties', 'avg_property_rating')
		tree = ttk.Treeview(self, columns = columns, show = 'headings', height=10)
		tree.grid(row = 1, column = 2, columnspan=100)
		tree.column('owner_name', width = 200)
		tree.heading('owner_name', text = 'Owner')
		tree.column('avg_rating', width = 100)
		tree.heading('avg_rating', text = 'Average Rating')
		tree.column('num_properties', width = 150)
		tree.heading('num_properties', text = 'Number of Properties')
		tree.column('avg_property_rating', width = 150)
		tree.heading('avg_property_rating', text = 'Average Property Rating')
		for owner in owners:
			tree.insert('', tk.END, values = owner)
		#place table on page
		tree.grid(row = 2, column = 1, sticky='nsew')
		#add scrollbar
		scrollbar = ttk.Scrollbar(self, orient = tk.VERTICAL, command = tree.yview)
		tree.configure(yscroll=scrollbar.set)
		scrollbar.grid(row = 2, column = 101, rowspan = 2, sticky = 'ns')

#view customers page
class ViewCustomers(tk.Frame):
	def __init__(self, parent, controller):
		tk.Frame.__init__(self, parent)
		#set page color
		ViewCustomers.configure(self, bg = '#00A7E1')
		#add header and home button
		header = tk.Label(self, text = "Customers", font = Header_Font2, bg = '#00A7E1', fg="white")
		header.grid(row = 0, column = 1, padx = 10, pady = 10)
		home_button = tk.Button(self, text = "Return to Home", highlightbackground = "#00A7E1",
			command = lambda : controller.show_frame(AdminHome))
		home_button.grid(row = 0, column = 0, padx = 10, pady = 10)

		#initialize empty list to store properties info tuples
		customers = []
		#SQL view to view all airlines
		view_customers = ("select * from view_customers;")
		cursor.execute(view_customers)
		for (customer_name, avg_rating, location, is_owner, total_seats_purchased) in cursor:
			customer_name = customer_name
			avg_rating = avg_rating
			location = location
			is_owner = is_owner
			total_seats_purchased = total_seats_purchased
			customers_info = (str(customer_name), str(avg_rating), str(location), str(is_owner), str(total_seats_purchased))
			customers.append(customers_info)
		#create table to show airlines
		columns = ('customer_name', 'avg_rating', 'location', 'is_owner', 'total_seats_purchased')
		tree = ttk.Treeview(self, columns = columns, show = 'headings', height=10)
		tree.grid(row = 1, column = 2, columnspan=100)
		tree.column('customer_name', width = 200)
		tree.heading('customer_name', text = 'Customer')
		tree.column('avg_rating', width = 100)
		tree.heading('avg_rating', text = 'Average Rating')
		tree.column('location', width = 100)
		tree.heading('location', text = 'Location')
		tree.column('is_owner', width = 150)
		tree.heading('is_owner', text = 'Owner')
		tree.column('total_seats_purchased', width = 150)
		tree.heading('total_seats_purchased', text = 'Total Seats Purchased')
		for customer in customers:
			tree.insert('', tk.END, values = customer)
		#place table on page
		tree.grid(row = 2, column = 1, sticky='nsew')
		#add scrollbar
		scrollbar = ttk.Scrollbar(self, orient = tk.VERTICAL, command = tree.yview)
		tree.configure(yscroll=scrollbar.set)
		scrollbar.grid(row = 2, column = 101, rowspan = 2, sticky = 'ns')

		def process_date(i_current_date):
			#clear current entries
			tree.delete(*tree.get_children())
            #sql query to process date
			process_date = (f"call process_date('{i_current_date}')")
			cursor.execute(process_date)
			cnx.commit()
			#SQL query to view customers
			view_customers = ("select * from view_customers;")
			cursor.execute(view_customers)
			customers = []
			for (customer_name, avg_rating, location, is_owner, total_seats_purchased) in cursor:
				customer_name = customer_name
				avg_rating = avg_rating
				location = location
				is_owner = is_owner
				total_seats_purchased = total_seats_purchased
				customers_info = (str(customer_name), str(avg_rating), str(location), str(is_owner), str(total_seats_purchased))
				customers.append(customers_info)
			for customer in customers:
				tree.insert('', tk.END, values = customer)

		#get current date
		current_date_label = tk.Label(self, text = "Date", bg = '#00A7E1', fg="white", font = main_font)
		current_date_label.grid(column = 2, row = 5, padx = 10, pady = 10)
		current_date = Entry(self, highlightbackground = "#FFA630")
		current_date.grid(column = 3, row = 5, padx = 10, pady = 10)
		current_date.insert(END, 'yyyy-mm-dd')
        #process date button
		process_date_button = tk.Button(self, text = "Process Date", highlightbackground = "#00A7E1", 
			command = lambda : process_date(current_date.get()))
		process_date_button.grid(column = 3, row = 6, padx = 10, pady = 10)

#view airlines page
class ViewAirlines(tk.Frame):
	def __init__(self, parent, controller):
		tk.Frame.__init__(self, parent)
		#set page color
		ViewAirlines.configure(self, bg = '#00A7E1')
		#add header and home button
		header = tk.Label(self, text = "View Airlines", font = Header_Font2, bg = '#00A7E1', fg="white")
		header.grid(row = 0, column = 1, padx = 10, pady = 10)
		home_button = tk.Button(self, text = "Return to Home", highlightbackground = "#00A7E1",
			command = lambda : controller.show_frame(AdminHome))
		home_button.grid(row = 0, column = 0, padx = 10, pady = 10)

		#initialize empty list to store properties info tuples
		airlines = []
		#SQL view to view all airlines
		view_airports = ("select * from view_airlines;")
		cursor.execute(view_airports)
		for (airline_name, rating, total_flights, min_flight_cost) in cursor:
			airline_name = airline_name
			rating = rating
			total_flights = total_flights
			min_flight_cost = min_flight_cost
			airlines_info = (str(airline_name), str(rating), str(total_flights), str(min_flight_cost))
			airlines.append(airlines_info)
		#create table to show airlines
		columns = ('airline_name', 'rating', 'total_flights', 'min_flight_cost')
		tree = ttk.Treeview(self, columns = columns, show = 'headings', height=10)
		tree.grid(row = 1, column = 2, columnspan=100)
		tree.column('airline_name', width = 200)
		tree.heading('airline_name', text = 'Airline')
		tree.column('rating', width = 100)
		tree.heading('rating', text = 'Rating')
		tree.column('total_flights', width = 100)
		tree.heading('total_flights', text = 'Total Flights')
		tree.column('min_flight_cost', width = 150)
		tree.heading('min_flight_cost', text = 'Minimum Flight Cost')
		for airline in airlines:
			tree.insert('', tk.END, values = airline)

		def refresh():
			#clear current entries
			tree.delete(*tree.get_children())
			#SQL query to view booked flights
			view_airlines = ("select * from view_airlines;")
			cursor.execute(view_airlines)
			airlines = []
			for (airline_name, rating, total_flights, min_flight_cost) in cursor:
				airline_name = airline_name
				rating = rating
				total_flights = total_flights
				min_flight_cost = min_flight_cost
				airlines_info = (str(airline_name), str(rating), str(total_flights), str(min_flight_cost))
				airlines.append(airlines_info)
			for airline in airlines:
				tree.insert('', tk.END, values = airline)
		refresh_button = tk.Button(self, text = "Refresh", highlightbackground = "#00A7E1", 
			command = lambda : refresh())
		refresh_button.grid(row = 0, column = 3, padx = 10, pady = 10)

		#place table on page
		tree.grid(row = 2, column = 1, sticky='nsew')
		#add scrollbar
		scrollbar = ttk.Scrollbar(self, orient = tk.VERTICAL, command = tree.yview)
		tree.configure(yscroll=scrollbar.set)
		scrollbar.grid(row = 2, column = 101, rowspan = 2, sticky = 'ns')



#buttons associated with Owner home page

#add property page
class AddProperty(tk.Frame):
	def __init__(self, parent, controller):
		tk.Frame.__init__(self, parent)
		self.controller = controller
		#set page color
		AddProperty.configure(self, bg = '#00A7E1')
		header = tk.Label(self, text = "Add New Property", font = Header_Font2, bg = '#00A7E1', fg="white")
		header.grid(row = 0, column = 4, padx = 10, pady = 10)
		home_button = tk.Button(self, text = "Return to Home", highlightbackground = "#00A7E1",
			command = lambda : controller.show_frame(OwnerHome))
		home_button.grid(row = 0, column = 0, padx = 10, pady = 10)

		#Get property information field
		#first name field
		property_name_label = tk.Label(self, text = "Name", bg = '#00A7E1', fg="white", font = main_font)
		property_name_label.grid(row = 1, column = 1, padx = 10, pady = 10)
		property_name = Entry(self, highlightbackground = "#FFA630")
		property_name.grid(row = 1, column = 2, padx = 10, pady = 10)
		#desc field
		description_label = tk.Label(self, text = "Description", bg = '#00A7E1', fg="white", font = main_font)
		description_label.grid(row = 2, column = 1, padx = 10, pady = 10)
		description = Entry(self, highlightbackground = "#FFA630")
		description.grid(row = 2, column = 2, padx = 10, pady = 10)
		#capacity field
		capacity_label = tk.Label(self, text = "Capacity", bg = '#00A7E1', fg="white", font = main_font)
		capacity_label.grid(row = 3, column = 1, padx = 10, pady = 10)
		capacity = Entry(self, highlightbackground = "#FFA630")
		capacity.grid(row = 3, column = 2, padx = 10, pady = 10)
		#cost field
		cost_label = tk.Label(self, text = "Cost", bg = '#00A7E1', fg="white", font = main_font)
		cost_label.grid(row = 4, column = 1, padx = 10, pady = 10)
		cost = Entry(self, highlightbackground = "#FFA630")
		cost.grid(row = 4, column = 2, padx = 10, pady = 10)
		#street field
		street_label = tk.Label(self, text = "Street", bg = '#00A7E1', fg="white", font = main_font)
		street_label.grid(row = 5, column = 1, padx = 10, pady = 10)
		street = Entry(self, highlightbackground = "#FFA630")
		street.grid(row = 5, column = 2, padx = 10, pady = 10)
		#city field
		city_label = tk.Label(self, text = "City", bg = '#00A7E1', fg="white", font = main_font)
		city_label.grid(row = 6, column = 1, padx = 10, pady = 10)
		city = Entry(self, highlightbackground = "#FFA630")
		city.grid(row = 6, column = 2, padx = 10, pady = 10)
		#state field
		state_label = tk.Label(self, text = "State", bg = '#00A7E1', fg="white", font = main_font)
		state_label.grid(row = 7, column = 1, padx = 10, pady = 10)
		state = Entry(self, highlightbackground = "#FFA630")
		state.grid(row = 7, column = 2, padx = 10, pady = 10)
		#zip field
		zip_label = tk.Label(self, text = "Zip", bg = '#00A7E1', fg="white", font = main_font)
		zip_label.grid(row = 8, column = 1, padx = 10, pady = 10)
		zip = Entry(self, highlightbackground = "#FFA630")
		zip.grid(row = 8, column = 2, padx = 10, pady = 10)
		#nearest airport field
		nearest_airport_label = tk.Label(self, text = "Nearest Airport", bg = '#00A7E1', fg="white", font = main_font)
		nearest_airport_label.grid(row = 9, column = 1, padx = 10, pady = 10)
		nearest_airport = Entry(self, highlightbackground = "#FFA630")
		nearest_airport.grid(row = 9, column = 2, padx = 10, pady = 10)
		#distance to airport field
		distance_airport_label = tk.Label(self, text = "Distance to Airport", bg = '#00A7E1', fg="white", font = main_font)
		distance_airport_label.grid(row = 10, column = 1, padx = 10, pady = 10)
		distance_airport = Entry(self, highlightbackground = "#FFA630")
		distance_airport.grid(row = 10, column = 2, padx = 10, pady = 10)

		#define funciton to add property
		def add_new_property(prop_name, description, capacity, cost, street, city, state, zip, nearest_airport, distance_airport):
			current_customer = self.controller.user_login["email"].get()
			add_property = (f"call add_property('{prop_name}', '{current_customer}', '{description}', '{capacity}', '{cost}', '{street}', '{city}', '{state}', '{zip}', '{nearest_airport}', '{distance_airport}')")
			check_register = (f"select Property_Name, Owner_Email from Property where Property_Name = '{prop_name}' and Owner_Email = '{current_customer}' and Street = '{street}' and City = '{city}' and State = '{state}' and Zip = '{zip}';")
			try:
				cursor.execute(add_property)
				cnx.commit()
				cursor.execute(check_register)
				reg_valid = 0
				for review in cursor:
					reg_valid += 1
				if reg_valid != 0:
					messagebox.showinfo("showinfo", "Your submission was successful")
				else:
					messagebox.showwarning("showwarning", "Your submission was unsuccessful. Please check your information.")
			except:
				messagebox.showwarning("showwarning", "Your submission was unsuccessful. Please check your information.")		

		#register button
		add_property = tk.Button(self, text = "Add Property", highlightbackground = "#00A7E1",
			command = lambda : add_new_property(property_name.get(), description.get(), capacity.get(), cost.get(), street.get(), city.get(), state.get(), zip.get(), nearest_airport.get(), distance_airport.get()))
		add_property.grid(row = 12, column = 1)

#remove property page
class RemoveProperty(tk.Frame):
	def __init__(self, parent, controller):
		tk.Frame.__init__(self, parent)
		self.controller = controller
		#set page color
		RemoveProperty.configure(self, bg = '#00A7E1')
		#add header and home button and Define return to home button
		header = tk.Label(self, text = "View and Remove Property", font = Header_Font2, bg = '#00A7E1', fg="white")
		header.grid(row = 0, column = 1, padx = 10, pady = 10)
		home_button = tk.Button(self, text = "Return to Home", highlightbackground = "#00A7E1",
			command = lambda : controller.show_frame(OwnerHome))
		home_button.grid(row = 0, column = 0, padx = 10, pady = 10)

		#create table to show properties
		columns = ('Property_Name', 'Owner_Email')
		tree = ttk.Treeview(self, columns = columns, show = 'headings', height=10)
		tree.grid(row = 1, column = 2, columnspan=100)
		tree.column('Property_Name', width = 175)
		tree.heading('Property_Name', text = 'Property')
		tree.column('Owner_Email', width = 100)
		tree.heading('Owner_Email', text = 'Owner Email')

		#function to view properties
		def view_properties():
			current_customer = self.controller.user_login["email"].get()
			#clear current entries
			tree.delete(*tree.get_children())
			#SQL query to view booked flights
			get_properties = (f"select Property_Name, Owner_Email from Property where Owner_Email = '{current_customer}'")
			cursor.execute(get_properties)
			properties = []
			for (Property_Name, Owner_Email) in cursor:
				Property_Name = Property_Name
				Owner_Email = Owner_Email
				owned_properties = (str(Property_Name), str(Owner_Email))
				properties.append(owned_properties)
			for property in properties:
				tree.insert('', tk.END, values = property)
		#place table on page
		tree.grid(row = 2, column = 1, sticky='nsew')
		#add scrollbar
		scrollbar = ttk.Scrollbar(self, orient = tk.VERTICAL, command = tree.yview)
		tree.configure(yscroll=scrollbar.set)
		scrollbar.grid(row = 2, column = 101, rowspan = 2, sticky = 'ns')
		#View booked flights button
		view_properties_button = tk.Button(self, text = "View Your Properties", highlightbackground = "#00A7E1", 
			command = lambda : view_properties())
		view_properties_button.grid(row = 1, column = 3, padx = 10, pady = 10)

		#define remove property function
		def remove_property(i_current_date):
			for selected_item in tree.selection():
				item = tree.item(selected_item)
				Property_Name = str(item['values'][0])
				Owner_Email = str(item['values'][1])
			#sql procedure to cancel flight
			remove_property = (f"call remove_property('{Property_Name}', '{Owner_Email}', '{i_current_date}')")
			#check to see if property was removed
			check_removal = (f"select Property_Name from Property where Property_Name = '{Property_Name}' and Owner_Email = '{Owner_Email}'")
			try:
				cursor.execute(remove_property)
				cnx.commit()
				cursor.execute(check_removal)
				review_valid = 0
				for review in cursor:
					review_valid += 1
				if review_valid == 0:
					messagebox.showinfo("showinfo", "Your submission was successful")
				else:
					messagebox.showwarning("showwarning", "Your submission was unsuccessful. Please check your information.")
			except:
				messagebox.showwarning("showwarning", "Your submission was unsuccessful. Please check your information.")

		#get current date
		current_date_label = tk.Label(self, text = "Today", bg = '#00A7E1', fg="white", font = main_font)
		current_date_label.grid(column = 2, row = 5, padx = 10, pady = 10)
		current_date = Entry(self, highlightbackground = "#FFA630")
		current_date.grid(column = 3, row = 5, padx = 10, pady = 10)
		current_date.insert(END, 'yyyy-mm-dd')

		#remove property button
		remove_property_button = tk.Button(self, text = "Remove Property", highlightbackground = "#00A7E1", 
			command = lambda : remove_property(current_date.get()))
		remove_property_button.grid(column = 3, row = 6, padx = 10, pady = 10)

#rate customer page
class RateCustomer(tk.Frame):
	def __init__(self, parent, controller):
		tk.Frame.__init__(self, parent)
		self.controller = controller
		#set page color
		RateCustomer.configure(self, bg = '#00A7E1')
		#Define return to home button
		#add header and home button
		header = tk.Label(self, text = "Rate Customer", font = Header_Font2, bg = '#00A7E1', fg="white")
		header.grid(row = 0, column = 1, padx = 10, pady = 10)
		home_button = tk.Button(self, text = "Return to Home", highlightbackground = "#00A7E1",
			command = lambda : controller.show_frame(OwnerHome))
		home_button.grid(row = 0, column = 0, padx = 10, pady = 10)

		#get current date
		current_date = Entry(self, highlightbackground = "#FFA630")
		current_date.grid(column = 3, row = 1, padx = 10, pady = 10)
		current_date.insert(END, 'Confirm Date: yyyy-mm-dd')

		#create table to show properties stayed at previously
		columns = ('Customer', 'Property_Name', 'Owner_Email')
		tree = ttk.Treeview(self, columns = columns, show = 'headings', height=10)
		tree.grid(row = 1, column = 2, columnspan=100)
		tree.column('Customer', width = 150)
		tree.heading('Customer', text = 'Customer')
		tree.column('Property_Name', width = 200)
		tree.heading('Property_Name', text = 'Property')
		tree.column('Owner_Email', width = 150)
		tree.heading('Owner_Email', text = 'Owner Email')

		#function to view and select reserved properties
		def view_reserved_property(i_current_date):
			current_customer = self.controller.user_login["email"].get()
			#clear current entries
			tree.delete(*tree.get_children())
			#SQL query to view booked flights
			get_reserved_property = (f"select Customer, Property_Name, Owner_Email from Reserve where '{current_customer}' = Owner_Email and '{i_current_date}' > End_Date")
			cursor.execute(get_reserved_property)
			properties = []
			for (Customer, Property_Name, Owner_Email) in cursor:
				Customer = Customer
				Property_Name = Property_Name
				Owner_Email = Owner_Email
				reserved_properties = (str(Customer), str(Property_Name), str(Owner_Email))
				properties.append(reserved_properties)
			for property in properties:
				tree.insert('', tk.END, values = property)

		#place table on page
		tree.grid(row = 2, column = 1, sticky='nsew')
		#add scrollbar
		scrollbar = ttk.Scrollbar(self, orient = tk.VERTICAL, command = tree.yview)
		tree.configure(yscroll=scrollbar.set)
		scrollbar.grid(row = 2, column = 101, rowspan = 2, sticky = 'ns')
		#View stayed at properties
		previous_rentals_button = tk.Button(self, text = "View Renters", highlightbackground = "#00A7E1", 
			command = lambda : view_reserved_property(current_date.get()))
		previous_rentals_button.grid(row = 1, column = 4, padx = 10, pady = 10)

		#define rate owner
		def review_customer(i_score, i_current_date):
			for selected_item in tree.selection():
				item = tree.item(selected_item)
				customer_email = str(item['values'][0])
				property_name = str(item['values'][1])
				owner_email = str(item['values'][2])
				#sql procedure to review property
			rate_customer = (f"call owner_rates_customer('{owner_email}', '{customer_email}', '{i_score}', '{i_current_date}')")
			check_review = (f"select Customer, Owner_Email from Owners_Rate_Customers where Customer = '{customer_email}' and Owner_Email = '{owner_email}'")
			try:
				cursor.execute(rate_customer)
				cnx.commit()
				cursor.execute(check_review)
				review_valid = 0
				for review in cursor:
					review_valid += 1
				if review_valid != 0:
					messagebox.showinfo("showinfo", "Your submission was successful")
				else:
					messagebox.showwarning("showwarning", "Your submission was unsuccessful. Please check your information.")
			except:
				messagebox.showwarning("showwarning", "Your submission was unsuccessful. Please check your information.")

		#Leave Rating
		rating = Entry(self, highlightbackground = "#FFA630", width = 15)
		rating.grid(column = 2, row = 8)
		rating.insert(END, 'Rating (1-5)')
		
		#rate owner button
		rate_owner = tk.Button(self, text = "Submit Rating", highlightbackground = "#00A7E1", 
			command = lambda : review_customer(rating.get(), current_date.get()))
		rate_owner.grid(column = 3, row = 8, padx = 10, pady = 10)

#manage account page
class ManageAccount(tk.Frame):
	def __init__(self, parent, controller):
		tk.Frame.__init__(self, parent)
		#set page color
		ManageAccount.configure(self, bg = '#00A7E1')
		header = tk.Label(self, text = "Manage Account", 
			font = Header_Font2, bg = '#00A7E1', fg="white")
		header.grid(column = 1, row = 0, padx = 10, pady = 10)
		home_button = tk.Button(self, text = "Return to Home", highlightbackground = "#00A7E1",
			command = lambda : controller.show_frame(OwnerHome))
		home_button.grid(row = 0, column = 0, padx = 10, pady = 10)
		#define register as customer button
		register_as_customer = tk.Button(self, text = "Register as Customer", height = 5, width = 20,
			highlightbackground = "#FFA630", font = main_font, command = lambda : controller.show_frame(RegisterCustomer))
		register_as_customer.grid(column = 1, row = 1, padx = 10, pady = 10)
		#remove account button
		remove_account = tk.Button(self, text = "Remove Account", height = 5, width = 20,
			highlightbackground = "#FFA630", font = main_font, command = lambda : controller.show_frame(RemoveAccount))
		remove_account.grid(column = 3, row = 1, padx = 10, pady = 10)

#remove owner account
class RemoveAccount(tk.Frame):
	def __init__(self, parent, controller):
		tk.Frame.__init__(self, parent)
		#set page color
		self.controller = controller
		RemoveAccount.configure(self, bg = '#00A7E1')
		header = tk.Label(self, text = "Are you sure you want to delete your account?", font = Header_Font2, bg = '#00A7E1', fg="white")
		header.grid(row = 0, column = 1, padx = 10, pady = 10)
		home_button = tk.Button(self, text = "Return to Home", highlightbackground = "#00A7E1",
			command = lambda : controller.show_frame(OwnerHome))
		home_button.grid(row = 0, column = 0, padx = 10, pady = 10)
		
		#define remove property function
		def remove_account():
			current_customer = self.controller.user_login["email"].get()
			#call sql procedure to remove account
			remove_owner = (f"call remove_owner('{current_customer}')")
			#check to see if account was removed
			check_removal = (f"select Email from Owners where Email = '{current_customer}'")
			try:
				cursor.execute(remove_owner)
				cnx.commit()
				cursor.execute(check_removal)
				review_valid = 0
				for review in cursor:
					review_valid += 1
				if review_valid == 0:
					messagebox.showinfo("showinfo", "Your submission was successful")
					controller.show_frame(LoginPage)
				else:
					messagebox.showwarning("showwarning", "Your submission was unsuccessful. Please check your information.")
			except:
				messagebox.showwarning("showwarning", "Your submission was unsuccessful. Please check your information.")

		#confirm removal button
		remove_button = tk.Button(self, text = "Delete Account", highlightbackground = "#00A7E1",
			command = lambda : remove_account())
		remove_button.grid(row = 2, column = 1)


#Registering new user (customer and owner)

#register new customer page
class RegisterCustomer(tk.Frame):
	def __init__(self, parent, controller):
		tk.Frame.__init__(self, parent)
		#set page color
		RegisterCustomer.configure(self, bg = '#00A7E1')
		header = tk.Label(self, text = "Welcome New Customer!", font = Header_Font2, bg = '#00A7E1', fg="white")
		header.grid(row = 0, column = 4, padx = 10, pady = 10)
		
		#Get registration information field
		#first name field
		fname_lable = tk.Label(self, text = "First Name", bg = '#00A7E1', fg="white", font = main_font)
		fname_lable.grid(row = 1, column = 1, padx = 10, pady = 10)
		fname_entry = Entry(self, highlightbackground = "#FFA630")
		fname_entry.grid(row = 1, column = 2, padx = 10, pady = 10)
		#last name filed
		lname_labeld = tk.Label(self, text = "Last Name", bg = '#00A7E1', fg="white", font = main_font)
		lname_labeld.grid(row = 2, column = 1, padx = 10, pady = 10)
		lname_entry = Entry(self, highlightbackground = "#FFA630")
		lname_entry.grid(row = 2, column = 2, padx = 10, pady = 10)
		#email fiel
		email_label = tk.Label(self, text = "Email", bg = '#00A7E1', fg="white", font = main_font)
		email_label.grid(row = 3, column = 1, padx = 10, pady = 10)
		email_entry = Entry(self, highlightbackground = "#FFA630")
		email_entry.grid(row = 3, column = 2, padx = 10, pady = 10)
		#password field
		password_label = tk.Label(self, text = "Password", bg = '#00A7E1', fg="white", font = main_font)
		password_label.grid(row = 4, column = 1, padx = 10, pady = 10)
		password_entry = Entry(self, highlightbackground = "#FFA630")
		password_entry.grid(row = 4, column = 2, padx = 10, pady = 10)
		#phone number field
		phone_number_label = tk.Label(self, text = "Phone Number", bg = '#00A7E1', fg="white", font = main_font)
		phone_number_label.grid(row = 5, column = 1, padx = 10, pady = 10)
		phone_number_entry = Entry(self, highlightbackground = "#FFA630")
		phone_number_entry.grid(row = 5, column = 2, padx = 10, pady = 10)
		#credit card number field
		cc_label = tk.Label(self, text = "Credit Card Number", bg = '#00A7E1', fg="white", font = main_font)
		cc_label.grid(row = 6, column = 1, padx = 10, pady = 10)
		cc_entry = Entry(self, highlightbackground = "#FFA630")
		cc_entry.grid(row = 6, column = 2, padx = 10, pady = 10)
		#cvv field
		cvv_label = tk.Label(self, text = "CVV", bg = '#00A7E1', fg="white", font = main_font)
		cvv_label.grid(row = 7, column = 1, padx = 10, pady = 10)
		cvv_entry = Entry(self, highlightbackground = "#FFA630")
		cvv_entry.grid(row = 7, column = 2, padx = 10, pady = 10)
		#exp date field
		exp_date_label = tk.Label(self, text = "Expiration Date", bg = '#00A7E1', fg="white", font = main_font)
		exp_date_label.grid(row = 8, column = 1, padx = 10, pady = 10)
		exp_date_entry = Entry(self, highlightbackground = "#FFA630")
		exp_date_entry.grid(row = 8, column = 2, padx = 10, pady = 10)
		#Locaton field
		location_label = tk.Label(self, text = "Location", bg = '#00A7E1', fg="white", font = main_font)
		location_label.grid(row = 9, column = 1, padx = 10, pady = 10)
		location_entry = Entry(self, highlightbackground = "#FFA630")
		location_entry.grid(row = 9, column = 2, padx = 10, pady = 10)

		#define funciton to register new customer
		def register_customer(email, fname, lname, password, phone, ccn, cvv, exp, location):
			register_new = (f"call register_customer('{email}', '{fname}', '{lname}', '{password}', '{phone}', '{ccn}', '{cvv}', '{exp}', '{location}')")
			check_register = (f"select Email from Customer where Email = '{email}';")
			try:
				cursor.execute(check_register)
				exists = 0
				for customer in cursor:
					exists += 1
				cursor.execute(register_new)
				cnx.commit()
				cursor.execute(check_register)
				reg_valid = 0
				for review in cursor:
					reg_valid += 1
				if reg_valid != 0 and exists == 0:
					messagebox.showinfo("showinfo", "Your submission was successful")
					controller.show_frame(LoginPage)
				else:
					messagebox.showwarning("showwarning", "Your submission was unsuccessful. Please check your information.")
			except:
				messagebox.showwarning("showwarning", "Your submission was unsuccessful. Please check your information.")		

		#register button
		register_button = tk.Button(self, text = "Register", highlightbackground = "#00A7E1",
			command = lambda : register_customer(email_entry.get(), fname_entry.get(), lname_entry.get(), password_entry.get(), phone_number_entry.get(), cc_entry.get(), cvv_entry.get(), exp_date_entry.get(), location_entry.get()))
		register_button.grid(row = 10, column = 1)

#Register new owner page
class RegisterOwner(tk.Frame):
	def __init__(self, parent, controller):
		tk.Frame.__init__(self, parent)
		#set page color
		RegisterOwner.configure(self, bg = '#00A7E1')
		header = tk.Label(self, text = "Welcome New Owner!", font = Header_Font2, bg = '#00A7E1', fg="white")
		header.grid(row = 0, column = 4, padx = 10, pady = 10)
		
		#Get registration information field
		#first name field
		fname_lable = tk.Label(self, text = "First Name", bg = '#00A7E1', fg="white", font = main_font)
		fname_lable.grid(row = 1, column = 1, padx = 10, pady = 10)
		fname_entry = Entry(self, highlightbackground = "#FFA630")
		fname_entry.grid(row = 1, column = 2, padx = 10, pady = 10)
		#last name filed
		lname_labeld = tk.Label(self, text = "Last Name", bg = '#00A7E1', fg="white", font = main_font)
		lname_labeld.grid(row = 2, column = 1, padx = 10, pady = 10)
		lname_entry = Entry(self, highlightbackground = "#FFA630")
		lname_entry.grid(row = 2, column = 2, padx = 10, pady = 10)
		#email fiel
		email_label = tk.Label(self, text = "Email", bg = '#00A7E1', fg="white", font = main_font)
		email_label.grid(row = 3, column = 1, padx = 10, pady = 10)
		email_entry = Entry(self, highlightbackground = "#FFA630")
		email_entry.grid(row = 3, column = 2, padx = 10, pady = 10)
		#password field
		password_label = tk.Label(self, text = "Password", bg = '#00A7E1', fg="white", font = main_font)
		password_label.grid(row = 4, column = 1, padx = 10, pady = 10)
		password_entry = Entry(self, highlightbackground = "#FFA630")
		password_entry.grid(row = 4, column = 2, padx = 10, pady = 10)
		#phone number field
		phone_number_label = tk.Label(self, text = "Phone Number", bg = '#00A7E1', fg="white", font = main_font)
		phone_number_label.grid(row = 5, column = 1, padx = 10, pady = 10)
		phone_number_entry = Entry(self, highlightbackground = "#FFA630")
		phone_number_entry.grid(row = 5, column = 2, padx = 10, pady = 10)
		#define funciton to register new customer
		def register_customer(email, fname, lname, password, phone):
			register_new = (f"call register_owner('{email}', '{fname}', '{lname}', '{password}', '{phone}')")
			check_register = (f"select Email from Owners where Email = '{email}';")
			try:
				cursor.execute(register_new)
				cnx.commit()
				cursor.execute(check_register)
				reg_valid = 0
				for review in cursor:
					reg_valid += 1
				if reg_valid != 0:
					messagebox.showinfo("showinfo", "Your submission was successful")
					controller.show_frame(OwnerHome)
				else:
					messagebox.showwarning("showwarning", "Your submission was unsuccessful. Please check your information.")
			except:
				messagebox.showwarning("showwarning", "Your submission was unsuccessful. Please check your information.")		

		#register button
		register_button = tk.Button(self, text = "Register", highlightbackground = "#00A7E1",
			command = lambda : register_customer(email_entry.get(), fname_entry.get(), lname_entry.get(), password_entry.get(), phone_number_entry.get()))
		register_button.grid(row = 6, column = 1)


#Registration Option Page
class RegistrationType(tk.Frame):
	def __init__(self, parent, controller):
		tk.Frame.__init__(self, parent)
		register_question = tk.Label(self, text = "Are you an owner or customer?", font = Header_Font2)
		register_question.grid(row = 0, column = 1, padx = 10, pady = 10)
		register_customer = tk.Button(self, text = "Register New Customer", command = lambda : controller.show_frame(RegisterCustomer))
		register_customer.grid(column = 1, row = 5, padx = 10, pady = 10)
		register_owner = tk.Button(self, text = "Register New Owner", command = lambda : controller.show_frame(RegisterOwner))
		register_owner.grid(column = 1, row = 6, padx = 10, pady = 10)

#Driver
app = ReservationService()
app.mainloop()
