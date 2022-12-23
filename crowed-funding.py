import re
import phonenumbers
from phonenumbers import carrier, timezone, geocoder
from getpass import getpass
import datetime


def checkemail(email):
    regex = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'
    result = False
    if (re.fullmatch(regex, email)):
        result = True
    else:
        result = False
    return result

def checkpassword(password, confpassword):
    while password != confpassword:
        print("password didn't match try again: ")
        password = input("enter your password: ")
        confpassword = input("re enter your password must match: ")
        checkpassword(password, confpassword)
    else:
        print("password set sucssfully")

def checkphone(phone):
    validphone = False
    phone_number = phonenumbers.parse(phone, "GB")
    country = geocoder.description_for_number(phone_number, 'en')
    validphone = phonenumbers.is_valid_number(phone_number)
    while validphone == False or country != "Egypt":
        print("wrong phone number try again")
        phone = input("enter you phone number: ")
        phone_number = phonenumbers.parse(phone, "GB")
        validphone = phonenumbers.is_valid_number(phone_number)
        country = geocoder.description_for_number(phone_number, 'en')

def add_id(file,index):
    try:
        fileobj = open(file, "r")
    except Exception as e :
        print(e)
    else:
        lines=fileobj.readlines()
        x=[]
        if len(lines) != 0:
            for line in lines:
                x=line.split(":")
            if len(x) != 0:
                lastid=int(x[index])
                return lastid+1
            else:
                return 1  
        else:
            return 1

def getid(logemail,logpass):
    fileobj = open("users.txt", "r")
    lines=fileobj.readlines()
    x=[]
    for line in lines:
        if logemail in line and logpass in line:
            x.append(line.split(":"))
    id=int(x[-1][0])
    return id

def getfname(logemail,logpass):
    fileobj = open("users.txt", "r")
    lines=fileobj.readlines()
    x=[]
    for line in lines:
        if logemail in line and logpass in line:
            x.append(line.split(":"))
    name=x[-1][1]
    return name

def registration():
    fname = input("enter your first name: ")
    while fname.isalpha() == False:
        print("name only in alphachars try again!!")
        fname = input("enter your first name: ")
    lname = input("enter your last name: ")
    while lname.isalpha() == False:
        print("name only in alphachars try again!!")
        fname = input("enter your first name: ")
    email = input("enter your email: ")
    validemail = checkemail(email)
    while validemail == False:
        print(f"in while {validemail} ")
        print("You entered wrong email please try again!")
        email = input("enter your email: ")
        validemail = checkemail(email)
    phone = input("enter your phone number: ")
    checkphone(phone)
    password = getpass("Please enter password ")
    confpassword = getpass("re enter your password must match: ")
    checkpassword(password, confpassword)
    try:
        fileobj = open("users.txt", "a")
    except Exception as e:
        print(f"error: {e}")
    else:
        newid=str(add_id("users.txt",0))
        fileobj.writelines([newid, ":",fname, ":", lname, ":", email, ":", password, ":", phone, "\n"])
        print("User Created Successfully")

def date_validation():
    while True:
        print("Note: Start date should be before end date")
        while True:
            date_string = input("Please enter project start date in format YYY-MM-DD ")
            date_format = '%Y-%m-%d'
            try:
                date_object = datetime.datetime.strptime(date_string, date_format)
                start_date = date_object.date()
                break
            except ValueError:
                print("ERROR::Invalid date")
        while True:
            date_string = input("Please enter project end date in format YYY-MM-DD ")
            date_format = '%Y-%m-%d'
            try:
                date_object = datetime.datetime.strptime(date_string, date_format)
                end_date = date_object.date()
                break
            except ValueError:
                print("ERROR::Invalid date")
        if start_date < end_date:
            break
    return [start_date,end_date]

