from ..errors.invalid_date_error import InvalidDateError

class Date():
    def __init__(self, value : str, strict: bool = True):
        # DD / MM / AAAA
        self.day, self.month, self.year = value.split("-")
        
    def __str__(self):
        return f"{self.day}-{self.month}-{self.year}"
    
    def __eq__(self, value):
        return self.self_to_dict() == value.self_to_dict()
    
    def self_to_dict(self):
        return {
            "day": self.day,
            "month": self.month,
            "year": self.year 
        }
        
    def self_validate(self, strict : bool = True):
        if not (self.day.isdigit() and self.month.isdigit() and self.year.isdigit()):
            if strict: raise InvalidDateError("Dia, mês e ano devem ser numéricos.")
            return False
        
        day = int(self.day)
        month = int(self.month)
        year = int(self.year)
        
        if strict:
            if len(self.day) != 2 or len(self.month) != 2 or len(self.year) != 4:
                raise InvalidDateError("Data deve estar no formato DD-MM-YYYY.")

        if not (1 <= month <= 12):
            if strict: raise InvalidDateError(f"Mês inválido: {month}.")
            return False
        
        def is_leap(y): 
            return y % 4 == 0 and (y % 100 != 0 or y % 400 == 0)

        DAY_PER_MONTH = {
            1: 31,
            2: 29 if is_leap(year) else 28,
            3: 31,
            4: 30,
            5: 31,
            6: 30,
            7: 31,
            8: 31,
            9: 30,
            10: 31,
            11: 30,
            12: 31,
        }

        if not (1 <= day <= DAY_PER_MONTH[month]):
            if strict:
                raise InvalidDateError(f"Dia inválido: {day} para o mês {month}.")
            return False

        return True