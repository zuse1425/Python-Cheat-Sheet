import csv

class Item:
    pay_rate = 0.8
    all = []      # Master list of unique items in memory (the 'store')
    basket = []   # Temporary shopping cart (optional usage)

    def __init__(self, name: str, price: float, quantity=0):
        # Basic validations
        if price < 0:
            raise ValueError(f"Price {price} must be >= 0.")
        if quantity < 0:
            raise ValueError(f"Quantity {quantity} must be >= 0.")

        self.name = name
        self.price = price
        self.quantity = quantity
        self.sell_price = self.price

    @staticmethod
    def find_item_by_name(name: str):
        """Return the item object if found in Item.all, otherwise None."""
        for obj in Item.all:
            if obj.name.lower() == name.lower():
                return obj
        return None

    @classmethod
    def create_or_update_item(cls, name: str, price: float, quantity: int):
        """
        Create a new Item if not found in cls.all,
        or update an existing item’s price and add quantity to it.
        Returns the (existing or newly created) Item object.
        """
        existing_item = cls.find_item_by_name(name)
        if existing_item:
            existing_item.price = price
            existing_item.quantity += quantity
            return existing_item
        else:
            new_item = cls(name, price, quantity)
            cls.all.append(new_item)
            return new_item

    @classmethod
    def remove_item(cls, name: str, rem_quantity: int):
        """
        Removes 'rem_quantity' from the in-memory store (cls.all).
        If the updated quantity is 0, the object is removed from 'all'.
        Raises ValueError if it would go negative.
        """
        item = cls.find_item_by_name(name)
        if not item:
            raise ValueError(f"Item '{name}' not found in the store.")

        new_quantity = item.quantity - rem_quantity
        if new_quantity < 0:
            raise ValueError("Quantity cannot go negative.")
        elif new_quantity == 0:
            cls.all.remove(item)
        else:
            item.quantity = new_quantity

    @classmethod
    def instantiate_from_CSV(cls, path='items.csv'):
        """
        Reads items from a CSV file and creates/upserts them into Item.all.
        CSV must have a header row: name, price, quantity
        """
        cls.all = []  # clear any old data in memory
        try:
            with open(path, 'r', newline='') as f:
                reader = csv.DictReader(f)
                for row in reader:
                    name = row.get('name')
                    price = float(row.get('price', 0))
                    quantity = int(row.get('quantity', 0))
                    cls.create_or_update_item(name, price, quantity)
        except FileNotFoundError:
            print(f"\nCSV file '{path}' not found. Starting with an empty store.\n")

    @classmethod
    def write_all_to_CSV(cls, path='items.csv'):
        """
        Overwrites the CSV with the current state of Item.all.
        """
        with open(path, 'w', newline='') as f:
            fieldnames = ['name', 'price', 'quantity']
            writer = csv.DictWriter(f, fieldnames=fieldnames)
            writer.writeheader()
            for item in cls.all:
                writer.writerow({
                    'name': item.name,
                    'price': item.price,
                    'quantity': item.quantity
                })

    @classmethod
    def show_store(cls):
        """
        Prints a readable summary of the current state of the store (cls.all).
        """
        print("\n=== Current State of the Store ===")
        if not cls.all:
            print("(No items in store.)")
        else:
            for item in cls.all:
                print(item)
        print("===================================")

    @classmethod
    def print_csv(cls, path='items.csv'):
        """
        Print each row from the CSV for quick inspection.
        """
        try:
            with open(path, 'r', newline='') as f:
                reader = csv.DictReader(f)
                for row in reader:
                    print(row)
        except FileNotFoundError:
            print(f"No CSV found at '{path}'.")

    def calculate_total_price(self):
        """Calculate total price = price * quantity."""
        return self.price * self.quantity

    def apply_discount(self):
        """Apply pay_rate discount to the sell_price."""
        self.sell_price = self.price * self.pay_rate

    def __repr__(self):
        return (f"Item(name={self.name}, price={self.price}, "
                f"quantity={self.quantity}, sell_price={self.sell_price}, "
                f"pay_rate={self.pay_rate})")
