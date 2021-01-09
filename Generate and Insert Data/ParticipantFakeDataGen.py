import csv
from faker import Faker


def datagenerate(records, headers):
    fake = Faker('en_US')
    fake1 = Faker('en_GB')  
    with open("ParticipantData.csv", 'w', newline="") as csvFile:
        writer = csv.DictWriter(csvFile, fieldnames=headers)
        writer.writeheader()
        MId=0
        for i in range(records):
            full_name = fake.name()
            FLname = full_name.split(" ")
            Fname = FLname[0]
            Lname = FLname[1]
            domain_name = "@testDomain.com"
            userId = Fname + "." + Lname + domain_name
            MId=MId+1

            if MId % 5 == 0:
                Subscribed = "0"
            else:
                Subscribed = "1"

            if MId % 2 == 0:
                IntinMemb = "1"
            else:
                IntinMemb = "0"

            writer.writerow({
                    "Email Id": userId,
                    "First Name": Fname,
                    "Last Name": Lname,
                    "Subscribed": Subscribed,
                    "Interest in Membership": IntinMemb
                    })


if __name__ == '__main__':
    records = 400
    headers = ["Email Id", "First Name", "Last Name", "Subscribed", "Interest in Membership"]
    datagenerate(records, headers)
    print("CSV generation complete!")

