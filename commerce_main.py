#start of announcments :D
#HIT 1000 LINES OF CODEEE LETS GOO :D
#end of announcments



#tasks
# addd 3 account types btw, vendor, admin, customer

# Allow admin users to add, update, or delete products. and give a reason opn why they rtemoved ur acc or banned ur ass
#end of tasks
# Vender ACCOUNT: "To sell products, create a vendor account. You'll get access to selling tools, trending products, " "and advertising features." make sure it shows other users too btw too make it advanced
# chnage how it uses product id to the name of the product instead or both
#end of tasks

# start of imports
import smtplib
import random
import os
import json
import time
from datetime import datetime, date
import mysql.connector
import msvcrt
from difflib import get_close_matches
import requests
#end of imports

sender_email = 'nagamanojp@gmail.com'
sender_password = 'nwwneuyfititykck'
positive_responses = {'y', 'yes', 'ye', 'why not', 'sure', 'certainly', 'for sure', 'of course', 'obviously', 'ok', 'fuck yeah'}
negative_responses = {'no', 'n', 'nah', 'na', 'nope', 'not feeling it', 'obviously not', 'hell no'}
ur_account = None
def custom_getpass(prompt="Password: "):
    print(prompt, end='', flush=True)
    password = ""
    while True:
        char = msvcrt.getch()
        if char == b'\r':  # Enter key
            break
        elif char == b'\x08':  # Backspace key
            if len(password) > 0:
                password = password[:-1]
                print('\b \b', end='', flush=True)
        else:
            password += char.decode('utf-8')
            print('*', end='', flush=True)
    print()
    return password
discounts = {
                        "fweah": 0.10,  # 10% off
                        "i am music": 0.40,  # 40% off
                        "carti": 0.15,  # 15% off
                        "schyeah": 0.5  # 50% off
                    }
API_KEY = '9eedc1631ae7d7847e3e3592'
BASE_URL = 'https://v6.exchangerate-api.com/v6'
def get_db_connection():
    return mysql.connector.connect(
        host="localhost",
        user="root",
        password="Sairam@09",
        database="fweah_ecommerce"
    )
def load_accounts():
    try:
        connection = get_db_connection()
        cursor = connection.cursor(dictionary=True)
        cursor.execute("SELECT * FROM accounts")
        accounts = cursor.fetchall()
        cursor.execute("SELECT * FROM transactions")
        transactions = cursor.fetchall()
  
        cursor.close()
        connection.close()

        accounts_dict = {}
        for account in accounts:
            account_name = account['account_name']
            
            account['budget'] = float(account.get('budget', 0))
            account['send_email'] = bool(account.get('send_email', False))
            account['is_restricted'] = bool(account.get('is_restricted', False))
            
            accounts_dict[account_name] = account

        return accounts_dict
    except mysql.connector.Error as err:
        print(f"Error: {err}")
        return {}

def save_account(account_details):
    try:
        connection = get_db_connection()
        cursor = connection.cursor()

        cursor.execute("""
            REPLACE INTO accounts (
                account_name, password, balance, first_name, middle_name, last_name, dob, 
                address_line1, address_line2, city, state, zip_code, phone_number, email, 
                country_of_residence, account_type, budget, budget_password, send_email, is_restricted
            )
            VALUES (
                %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s
            )
        """, (
            account_details["username"],
            account_details["password"],
            str(account_details["balance"]),
            account_details["first_name"],
            account_details["middle_name"],
            account_details["last_name"],
            account_details["dob"],
            account_details["address_line1"],
            account_details["address_line2"],
            account_details["city"],
            account_details["state"],
            account_details["zip_code"],
            account_details["phone_number"],
            account_details["email"],
            account_details["country_of_residence"],
            account_details["account_type"],
            str(account_details["budget"]),
            account_details["send_email"],
            account_details["is_restricted"]
        ))

        connection.commit()
        print("Account successfully created!")
        cursor.close()
        connection.close()
    except mysql.connector.Error as err:
        print(f"Error: {err}")




def wishlist(name):
    print("--------List of Our Products--------")
    time.sleep(0.5)
    for product in products:
        print(f"ID: {product['id']} | Name: {product['name']} | Price: ${product['price']:.2f}")
    
    syss = input("Would you like to add any products to your wishlist? ").lower()
    print("Please keep in mind the product id(s) of the product you want to wishlist.")
    if syss in positive_responses:
        add_to_wishlist(name)
    elif syss in negative_responses:
        time.sleep(0.79)
        print("Alright have a good day :D")
        time.sleep(0.79)
def save_wishlist(wishlist):
    with open("freak.json", "w") as file:
        json.dump(wishlist, file, indent=4)
def load_json():
    try:
        with open("freak.json", "r") as file:
            return json.load(file)
    except (FileNotFoundError, json.JSONDecodeError):
        return {}
def add_to_wishlist(name):
    wishlist = load_json()
    if name not in wishlist:
        wishlist[name] = []
    his = input("Do you have multiple name's or just a singular one (singular, multiple)?").lower()
    if his == "singular":
        suf = int(input("What is the name of the product you want to wishlist? ")).lower()
        if suf in wishlist[name]:
            print("Item is already in your wishlist!")
            return
        else:
            wishlist[name].append(suf)
            save_wishlist(wishlist)
            print("Item added to your wishlist successfully!")
    elif his == "multiple":
        sus = int(input("How many names do you wanna add? "))
        item_ids = []
        for i in range(sus):
                item_ids = int(input("Enter a product name: ")).lower()
                wishlist[name].append(item_ids)
                save_wishlist(wishlist)
        print("Items added to your wishlist successfully!")


def view_wishlist(name):
    wishlist = load_json()
    if name in wishlist and wishlist[name]:
        print("--------Your Wishlist--------")
        for item in wishlist[name]:
            product = next((p for p in products if p['id'] == item), None)
            if product:
                print(f"ID: {product['id']} | Name: {product['name']} | Price: ${product['price']:.2f}")
    else:
        print("Your wishlist is empty.")

def remove_from_wishlist(name):
    wishlist = load_json()
    if name in wishlist and wishlist[name]:
        print("--------Your Wishlist--------")
        for item in wishlist[name]:
            product = next((p for p in products if p['name'] == item), None)
            if product:
                print(f"ID: {product['id']} | Name: {product['name']} | Price: ${product['price']:.2f}")
        
        item_id = int(input("Enter the name of the product you want to remove: ")).lower()
        if item_id in wishlist[name]:
            wishlist[name].remove(item_id)
            save_wishlist(wishlist)
            print("Item removed from your wishlist successfully!")
        else:
            print("Item not found in your wishlist.")
    else:
        print("Your wishlist is empty.")



