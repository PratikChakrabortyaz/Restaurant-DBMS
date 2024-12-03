# French Restaurant DBMS

An efficient database management system for a French restaurant, designed to streamline customer management, order processing, menu handling, and reservations. This project includes a user-friendly GUI built with Tkinter, allowing customers and employees to navigate seamlessly through various functionalities and make informed financial decisions.

## Problem Statement
The French Restaurant DBMS is developed to enhance the workflow within a restaurant ecosystem. It handles diverse datasets ranging from customer information to reservations, orders, billing, and employee insights. The system ensures smooth operations for both customers and staff through an interactive interface.

---

## Objectives
1. **Customer Management:**  
   - Customers can register using their name and phone number.  
   - Details are stored in the `customer` table.  

2. **Table Booking:**  
   - Customers can book available tables for a specified duration.  
   - Booking details are also stored in the `customer` table.  

3. **Order from Menu:**  
   - A menu displays food items with their prices.  
   - Customers can place orders by selecting items and specifying quantities.  
   - Order details are stored in the `orders` table.  

4. **Ingredients Stock Management:**  
   - Items ordered reduce the corresponding ingredient quantities in stock.  

5. **Pay Bill:**  
   - Bills are calculated based on the total price of ordered items.  
   - Billing details are stored in the `bill` table.  

6. **Discount System:**  
   - Discounts are applied based on the total amount spent by the customer.  

7. **Ratings and Reviews:**  
   - Customers can provide a rating and write a review about their restaurant experience.  
   - Feedback details are stored in the `rating` table.  

8. **Restaurant Interface for Employees:**  
   - Employees can:  
     - View the most ordered item.  
     - Check total revenue.  
     - Access customer details, including table bookings and orders.  

---

## Features
- **Customer Interaction:** Easy registration, table booking, and order placement via a Tkinter GUI.  
- **Inventory Management:** Automatic ingredient stock updates based on orders.  
- **Financial Insights:** Employee interface to monitor revenue and popular items.  
- **Feedback Mechanism:** Customers can provide ratings and reviews for improved service quality.  

---

## Tools and Technologies Used
- **Programming Language:** Python  
- **GUI Framework:** Tkinter  
- **Database:** Oracle

---

## Installation
1. Clone the repository:
   ```bash
   git clone https://github.com/PratikChakrabortyaz/Restaurant-DBMS.git
