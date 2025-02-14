"""
Module: Hotel Reservation System
This module provides classes and methods to manage hotels, customers, and reservations.
It includes persistent storage using JSON files and provides functionality to create,
delete, and manage reservations.
"""

import json
import os
import uuid
import unittest

# File paths for storing data persistently
HOTELS_FILE = "hotels.json"
CUSTOMERS_FILE = "customers.json"
RESERVATIONS_FILE = "reservations.json"


# Function to load data from a JSON file
def load_data(file_path):
    """Loads data from a JSON file, handling errors gracefully."""
    if os.path.exists(file_path):
        try:
            with open(file_path, 'r', encoding='utf-8') as file:
                return json.load(file)
        except (json.JSONDecodeError, FileNotFoundError):
            print(f"Error reading {file_path}. Initializing empty data.")
    return {}


# Function to save data to a JSON file
def save_data(file_path, data):
    """Saves data to a JSON file."""
    with open(file_path, 'w', encoding='utf-8') as file:
        json.dump(data, file, indent=4)


class Hotel:
    """Represents a hotel with rooms and location."""

    def __init__(self, name, location, rooms):
        """Initializes a hotel with a name, location, and number of rooms."""
        self.hotel_id = str(uuid.uuid4())
        self.name = name
        self.location = location
        self.rooms = rooms
        self.available_rooms = rooms

    def to_dict(self):
        """Converts hotel object to dictionary for JSON storage."""
        return {
            "hotel_id": self.hotel_id,
            "name": self.name,
            "location": self.location,
            "rooms": self.rooms,
            "available_rooms": self.available_rooms
        }

    @staticmethod
    def create_hotel(name, location, rooms):
        """Creates and stores a new hotel."""
        hotels = load_data(HOTELS_FILE)
        new_hotel = Hotel(name, location, rooms)
        hotels[new_hotel.hotel_id] = new_hotel.to_dict()
        save_data(HOTELS_FILE, hotels)
        return new_hotel

    @staticmethod
    def delete_hotel(hotel_id):
        """Deletes a hotel by its ID."""
        hotels = load_data(HOTELS_FILE)
        if hotel_id in hotels:
            del hotels[hotel_id]
            save_data(HOTELS_FILE, hotels)
            return True
        return False

    @staticmethod
    def display_hotels():
        """Returns all stored hotels."""
        return load_data(HOTELS_FILE)


class Customer:
    """Represents a customer with name and email."""

    def __init__(self, name, email):
        """Initializes a customer with a name and email."""
        self.customer_id = str(uuid.uuid4())
        self.name = name
        self.email = email

    def to_dict(self):
        """Converts customer object to dictionary for JSON storage."""
        return {
            "customer_id": self.customer_id,
            "name": self.name,
            "email": self.email
        }

    @staticmethod
    def create_customer(name, email):
        """Creates and stores a new customer."""
        customers = load_data(CUSTOMERS_FILE)
        new_customer = Customer(name, email)
        customers[new_customer.customer_id] = new_customer.to_dict()
        save_data(CUSTOMERS_FILE, customers)
        return new_customer

    @staticmethod
    def delete_customer(customer_id):
        """Deletes a customer by their ID."""
        customers = load_data(CUSTOMERS_FILE)
        if customer_id in customers:
            del customers[customer_id]
            save_data(CUSTOMERS_FILE, customers)
            return True
        return False

    @staticmethod
    def display_customers():
        """Returns all stored customers."""
        return load_data(CUSTOMERS_FILE)


class Reservation:
    """Manages reservations for hotel rooms."""

    def __init__(self, customer_id, hotel_id):
        """Initializes a reservation with a customer ID and hotel ID."""
        self.reservation_id = str(uuid.uuid4())
        self.customer_id = customer_id
        self.hotel_id = hotel_id

    def to_dict(self):
        """Converts reservation object to dictionary for JSON storage."""
        return {
            "reservation_id": self.reservation_id,
            "customer_id": self.customer_id,
            "hotel_id": self.hotel_id
        }

    @staticmethod
    def create_reservation(customer_id, hotel_id):
        """Creates and stores a new reservation."""
        reservations = load_data(RESERVATIONS_FILE)
        hotels = load_data(HOTELS_FILE)

        if hotel_id not in hotels or hotels[hotel_id]["available_rooms"] == 0:
            print("Error: Hotel not found or no available rooms.")
            return None

        hotels[hotel_id]["available_rooms"] -= 1
        save_data(HOTELS_FILE, hotels)

        new_reservation = Reservation(customer_id, hotel_id)
        reservations[new_reservation.reservation_id] = new_reservation.to_dict()
        save_data(RESERVATIONS_FILE, reservations)
        return new_reservation

    @staticmethod
    def cancel_reservation(reservation_id):
        """Cancels an existing reservation."""
        reservations = load_data(RESERVATIONS_FILE)
        hotels = load_data(HOTELS_FILE)

        if reservation_id in reservations:
            hotel_id = reservations[reservation_id]["hotel_id"]
            if hotel_id in hotels:
                hotels[hotel_id]["available_rooms"] += 1
                save_data(HOTELS_FILE, hotels)

            del reservations[reservation_id]
            save_data(RESERVATIONS_FILE, reservations)
            return True
        return False


# Unit Tests to verify the functionality
class TestHotelReservationSystem(unittest.TestCase):
    def test_create_hotel(self):
        hotel = Hotel.create_hotel("Test Hotel", "NYC", 10)
        self.assertIn(hotel.hotel_id, load_data(HOTELS_FILE))

    def test_delete_hotel(self):
        hotel = Hotel.create_hotel("Delete Hotel", "LA", 5)
        self.assertTrue(Hotel.delete_hotel(hotel.hotel_id))

    def test_create_customer(self):
        customer = Customer.create_customer("John Doe", "john@example.com")
        self.assertIn(customer.customer_id, load_data(CUSTOMERS_FILE))

    def test_delete_customer(self):
        customer = Customer.create_customer("Jane Doe", "jane@example.com")
        self.assertTrue(Customer.delete_customer(customer.customer_id))

    def test_create_reservation(self):
        hotel = Hotel.create_hotel("Reserve Hotel", "Chicago", 3)
        customer = Customer.create_customer("Alice", "alice@example.com")
        reservation = Reservation.create_reservation(customer.customer_id, hotel.hotel_id)
        self.assertIsNotNone(reservation)
        self.assertIn(reservation.reservation_id, load_data(RESERVATIONS_FILE))

    def test_cancel_reservation(self):
        hotel = Hotel.create_hotel("Cancel Hotel", "Miami", 2)
        customer = Customer.create_customer("Bob", "bob@example.com")
        reservation = Reservation.create_reservation(customer.customer_id, hotel.hotel_id)
        self.assertTrue(Reservation.cancel_reservation(reservation.reservation_id))


if __name__ == "__main__":
    unittest.main()
