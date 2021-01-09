import pandas as pd
from PIL import Image
import streamlit as st
import pymysql as sql


def connect():
    host_ = '150.140.186.221'
    user_ = 'db20_up1053706'
    psw_ = 'up1053706'
    db_ = 'project_db20_up1053706'
    connection = sql.connect(host=host_, user=user_, password=psw_, db=db_)
    cursor = connection.cursor()
    return connection, cursor


def disconnect(connection, cursor):
    cursor.close()
    connection.close()


def query(sql_command, cursor):
    cursor.execute(sql_command)
    result = []
    field_names = [i[0] for i in cursor.description]
    for row in cursor:
        result.append(row)

    result = pd.DataFrame.from_records(result)
    result.columns = field_names
    result = result.assign(hack='').set_index('hack')
    return result


@st.cache
def load_image(source):
    image = Image.open(source)
    return image


def sidebar():
    with st.sidebar:
        st.image(load_image("logo.png"), use_column_width=True)
        tab = st.radio("Select a tab", ("Overview", "Members", "Teams", "Events & Projects",
                                        "Contacts", "Attendees", "Financial"))
        return tab


def turn_to_query_str(list_obj):
    result = ""
    for item in list_obj:
        result += " `" + item + "`,"
    result = result[:-1]
    return result

#######################################################################################################################


conn, curs = connect()

selected_tab = sidebar()
if selected_tab == "Overview":
    st.title("Volunteer Organization 🗄️: An Overview")
    st.text("")
    q = """ SELECT COUNT(*) AS `C` FROM `Member` WHERE `Deletion Date` IS NULL"""
    res = query(q, curs)
    st.subheader("👉 " + str(res.iloc[0]["C"]) + " Member Registrations")

    q = """ SELECT COUNT(*) AS `C` FROM `Member` 
            WHERE (`Deletion Date` IS NULL AND `Activity Status` = 1)"""
    res = query(q, curs)
    st.subheader("👉 " + str(res.iloc[0]["C"]) + " Active Members")

    q = """ SELECT COUNT(*) AS `C` FROM `Member` 
                WHERE (`Deletion Date` IS NULL AND `Activity Status` = 1 AND `Training Date` IS NOT NULL)"""
    res = query(q, curs)
    st.subheader("👉 " + str(res.iloc[0]["C"]) + " Active Volunteers")
    st.text("i.e. Members who actively participate in teams,\n"
            "events and projects, and who have trained as volunteers.")

    q = """ SELECT COUNT(*) AS `C` FROM `Member` 
                    WHERE (`Deletion Date` IS NULL AND `Activity Status` = 1 
                            AND `Training Date` IS NOT NULL AND `IEEE Number` IS NOT NULL)"""
    res = query(q, curs)
    st.subheader("👉 " + str(res.iloc[0]["C"]) + " Full Members")
    st.text("i.e. Active Volunteers who are also IEEE Members.")

    q = """ SELECT COUNT(*) AS `C` FROM `Member` 
                        WHERE (`Deletion Date` IS NOT NULL
                                AND `Training Date` IS NOT NULL)"""
    res = query(q, curs)
    st.subheader("👉 " + str(res.iloc[0]["C"]) + " Alumni")
    st.text("i.e. Past Active Volunteers.")

    q = """ SELECT COUNT(*) AS `C` FROM `Team`"""
    res = query(q, curs)
    st.subheader("👉 " + str(res.iloc[0]["C"]) + " Teams")

    q = """ SELECT COUNT(*) AS `C` FROM `Attends`"""
    res = query(q, curs)
    st.subheader("👉 " + str(res.iloc[0]["C"]) + " Attendees in Events")

    q = """ SELECT COUNT(*) AS `C` FROM `Contact`"""
    res = query(q, curs)
    st.subheader("👉 " + str(res.iloc[0]["C"]) + " Contacts")