def create_acc(accounts):
        print("Please provide the following information to create an account:")
        first_name = input("First name: ")
        time.sleep(0.43)
        middle_name = input("Middle name (optional): ")
        time.sleep(0.43)
        last_name = input("Last name: ")
        time.sleep(0.43)
        dob = input("Date of birth (YYYY-MM-DD): ")
        time.sleep(0.43)
        address_line1 = input("Address line 1: ")
        time.sleep(0.43)
        address_line2 = input("Address line 2 (Apartment #, Unit #, etc., optional): ")
        time.sleep(0.43)
        city = input("City: ")
        time.sleep(0.43)
        state = input("State: ")
        time.sleep(0.43)
        zip_code = input("ZIP code: ")
        time.sleep(0.43)
        phone_number = input("Phone number (XXX-XXX-XXXX): ")
        time.sleep(0.43)
        email = input("Email address: ")
        time.sleep(0.43)

        re_enter_email = input("Re-enter email address: ")
        while email != re_enter_email:
            print("Emails do not match. Please re-enter the correct email address.")
            time.sleep(0.43)
            re_enter_email = input("Re-enter email address: ")
            time.sleep(0.43)

        country_of_residence = input("Country: ")
        time.sleep(0.43)

        username = input("What would you like the username of the account to be: ")
        time.sleep(0.43)
        while username == 'sigma':
            username = input("Sorry, that username is already in use, please choose another one: ")
            time.sleep(0.43)

        password = input("What would you like the password to be (needs to have at least 8 characters): ")
        time.sleep(0.43)
        while len(password) < 8:
            print("Your password was not over 8 characters. Please enter a password that is over 8 characters.")
            time.sleep(0.43)
            password = input("What would you like the password to be (needs to have at least 8 characters): ")
            time.sleep(0.43)

        account_types = ['customer', 'vendor', 'admin']
        account_type = input("What type of account would you like? Customer, Vendor, or Admin? ").lower()
        while account_type not in account_types:
            print("Looks like you haven't inputted a valid account type. Please try again.")
            account_type = input("What type of account would you like? Customer, Vendor, or Admin? ").lower()
            if account_type == 'customer' or 'vendor':
                suck = round(float(input("How much balance do you have? ")), 2)
        typed = input("What is the currency you use? ")



        accounts[username] = {
            "first_name": first_name,
            "middle_name": middle_name,
            "last_name": last_name,
            "dob": dob,
            "address_line1": address_line1,
            "address_line2": address_line2,
            "city": city,
            "state": state,
            "zip_code": zip_code,
            "phone_number": phone_number,
            "email": email,
            "country_of_residence": country_of_residence,
            "account_name": username,
            "password": password,
            "account_type": account_type,
            "balance": suck,  # Default balance
            "budget": 0.0, 
            "send_email": False,  # Default value
            "is_restricted": False,  # Default restriction status
            "currency": typed
        }
        save_account(accounts)

products = [
    {"id": 1, "name": "laptop", "price": 1000.00},
    {"id": 2, "name": "smartphone", "price": 699.99},
    {"id": 3, "name": "headphones", "price": 199.99},
    {"id": 4, "name": "monitor", "price": 299.99}
]
cart = []


def submit_review(user_id, product_id, rating, review):
    """Inserts a user review into the database."""
    connection = get_db_connection()
    cursor = connection.cursor()

    # Insert the review into the database
    try:
        cursor.execute(
            "INSERT INTO reviews (user_id, product_id, rating, review) VALUES (%s, %s, %s, %s)",
            (user_id, product_id, rating, review)
        )
        connection.commit()
        print("Processing your review...")
        time.sleep(1.5)
        print("Thank you for your feedback! 🎉")
    except mysql.connector.Error as err:
        print(f"Error: {err}")
    finally:
        cursor.close()
        connection.close()

# Example: Allowing the user to submit a review
def user_submit_review(user_id):
    """Prompts user to input a product review."""
    print("Rate and review a product: ")
    product_id = input("Enter the product ID: ")
    
    # Validate rating input
    while True:
        try:
            rating = int(input("Rate the product (1-5): "))
            if 1 <= rating <= 5:
                break
            else:
                print("Invalid rating. Please enter a number between 1 and 5.")
        except ValueError:
            print("Invalid input. Please enter a valid number.")

    review = input("Write your review: ")

    # Submit review to the database
    submit_review(user_id, product_id, rating, review)

def show_reviews(product_id):
    connection = get_db_connection()
    cursor = connection.cursor(dictionary=True)

    cursor.execute("SELECT account_name, rating, review, review_date FROM reviews WHERE product_id = %s", (product_id,))
    reviews = cursor.fetchall()

    if not reviews:
        print("No reviews found for this product.")
    else:
        print(f"Reviews for Product ID {product_id}:")
        for review in reviews:
            print(f"- User: {review['user_id']}")
            print(f"  Rating: {review['rating']}/5")
            print(f"  Review: {review['review']}")
            print(f"  Date: {review['review_date']}\n")
    while 1==1:
        ff = input("Would like to see another one? ")
        if ff in positive_responses:
            fweah = int(input("Enter the product ID to see its review: "))
            cursor.execute("SELECT account_name, rating, review, review_date FROM reviews WHERE product_id = %s", (fweah,))
            reviews = cursor.fetchall()
            if not reviews:
                print("No reviews found for this product.")
            else:
                print(f"Reviews for Product ID {product_id}:")
                for review in reviews:
                    print(f"- User: {review['account_name']}")
                    print(f"  Rating: {review['rating']}/5")
                    print(f"  Review: {review['review']}")
                    print(f"  Date: {review['review_date']}\n")
        elif ff in negative_responses:
            print("Alright have a good day :D ") 
            break
        else:
            print("Invalid option, sorry. ")
            break

    cursor.close()
    connection.close()


def list_product(account_name):
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)

    cursor.execute("SELECT id, name, price, vendor_name FROM products")
    products = cursor.fetchall()

    print("--------List of Products--------")
    time.sleep(0.5)
    for product in products:
        vendor = product['vendor_name'] if product['vendor_name'] else "MANOJ :D"
        print(f"ID: {product['id']} | Name: {product['name']} | Price: ${product['price']:.2f} | Vendor: {vendor}")

    fweah = input("Would you like to buy any products, see their reviews, or add them to your wishlist (reviews, buy, wishlist)? ").lower()
    if fweah == "reviews":
        time.sleep(0.79)
        product_id = int(input("Enter the product ID to see its reviews: "))
        time.sleep(0.79)
        show_reviews(product_id)
    elif fweah == "wishlist":
        add_to_wishlist(account_name)
    elif fweah == "buy":
        time.sleep(0.79)
        add_to_cart()
    else:
        print("Sorry, you have input an invalid option.")

    cursor.close()
    conn.close()


def advanced_search(category, min_price, max_price, rating):
                            connection = get_db_connection()
                            cursor = connection.cursor(dictionary=True)

                            query = """
                            SELECT id, name, category, price, rating 
                            FROM products 
                            WHERE category = %s AND price BETWEEN %s AND %s AND rating >= %s
                            """
                            cursor.execute(query, (category, min_price, max_price, rating))
                            results = cursor.fetchall()

                            cursor.close()
                            connection.close()
                            return results

