from collections import UserDict

class Field:
    def __init__(self, value):
        self.value = value

    def __str__(self):
        return str(self.value)

class Name(Field):
    def __init__(self, value):
        super().__init__(value)

class Phone(Field):
    def __init__(self, value):
        if not isinstance(value, str) or not value.isdigit() or len(value) != 10:
            raise ValueError("Invalid phone number format")
        super().__init__(value)

class Record:
    def __init__(self, name):
        self.name = Name(name)
        self.phones = []

    def add_phone(self, phone):
        self.phones.append(Phone(phone))

    def find_phone(self, target_phone):
        # ????? ?????? ???????? ? ??????
        found_phone = next((phone for phone in self.phones if phone.value == target_phone), None)
        return found_phone

    def remove_phone(self, phone):
        self.phones = [p for p in self.phones if p.value != phone]

    def edit_phone(self, old_phone, new_phone):
        for phone in self.phones:
            if phone.value == old_phone:
                phone.value = new_phone
                return  # Break out of the loop after updating the phone number

        raise ValueError(f"Phone number {old_phone} not found in the contact.")

    def edit_name(self, new_name):
        self.name = Name(new_name)

    def search_phone(self, phone):
        return phone in [p.value for p in self.phones]

    def __str__(self):
        return f"Contact name: {self.name.value}, phones: {'; '.join(p.value for p in self.phones)}"

class AddressBook(UserDict):
    def add_record(self, record):
        self.data[record.name.value] = record

    def find(self, name):
        return self.data.get(name)

    def delete(self, name):
        if name in self.data:
            del self.data[name]
            return True  # or you can return some indication of success
        else:
            print(f"No record found with name {name}")
            return False  # or raise an exception if you prefer

    def remove_record(self, name):
        del self.data[name]

    def search_records(self, keyword):
        return [record for record in self.data.values() if keyword.lower() in record.name.value.lower()]

    def add_phone_to_record(self, name, phone):
        # ????????? ???????? ?? ?????? ?? ??????
        if name in self.data:
            self.data[name].add_phone(phone)
        else:
            raise KeyError(f"No record found with name {name}")

    def remove_phone_from_record(self, name, phone):
        # ????????? ???????? ? ?????? ?? ??????
        if name in self.data:
            self.data[name].remove_phone(phone)
        else:
            raise KeyError(f"No record found with name {name}")

    def edit_record_name(self, old_name, new_name):
        # ??????????? ????? ??????
        if old_name in self.data:
            record = self.data.pop(old_name)
            record.edit_name(new_name)
            self.add_record(record)
        else:
            raise KeyError(f"No record found with name {old_name}")

    def search_phone(self, phone):
        # ????? ?????? ?? ??????? ????????
        return [record for record in self.data.values() if record.search_phone(phone)]