def projectmenue(name):
    print(f"welcome {name}")
    print("1) create project")
    print("2) view all projects")
    print("3) select project")
    print("4) search by date")
    print("5) log out and re log in")
    print("6) Exit")
    choice = input("please type your choice number>>")
    while not choice.isdigit() or int(choice) not in range(1,7):
        print("wrong choice please re enter your choice number: ")
        choice = input("please type your choice number>>")
    return choice

def prject_editORdelete():
    print("1) edit project")
    print("2) delete project")
    choice = input("please type your choice number>>")
    while not choice.isdigit() or int(choice) not in range(1,3):
        print("wrong choice please re enter your choice number: ")
        choice = input("please type your choice number>>")
    return choice

def Create_project(logemail,logpass):
    title = input("enter your new project Title: ")
    while title.isalpha() == False:
        print("title only in alphachars try again!!")
        title = input("enter your new project Title Again: ")
    details = input("enter your project details: ")
    target = input("enter your project Target: ")
    while target.isdigit() == False:
        print("target only in digits try again!!")
        target = input("enter your project Target Again: ")
    date=date_validation()
    try:
        fileobj = open("project.txt", "a")
    except Exception as e:
        print(f"error: {e}")
    else:
        userid=str(getid(logemail,logpass))
        project_id=add_id("project.txt",1)
        fileobj.writelines([userid, ":",str(project_id), ":",title, ":", details, ":", target, ":", str(date[0]), ":", str(date[1]), ":","\n"])
        print("project Created Successfully")

def edite_project(selected_project,logemail,logpass):
    selected_column=column_menue()
    if selected_column == "2":
        Newvalue=input("Enter New Value To Edite")
        while Newvalue.isalpha() == False:
            print("title only in alphachars try again!!")
            Newvalue = input("enter your new project Title Again: ")
    elif selected_column == "3":
        Newvalue = input("enter your new project details: ")
    elif selected_column == "4":
        Newvalue=input("Enter New Value To Edite")
        while Newvalue.isdigit() == False:
            print("target only in digits try again!!")
            Newvalue = input("enter your project Target Again: ")
    elif selected_column == "5":
        Newdatevalue=date_validation()
    with open('project.txt', 'r') as file:
        data = file.readlines() 
        index=0
        userid=str(getid(logemail,logpass))
        for line in data:
            if line.split(":")[1] == selected_project and selected_column == "2":
                data[index]=f"{userid}:{selected_project}:{Newvalue}:{line.split(':')[3]}:{line.split(':')[4]}:{line.split(':')[5]}:{line.split(':')[6]}:"
            elif line.split(":")[1] == selected_project and selected_column == "3":
               data[index]=f"{userid}:{selected_project}:{line.split(':')[2]}:{Newvalue}:{line.split(':')[4]}:{line.split(':')[5]}:{line.split(':')[6]}:"
            elif line.split(":")[1] == selected_project and selected_column == "4":
                data[index]=f"{userid}:{selected_project}:{line.split(':')[2]}:{line.split(':')[3]}:{Newvalue}:{line.split(':')[5]}:{line.split(':')[6]}:"
            elif line.split(":")[1] == selected_project and selected_column == "5":
                data[index]=f"{userid}:{selected_project}:{line.split(':')[2]}:{line.split(':')[3]}:{line.split(':')[4]}:{Newdatevalue[0]}:{Newdatevalue[1]}:\n" 
            index +=1
    with open('project.txt', 'w') as file:
        file.writelines( data )
        print("project Edited Successfully")
    
def delete_project(selected_project):
    with open('project.txt', 'r') as file:
        data = file.readlines()
        index=0
        for line in data:
            if line.split(":")[1] == selected_project:
                data.pop(index)
            index +=1
    with open('project.txt', 'w') as file:
        file.writelines( data )
        print("project Deleted Successfully")

def search_by_date():
    print("Searching using Date ....")
    date_to_search_with=date_validation()
    try:
        fileobj = open("project.txt", "r")
    except Exception as e:
        print (e)
    else:
        lines=fileobj.readlines()
        result=[]
        for line in lines:
            if date_to_search_with[0] <= datetime.datetime.strptime(line.split(":")[5],'%Y-%m-%d').date() and date_to_search_with[1] >= datetime.datetime.strptime(line.split(":")[6],'%Y-%m-%d').date():
                result.append(line)
        if len(result) > 0:
            ShowTable(result)
        else:
            print("found nothing")    

