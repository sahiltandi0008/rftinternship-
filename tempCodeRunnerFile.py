phonebook = {
    "AMIT": "9876543210",
    "RIYA": "9123456780"
}

def add_contact():
    name = input("Enter name: ").upper()
    number = input("Enter number: ")

    if name in phonebook:
        print("Contact already exists!")
    else:
        phonebook[name] = number
        print("Contact added successfully.")

def search_contact():
    search = input("Enter name to search: ").upper()
    found = False

    for name in phonebook:
        if search in name:  
            print(f"{name} : {phonebook[name]}")
            found = True

    if not found:
        print("No contact found.")

def delete_contact():
    name = input("Enter name to delete: ").upper()

    if name in phonebook:
        del phonebook[name]
        print("Contact deleted.")
    else:
        print("Contact not found.")

def display_contacts():
    if not phonebook:
        print("Phonebook is empty.")
    else:
        print("\nAll Contacts:")
        for name, number in phonebook.items():
            print(f"{name} : {number}")


while True:
    print("\n--- PHONEBOOK MENU ---")
    print("1. Add Contact")
    print("2. Search Contact")
    print("3. Delete Contact")
    print("4. Display Contacts")
    print("5. Exit")

    choice = input("Enter your choice: ")

    if choice == '1':
        add_contact()
    elif choice == '2':
        search_contact()
    elif choice == '3':
        delete_contact()
    elif choice == '4':
        display_contacts()
    elif choice == '5':
        print("Exiting program...")
        break
    else:
        print("Invalid choice. Try again.")