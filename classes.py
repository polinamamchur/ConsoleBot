from collections import UserDict
import datetime


class Field:
    def __init__(self, value):
        self.value = value

    def validate(self):
        pass

    def __str__(self):
        return str(self.value)


class Phone(Field):
    def __init__(self, value):
        super().__init__(value)
        self.validate()

    def validate(self):
        if not isinstance(self.value, str) or not self.value.isdigit() or len(self.value) != 10:
            raise ValueError("Invalid phone number format")

    @property
    def value(self):
        return self._value

    @value.setter
    def value(self, value):
        self._value = value
        self.validate()


class Birthday(Field):
    def __init__(self, value):
        super().__init__(value)
        self.validate()

    def validate(self):
        try:
            datetime.datetime.strptime(str(self.value), '%Y-%m-%d')
        except ValueError:
            raise ValueError("Incorrect birthday format, should be YYYY-MM-DD")

    @property
    def value(self):
        return self._value

    @value.setter
    def value(self, value):
        if isinstance(value, datetime.date):
            self._value = value
        elif isinstance(value, str):
            self._value = datetime.datetime.strptime(value, '%Y-%m-%d').date()
        else:
            raise ValueError("Invalid birthday format")

        self.validate()



class Record:
    def __init__(self, name, birthday=None):
        self.name = Field(name)
        self.phones = []
        self.birthday = birthday

    def add_phone(self, phone):
        self.phones.append(Phone(phone))

    def find_phone(self, target_phone):
        found_phone = next((phone for phone in self.phones if phone.value == target_phone), None)
        return found_phone

    def remove_phone(self, phone):
        self.phones = [p for p in self.phones if p.value != phone]

    def edit_phone(self, old_phone, new_phone):
        for phone in self.phones:
            if phone.value == old_phone:
                phone.value = new_phone
                return
        raise ValueError(f"Phone number {old_phone} not found in the contact.")

    def edit_name(self, new_name):
        self.name = Field(new_name)

    def search_phone(self, phone):
        return phone in [p.value for p in self.phones]

    def days_to_birthday(self):
        if not self.birthday:
            return None
        today = datetime.date.today()
        next_birthday = datetime.date(today.year, self.birthday.month, self.birthday.day)
        if next_birthday < today:
            next_birthday = next_birthday.replace(year=today.year + 1)
        delta = next_birthday - today
        return delta.days

    @property
    def name(self):
        return self._name.value

    @name.setter
    def name(self, value):
        self._name = Field(value)

    @property
    def birthday(self):
        return self._birthday.value if self._birthday else None

    @birthday.setter
    def birthday(self, value):
        if value:
            self._birthday = Birthday(value)
        else:
            self._birthday = None


class AddressBook(UserDict):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.page_size = 5

    def add_record(self, record):
        self.data[record.name.value] = record

    def find(self, name):
        return self.data.get(name)

    def delete(self, name):
        if name in self.data:
            del self.data[name]
            return True
        else:
            print(f"No record found with name {name}")
            return False

    def remove_record(self, name):
        del self.data[name]

    def search_records(self, keyword):
        return [record for record in self.data.values() if keyword.lower() in record.name.value.lower()]

    def add_phone_to_record(self, name, phone):
        if name in self.data:
            self.data[name].add_phone(phone)
        else:
            raise KeyError(f"No record found with name {name}")

    def remove_phone_from_record(self, name, phone):
        if name in self.data:
            self.data[name].remove_phone(phone)
        else:
            raise KeyError(f"No record found with name {name}")

    def edit_record_name(self, old_name, new_name):
        if old_name in self.data:
            record = self.data.pop(old_name)
            record.edit_name(new_name)
            self.add_record(record)
        else:
            raise KeyError(f"No record found with name {old_name}")

    def search_phone(self, phone):
        return [record for record in self.data.values() if record.search_phone(phone)]

    def __iter__(self):
        self._iter_keys = list(self.data.keys())
        self._iter_index = 0
        return self

    def __next__(self):
        if self._iter_index >= len(self._iter_keys):
            raise StopIteration
        record = self.data[self._iter_keys[self._iter_index]]
        self._iter_index += 1
        return record

    def paginate(self):
        num_pages = len(self.data) // self.page_size + (1 if len(self.data) % self.page_size > 0 else 0)
        for page_num in range(num_pages):
            start_index = page_num * self.page_size
            end_index = min(start_index + self.page_size, len(self.data))
            yield [self.data[key] for key in list(self.data.keys())[start_index:end_index]]


address_book = AddressBook()

record1 = Record("John Doe", "1990-05-20")
record1.add_phone("1234567890")
record1.add_phone("9876543210")
address_book.add_record(record1)

record2 = Record("Alice Smith", "1985-10-15")
record2.add_phone("5551234567")
address_book.add_record(record2)


record3 = Record("Emma Johnson", "1992-08-30")
record3.add_phone("1112223333")
address_book.add_record(record3)

record4 = Record("Michael Brown", "1980-03-14")
record4.add_phone("4445556666")
record4.add_phone("7778889999")
address_book.add_record(record4)

record5 = Record("Sophia Garcia", "1995-11-25")
record5.add_phone("1231231234")
record5.add_phone("4564564567")
record5.add_phone("7897897890")
address_book.add_record(record5)

record6 = Record("James Lee", "1988-06-10")
record6.add_phone("3213213210")
record6.add_phone("6546546540")
record6.add_phone("9879879870")
address_book.add_record(record6)


for page_number, page_records in enumerate(address_book.paginate(), start=1):
    print(f"Page {page_number}:")
    for record in page_records:
        print(record.name)


print(f'Days to birtday: {record1.days_to_birthday()}')