def ShowTable(lines):
    print()
    print ("{:<15}{:<15} {:<20} {:<10} {:<15} {:<15}".format('Project ID','Project Title','Project Details','Target','Start Date','End Date'))
    print()
    for line in lines:
        line=line.split(":")
        print ("{:<15}{:<15} {:<20} {:<10} {:<15} {:<15}".format(line[1],line[2],line[3],line[4],line[5],line[6]))

def view_all_projects():
    try:
        fileobj = open("project.txt", "r")
        lines=fileobj.readlines()
    except Exception as e:
        print (e)
    else:
        if len(lines) != 0:
            
            ShowTable(lines)
        else:
            print(" No Data To Show !! ")

def project_exist(UserProjects,selected_project):
    valid = 0
    for line in UserProjects:
        if str(selected_project) == str(line.split(":")[1]):
            valid = 1
        else:
            pass
    if valid == 1:
        return True
    else:
        return False

def column_menue():
    print("2) Project Title")
    print("3) Project Details")
    print("4) Target")
    print("5) Start Date or End Date")
    choice = input("please type your choice number>>")
    while not choice.isdigit() or int(choice) not in range(2,6):
        print("wrong choice please re enter your choice number: ")
        choice = input("please type your choice number>>")
    return choice

def select_project(logemail,logpass):
    UserId=getid(logemail,logpass)
    try:
        fileobj = open("project.txt", "r")
    except Exception as e:
        print (e)
    else:
        lines=fileobj.readlines()
        UserProjects=[]
        for line in lines:
            if str(UserId) == line.split(":")[0]:
                UserProjects.append(line)
        if len(UserProjects) != 0:
            print("<< Select Project By ID To Edit Or Delete >>")
            ShowTable(UserProjects)
            selected_project=input("Enter Your Selection >> ")
            while project_exist(UserProjects,selected_project) == False:
                print("You Don't Have Project With This ID Try Again!!")
                selected_project=input("Enter Your Selection >> ")
            print()
            print("project successfully selected")
            print()
            action=prject_editORdelete()
            if action == "1":
                edite_project(selected_project,logemail,logpass)
            elif action == "2":
                delete_project(selected_project)
        else:
            print("you don't have Projects to select")

def first_layer(logemail,logpass):
    fname=str(getfname(logemail,logpass))
    choice=projectmenue(fname)
    if choice == "1":
        Create_project(logemail,logpass)
        first_layer(logemail,logpass)
    elif choice == "2":
        view_all_projects()
        first_layer(logemail,logpass)
    elif choice == "3":
        select_project(logemail,logpass)
        first_layer(logemail,logpass)
    elif choice == "4":
        search_by_date()
        first_layer(logemail,logpass)
    elif choice == "5":
        login()
    elif choice == "6":
        exit()

def login():
    logemail = input("Enter Your Email>> ")
    validemail = checkemail(logemail)
    while validemail == False:
        print("You entered wrong email please try again!")
        email = input("enter your email: ")
        validemail = checkemail(email)
    logpass = getpass("Enter Your Password>> ")
    try:
        fileobj = open("users.txt", "r")
    except Exception as e:
        print(e)
    else:
        for line in fileobj:
            if logemail in line and logpass in line:
                print("Logged In Successfully")
                first_layer(logemail,logpass)
                break
            else:
                print("Wrong email or password")
        fileobj.close

def start():
    select = input("Enter Signup for Registration or Signin for login: ")
    while select.lower() != "signup" and select.lower() != "signin":
        print("Wrong Choice Try Again!!!")
        select = input("Enter Signup for Registration or Signin for login: ")

    if select.lower() == "signup":
        registration()
        start()
    elif select.lower() == "signin":
        login()
        start()

start()