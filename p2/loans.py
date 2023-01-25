
race_lookup = {
    "1": "American Indian or Alaska Native",
    "2": "Asian",
    "21": "Asian Indian",
    "22": "Chinese",
    "23": "Filipino",
    "24": "Japanese",
    "25": "Korean",
    "26": "Vietnamese",
    "27": "Other Asian",
    "3": "Black or African American",
    "4": "Native Hawaiian or Other Pacific Islander",
    "41": "Native Hawaiian",
    "42": "Guamanian or Chamorro",
    "43": "Samoan",
    "44": "Other Pacific Islander",
    "5": "White",
}


class Applicant:
    def __init__(self, age, race):
        self.age = age
        self.race = set()
        for r in race:
            if r in race_lookup:
                self.race.add(race_lookup[r])
    
    def __repr__(self):
        race = sorted(self.race)
        return f"Applicant({repr(self.age)}, {repr(race)})"
        
    def lower_age(self):
        age = self.age
        if '-' in age:
            age = int(age[:2])
        elif '<' or '>' in age:
            age = int(age[1:])
        return age
            
    
    def __lt__(self, other):
        return self.lower_age() < other.lower_age()


    

class Loan:
    def __init__(self, values):
        for key in values:
            if values[key] == 'NA' or values[key] == 'Exempt':
                values[key] = -1
        self.loan_amount = float(values["loan_amount"])
        self.property_value = float(values['property_value'])
        self.interest_rate = float(values['interest_rate'])
        self.applicants = []
        self.applicants.append(Applicant(values["applicant_age"],[values[f"applicant_race-{i}"] for i in range(1,6)]))
        if values["co-applicant_age"] != "9999":
            self.applicants.append(Applicant(values["co-applicant_age"],[values[f"co-applicant_race-{i}"] for i in range(1,6)]))
    
    def __str__(self):
        return f"<Loan: {self.interest_rate}% on ${self.property_value} with {len(self.applicants)} applicant(s)>"
    
    def __repr__(self):
        return f"<Loan: {self.interest_rate}% on ${self.property_value} with {len(self.applicants)} applicant(s)>"
    
    def yearly_amounts(self, yearly_payment):
        assert self.interest_rate > 0 and self.loan_amount > 0
        # TODO: assert interest and amount are positive
        amt = self.loan_amount

        while amt > 0:
            yield amt
            amt += (amt * (self.interest_rate*0.01))
            # TODO: add interest rate multiplied by amt to amt
            amt -= yearly_payment
            # TODO: subtract yearly payment from amt
            
        
class Bank:
    def __init__(self, other):
        import json
        import csv
        import io
        from zipfile import ZipFile
        from io import TextIOWrapper
        f = open("banks.json")
        data = json.load(f)
        f.close()
        self.loan = []
        for elem in data:
            if elem['name'] == other:
                self.lei = elem['lei']
        with ZipFile('wi.zip') as zf:
            with zf.open('wi.csv') as w:
                for row in csv.DictReader(io.TextIOWrapper(w)):
                    if row['lei'] == self.lei:
                        self.loan.append(Loan(row))
    
    def __getitem__(self, index):
        return self.loan[index]
    
    def __len__(self):
        return len(self.loan)



