from datetime import datetime, timedelta

class Phone:
    def __init__(self, value):
        if len(value) == 10 and value.isdigit():
            self.value = value
        else:
            raise ValueError("Invalid phone number format. Use 10 digits.")

class Name:
    def __init__(self, value):
        self.value = value

class Birthday:
    def __init__(self, value):
        try:
            self.value = datetime.strptime(value, '%d.%m.%Y')
        except ValueError:
            raise ValueError("Invalid date format. Use DD.MM.YYYY")

class Record:
    def __init__(self, name):
        self.name = Name(name)
        self.phones = []
        self.birthday = None

    def add_phone(self, value):
        self.phones.append(Phone(value))

    def add_birthday(self, value):
        self.birthday = Birthday(value)

class AddressBook:
    def __init__(self):
        self.contacts = []

    def add_record(self, record):
        self.contacts.append(record)

    def find(self, name):
        for contact in self.contacts:
            if contact.name.value.lower() == name.lower():
                return contact
        return None

    def get_upcoming_birthdays(self):
        today = datetime.today()
        next_week = today + timedelta(days=7)
        upcoming_birthdays = []

        for contact in self.contacts:
            if contact.birthday:
                birthday_this_year = contact.birthday.value.replace(year=today.year)
                greeting_date = self._calculate_greeting_date(birthday_this_year, today)
                if today <= greeting_date <= next_week:
                    upcoming_birthdays.append((contact, greeting_date))

        return upcoming_birthdays

    def _calculate_greeting_date(self, birthday, today):
        if birthday < today:
            birthday = birthday.replace(year=today.year + 1)
        return birthday + timedelta(days=2)

def input_error(func):
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except (ValueError, IndexError, TypeError) as e:
            return str(e)
    return wrapper

def parse_input(user_input):
    parts = user_input.strip().split(maxsplit=2)
    command = parts[0].lower()
    args = parts[1:] if len(parts) > 1 else []
    return command, args

def main():
    book = AddressBook()
    print("Welcome to the assistant bot!")
    while True:
        user_input = input("Enter a command: ")
        command, args = parse_input(user_input)

        if command in ["close", "exit"]:
            print("Good bye!")
            break

        elif command == "hello":
            print("How can I help you?")

        elif command == "add":
            print(add_contact(args, book))

        elif command == "change":
            print(change_contact(args, book))

        elif command == "phone":
            print(show_phone(args, book))

        elif command == "all":
            print(show_all_contacts(book))

        elif command == "add-birthday":
            print(add_birthday(args, book))

        elif command == "show-birthday":
            print(show_birthday(args, book))

        elif command == "birthdays":
            print(show_upcoming_birthdays(book))

        else:
            print("Invalid command.")

@input_error
def add_contact(args, book: AddressBook):
    if len(args) < 2:
        raise ValueError("Usage: add [name] [phone]")
    name, phone = args
    record = book.find(name)
    message = "Contact updated."
    if record is None:
        record = Record(name)
        book.add_record(record)
        message = "Contact added."
    record.add_phone(phone)
    return message

@input_error
def change_contact(args, book: AddressBook):
    if len(args) < 2:
        raise ValueError("Usage: change [name] [new phone]")
    name, phone = args
    record = book.find(name)
    if record:
        record.phones = []
        record.add_phone(phone)
        return "Phone number updated for " + name + "."
    else:
        return "Contact not found."

@input_error
def show_phone(args, book: AddressBook):
    if len(args) < 1:
        raise ValueError("Usage: phone [name]")
    name = args[0]
    record = book.find(name)
    if record:
        phones = ", ".join([phone.value for phone in record.phones])
        return f"{name}'s phone number(s): {phones}."
    else:
        return f"Contact {name} not found."

@input_error
def show_all_contacts(book: AddressBook):
    if book.contacts:
        return "\n".join([f"{contact.name.value}: {', '.join([phone.value for phone in contact.phones])}" for contact in book.contacts])
    else:
        return "No contacts in the address book."

@input_error
def add_birthday(args, book):
    if len(args) < 2:
        raise ValueError("Usage: add-birthday [name] [birthday]")
    name, birthday = args
    record = book.find(name)
    if record:
        record.add_birthday(birthday)
        return f"Birthday added for {name}."
    else:
        return f"Contact {name} not found."

@input_error
def show_birthday(args, book):
    if len(args) < 1:
        raise ValueError("Usage: show-birthday [name]")
    name = args[0]
    record = book.find(name)
    if record and record.birthday:
        return f"{name}'s birthday is on {record.birthday.value.strftime('%d.%m.%Y')}."
    else:
        return f"No birthday found for {name}."

@input_error
def show_upcoming_birthdays(book):
    upcoming_birthdays = book.get_upcoming_birthdays()
    if upcoming_birthdays:
        return "Upcoming birthdays:\n" + "\n".join([f"{contact.name.value}: {greeting_date.strftime('%d.%m.%Y')}" for contact, greeting_date in upcoming_birthdays])
    else:
        return "No upcoming birthdays."

if __name__ == "__main__":
    main() 
