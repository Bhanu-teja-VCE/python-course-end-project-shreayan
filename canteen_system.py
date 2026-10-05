# Canteen Order and Billing Management System
# Done by: Shreayan

import json
import os
from datetime import datetime

DATA_FILE = os.path.join(os.path.dirname(os.path.abspath(__file__)), "canteen_data.json")


def load_data():
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE, "r") as f:
            return json.load(f)
    # some default food items to start with
    return {
        "menu": {
            "1": {"name": "Idli", "price": 30},
            "2": {"name": "Dosa", "price": 40},
            "3": {"name": "Veg Meals", "price": 80},
            "4": {"name": "Tea", "price": 10},
            "5": {"name": "Coffee", "price": 15},
        },
        "orders": [],
    }


def save_data(data):
    with open(DATA_FILE, "w") as f:
        json.dump(data, f, indent=4)


def show_menu(data):
    print("\n--- Food Menu ---")
    for code, item in data["menu"].items():
        print(f"{code}. {item['name']:<15} Rs. {item['price']}")


def add_item(data):
    name = input("Enter food name: ").strip().title()
    try:
        price = float(input("Enter price: "))
    except ValueError:
        print("Invalid price.")
        return
    new_code = str(max([int(c) for c in data["menu"]] + [0]) + 1)
    data["menu"][new_code] = {"name": name, "price": price}
    save_data(data)
    print(f"{name} added with code {new_code}.")


def remove_item(data):
    show_menu(data)
    code = input("Enter item code to remove: ").strip()
    if code in data["menu"]:
        removed = data["menu"].pop(code)
        save_data(data)
        print(f"{removed['name']} removed from menu.")
    else:
        print("Item not found.")


def place_order(data):
    customer = input("Enter customer name: ").strip().title()
    cart = []
    while True:
        show_menu(data)
        code = input("Enter item code (or 'done' to finish): ").strip()
        if code.lower() == "done":
            break
        if code not in data["menu"]:
            print("Invalid code.")
            continue
        try:
            qty = int(input("Enter quantity: "))
            if qty <= 0:
                raise ValueError
        except ValueError:
            print("Invalid quantity.")
            continue
        item = data["menu"][code]
        cart.append({"name": item["name"], "price": item["price"], "qty": qty})
        print(f"Added {qty} x {item['name']}")

    if not cart:
        print("No items ordered.")
        return

    # Billing
    subtotal = sum(i["price"] * i["qty"] for i in cart)
    gst = round(subtotal * 0.05, 2)
    total = round(subtotal + gst, 2)

    print("\n========== BILL ==========")
    print(f"Customer: {customer}")
    print(f"Date    : {datetime.now().strftime('%Y-%m-%d %H:%M')}")
    print("--------------------------")
    for i in cart:
        print(f"{i['name']:<12} {i['qty']} x {i['price']} = {i['price'] * i['qty']}")
    print("--------------------------")
    print(f"Subtotal : Rs. {subtotal}")
    print(f"GST (5%) : Rs. {gst}")
    print(f"TOTAL    : Rs. {total}")
    print("==========================")

    data["orders"].append({
        "customer": customer,
        "date": datetime.now().strftime("%Y-%m-%d"),
        "items": cart,
        "total": total,
    })
    save_data(data)


def daily_sales(data):
    date = input("Enter date (YYYY-MM-DD) or press Enter for today: ").strip()
    if not date:
        date = datetime.now().strftime("%Y-%m-%d")
    orders = [o for o in data["orders"] if o["date"] == date]
    print(f"\n--- Sales Report for {date} ---")
    if not orders:
        print("No orders on this date.")
        return
    for n, o in enumerate(orders, 1):
        print(f"{n}. {o['customer']} - Rs. {o['total']}")
    print(f"Total orders: {len(orders)}")
    print(f"Total sales : Rs. {round(sum(o['total'] for o in orders), 2)}")


def main():
    data = load_data()
    while True:
        print("\n===== CANTEEN ORDER & BILLING SYSTEM =====")
        print("1. Show menu")
        print("2. Add food item")
        print("3. Remove food item")
        print("4. Place order & generate bill")
        print("5. Daily sales report")
        print("6. Exit")
        choice = input("Enter choice: ").strip()

        if choice == "1":
            show_menu(data)
        elif choice == "2":
            add_item(data)
        elif choice == "3":
            remove_item(data)
        elif choice == "4":
            place_order(data)
        elif choice == "5":
            daily_sales(data)
        elif choice == "6":
            print("Thank you!")
            break
        else:
            print("Invalid choice, try again.")


if __name__ == "__main__":
    main()
