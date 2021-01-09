import random
import csv
import insert_data as indata
from faker import Faker


def gen_heads_supers_participates():

    headers = ["Member Id", "Team Id", "Title", "Start Date", "End Date"]
    members = indata.read_csv("MemberData.csv")
    teams = [str(x) for x in range(1, 21)]
    id = 0
    status = 6
    train = 7
    reg = 9
    delet = 10
    participates = []
    heads = []
    supervises = []

    # Committee Members
    for member in members:
        mid = member[id]
        if member[status]:
            teamsset = set()
            for i in range(random.randint(0,5)):
                teamsset.add(random.choice(teams))
            for t in teamsset:
                participates.append({"Member Id":str(mid), "Team Id":str(t),
                                    "Title":"Member", "Start Date":member[reg], "End Date":"None"})

    # Committee Heads
    for t in teams:
        mid = random.choice(members)[id]
        heads.append({"Member Id": str(mid), "Team Id": str(t),
                             "Title": "Team Head", "Start Date": members[mid-1][reg], "End Date": "None"})
        mid = random.choice(members)[id]
        supervises.append({"Member Id": str(mid), "Team Id": str(t),
                            "Title": "Team Supervisor", "Start Date": members[mid-1][reg], "End Date": "None"})

    with open("participates.csv", 'w', newline='') as csvFile:
        writer = csv.DictWriter(csvFile, fieldnames=headers)
        writer.writeheader()
        for d in participates:
            writer.writerow(d)

    with open("heads.csv", 'w', newline='') as csvFile:
        writer = csv.DictWriter(csvFile, fieldnames=headers)
        writer.writeheader()
        for d in heads:
            writer.writerow(d)

    with open("supervises.csv", 'w', newline='') as csvFile:
        writer = csv.DictWriter(csvFile, fieldnames=headers)
        writer.writeheader()
        for d in supervises:
            writer.writerow(d)

    return


def gen_attends():

    headers = ['Participant Email', 'Event Title', 'Event Date']
    participants = indata.read_csv("ParticipantData.csv")
    events = indata.read_csv("events.csv")
    attends = []

    for p in participants:
        pemail = p[0]
        eventset = set()
        for i in range(random.randint(0,5)):
            eventset.add(random.randint(0,5))
        for t in eventset:
            attends.append({'Participant Email':pemail, 'Event Title':events[t][0], 'Event Date':events[t][1]})

    with open("attends.csv", 'w', newline='') as csvFile:
        writer = csv.DictWriter(csvFile, fieldnames=headers)
        writer.writeheader()
        for d in attends:
            writer.writerow(d)

    return


def gen_hascontact():
    headers = ['Team Id', 'Contact Id']
    teams = [str(x) for x in range(1, 22)]
    contacts = [str(x) for x in range(1, 201)]
    rows = []

    for elem in contacts:
        teamset = set()
        for i in range(random.randint(1, 3)):
            teamset.add(random.choice(teams))
        for t in teamset:
            rows.append({'Team Id': t, 'Contact Id': elem})

    with open("hascontact.csv", 'w', newline='') as csvFile:
        writer = csv.DictWriter(csvFile, fieldnames=headers)
        writer.writeheader()
        for d in rows:
            writer.writerow(d)
    return


def gen_contributesto():
    headers = ['Event Title', 'Event Date', 'Contact Id']
    events = indata.read_csv("events.csv")
    contacts = [str(x) for x in range(1, 201)]
    rows = []

    for elem in events:
        conset = set()
        for i in range(random.randint(1, 2)):
            conset.add(random.choice(contacts))
        for t in conset:
            rows.append({'Event Title': elem[0], 'Event Date': elem[1], 'Contact Id': t})

    with open("contributesto.csv", 'w', newline='') as csvFile:
        writer = csv.DictWriter(csvFile, fieldnames=headers)
        writer.writeheader()
        for d in rows:
            writer.writerow(d)
    return


def gen_contributions(num):
    headers = ['Contribution Id', 'Given By', 'Date', 'Type', 'Package', 'Stored In']
    contacts = [str(x) for x in range(1, 201)]
    rows = []
    fake = Faker('en_US')
    for elem in range(1, num+1):
        cont = random.choice(contacts)
        rows.append({'Contribution Id': elem,
                     'Given By': cont,
                     'Date': str(fake.date_between(start_date='-10y', end_date='today')) + " 12:00:00",
                     'Type': random.choice(["In Kind", "Money"]),
                     'Package': random.choice(["Golden", "Silver", "Bronze"]),
                     'Stored In': random.choice(["Office 1", "Office 2"])})

    with open("contributions.csv", 'w', newline='') as csvFile:
        writer = csv.DictWriter(csvFile, fieldnames=headers)
        writer.writeheader()
        for d in rows:
            writer.writerow(d)
    return


def gen_purchases(num):
    headers = ['Purchase Id', 'Purchased By', 'Date', 'Type', 'Cost', 'Stored In']
    contacts = [str(x) for x in range(1, 201)]
    rows = []
    fake = Faker('en_US')
    for elem in range(1, num+1):
        cont = random.choice(contacts)
        rows.append({'Purchase Id': elem,
                     'Purchased By': cont,
                     'Date': str(fake.date_between(start_date='-10y', end_date='today')) + " 12:00:00",
                     'Type': random.choice(["Merchandise", "Equipment", "Supplies"]),
                     'Cost': str(random.randint(20, 500)),
                     'Stored In': random.choice(["Office 1", "Office 2"])})

    with open("purchases.csv", 'w', newline='') as csvFile:
        writer = csv.DictWriter(csvFile, fieldnames=headers)
        writer.writeheader()
        for d in rows:
            writer.writerow(d)
    return


if __name__ == "__main__":
    gen_contributions(30)
    gen_purchases(50)