def add_to_cart(account_name):
    while True:
        try:
            product_name = int(input("Enter the Product name to add to cart: "))
            if product_name not in products:
                print("Sorry we don't have this product doesn't exist. ")
                swamp = input("Do you want to search for another item? ").lower()
                if swamp in positive_responses:
                    izzo = input("Do you want an category type search or just search for a product (category, search)? ").lower()
                    fin = ["category", "search"]
                    flip = 0
                    while izzo not in fin:
                        flip+ 1
                        izzo = input("You have inputed a invalid option, please pick category or search. ")
                        if flip >= 6:
                            print("Sorry you have inputed an invalid option too many times. ")
                            return
                    if izzo == 'category':
                        results = advanced_search(category, min_price, max_price, rating)

                        print("\nSearch Results:")
                        if results:
                            for product in results:
                                print(f"- {product['name']} (${product['price']}, {product['rating']} stars)")
                        else:
                            print("No products found matching your criteria.")
                        print("Advanced Product Search:")
                        category = input("Enter category: ")
                        min_price = float(input("Enter minimum price: "))
                        max_price = float(input("Enter maximum price: "))
                        rating = float(input("Enter minimum rating (1-5): "))
                        results = advanced_search(category, min_price, max_price, rating)  # Custom function
                        print("Search Results:")
                        for product in results:
                            print(f"- {product['name']} (${product['price']}, {product['rating']} stars)")
                    elif izzo in 'search':
                        time.sleep(0.79)
                        search_product()


                elif swamp in negative_responses:
                    time.sleep(0.79)
                    print("Alright have a great day :D")
                    time.sleep(0.79)
                    return
                else:
                    print("Sorry have a great day :D ")
                    time.sleep(0.79)

            product = next((p for p in products if p['name'] == product_name), None)

            if product:
                connection = get_db_connection()
                cursor = connection.cursor()

                # Check if the product already exists in the cart
                cursor.execute("SELECT quantity FROM cart WHERE account_name = %s AND product_name = %s", 
                               (account_name, product_name))
                existing_item = cursor.fetchone()

                if existing_item:
                    # Update quantity if already in cart
                    new_quantity = existing_item["quantity"] + 1

                    cursor.execute("UPDATE cart SET quantity = %s WHERE account_name = %s AND product_name = %s", 
                                   (new_quantity, account_name, product_name))
                else:
                    # Insert new product into cart
                    cursor.execute("INSERT INTO cart (account_name, product_id, product_name, price, quantity) VALUES (%s, %s, %s, %s, %s)", 
                                   (account_name, product['id'], product['name'], product['price'], 1))
                
                connection.commit()
                print(f"Added {product['name']} to the cart.")
                cursor.close()
                connection.close()
            else:
                print("Invalid Product ID. Please try again.")
        except ValueError:
            print("Invalid input. Please enter a valid Product ID.")

def check_cart(account_name):
    connection = get_db_connection()
    cursor = connection.cursor(dictionary=True)

    cursor.execute("SELECT product_name, price, quantity FROM cart WHERE account_name = %s", (account_name,))
    cart_items = cursor.fetchall()

    cursor.close()
    connection.close()

    print("--------Your Cart--------")
    if not cart_items:
        print("Your cart is empty.")
    else:
        total = 0
        for item in cart_items:
            print(f"Name: {item['product_name']} | Price: ${item['price']:.2f} | Quantity: {item['quantity']}")
            total += item['price'] * item['quantity']
        print(f"Total: ${total:.2f}")

discount_codes = {
    "fweah": 0.10,  # 10% off
    "i am music": 5.00,      # $5 off
    "carti": 0.15,    # 15% off
    "schyeah": 0.5

}


def send_gift_item(sender_name, recipient_address, product_id, products):
    selected_product = next((p for p in products if p["id"] == product_id), None)
    if selected_product:
        print(f"\n{sender_name} is sending '{selected_product['name']}' "
              f"(worth ${selected_product['price']:.2f}) to {recipient_address}!")
    else:
        print("Product not found.")

def log_recently_viewed(account_name, product_id):
    conn = mysql.connector.connect(
        host="localhost",
        user="root",
        password="Sairam@09",
        database="fweah_ecommerce"
    )
    cursor = conn.cursor()

    query = """
    INSERT INTO recently_viewed (account_name, product_id, viewed_at)
    VALUES (%s, %s, %s)
    ON DUPLICATE KEY UPDATE viewed_at = VALUES(viewed_at)
    """
    cursor.execute(query, (account_name, product_id, datetime.now()))
    conn.commit()
    cursor.close()
    conn.close()


def get_recently_viewed(account_name):
    conn = mysql.connector.connect(
        host="localhost",
        user="root",
        password="Sairam@09",
        database="fweah_ecommerce"
    )
    cursor = conn.cursor()

    query = """
    SELECT p.name, p.price
    FROM recently_viewed rv
    JOIN products p ON rv.product_id = p.product_id
    WHERE rv.account_name = %s
    ORDER BY rv.viewed_at DESC
    LIMIT 10
    """
    cursor.execute(query, (account_name,))
    products = cursor.fetchall()
    cursor.close()
    conn.close()
    return products




def spin_the_wheel(account_name):
    conn = mysql.connector.connect(
        host="localhost",
        user="root",
        password="Sairam@09",
        database="fweah_ecommerce"
    )
    cursor = conn.cursor()

    # Check if the user has already spun today
    query = "SELECT last_spin_date FROM daily_spin WHERE account_name = %s"
    cursor.execute(query, (account_name,))
    result = cursor.fetchone()
    today = date.today()
    if result and result[0] == today:
        print("You already spun the wheel today! Come back tomorrow! 🎯")
        return
    else:
        print("---------Welcome to SPIN THE WHEEL!!!---------")
        print("You have a daily spin available ")
        rewards = [
            "5% Off Coupon",
            "10% Off Coupon",
            "50 Bonus Loyalty Points",
            "Free Shipping",
            "Mystery Gift",
            "15% Off Coupon",
            "100 Bonus Loyalty Points",
            "No Prize, Try Again Tomorrow"
        ]
        reward = random.choice(rewards)

        print(f"🎉 Congratulations {account_name}! You won: {reward} 🎉")

        if result:
            # Update existing spin record
            update_query = "UPDATE daily_spin SET last_spin_date = %s, reward = %s WHERE account_name = %s"
            cursor.execute(update_query, (today, reward, account_name))
        else:
            # Insert new spin record
            insert_query = "INSERT INTO daily_spin (account_name, last_spin_date, reward) VALUES (%s, %s, %s)"
            cursor.execute(insert_query, (account_name, today, reward))

        conn.commit()

    cursor.close()
    conn.close()

def apply_discount(total_cost, discount_code):
    """Applies a discount if a valid discount code is entered."""
    if discount_code in discount_codes:
        discount = discount_codes[discount_code]

        if isinstance(discount, float):  # Percentage discount
            discount_amount = round(total_cost * discount, 2)
        else:  # Fixed amount discount
            discount_amount = discount

        final_price = max(0, round(total_cost - discount_amount, 2))  # Prevent negative prices
        print(f"✅ Discount Applied: -${discount_amount:.2f}")
        return final_price
    else:
        print("❌ Invalid discount code.")
        return total_cost  # No discount applied

def checkout(account_name):
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)

    cursor.execute("SELECT loyalty_points FROM loyalty WHERE account_name = %s", (account_name,))
    result = cursor.fetchone()
    points = result['loyalty_points'] if result else 0

    # Retrieve cart items
    cursor.execute("SELECT product_id, product_name, price, quantity FROM cart WHERE account_name = %s", (account_name,))
    cart_items = cursor.fetchall()

    if not cart_items:
        print("Your cart is empty. Add some products first.")
        return

    # Calculate total cost
    total_cost = sum(item['price'] * item['quantity'] for item in cart_items)
    print(f"\nTotal cost: ${total_cost:.2f}")

    if points > 0:
        use_points = input(f"You have {points} loyalty points. Would you like to redeem them for a discount? (yes/no) ").strip().lower()
        if use_points in positive_responses:
            discounty = round(points * 0.10, 2)
            total_cost = max(0, total_cost - discounty)

            cursor.execute("""
                UPDATE loyalty 
                SET loyalty_points = 0 
                WHERE account_name = %s
            """, (account_name,))
            print(f"You used {points} points for a ${discounty:.2f} discount.")
            update_loyalty(account_name, 0)  # Re-evaluate tier

    import time
    time.sleep(0.79)
    discount_code = input("Enter a discount code (or press Enter to skip): ").upper()
    total_cost = apply_discount(total_cost, discount_code)

    # Check user balance
    cursor.execute("SELECT balance FROM accounts WHERE account_name = %s", (account_name,))
    account = cursor.fetchone()

    if account and account['balance'] >= total_cost:
        new_balance = round(account['balance'] - total_cost, 2)
        cursor.execute("UPDATE accounts SET balance = %s WHERE account_name = %s", (new_balance, account_name))

        # 🛒 Insert each purchased item into the orders table
        for item in cart_items:
            cursor.execute("""
                INSERT INTO orders (product_id, customer_name, quantity)
                VALUES (%s, %s, %s)
            """, (item['product_id'], account_name, item['quantity']))

        # 🛒 Clear the user's cart
        cursor.execute("DELETE FROM cart WHERE account_name = %s", (account_name,))
        
        conn.commit()
        print("\nProcessing payment...")
        time.sleep(1.5)
        print("✅ Payment successful! Thank you for your purchase.")
    else:
        print("❌ Insufficient balance.")

    cursor.close()
    conn.close()



