from collections import UserDict
import re
from datetime import datetime, timedelta
from colorama import Fore, Style



class Field:
    def __init__(self, value):
        self.value = value

    def __str__(self):
        return str(self.value)


class Name(Field):
    def __init__(self, name):
        super().__init__(name)


class Phone(Field):
    def __init__(self, phone_number):
        if not re.fullmatch(r"\d{10}", phone_number):
            raise ValueError("Phone number must be 10 digits.")
            return
        super().__init__(phone_number)


class Email(Field):
    def __init__(self, email):
        if not re.fullmatch(r"[^@]+@[^@]+\.[^@]+", email):
            raise ValueError("Invalid email format.")
        super().__init__(email)


class Address(Field):
    pass


class Birthday(Field):
    def __init__(self, value):
        try:
            self.value = datetime.strptime(value, "%d.%m.%Y").date()
        except ValueError:
            raise ValueError("Invalid date format. Use DD.MM.YYYY")
        super().__init__(self.value)


class Note:
    def __init__(self, text):
        self.text = text

    def __str__(self):
        return self.text


class Record:
    def __init__(self, name, address=None, phones=None, email=None, birthday=None):
        self.name = Name(name)
        self.address = Address(address) if address else None
        self.phones = phones if phones else []
        self.email = Email(email) if email else None
        self.birthday = Birthday(birthday) if birthday else None


    def add_phone(self, phone):
        new_phone = Phone(str(phone))
        if any(p.value == new_phone.value for p in self.phones):
            return f"{Fore.MAGENTA}Phone {phone} already exists for {self.name.value}.{Style.RESET_ALL}"
        self.phones.append(new_phone)
        return f"{Fore.GREEN}Phone {phone} added to {self.name.value}.{Style.RESET_ALL}"
        return [p.value for p in self.phones]

    # TODO: Implement remove_phone method
    # def remove_phone(self, phone):
    #     for p in self.phones:
    #         if p.value == phone:
    #             self.phones.remove(p)
    #             return f"{Fore.RED}Phone {phone} removed.{Style.RESET_ALL}"
    #     raise ValueError("Phone not found.")

    # TODO: Implement edit_phone method
    # def edit_phone(self, old_phone, new_phone):
    #     for idx, p in enumerate(self.phones):
    #         if p.value == old_phone:
    #             self.phones[idx] = Phone(new_phone)
    #             return f"{Fore.YELLOW}Phone {old_phone} changed to {new_phone}.{Style.RESET_ALL}"

    def add_email(self, email):
        self.email = Email(email)
        return f"Email {email} added to {self.name.value}."

    def add_address(self, address):
        self.address = Address(address)
        return f"Address {address} added to {self.name.value}."

    def add_birthday(self, birthday):
        self.birthday = Birthday(birthday)
        return f"Birthday {birthday} added to {self.name.value}."

    def __str__(self):
        phones = "; ".join(p.value for p in self.phones)
        birthday = (
            self.birthday.value.strftime("%d.%m.%Y")
            if self.birthday
            else "No birthday set"
        )
        email = self.email.value if self.email else "No email set"
        address = self.address.value if self.address else "No address set"
        return f"Contact name: {self.name.value}, phones: {phones}, birthday: {birthday}, email: {email}, address: {address}"


class AddressBook(UserDict):
    def add_record(self, record):
        self.data[record.name.value] = record

    def find(self, name):
        if name in self.data:
            return self.data[name]
        raise KeyError(f"Record for {name} not found.")

    def delete(self, name):
        if name in self.data:
            del self.data[name]
            return f"Record for {name} deleted."
        raise KeyError(f"Record for {name} not found.")

    def get_upcoming_birthdays(self, days=7):
        today = datetime.today().date()
        upcoming_birthdays = []

        for record in self.data.values():
            if record.birthday:
                birthday = record.birthday.value
                birthday_this_year = datetime(
                    today.year, birthday.month, birthday.day
                ).date()

                if birthday_this_year < today:
                    birthday_this_year = datetime(
                        today.year + 1, birthday.month, birthday.day
                    ).date()

                days_before_birthday = (birthday_this_year - today).days

                if days_before_birthday <= days:
                    upcoming_birthdays.append(record.name.value)

        return upcoming_birthdays


class NoteBook(UserDict):
    def add_record(self, note):
        self.data[len(self.data) + 1] = note

    def search(self, text):
        return [note for note in self.data.values() if text in note.text]

    def delete(self, note_id):
        if note_id in self.data:
            del self.data[note_id]
            return f"Note {note_id} deleted."
        raise KeyError(f"Note {note_id} not found.")
