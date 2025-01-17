# main.py

from Item import Item

def main():
    """
    A simple interactive CLI app demonstrating usage of the Item class,
    """

    csv_path = 'items.csv'
    Item.instantiate_from_CSV(csv_path)

    prev_choice = None  # Will store the previous user choice
    while True:
        print("\n===== INVENTORY MANAGEMENT MENU =====")
        print("1. Show current items in store")
        print("2. Add or update an item")
        print("3. Remove quantity from an item")
        print("4. Print CSV contents (disk)")
        print("5. Save all changes to CSV")
        print("6. Quit")

        choice = input("Enter your choice (1-6): ").strip()

        # Display info about previous vs. current choice
        # if prev_choice is not None:
        #     print(f"\n[DEBUG] Previous choice was '{prev_choice}', now user chose '{choice}'.")
        # else:
        #     print(f"\n[DEBUG] No previous choice recorded. Current choice is '{choice}'.")

        match choice:
            case '1':
                # Show the current state of the store from memory
                Item.show_store()

            case '2':
                # Add or update an item
                name = input("\nEnter item name: ")
                price_str = input("Enter item price: ")
                quantity_str = input("Enter quantity to add: ")

                try:
                    price = float(price_str)
                    quantity = int(quantity_str)
                except ValueError:
                    print("Invalid price or quantity. Please try again.")
                else:
                    Item.create_or_update_item(name, price, quantity)
                    print(f"\nItem '{name}' has been added/updated with price={price} and quantity={quantity}.")
                    # (Optional) Show the store after adding/updating
                    Item.show_store()

            case '3':
                # Remove quantity from an existing item
                name = input("\nEnter item name to remove quantity from: ")
                rem_quantity_str = input("Enter quantity to remove: ")

                try:
                    rem_quantity = int(rem_quantity_str)
                except ValueError:
                    print("Invalid quantity. Please try again.")
                else:
                    try:
                        Item.remove_item(name, rem_quantity)
                        print(f"\nRemoved {rem_quantity} from '{name}'.")
                    except ValueError as e:
                        print(f"Error: {e}")
                    # (Optional) Show the store after removal
                    Item.show_store()

            case '4':
                # Print CSV contents on disk
                print("\n--- Current CSV Contents on Disk ---")
                Item.print_csv(csv_path)

            case '5':
                # Save all changes in memory (Item.all) to CSV
                if prev_choice == choice:
                    print("CSV already updated!")
                else:
                    Item.write_all_to_CSV(csv_path)
                    print("\nChanges have been saved to CSV.")

            case '6':
                # Quit
                print("\nExiting. Have a nice day!")
                break

            case _:
                # Catch-all for invalid choices
                print("\nInvalid choice. Please select a number from 1 to 6.")

        # Update prev_choice after processing current choice
        prev_choice = choice


if __name__ == "__main__":
    main()
