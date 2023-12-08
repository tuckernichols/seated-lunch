import os.path
import datetime
import csv

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

from email.message import EmailMessage
import ssl
import smtplib


def getNames(fileName):
    nameList = []
    with open(fileName, newline="") as csvfile:
        reader = csv.reader(csvfile, delimiter='/', quotechar='|')
        for row in reader:
            nameList.append(row)
    return nameList


def fetch(range, spreadsheet):
  SCOPES = ["https://www.googleapis.com/auth/spreadsheets"]
  creds = None
  if os.path.exists("seatLunchData/tokenN9.json"):
    creds = Credentials.from_authorized_user_file("tokenN9.json", SCOPES)
  # If there are no (valid) credentials available, let the user log in.
  if not creds or not creds.valid:
    if creds and creds.expired and creds.refresh_token:
      creds.refresh(Request())
    else:
      flow = InstalledAppFlow.from_client_secrets_file(
          "oath creds N9 pro.json", SCOPES
      )
      creds = flow.run_local_server(port=0)
    # Save the credentials for the next run
    with open("seatLunchData/tokenN9.json", "w") as token:
      token.write(creds.to_json())

  try:
    service = build("sheets", "v4", credentials=creds)
    sheet = service.spreadsheets()
    result = sheet.values().get(spreadsheetId=spreadsheet, range=range).execute()

    values = result.get("values", [])

  except HttpError as error:
    print(error)
    return "ERROR"

  return values


def allData():
    dataReturnObj = {}              # monday = 0
    if datetime.date.today().weekday() == 0 or datetime.date.today().weekday() == 6:  # if monday data = below
        dataReturnObj["firstTeachersNames"] = fetch("Adult Assignments Mon 2023!A3:A45", "1j5h6rnKTc385xlEZ_lUB-RBvxU6_mEZtzq8uU7ER4vA")
        dataReturnObj['firstTeachersNumbers'] = fetch("Adult Assignments Mon 2023!B3:B45", "1j5h6rnKTc385xlEZ_lUB-RBvxU6_mEZtzq8uU7ER4vA")
        dataReturnObj["secondTeachersNames"] = fetch("Adult Assignments Mon 2023!D3:D45", "1j5h6rnKTc385xlEZ_lUB-RBvxU6_mEZtzq8uU7ER4vA")
        dataReturnObj["secondTeachersNumbers"] = fetch("Adult Assignments Mon 2023!E3:E45", "1j5h6rnKTc385xlEZ_lUB-RBvxU6_mEZtzq8uU7ER4vA")

        dataReturnObj["firstNames"] = fetch("Students by Table Mon Oct 16!A3:A190", "1j5h6rnKTc385xlEZ_lUB-RBvxU6_mEZtzq8uU7ER4vA")
        dataReturnObj["firstNumbers"] = fetch("Students by Table Mon Oct 16!B3:B190", "1j5h6rnKTc385xlEZ_lUB-RBvxU6_mEZtzq8uU7ER4vA")
        dataReturnObj["secondNames"] = fetch("Students by Table Mon Oct 16!D3:D190", "1j5h6rnKTc385xlEZ_lUB-RBvxU6_mEZtzq8uU7ER4vA")
        dataReturnObj["secondNumbers"] = fetch("Students by Table Mon Oct 16!E3:E190", "1j5h6rnKTc385xlEZ_lUB-RBvxU6_mEZtzq8uU7ER4vA")

    elif datetime.date.today().weekday() == 2 or datetime.date.today().weekday() == 3: #if thursday or wednesday data = below
        dataReturnObj["firstTeachersNames"] = fetch("Adult Assignments Thurs!A3:A45", "1MkF2o_YQfM5b-mBLB0Rnmd5zujx2OnFILmH-8riJwlo")
        dataReturnObj['firstTeachersNumbers'] = fetch("Adult Assignments Thurs!B3:B45", "1MkF2o_YQfM5b-mBLB0Rnmd5zujx2OnFILmH-8riJwlo")
        dataReturnObj["secondTeachersNames"] = fetch("Adult Assignments Thurs!D3:D45", "1MkF2o_YQfM5b-mBLB0Rnmd5zujx2OnFILmH-8riJwlo")
        dataReturnObj["secondTeachersNumbers"] = fetch("Adult Assignments Thurs!E3:E45", "1MkF2o_YQfM5b-mBLB0Rnmd5zujx2OnFILmH-8riJwlo")

        dataReturnObj["firstNames"] = fetch("Students Table Thurs!A3:A190", "1MkF2o_YQfM5b-mBLB0Rnmd5zujx2OnFILmH-8riJwlo")
        dataReturnObj["firstNumbers"] = fetch("Students Table Thurs!B3:B190", "1MkF2o_YQfM5b-mBLB0Rnmd5zujx2OnFILmH-8riJwlo")
        dataReturnObj["secondNames"] = fetch("Students Table Thurs!D3:D190", "1MkF2o_YQfM5b-mBLB0Rnmd5zujx2OnFILmH-8riJwlo")
        dataReturnObj["secondNumbers"] = fetch("Students Table Thurs!E3:E190", "1MkF2o_YQfM5b-mBLB0Rnmd5zujx2OnFILmH-8riJwlo")

    return dataReturnObj