def sell_product(vendor_name):
    conn = mysql.connector.connect(
        host="localhost",
        user="root",
        password="Sairam@09",
        database="fweah_ecommerce"
    )
    randome = random.randint(1, 100000000)
    cursor = conn.cursor()
    fun = int(input("How many products would you like to list? "))
    while fun > 0:
        print("You have inputed a product less than 0")
        fun = int(input("How many products would you like to list? "))
    for i in range(fun):
        product_name = input("Enter product name: ").strip()
        product_id = print(f"Your product id is {randome}")
        print(product_id)
        description = input("Enter product description: ").strip()
        price = float(input("Enter product price ($): "))
        stock = int(input("Enter how many units are available: "))
        category = input("Enter product category: ").strip()
        created_at = datetime.now().strftime('%Y-%m-%d %H:%M:%S')  # Format: 'YYYY-MM-DD HH:MM:SS'

        query = """
        INSERT INTO products (id, name, description, price, stock, category, vendor_name, created_at)
        VALUES (%s, %s, %s, %s, %s, %s)
        """
        cursor.execute(query, (randome, product_name, description, price, stock, category, vendor_name, created_at))
        conn.commit()

        print(f"\n✅ Product '{product_name}' listed successfully!")

    cursor.close()
    conn.close()


def view_my_products(vendor_name):
    conn = mysql.connector.connect(
        host="localhost",
        user="root",
        password="Sairam@09",
        database="fweah_ecommerce"
    )
    cursor = conn.cursor()

    query = """
    SELECT id, name, description, price, stock, category,
    FROM products
    WHERE vendor_name = %s
    """
    cursor.execute(query, (vendor_name,))
    products = cursor.fetchall()
    cursor.close()
    conn.close()

    if not products:
        print("No products listed yet.")
        sus = input("Would you like to sell a product? ").lower()
        if sus in positive_responses:
            sell_product(vendor_name)
        elif sus in negative_responses:
            print("Alright have a great day :D ")  
        return

    print("\n📋 Your Listed Products:")

    # Print a nice header
    print(f"{'ID':<5}{'Name':<25}{'Category':<15}{'Price':<10}{'Stock':<10}{'Created At'}")
    print("-" * 75)  # Just a separator line for readability

    # Loop through each product and display it
    for product in products:
        id, name, description, price, stock, category, created_at = product
        print(f"{id:<5}{name:<25}{category:<15}${price:<10}{stock:<10}{created_at}")
    
    print("\n--- End of List ---")

def respond_to_reviews(vendor_name):
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)

    # Fetch all reviews for this vendor's products
    cursor.execute("""
        SELECT r.id, r.product_id, r.review_text, r.response, p.name AS product_name
        FROM reviews r
        JOIN products p ON r.product_id = p.id
        WHERE p.vendor_name = %s
    """, (vendor_name,))
    reviews = cursor.fetchall()

    if not reviews:
        print("\nYou have no reviews to respond to yet!")
        cursor.close()
        conn.close()
        return

    print("\n--- Customer Reviews for Your Products ---")
    for review in reviews:
        print(f"\nReview ID: {review['id']}")
        print(f"Product: {review['product_name']}")
        print(f"Customer Review: {review['review_text']}")
        print(f"Your Response: {review['response'] if review['response'] else 'No response yet.'}")

    try:
        review_id = int(input("\nEnter the Review ID you want to respond to (or 0 to cancel): "))
    except ValueError:
        print("Invalid input. Returning to menu.")
        cursor.close()
        conn.close()
        return

    if review_id == 0:
        print("Returning to menu.")
        cursor.close()
        conn.close()
        return

    # Make sure the review belongs to one of their products
    matching_review = next((rev for rev in reviews if rev['id'] == review_id), None)
    if not matching_review:
        print("Review not found or doesn't belong to your products.")
        cursor.close()
        conn.close()
        return

    response = input("Write your response to the customer: ").strip()

    # Update the review with vendor's response
    cursor.execute("""
        UPDATE reviews
        SET response = %s
        WHERE id = %s
    """, (response, review_id))

    conn.commit()
    print("\n✅ Your response has been posted!")

    cursor.close()
    conn.close()


def update_my_product(vendor_name):
    conn = mysql.connector.connect(
        host="localhost",
        user="root",
        password="Sairam@09",
        database="fweah_ecommerce"
    )
    cursor = conn.cursor()
    query = """
    SELECT name, description, price, category
    FROM products
    WHERE vendor_name = %s
    """
    cursor.execute(query, (vendor_name,))
    products = cursor.fetchall()
    if not products:
        print("You have no products listed.")
        return
    print("Here are your products:")
    for product in products:
        print(f"ID: {product[0]}, Name: {product[1]}")

    sus = input("Which product would you like to update? ").strip()
    product_found = None
    dang = 0

    # Find the product by name
    while product_found is None and dang <= 5:
        for product in products:
            if sus.lower() == product[1].lower():  # Compare product name, case insensitive
                product_found = product
                break

        if product_found is None:
            if dang >= 5:
                god = input(f"It seems like you have entered the product name incorrectly {dang} times. Would you like to try again or exit? ").lower()
                if god == "exit":
                    print("Sorry we couldn't find your product, have a great day :D")
                    return
                else:
                    sus = input("Please re-enter the product name: ").strip()
                    dang += 1
            else:
                sus = input("Sorry, we couldn't find your product. Please re-enter the name: ").strip()
                dang += 1

    # If product is found, proceed with updating
    if product_found:
        print(f"You selected: {product_found[1]}")
        what = input("What would you like to update about it? (Name, Description, Price, Stock, Category): ").lower()

        # Fields that cannot be updated
        listy = ["id", "created at"]
        while what in listy:
            print(f"Sorry, you can't change that. Please update something else or type 'exit' to quit.")
            what = input("What would you like to update about it? ").lower()

            if what == "exit":
                print("Alright, have a great day :D")
                return

        # Handle product updates
        if what == "name":
            new_name = input("Enter the new product name: ")
            query = "UPDATE products SET name = %s WHERE id = %s"
            cursor.execute(query, (new_name, product_found[0]))
        elif what == "description":
            new_description = input("Enter the new product description: ")
            query = "UPDATE products SET description = %s WHERE id = %s"
            cursor.execute(query, (new_description, product_found[0]))
        elif what == "price":
            new_price = float(input("Enter the new product price: "))
            query = "UPDATE products SET price = %s WHERE id = %s"
            cursor.execute(query, (new_price, product_found[0]))
        elif what == "stock":
            new_stock = int(input("Enter the new stock quantity: "))
            query = "UPDATE products SET stock = %s WHERE id = %s"
            cursor.execute(query, (new_stock, product_found[0]))
        elif what == "category":
            new_category = input("Enter the new product category: ")
            query = "UPDATE products SET category = %s WHERE id = %s"
            cursor.execute(query, (new_category, product_found[0]))

        conn.commit()
        print(f"✅ Product '{product_found[1]}' updated successfully!")

    cursor.close()
    conn.close()