elif selected_tab == "Members":
    st.title("Members Tab")
    ##################################################
    st.header("Members Catalogue")
    columns = ["First Name", "Last Name"]
    category = st.selectbox("Categories to display:", ("All Members", "Active Members",
                                                       "Active Volunteers", "Full Members", "Alumni"))
    columns += st.multiselect("Columns:", ("Email", "Phone", "Activity Status", "Registration Date",
                                           "Training Date", "IEEE Number", "Univ Grade",
                                           "Reg Year to Univ", "Studies at"))
    order_by = st.multiselect("Order By:", columns)
    if not order_by:
        order_by = ["Id"]
    pressed = st.button("Run Query")
    where = ""
    if category == "All Members":
        where = """WHERE `Deletion Date` IS NULL"""
    elif category == "Active Members":
        where = """WHERE (`Deletion Date` IS NULL AND `Activity Status` = 1)"""
    elif category == "Active Volunteers":
        where = """WHERE (`Deletion Date` IS NULL AND `Activity Status` = 1 AND `Training Date` IS NOT NULL)"""
    elif category == "Full Members":
        where = """WHERE (`Deletion Date` IS NULL AND `Activity Status` = 1 
                          AND `Training Date` IS NOT NULL AND `IEEE Number` IS NOT NULL)"""
    elif category == "Alumni":
        where = """WHERE (`Deletion Date` IS NOT NULL
                                AND `Training Date` IS NOT NULL)"""

    if pressed:
        st.button("Hide List")

        if "Studies at" not in columns:
            q = """
                    SELECT """ + turn_to_query_str(columns) + """
                    FROM `Member` 
                    """ + where + """
                    ORDER BY """ + turn_to_query_str(order_by)
        else:
            columns.pop(columns.index("Studies at"))
            q = """
                    SELECT """ + turn_to_query_str(columns) + """, 
                    `University Department`.`Department Name` AS `Studies at`
                    FROM (`Member` JOIN `University Department` ON 
                    `Member`.`Studies at` = `University Department`.`Department Id`)
                    """ + where + """
                    ORDER BY """ + turn_to_query_str(order_by)

        res = query(q, curs)
        st.table(res)
    ########################################################
    st.header("Categories Overview")
    category = st.selectbox("Categories to display:", ("Studies at", "Univ Grade", "Reg Year to Univ",
                                                       "Generation", "Team"))
    pressed_2 = st.button("Run Query", key=1)
    if pressed_2:
        st.button("Hide List", key=1)
        if category == "Studies at":
            q = """
                    SELECT `Department Name` , count(*) AS `Num of Members`
                    FROM `Member` JOIN `University Department`
                    On Member.`Studies at` = `University Department`.`Department Id`
                    GROUP BY `Department Id`
                    """
        if category == "Univ Grade":
            q = """
                    SELECT `Univ Grade`, count(*) AS `Num of Members`
                    FROM `Member`
                    GROUP BY `Univ Grade`
                    ORDER BY `Univ Grade` DESC
                    """
        if category == "Reg Year to Univ":
            q = """
                    SELECT 2021 - `y` AS `In Year`, count(*) AS `Num of Members`
                    FROM (Select `Id`, YEAR(`Reg Year to Univ`) AS `y` from Member) AS `YEARS`
                    GROUP BY `YEARS`.y
                    ORDER BY `YEARS`.y
                    """
        if category == "Generation":
            q = """
                    SELECT `Generation`, count(*) AS `Num of Members`
                    FROM `Member`
                    WHERE `Generation` IS NOT NULL
                    GROUP BY `Generation`
                    ORDER BY `Generation`
                    """
        if category == "Team":
            q = """
                    SELECT Team.`Team Name` , count(*) AS `Num of Members`
                    FROM `Participates In` JOIN Team ON `Participates In`.`Team Id`=`Team`.`Team Id`
                    GROUP BY `Team`.`Team Id`
                    """
        res = query(q, curs)
        st.table(res)

elif selected_tab == "Teams":
    st.title("Teams Tab")
    st.header("Teams Catalogue")

    types = query("""SELECT DISTINCT `Team Type` FROM `Team`""", curs)
    types = types.values.tolist()
    options = ["All Types"]
    for t in types:
        options.append(t[0])
    category = st.selectbox("Select a Team Type:", tuple(options))
    p1 = st.button("Run Query", key=1)
    if p1:
        st.button("Hide List")
        if category == "All Types":
            q = """
                    SELECT `Team Name`, `Team Type`, `IEEE Code`, `Field`.`Field Name` AS `Team's Field`
                    FROM (`Team` JOIN `Field` ON Team.Field = Field.`Field Id`)
                    """
        else:
            q = """
                    SELECT `Team Name`, `IEEE Code`, `Field`.`Field Name` AS `Team's Field`
                    FROM (`Team` JOIN `Field` ON Team.Field = Field.`Field Id`)
                    WHERE (`Team Type` = '""" + category + """')"""
        res = query(q, curs)
        st.table(res)

