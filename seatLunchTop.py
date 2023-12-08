import CSProjectFunctions
#hi
# sources
# https://developers.google.com/sheets/api/quickstart/python
# https://www.youtube.com/watch?v=3wC-SCdJK2c&t=1157s
# MUST USE FUNNY BACKTCK '


def main():
    studentNames = CSProjectFunctions.getNames("seatLunchData/studentNames.CSV")[1:]
    teacherNames = CSProjectFunctions.getNames("seatLunchData/teacherNames.CSV")[1:]
    data = CSProjectFunctions.allData()

    for student in studentNames:
        emailData = {}
        emailData['lunch'], emailData['table'] = CSProjectFunctions.findlunch(student[0],data)
        emailData["people"] = CSProjectFunctions.findTable(table=emailData["table"], lunch=emailData["lunch"], data=data)
        emailData["teacher"] = CSProjectFunctions.findTeacher(lunch=emailData["lunch"], data=data, tableNumber=emailData["table"])
        try:
            CSProjectFunctions.emailInfo(dataDict=emailData, Recipient=student[1])
        except:
            print(f"could not send to {student[1]}")


    for teacher in teacherNames:
        emailData = {}
        emailData['lunch'], emailData['table'] = CSProjectFunctions.findLunchteacher(teacher[0], data)
        emailData['people'] = CSProjectFunctions.findTable(lunch=emailData["lunch"], data=data, table=emailData["table"])
        emailData["teacher"] = teacher[0]
        try:
            CSProjectFunctions.emailInfo(dataDict=emailData, Recipient=teacher[1])
        except:
            print(f"could not send to {teacher[1]}")


if __name__ == "__main__":
    main()