def delete_my_product(vendor_name):
    conn = mysql.connector.connect(
        host="localhost",
        user="root",
        password="Sairam@09",
        database="fweah_ecommerce"
    )
    cursor = conn.cursor()

    # Fetch products for the given vendor
    query = """
    SELECT id, name, stock
    FROM products
    WHERE vendor_name = %s
    """
    cursor.execute(query, (vendor_name,))
    products = cursor.fetchall()

    # Check if the vendor has any products
    if not products:
        print("You have no products listed.")
        return

    # Display the products
    print("Here are your products:")
    for product in products:
        print(f"ID: {product[0]}, Name: {product[1]}")

    # Ask which product the vendor wants to update
    sus = input("Which product would you like to delete? ").strip()
    product_found = None

    # Find the product by name
    for product in products:
        if sus.lower() == product[1].lower():  # Compare product name, case insensitive
            product_found = product
            break

    if product_found:
        print(f"You selected: {product_found[1]}")
        
        # Confirm deletion
        confirm = input(f"Are you sure you want to delete '{product_found[1]}'? Type 'yes' to confirm: ").strip().lower()
        if confirm == 'yes':
            # Delete the product from the database
            query = "DELETE FROM products WHERE id = %s"
            cursor.execute(query, (product_found[0],))
            conn.commit()
            print(f"✅ Product '{product_found[1]}' deleted successfully!")
        else:
            print("Deletion canceled.")
    else:
        print(f"Product '{sus}' not found.")

    cursor.close()
    conn.close()
def update_inventory(vendor_name):
    conn = mysql.connector.connect(
        host="localhost",
        user="root",
        password="Sairam@09",
        database="fweah_ecommerce"
    )
    cursor = conn.cursor()

    # Fetch products for the given vendor
    query = """
    SELECT id, name, stock
    FROM products
    WHERE vendor_name = %s
    """
    cursor.execute(query, (vendor_name,))
    products = cursor.fetchall()

    # Check if the vendor has any products
    if not products:
        print("You have no products listed.")
        return

    # Display the products
    print("Here are your products:")
    for product in products:
        print(f"ID: {product[0]}, Name: {product[1]}, Stock: {product[2]}")

    # Ask which product the vendor wants to update
    sus = input("Which product would you like to update the stock for? ").strip()
    product_found = None

    # Find the product by name
    for product in products:
        if sus.lower() == product[1].lower():  # Compare product name, case insensitive
            product_found = product
            break

    if product_found:
        print(f"You selected: {product_found[1]}")
        try:
            new_stock = int(input("Enter the new stock quantity: "))
            if new_stock < 0:
                print("Stock cannot be negative. Please enter a valid number.")
                return
        except ValueError:
            print("Invalid input. Please enter a valid number for the stock.")
            return

        # Update the product's stock in the database
        query = "UPDATE products SET stock = %s WHERE id = %s"
        cursor.execute(query, (new_stock, product_found[0]))
        conn.commit()
        print(f"✅ Stock for product '{product_found[1]}' updated to {new_stock}!")

    else:
        print(f"Product '{sus}' not found.")

    cursor.close()
    conn.close()


def manage_discounts():
    conn = mysql.connector.connect(
        host="localhost",
        user="root",
        password="Sairam@09",
        database="fweah_ecommerce"
    )
    cursor = conn.cursor()

    sigma = input("What is the name of the discount you want to create? ").strip()
    diog = float(input("How much percent is the discount (don't include the % symbol, just the number)? "))
    
    # Convert to decimal
    diog = diog / 100
    diog = round(diog, 2)

    # Ask if it applies to a specific product
    target_type = input("Is this discount for a 'specific product' or 'sitewide'? ").lower()

    if target_type == "specific product":
        product_name = input("Enter the name of the product this discount applies to: ").strip()

        # Optional: check if product exists first
        cursor.execute("SELECT id FROM products WHERE name = %s", (product_name,))
        product = cursor.fetchone()

        if not product:
            print(f"❌ Product '{product_name}' not found. Discount creation canceled.")
            cursor.close()
            conn.close()
            return

        # Insert discount into discounts table
        query = """
        INSERT INTO discounts (discount_name, discount_percent, product_id)
        VALUES (%s, %s, %s)
        """
        cursor.execute(query, (sigma, diog, product[0]))
        conn.commit()
        print(f"✅ Discount '{sigma}' of {diog*100}% created for product '{product_name}'!")

    elif target_type == "sitewide":
        # Insert sitewide discount
        query = """
        INSERT INTO discounts (discount_name, discount_percent, product_id)
        VALUES (%s, %s, NULL)
        """
        cursor.execute(query, (sigma, diog))
        conn.commit()
        print(f"✅ Sitewide discount '{sigma}' of {diog*100}% created!")

    else:
        print("❌ Invalid discount type. Please choose either 'specific product' or 'sitewide'.")

    cursor.close()
    conn.close()



def redeem_points(account_name):
    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute("SELECT loyalty_points FROM loyalty WHERE account_name = %s", (account_name,))
    result = cursor.fetchone()


    points = result[0]
    discount = 0

    swamp = int(input("How many points would you like to redeem? "))
    cursor.execute("SELECT loyalty_points FROM loyalty WHERE account_name = %s", (account_name,))
    points = cursor.fetchone()[0]

    if points >= 50:
        cursor.execute("""
            UPDATE loyalty 
            SET loyalty_points = loyalty_points - 50 
            WHERE account_name = %s
        """, (account_name,))
        conn.commit()
        print("You redeemed 50 points for a reward!")
        update_loyalty(account_name, 0)  # Re-evaluate tier
    else:
        print(f"Not enough points to redeem. You have {points} points.")

    conn.close()


def get_exchange_rate(target_currency):
    try:
        response = requests.get(f'{BASE_URL}/{API_KEY}/latest/USD')
        data = response.json()
        return data['conversion_rates'][target_currency.upper()]
    except Exception as e:
        print(f"Error fetching exchange rate: {e}")
        return None

def order_history(account_name):
    conn = mysql.connector.connect(
        host="localhost",
        user="root",
        password="Sairam@09",
        database="fweah_ecommerce"
    )
    cursor = conn.cursor()

    query = """
    SELECT oh.id, oh.order_date, oh.total_price, oh.status, 
           oi.product_id, oi.quantity, oi.price 
    FROM order_history oh
    JOIN order_items oi ON oh.id = oi.order_id
    WHERE oh.account_name = %s
    ORDER BY oh.order_date DESC;
    """
    
    cursor.execute(query, (account_name,))
    results = cursor.fetchall()

    conn.close()

    if results:
        print("Order History:")
        for row in results:
            print(f"Order ID: {row[0]}, Date: {row[1]}, Total: ${row[2]}, Status: {row[3]}")
            print(f"  Product ID: {row[4]}, Quantity: {row[5]}, Price: ${row[6]}")
    else:
        print("No orders found.")

def account_info(account_name):
    conn = mysql.connector.connect(
        host="localhost",
        user="root",
        password="Sairam@09",
        database="fweah_ecommerce"
    )
    cursor = conn.cursor(dictionary=True)  # Fetch results as a dictionary

    query = """
    SELECT * FROM accounts WHERE account_name = %s;
    """
    cursor.execute(query, (account_name,))
    account = cursor.fetchone() 

    conn.close()

    if account:
        print("\n=== Account Information ===")
        for key, value in account.items():
            print(f"{key.replace('_', ' ').title()}: {value}")
        print("==========================\n")
    else:
        print("No account found with that username.")