###############################################################
    st.header("Organization's Roster")
    teams = query("""SELECT `Team Name` FROM `Team`""", curs)
    teams = teams.values.tolist()
    options = []
    for t in teams:
        options.append(t[0])
    teamname = st.selectbox("Select a Team:", tuple(options))
    p2 = st.button("Run Query", key=2)
    if p2:
        st.button("Hide List")
        st.subheader("Team Supervisor")
        q = """ SELECT `First Name`, `Last Name`, `Title`, `Start Date`, `Email`, `Phone`
                        FROM ( `Member` JOIN 
                        (SELECT `Member Id`, `Title`, `Start Date` 
                        FROM (`Team` JOIN `Supervises` AS `P I` on Team.`Team Id` = `P I`.`Team Id`)
                        WHERE (`Team Name` = '""" + teamname + """' AND `End Date` IS NULL)) AS `Team Members` 
                        ON `Member`.`Id` = `Team Members`.`Member Id`)
                        """
        res = query(q, curs)
        st.table(res)
        st.subheader("Team Head")
        q = """ SELECT `First Name`, `Last Name`, `Title`, `Start Date`, `Email`, `Phone`
                                FROM ( `Member` JOIN 
                                (SELECT `Member Id`, `Title`, `Start Date` 
                                FROM (`Team` JOIN `Heads` AS `P I` on Team.`Team Id` = `P I`.`Team Id`)
                                WHERE (`Team Name` = '""" + teamname + """' AND `End Date` IS NULL)) AS `Team Members` 
                                ON `Member`.`Id` = `Team Members`.`Member Id`)
                                """
        res = query(q, curs)
        st.table(res)
        st.subheader("Team Members")
        q = """ SELECT `First Name`, `Last Name`, `Title`, `Start Date`, `Email`, `Phone`
                FROM ( `Member` JOIN 
                (SELECT `Member Id`, `Title`, `Start Date` 
                FROM (`Team` JOIN `Participates In` AS `P I` on Team.`Team Id` = `P I`.`Team Id`)
                WHERE (`Team Name` = '""" + teamname + """' AND `End Date` IS NULL)) AS `Team Members` 
                ON `Member`.`Id` = `Team Members`.`Member Id`)
                """
        res = query(q, curs)
        st.table(res)

###############################################################
    st.header("Heads")
    p3 = st.button("Run Query", key=3)
    if p3:
        st.button("Hide List")
        q = """ SELECT `Team Name`, `First Name`, `Last Name`, `Start Date`, `Email`, `Phone`
                FROM ( `Member` JOIN 
                (SELECT `Member Id`, `Start Date`, `Team Name` 
                FROM (`Team` JOIN `Heads` AS `P I` on Team.`Team Id` = `P I`.`Team Id`)
                WHERE (`End Date` IS NULL)) AS `Team Members` 
                ON `Member`.`Id` = `Team Members`.`Member Id`)
                ORDER BY `Team Name`
                """
        res = query(q, curs)
        st.table(res)

###############################################################
    st.header("Supervisors")
    p4 = st.button("Run Query", key=4)
    if p4:
        st.button("Hide List")
        q = """ SELECT `Team Name`, `First Name`, `Last Name`, `Start Date`, `Email`, `Phone`
                FROM ( `Member` JOIN 
                (SELECT `Member Id`, `Start Date`, `Team Name` 
                FROM (`Team` JOIN `Supervises` AS `P I` on Team.`Team Id` = `P I`.`Team Id`)
                WHERE (`End Date` IS NULL)) AS `Team Members` 
                ON `Member`.`Id` = `Team Members`.`Member Id`)
                ORDER BY `Team Name`
                """
        res = query(q, curs)
        st.table(res)

elif selected_tab == "Events & Projects":
    st.title("Events & Projects Tab")
    st.header("Events Catalogue")
    p1 = st.button("Show Events")
    if p1:
        st.button("Hide List")
        q = """ SELECT `Event Title`, `Event Date`, `Team Name`, `Event Type`, `Place`
                FROM (`Event` JOIN Team ON Event.`Organized By` = Team.`Team Id`)
                ORDER BY `Event Date`"""
        res = query(q, curs)
        st.table(res)

    st.header("Projects Catalogue")
    p2 = st.button("Show Projects")
    if p2:
        st.button("Hide List")
        q = """ SELECT `Project Title`, `Start Date`, `End Date`
                FROM `Project`"""
        res = query(q, curs)
        st.table(res)

    st.header("Contributors")
    p3 = st.button("Show Contributors")
    if p3:
        st.button("Hide List")
        q = """ SELECT `First Name`, `Last Name`, `Contact Email`, Phone, `Event Title`, `Event Date`
                FROM (`Contributes to Event` JOIN Contact AS C 
                      on `Contributes to Event`.`Contact Id` = C.`Contact Id`)"""
        res = query(q, curs)
        st.table(res)

