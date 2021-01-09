import csv
from faker import Faker
import datetime
from random import randint
import random


def datagenerate(records, headers):
    fake = Faker('en_US')
    with open("MemberData.csv", 'w', newline='') as csvFile:
        writer = csv.DictWriter(csvFile, fieldnames=headers)
        writer.writeheader()
        MId=0

        for i in range(records):
            full_name = fake.name()
            FLname = full_name.split(" ")
            Fname = FLname[0]
            Lname = FLname[1]
            domain_name = "@testDomain.com"
            userId = Fname +"."+ Lname + domain_name
            MId=MId+1

            if MId % 4:
                IEEENumber = MId+96196145
            else:
                IEEENumber = "Null"

            if MId % 3 == 0:
                Status= "1"
            else:
                Status= "0"

            RegistrationDate = fake.date_between(start_date ='-10y', end_date='today')
            Number = randint(1000000000, 9999999999)
            if MId % 2 ==0:
                TrainingDate  = fake.date_between(start_date = RegistrationDate, end_date='today')
                                                  
            else:
                TrainingDate  = "Null"

            if MId % 10 == 0 and Status == "0":
                DeletionDate  = fake.date_between(start_date= RegistrationDate, end_date='today')
                                                  
            else:
                DeletionDate  = "Null"
                
            Gens=['A','B','C','D','E','F','G','H']

            if MId % 2 ==0:
                Generation = random.choice(Gens)
                                                  
            else:
                Generation  = "Null"
            Departments=[str(x) for x in range(19, 28)]
            Department = random.choice(Departments)
            
            RegYearUni = fake.date_between(start_date='-10y', end_date=RegistrationDate)
            Date1 = datetime.date(2015, 9, 25)
            if MId % 2 == 0:
                if RegYearUni>Date1:
                    UniGrade="Postraduate"                                      
            else:
                UniGrade  = "Undergraduate"
            
            writer.writerow({
                    "Member Id" : MId,
                    "First Name": Fname,
                    "Last Name": Lname,
                    "Email Id" : userId,
                    "Phone Number" : Number,
                    "IEEE Number" : IEEENumber,
                    "Status" : Status,
                    "Training Date" : TrainingDate,
                    "Generation" : Generation,
                    "Registration Date" : RegistrationDate,
                    "Deletion Date" : DeletionDate,
                    "Department" : Department,
                    "UniGrade" : UniGrade,
                    "RegYearUni" : RegYearUni
                    })
            
if __name__ == '__main__':
    records = 400
    headers = ["Member Id","First Name", "Last Name", "Email Id",  "Phone Number","IEEE Number","Status","Training Date","Generation","Registration Date","Deletion Date",
               "Department","UniGrade","RegYearUni"]
    datagenerate(records, headers)
    print("CSV generation complete!")