def search_product(accounts, name):
    fweah = input("What is the product name you would like to search for? ")
    matches = get_close_matches(fweah.lower(), products, n=1, cutoff=0.6)
    if matches:
        fweah = 0
        sus = input(f"Did you mean: {matches[fweah]}? ✅")
        while sus in negative_responses:
            fweah +1
            sus = input(f"Did you mean: {matches[fweah]}?")
            
            if fweah >= 6:
                print("Sorry we could not find the product you were looking for :c")
                return
        bruh = input("Great :D, would you like to add this product to your cart or directly buy it right now (cart, directly buy it, or leave)? ")
        if bruh in positive_responses or "right now" or "please" or "buy" or "directly buy it":
            pass
        elif bruh in negative_responses or "cart":
            add_to_cart_search(accounts[name], matches[fweah])
        else:
            print("Alright Bye :D")
            return
    else:
        print("Sorry we could not find this product :c")
def add_to_cart_search(accounts, name, product_name):
     product = next((p for p in products if p['name'] == product_name), None)

     if product:
                connection = get_db_connection()
                cursor = connection.cursor()

                # Check if the product already exists in the cart
                cursor.execute("SELECT quantity FROM cart WHERE account_name = %s AND product_name = %s", 
                               (accounts[name], product_name))
                existing_item = cursor.fetchone()

                if existing_item:
                    # Update quantity if already in cart
                    new_quantity = existing_item["quantity"] + 1

                    cursor.execute("UPDATE cart SET quantity = %s WHERE account_name = %s AND product_name = %s", 
                                   (new_quantity, accounts[name], product_name))
                else:
                    # Insert new product into cart
                    cursor.execute("INSERT INTO cart (account_name, product_id, product_name, price, quantity) VALUES (%s, %s, %s, %s, %s)", 
                                   (accounts[name], product['id'], product['name'], product['price'], 1))
                
                connection.commit()
                print(f"Added {product['name']} to the cart.")
                cursor.close()
                connection.close()
     else:
                print("Invalid Product. Please try again.")



def init_loyalty(account_name):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("INSERT INTO loyalty (account_name) VALUES (%s)", (account_name,))
    conn.commit()
    conn.close()
    print(f"Loyalty record created for {account_name}.")

# Update loyalty points and tier
def update_loyalty(account_name, points_earned):
    conn = get_db_connection()
    cursor = conn.cursor()

    # Add points
    cursor.execute("""
        UPDATE loyalty 
        SET loyalty_points = loyalty_points + %s 
        WHERE account_name = %s
    """, (points_earned, account_name))

    # Get updated point total
    cursor.execute("SELECT loyalty_points FROM loyalty WHERE account_name = %s", (account_name,))
    points = cursor.fetchone()[0]

    # Update tier
    if points >= 200:
        tier = "Platinum"
    elif points >= 100:
        tier = "Gold"
    elif points >= 50:
        tier = "Silver"
    else:
        tier = "Bronze"

    cursor.execute("""
        UPDATE loyalty 
        SET tier = %s 
        WHERE account_name = %s
    """, (tier, account_name))

    conn.commit()
    conn.close()
    print(f"{account_name} earned {points_earned} points. New total: {points}, Tier: {tier}.")

# Redeem points


# Check current status
def get_loyalty_status(account_name):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT loyalty_points, tier FROM loyalty WHERE account_name = %s", (account_name,))
    result = cursor.fetchone()
    conn.close()
    
    if result:
        points, tier = result
        print(f"{account_name} has {points} points and is in the {tier} tier.")
        return points, tier
    else:
        print("No loyalty record found.")
        return None, None

def track_orders():
    print("Work on this")

def log_query_json(query):
    log_entry = {
        "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "user_query": query
    }

    # Load existing logs or create new
    if os.path.exists("freak.json"):
        with open("freak.json", "r") as f:
            try:
                data = json.load(f)
            except json.JSONDecodeError:
                data = []
    else:
        data = []

    data.append(log_entry)

    with open("freak.json", "w") as f:
        json.dump(data, f, indent=4)


def view_sales_report(vendor_name):
    # Connect to the database
    conn = mysql.connector.connect(
        host="localhost",
        user="root",
        password="Sairam@09",
        database="fweah_ecommerce"
    )
    cursor = conn.cursor()

    # Fetch total units sold and total revenue for the vendor
    query_total = """
    SELECT 
        SUM(o.quantity) AS total_units_sold,
        SUM(o.quantity * p.price) AS total_revenue
    FROM orders o
    JOIN products p ON o.product_id = p.id
    WHERE p.vendor_name = %s
    """
    cursor.execute(query_total, (vendor_name,))
    total_result = cursor.fetchone()
    total_units_sold, total_revenue = total_result if total_result else (0, 0.0)

    print(f"\n📊 Sales Report for Vendor: {vendor_name}")
    print(f"Total Units Sold: {total_units_sold}")
    print(f"Total Revenue: ${total_revenue:.2f}\n")

    # Fetch sales breakdown by product
    query_breakdown = """
    SELECT 
        p.name AS product_name,
        SUM(o.quantity) AS units_sold,
        SUM(o.quantity * p.price) AS revenue
    FROM orders o
    JOIN products p ON o.product_id = p.id
    WHERE p.vendor_name = %s
    GROUP BY p.name
    ORDER BY revenue DESC
    """
    cursor.execute(query_breakdown, (vendor_name,))
    breakdown_results = cursor.fetchall()

    if breakdown_results:
        print("Product-wise Sales Breakdown:")
        print(f"{'Product Name':<30} {'Units Sold':<15} {'Revenue':<10}")
        print("-" * 60)
        for product_name, units_sold, revenue in breakdown_results:
            print(f"{product_name:<30} {units_sold:<15} ${revenue:.2f}")
    else:
        print("No sales data available for this vendor.")

    # Close the cursor and connection
    cursor.close()
    conn.close()


def advertise_product(vendor_name):
    conn = mysql.connector.connect(
        host="localhost",
        user="root",
        password="Sairam@09",
        database="fweah_ecommerce"
    )
    cursor = conn.cursor()

    # Fetch the vendor's products
    query = """
    SELECT id, name
    FROM products
    WHERE vendor_name = %s
    """
    cursor.execute(query, (vendor_name,))
    products = cursor.fetchall()

    if not products:
        print("❌ You have no products to advertise.")
        cursor.close()
        conn.close()
        return

    # Show products
    print("\nHere are your products you can advertise:")
    for product in products:
        print(f"ID: {product[0]} - Name: {product[1]}")

    # Choose a product to advertise
    product_name = input("\nEnter the name of the product you want to advertise: ").strip()

    # Find the matching product
    selected_product = None
    for product in products:
        if product_name.lower() == product[1].lower():
            selected_product = product
            break

    if not selected_product:
        print(f"❌ Product '{product_name}' not found.")
        cursor.close()
        conn.close()
        return

    # Ask for how many days they want to advertise
    try:
        days = int(input("For how many days would you like to advertise this product? (example: 7): "))
        if days <= 0:
            print("❌ Days must be a positive number.")
            cursor.close()
            conn.close()
            return
    except ValueError:
        print("❌ Invalid input. Please enter a valid number of days.")
        cursor.close()
        conn.close()
        return

    # Insert into advertisements table
    query = """
    INSERT INTO advertisements (product_id, vendor_name, days)
    VALUES (%s, %s, %s)
    """
    cursor.execute(query, (selected_product[0], vendor_name, days))
    conn.commit()

    print(f"✅ Product '{selected_product[1]}' is now being advertised for {days} days!")

    cursor.close()
    conn.close()




