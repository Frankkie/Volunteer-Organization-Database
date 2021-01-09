import csv
from faker import Faker
import datetime
from random import randint
import random

def datagenerate(records, headers):
    fake = Faker('en_US')
    fake1 = Faker('en_GB')  
    with open("ContactData.csv", 'wt', newline ="") as csvFile:
        writer = csv.DictWriter(csvFile, fieldnames=headers)
        writer.writeheader()
        CId=0
        for i in range(records):
            full_name = fake.name()
            FLname = full_name.split(" ")
            Fname = FLname[0]
            Lname = FLname[1]
            domain_name = "@testDomain.com"
            userId = Fname +"."+ Lname + domain_name
            CId=CId+1
            RegistrationDate = fake.date_between(start_date='-10y', end_date='today')
            Number = randint(1000000000, 9999999999)
            Departments=[str(x) for x in range(19, 28)]
            if CId % 10 ==0:
                Department = random.choice(Departments)
            else:
                Department = 'Null'
            IEEEPoss=['SSR','Councelor','Advisor','Section Chair','Section Treasurer']
            if CId % 20 ==0:
                IEEEPos = random.choice(IEEEPoss)
            else:
                IEEEPos = 'Null'
            fields = [str(x) for x in range(23,35)]
            field = random.choice(fields)
            writer.writerow({
                    "Contact Id" : CId,
                    "Email Id" : userId,
                    "Phone Number" : Number,
                    "First Name": Fname,
                    "Last Name": Lname,
                    "Address": fake.street_address(),
                    "Registration Date": RegistrationDate,
                    "IEEE Position": IEEEPos,
                    "Field": field,
                    "Department" : Department
                    })


if __name__ == '__main__':
    records = 200
    headers = ["Contact Id", "Email Id", "Phone Number", "First Name", "Last Name",
               "Address", "Registration Date", "IEEE Position", "Field", "Department"]
    datagenerate(records, headers)
    print("CSV generation complete!")

  
