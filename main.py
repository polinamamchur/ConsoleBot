def input_error(func):
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except KeyError:
            return "Enter a valid user name."
        except ValueError:
            return "Give me a name and phone, please."
        except IndexError:
            return "Contact not found. Please check the name."

    return wrapper


contacts = {}


def hello():
    return "How can I help you?"


def add_contact(name, phone_number):
    contacts[name] = phone_number
    return f"Contact {name} with phone number {phone_number} added."


def change_contact(name, new_phone_number):
    contacts[name] = new_phone_number
    return f"Phone number for {name} changed to {new_phone_number}."


def phone_contact(name):
    return f"The phone number for {name} is {contacts[name]}."


def show_all_contacts():
    if not contacts:
        return "No contacts found."
    else:
        result = "All contacts:\n"
        for name, phone_number in contacts.items():
            result += f"{name}: {phone_number}\n"
        return result.strip()


def main():
    while True:
        print("\nEnter a command:")
        print("1. Hello")
        print("2. Add contact")
        print("3. Change contact")
        print("4. Phone contact")
        print("5. Show all contacts")
        print("6. Good bye, close, exit")

        command = input("Your command: ").lower()

        if command == "hello":
            print(hello())
        elif command.startswith("add "):
            try:
                _, name, phone_number = command.split()
                print(add_contact(name, phone_number))
            except ValueError:
                print("Invalid command format. Please use 'add [name] [phone_number]'.")
        elif command.startswith("change "):
            try:
                _, name, new_phone_number = command.split()
                print(change_contact(name, new_phone_number))
            except ValueError:
                print("Invalid command format. Please use 'change [name] [new_phone_number]'.")
        elif command.startswith("phone "):
            try:
                _, name = command.split()
                print(phone_contact(name))
            except ValueError:
                print("Invalid command format. Please use 'phone [name]'.")
        elif command == "show all":
            print(show_all_contacts())
        elif command in ("good bye", "close", "exit"):
            print("Good bye!")
            break
        else:
            print("Unknown command. Please try again.")


if __name__ == "__main__":
    main()