elif selected_tab == "Contacts":
    st.title("Contacts Tab")
    st.header("Contacts Catalogue")

    category = st.selectbox("Select a Team Type:", ("All Contacts", "Vendors", "Sponsors", "Contributors to Events",
                                                    "Professors", "IEEE Members"))
    p1 = st.button("Run Query", key=1)
    q = ""
    if p1:
        st.button("Hide List")
        if category == "All Contacts":
            q = """
                        SELECT `First Name`, `Last Name`, `Phone`, `Address`, `Date Created`, F.`Field Name`
                        FROM (`Contact` JOIN Field AS F on Contact.Field = F.`Field Id`)
                        """
        elif category == "Professors":
            q = """
                    SELECT `First Name`, `Last Name`, `Phone`, `Address`, `Date Created`, `U D`.`Department Name`
                    FROM (`Contact` JOIN `University Department` `U D` 
                          on Contact.`Uni Department` = `U D`.`Department Id`)
                    """
        elif category == "Sponsors":
            q = """
                    SELECT `First Name`, `Last Name`, `Phone`, `Address`, `Date Created`
                    FROM `Contact`
                    WHERE `Contact Id` IN (SELECT DISTINCT `Given By` FROM `Contribution`)
                    """
        elif category == "Vendors":
            q = """
                    SELECT `First Name`, `Last Name`, `Phone`, `Address`, `Date Created`
                    FROM `Contact`
                    WHERE `Contact Id` IN (SELECT DISTINCT `Purchased by` FROM `Purchase`)
                    """
        elif category == "Contributors to Events":
            q = """
                    SELECT `First Name`, `Last Name`, `Phone`, `Address`, `Date Created`, `U D`.`Department Name`
                    FROM (`Contact` LEFT JOIN `University Department` `U D` 
                          on Contact.`Uni Department` = `U D`.`Department Id`)
                    WHERE `Contact Id` IN (SELECT DISTINCT `Contributes to Event`.`Contact Id` FROM `Contributes to Event`)
                    """
        elif category == "IEEE Members":
            q = """
                    SELECT `First Name`, `Last Name`, `Phone`, `Address`, `Date Created`, `IEEE Position`
                    FROM `Contact`
                    WHERE `IEEE Position` IS NOT NULL
                    """
        res = query(q, curs)
        st.table(res)

elif selected_tab == "Attendees":
    st.title("Attendees Tab")
    st.header("Mailing List")
    p = st.button("Show Participants", key=4)
    export = st.button("Export Mailing List")

    if export:
        q = """ SELECT `Email`, `First Name`, `Last Name`
                FROM (`Participant` JOIN Attends AS A on Participant.Email = A.`Participant Email`)
                WHERE `Subscribed` = 1
                GROUP BY `Participant Email`
                """
        res = query(q, curs)
        res.to_csv(path_or_buf="Mailing_List.csv", index=False)
        st.write("Exported Mailing List!")
        st.table(res)

    sub = st.checkbox("Only Subscribed")
    if p:
        st.button("Hide List")
        if sub:
            q = """ SELECT `Email`, `First Name`, `Last Name`, Subscribed, `Interested in Membership`, 
                    COUNT(*) AS `Events Attended`
                    FROM (`Participant` JOIN Attends AS A on Participant.Email = A.`Participant Email`)
                    WHERE `Subscribed` = 1
                    GROUP BY `Participant Email`
                    ORDER BY `Events Attended` DESC 
                    """
        else:
            q = """ SELECT `Email`, `First Name`, `Last Name`, Subscribed, `Interested in Membership`, 
                    COUNT(*) AS `Events Attended`
                    FROM (`Participant` JOIN Attends AS A on Participant.Email = A.`Participant Email`)
                    GROUP BY `Participant Email`
                    ORDER BY `Events Attended` DESC 
                    """
        res = query(q, curs)
        st.table(res)

elif selected_tab == "Financial":
    st.title("Financial Figures Tab")
    st.header("Contributions")
    p1 = st.button("Show Contributions", key=4)
    if p1:
        st.button("Hide List")
        q = """ SELECT C.`First Name` AS `Sponsor's First Name`, C.`Last Name` AS `Sponsor's Last Name`, 
                `Date`, `Type`, `Package`, `Stored In`
                FROM (`Contribution` JOIN Contact AS C on Contribution.`Given By` = C.`Contact Id`)
                ORDER BY `Date` DESC"""
        res = query(q, curs)
        st.table(res)

    st.header("Purchases")
    p1 = st.button("Show Purchases")
    if p1:
        st.button("Hide List")
        q = q = """ SELECT C.`First Name` AS `Vendor's First Name`, C.`Last Name` AS `Vendor's Last Name`, 
                `Date`, `Type`, `Cost`, `Stored In`
                FROM (`Purchase` JOIN Contact AS C on Purchase.`Purchased by` = C.`Contact Id`)
                ORDER BY `Date` DESC"""
        res = query(q, curs)
        st.table(res)


disconnect(conn, curs)



