from collections import UserDict
from datetime import datetime, timedelta

class ValidationError(Exception):
    def __init__(self, message):
        super().__init__(message)

def validate_phone(func):
    def wrapper(*args, **kwargs):
        value = args[1]
        if not value.isdigit() or len(value) != 10:
            raise ValidationError("Incorrect phone format")
        return func(*args, **kwargs)
    return wrapper

def validate_birthday(func):
    def wrapper(*args, **kwargs):
        value = args[1]
        try:
           datetime.strptime(value, '%d.%m.%Y')
        except Exception:
            raise ValidationError("Incorrect date format. Use DD.MM.YYYY.")
        return func(*args, **kwargs)
    return wrapper

class Field:
    def __init__(self, value):
        self.value = value

    def __str__(self):
        return str(self.value)

class Name(Field):
    pass

class Birthday(Field):
    @validate_birthday
    def __init__(self, value):
        super().__init__(datetime.strptime(value, "%d.%m.%Y"))
    

class Phone(Field):
    @validate_phone
    def __init__(self, value):
        super().__init__(value)

class Record:
    def __init__(self, name, birthday=None):
        self.name = Name(name)
        self.phones = []
        self.birthday = birthday
        
        if birthday is not None:
            self.birthday = Birthday(birthday)

    def add_phone(self, phone) -> 'Record':
        self.phones.append(Phone(phone))
        
        return self

    def delete_phones(self) -> 'Record':
        self.phones = []
        return self

    def delete_phone(self, phone_for_delete):
        self.phones = [phone for phone in self.phones if phone.value != phone_for_delete]

    def edit_phone(self, old_phone, new_phone):
        self.delete_phone(old_phone)
        self.add_phone(new_phone)

    def find_phone(self, search_phone):
        for phone in self.phones:
            if phone.value == search_phone:
                return phone.value
        return None
    
    def print_phones(self) -> str:
        return  f"phones: {'; '.join(phone.value for phone in self.phones)}"
    
    def add_birthday(self, birthday) -> 'Record':
        self.birthday = Birthday(birthday)
        return self
    
    def show_birthday(self):
        print(self.birthday.value.strftime("%d.%m.%Y"))
    
    def has_birthday(self) -> bool:
        return self.birthday != None
    
    def __str__(self):
        return f"Contact name: {self.name.value}, birthday: {self.birthday} phones: {'; '.join(phone.value for phone in self.phones)}"

class AddressBook(UserDict):
    def add_record(self, record: Record) -> None:
        self.data[record.name.value] = record

    def delete(self, name: str) -> None:
        del self.data[name]

    def find(self, name: str) -> Record|None:
        return self.data.get(name, None)
    
    def get_birthdays_per_week(self) -> dict:
        today = datetime.now()
        start_day = today + timedelta(days=1)
        end_day = start_day + timedelta(days=7)
        
        birth_week = {day: [] for day in ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday']}
        
        for name, record in self.data.items():
            if record.has_birthday():
                contact_birthday = record.birthday.value.replace(year=today.year)
            
                if contact_birthday.month == 2 and contact_birthday.day == 29 and not today.year % 4 == 0:
                    contact_birthday = contact_birthday.replace(day=28)
                if start_day <= contact_birthday < end_day:
                    if contact_birthday.weekday() == 5 or contact_birthday.weekday() == 6:
                        birth_day = 'Monday'
                    else:
                        birth_day = contact_birthday.strftime('%A')
                    birth_week[birth_day].append(name)
           
        return birth_week                