def contact_support():
    sus = input("Hi, what would you like help with? ").lower()
    log_query_json(sus)

    help_topics = {
        "how to get loyalty points? ": (
            "You just need to buy products from us :D,"
            "and if you don't refund them (unless the refund is a valid reason)"
        ), 
        "whats the point of loyalty points?": (
            "You can get free products :D"
        ),
        "i can't buy anything": (
            "Please restart your application. If it seems like a technical error on our side, "
            "submit a report at https://forms.gle/YNbVze7Frzj8v37v6"
        ),
        "why aren't some of the functions working?": (
            "This may be because the app is still in beta. If it's urgent or seems like a bug, report it here: "
            "https://forms.gle/YNbVze7Frzj8v37v6"
        ),
        "how do i sell my own products?": (
            "To sell products, create a vendor account. You'll get access to selling tools, trending products, "
            "and advertising features."
        ),
        "how do i reset my password?": (
            "Go to the login page and click 'Forgot Password'. Follow the instructions sent to your email."
        ),
        "where can i see my past orders?": (
            "You can view past orders in the transactions section."
        ),
        "how do i contact customer support directly?": (
            "You can email our support team at nagamanojp@gmail.com or call us at 1-925-997-8653."
        ),
        "i want to delete my account": (
            "We're sorry to see you go! Please visit your account and choose 'Delete Account' at the bottom. "
            "Or contact us directly to help with the process."
        ),
        "how do i get a refund?": (
            "To request a refund, go to your list of options and please select the request a refund option, there you will be asked a reason on why you are requesting a refund and the money will shortly be transfered to you. "
        )
    }

    matches = get_close_matches(sus, help_topics.keys(), n=1, cutoff=0.6)

    if matches:
        print(help_topics[matches[0]])
    else:
        print("Sorry, I couldn't understand your question. Please try rephrasing or submit your query directly at https://forms.gle/YNbVze7Frzj8v37v6")
        
def get_recommendations(account_name):
    conn = mysql.connector.connect(
        host="localhost",
        user="root",
        password="Sairam@09",
        database="fweah_ecommerce"
    )
    cursor = conn.cursor(dictionary=True)

    # Step 1: Get most frequently purchased categories by the user
    cursor.execute("""
        SELECT p.category, COUNT(*) as count
        FROM transactions t
        JOIN transaction_items ti ON t.id = ti.transaction_id
        JOIN products p ON ti.product_id = p.id
        WHERE t.account_name = %s AND t.status = 'completed'
        GROUP BY p.category
        ORDER BY count DESC
        LIMIT 1
    """, (account_name,))
    
    result = cursor.fetchone()
    
    if not result:
        print(f"No purchases found for {account_name}")
        return

    favorite_category = result['category']

    # Step 2: Recommend products from the same category (that the user hasn't already bought)
    cursor.execute("""
        SELECT DISTINCT p.name
        FROM products p
        WHERE p.category = %s
        AND p.id NOT IN (
            SELECT ti.product_id
            FROM transactions t
            JOIN transaction_items ti ON t.id = ti.transaction_id
            WHERE t.account_name = %s
        )
        LIMIT 5
    """, (favorite_category, account_name))

    recommendations = cursor.fetchall()
    
    if recommendations:
        print(f"Recommended products for {account_name} (based on category '{favorite_category}'):")
        for rec in recommendations:
            print("- " + rec['name'])
    else:
        print(f"No new recommendations found for {account_name}")

    cursor.close()
    conn.close()
reason = ["product didnt work", "useless", "scam", "didnt arrive", "fake"]

def request_a_refund(accounts, name):
    omg = input("What product would you like to get a refund for? ").strip().lower()
    reasons = input("Why did you refund this? ")

    if name not in accounts or 'purchases' not in accounts[name]:
        print("No purchases found for this account.")
        return

    user_purchases = accounts[name]['purchases']
    matching_products = [item for item in user_purchases if omg in item.lower()]

    if not matching_products:
        print("Sorry, we couldn't find a matching product in your purchase history.")
        return

    print("Found the following product(s):")
    for i, product in enumerate(matching_products, 1):
        print(f"{i}. {product}")

    try:
        selection = int(input("Enter the number of the product you want to refund: "))
        if 1 <= selection <= len(matching_products):
            product_to_refund = matching_products[selection - 1]
            user_purchases.remove(product_to_refund)
            if reasons in get_close_matches(reasons.lower(), reason, n=1, cutoff=0.6):
                print(f"Your refund for {product_to_refund} has been processed. Apologies for the inconvenience. ")
                return
            else: 
                accounts[name]['loyalty_points'] = max(0, accounts[name].get('loyalty_points', 0) - 10)
                print(f"✅ Refund for '{product_to_refund}' has been processed. 10 loyalty points have been deducted.")
        else:
            print("Invalid selection.")
    except ValueError:
        print("Invalid input. Please enter a number.")