def findlunch(studentname, data):
    count = 0
    for i in data["firstNames"]:
        if i[0] == studentname:
            return "First Lunch", data["firstNumbers"][count][0]  # lunch and table number
        count += 1
    count = 0
    for i in data["secondNames"]:
        if i[0] == studentname:
            return "Second Lunch", data["secondNumbers"][count][0]
        count += 1
    print("student name not found")


def findTable(table, lunch, data):
    tablePeople = []
    count = 0
    if lunch == 'First Lunch':
        for i in data["firstNumbers"]:
            if i[0] == table:
                tablePeople.append(data["firstNames"][count][0])
            count += 1

    elif lunch == "Second Lunch":
        for i in data["secondNumbers"]:
            if i[0] == table:
                tablePeople.append(data["secondNames"][count][0])
            count += 1

    return tablePeople


def findTeacher(tableNumber, lunch, data):
    count = 0
    if lunch == "First Lunch":
        for i in data["firstTeachersNumbers"]:
            if i[0] == tableNumber:
                return data["firstTeachersNames"][count][0]
            count += 1
    elif lunch == "Second Lunch":
        for i in data["secondTeachersNumbers"]:
            if i[0] == tableNumber:
                return data["secondTeachersNames"][count][0]
            count += 1


emPassword = "vtnw qnxq pxtw pfqs"
emSender = "pytucker21@gmail.com"


def emailInfo(Recipient, dataDict):   # ["first/second", table, teacher, people]
    teacher = str(dataDict["teacher"]).split(",")
    dataDict["people"] = parsePeopleData(dataDict["people"])
    em = EmailMessage()
    em['From'] = emSender
    em["To"] = Recipient                               # my understanding
    em["Subject"] = f"{dataDict['lunch']} Table {dataDict['table']} "  # the email is created we have the info but the infor isnt being used
    em.set_content(f"""Table {dataDict['table']}
Teacher: {teacher[1] + " " + teacher[0]}
{dataDict["people"]}
""")  # this is the outline or the bones

    contex = ssl.create_default_context()
    with smtplib.SMTP_SSL("smtp.gmail.com", 465, context=contex) as sMTp:
        sMTp.login(emSender, emPassword)  # login
        sMTp.sendmail(emSender, Recipient, em.as_string())  # send


def parsePeopleData(tableStudents):
    returnlist = []
    for i in tableStudents:
        split = i.split(",")
        last = split[0]
        split = split[1].split("'")
        if split[0].count("(") == 1:
            first = split[0].split("(")
            first = first[1][:-2]
        else: first  = split[0]
        returnlist.append(first +' ' + last + " '" + split[1])
    return returnlist

def findLunchteacher(teacher, data):
    count = 0
    for i in data["firstTeachersNames"]:
        if i[0] == teacher:
            return "First Lunch", data["firstTeachersNumbers"][count][0] # lunch and table number
        count += 1
    count = 0
    for i in data["secondTeachersNames"]:
        if i[0] == teacher:
            return "Second Lunch", data["secondTeachersNumbers"][count][0]
        count += 1
    print("teacher name not found")
    return "error"


def findStudentsTeacher(lunch, tablenumber, data):
    count = 0
    studentsAtTable = []
    if lunch == "First Lunch":
        for i in data["firstNumbers"]:
            if i[0] == tablenumber:
                studentsAtTable.append(data["firstNames"][count][0])
            count += 1
    elif lunch == "Second Lunch":
        pass