def sign_in(accounts, name, password):
    while 1 == 1:
        if ur_account == 'customer':
            while True:
                print("\nWhat would you like to do?")
                print("1) Check out our products")
                print("2) Check cart")
                print("3) Checkout")
                print("4) View Order History")
                print("5) Update Account Information")
                print("6) Search for Products")
                print("7) Display All Discount Codes")
                print("8) Track Orders in Real-Time")
                print("9) Contact Support") #add info abt loyalty program
                print("10) View Personalized Recommendations") 
                print("11) Manage Wishlist")
                print("12) Write a Review")
                print("13) Check Loyalty Tier & Points")
                print("14) Advanced Product Search")
                print("15) View Recently Viewed Products")
                print("16) Set Preferred Currency")
                print("17) Purchase E-Gift Cards")
                print("18) Request Refund")
                print("19) Spin the Wheel for a Daily Reward!")
                print("0) Exit")

                choice = input("Enter your choice: ")

                if choice == "1":
                    list_product(name)
                elif choice == "2":
                    check_cart()
                elif choice == "3":
                    checkout()
                elif choice == "4":
                    order_history()
                elif choice == "5":
                    account_info()
                elif choice == "6":
                    search_product()
                elif choice == "7":
                    for code, percentage in discounts.items():
                        print(f"Discount Code: {code}, Percentage Off: {percentage * 100:.0f}%")
                elif choice == "8":
                    print("Track your order:")
                    order_id = input("Enter your order ID: ")
                    status = track_orders(order_id)  # Custom function
                    print(f"Order Status: {status}")
                elif choice == "9":
                    contact_support()
                elif choice == "10":
                    print("Here are some recommendations for you:")
                    recommendations = get_recommendations(name)  # Custom function
                    for product in recommendations:
                        print(f"- {product}")
                elif choice == "11":
                    print("Manage your wishlist:")
                    print("1) View Wishlist")
                    print("2) Add Item to Wishlist")
                    print("3) Remove Item from Wishlist")
                    wishlist_choice = input("Choose an option: ")
                    if wishlist_choice == "1":
                        view_wishlist(name)  # Custom function to view wishlist
                    elif wishlist_choice == "2":
                        add_to_wishlist(name)  # Custom function to add
                    elif wishlist_choice == "3":
                        item_id = input("Enter the product name to remove: ")
                        remove_from_wishlist(name, item_id)  # Custom function to remove
                elif choice == "12":
                    time.sleep(0.79)
                    user_submit_review(name)
                    time.sleep(0.89)
                elif choice == "13":
                    print("Loyalty Tier & Points:")
                    get_loyalty_status(name)  # Custom function to fetch points
                elif choice == "14":
                    results = advanced_search(category, min_price, max_price, rating)
                    print("\nSearch Results:")
                    if results:
                        for product in results:
                            print(f"- {product['name']} (${product['price']}, {product['rating']} stars)")
                    else:
                        print("No products found matching your criteria.")
                    print("Advanced Product Search:")
                    category = input("Enter category: ")
                    min_price = float(input("Enter minimum price: "))
                    max_price = float(input("Enter maximum price: "))
                    rating = float(input("Enter minimum rating (1-5): "))
                    results = advanced_search(category, min_price, max_price, rating)  # Custom function
                    print("Search Results:")
                    for product in results:
                        print(f"- {product['name']} (${product['price']}, {product['rating']} stars)")
                elif choice == "15":
                    sigma = get_recently_viewed(name)
                    print(sigma)
                elif choice == "16":
                    def set_currency(currency_type):
                        accounts[name]["currency"] = currency_type
                        save_account(accounts)
                    print("Set your preferred currency: ")
                    currency = input("Enter your currency (e.g., USD, EUR, INR): ")
                    set_currency(name, currency)  # add the shit for price
                    print("Currency updated. Prices will now be displayed in your preferred currency.")
                elif choice == "17":
                    print("Purchase a gift item:")
                    recipient = input("Enter recipient's address: ")
                    duck = input("Would you like to see the products or immediately buy them something (see, buy)? ").lower()
                    if duck == "see":
                        for product in products:
                            print(f"ID: {product['id']} | Name: {product['name']} | Price: ${product['price']:.2f}")

                    amount = float(input("Enter the item you want to gift to your friend: "))
                    send_gift_item(name, recipient, amount)  # Custom function
                    print(f"Gift card of ${amount} sent to {recipient}.")
                elif choice == "18":
                    request_a_refund(accounts, name)
                elif choice == "19":
                    spin_the_wheel()
                elif choice == "0": 
                    print("Thank you for visiting. Goodbye! ")
                    return
                else:
                    print("Invalid choice. Please try again.")
        elif ur_account == 'vendor':
            while True:
                print("\nWhat would you like to do?")
                print("1) View All Products")
                print("2) Add (Sell) a Product")
                print("3) View My Products")
                print("4) Update My Product Details")
                print("5) Delete a Product Listing")
                print("6) View My Sales Report")
                print("7) Manage Product Discounts")
                print("8) Update Inventory (Stock)")
                print("9) Advertise Your Products!")
                print("10) Respond to Customers Reviews")
                print("0) Exit")

                choice = input("Enter your choice: ")
                if choice == "1":
                    list_product(name)
                elif choice == "2":
                    sell_product(name)
                elif choice == "3":
                    view_my_products(name)
                elif choice == "4":
                    update_my_product(name)
                elif choice == "5":
                    delete_my_product()
                elif choice == "6":
                    view_sales_report()
                elif choice == "7":
                    manage_discounts()
                elif choice == "8":
                    update_inventory(name)
                elif choice == "9":
                    advertise_product()
                elif choice =="10":
                    respond_to_reviews(name)
                elif choice == "0":
                    print("Thank you for visiting. Goodbye!")
                    return
                
                else: 
                    print("Invalid choice. Please try again.")

        elif ur_account == 'admin':
            pass

def forgot_password(accounts):
    batman = input("Whats the username of your account. ")
    if batman not in accounts:
        print("This username doesn't exist. ")
        return
    else: 
        cool_number = random.randint(100000, 999999)
        time.sleep(0.73)
        why = input(f"Is your email still {accounts[batman]['email']}: ").lower()
        time.sleep(0.73)
        if get_close_matches(why.lower(), positive_responses, n=1, cutoff=0.6):
            pass
        elif get_close_matches(why.lower(), negative_responses, n=1, cutoff=0.6):
            rizz = input('What is your current email? ')
            time.sleep(0.73)
            if rizz == accounts[batman]['email']:
                print("Hmm it seems that I have already displayed this email and you said no its not my current email, are you serious???? ")
                time.sleep(0.73)
                pass
            else:
                time.sleep(0.73)
                rizzy = input("What would you like your new email to be: ")
                time.sleep(0.73)
                accounts[batman]['email'] = rizzy
                save_account(accounts)
                pass
        receiver_email = accounts[batman]['email']
        message = f"""\
Subject: Password Reset
            
Dear {accounts[batman]['first_name']},
            
    Your randomly generated number is {cool_number}
    Please input this number in the website to change your password
            
    Hope you have a great day.
            
Regards,
    Manoj :)
                    """
        try:
                    server = smtplib.SMTP('smtp.gmail.com', 587)
                    server.starttls()
                    server.login(sender_email, sender_password)
                    server.sendmail(sender_email, receiver_email, message)
                    time.sleep(0.79)
                    print("Randomly genrated number sent successfully. ")
                    time.sleep(0.79)
        except Exception as e:
                    time.sleep(0.79)
                    print(f"Failed to send email: {e}")
                    time.sleep(0.79)
        sus = int(input("Please enter the randomly generated number you have received in your email: "))
        while sus != cool_number:
                    sussy = input("Would you like to try again or exit: ").lower()
                    if sussy == 'try again' or 'tryagain':
                        sus = int(input("Re enter the number: ")).lower()
                    elif sussy == 'exit':
                        return
                    else:
                        print("Invalid Option ")
                        return
        if sus == cool_number:
                    how = input("What would you like your new password to be? ")
                    time.sleep(0.73)
                    if how == accounts[batman]['password']:
                        print("This is already your current password. ")
                        time.sleep(0.73)
                        son = input
                        wow = son("Would you like to change your password? ")
                        time.sleep(0.73)
                        if get_close_matches(wow.lower(), positive_responses, n=1, cutoff=0.6):
                            new_pass = son("What would you like your new password to be: ")
                            time.sleep(0.73)
                            accounts[batman]['password'] = new_pass
                            save_account(accounts)
                        elif get_close_matches(wow.lower(), negative_responses, n=1, cutoff=0.6):
                            print("Alright have a great day then. ")
                            time.sleep(0.73)
                            return
                        else:
                            return
                    else:
                        new_pass = son("What would you like your new password to be: ")
                        time.sleep(0.73)
                        accounts[batman]['password'] = new_pass
                        save_account(accounts)
        
        else:
            print("Sorry you have inputed an incorrect option. ")
            time.sleep(0.73)
            return

def main():
    accounts = load_accounts()
    while True:
        choice = int(input("Would you like to: 1. Create an account, 2. Sign into an account, 3. Forgot Password, 4. Exit: "))
        time.sleep(0.73)

        if choice == 1:
            create_acc()
            
        elif choice == 2:
            name = input("Enter account name: ")
            wowie = input("Would you like to see your password as you type or would like it to be hidden? ").lower()
            if wowie in ['see', 'yeah i would like to see', 'seeing', 'unhidden', 'visible', 'u get no bitches', 'p diddy jokes aint funny', 'say before GTA 6 I dare u lil bro', 'chat', 'is this a hood banger']:
                password = input("Enter password: ")
                sign_in(name, password)
            elif wowie in ['hidden', 'stay hidden']:
                password = custom_getpass("Enter password: ")
                sign_in(accounts, name, password)
            else:
                print("Invalid Option.")
                return
        elif choice == 3:
            forgot_password(accounts)
        elif choice == 4:
            print("Alright have a good day :D")
            break
        else:
            print("Invalid option.")
            time.sleep(0.73)


if __name__ == "__main__":
    time.sleep(0.73)
    main()