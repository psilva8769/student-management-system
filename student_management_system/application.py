from dearpygui.core import *
from dearpygui.simple import *
from pymongo import MongoClient
import sys

def connect_to_mongodb():
    try:
        client = MongoClient(port=27017)
        db = client.Assignment08
        print("Connected to MongoDB")
        return db
    except Exception as e:
        print("Database connection Error: ", e)
        sys.exit(1)

def add_student(sender, data):
    prn, name, email, batch, mobile = get_value("PRN"), get_value("Name"), get_value("Email"), get_value("Batch"), get_value("Mobile")
    if not all([prn, name, email, batch]):
        log_warning("All fields are compulsory (Except: Mobile number)")
        return
    if db.students.count_documents({'PRN': prn}, limit=1) != 0:
        log_warning("STUDENT Already Exists")
        return
    db.students.insert_one({'PRN': prn, 'NAME': name, 'EMAIL': email, 'BATCH': batch, 'MOBILE': mobile})
    log_info("Student Added")

def delete_student(sender, data):
    prn = get_value("PRN")
    if not prn:
        log_warning("Enter a Valid PRN")
        return
    if db.students.count_documents({'PRN': prn}, limit=1) == 0:
        log_warning("STUDENT Does Not Exist")
        return
    db.students.delete_one({'PRN': prn})
    log_info("Student Deleted")

def update_student(sender, data):
    prn = get_value("PRN")
    if not prn:
        log_warning("Enter a Valid PRN")
        return
    updates = {'NAME': get_value("Name"), 'EMAIL': get_value("Email"), 'BATCH': get_value("Batch"), 'MOBILE': get_value("Mobile")}
    db.students.update_one({"PRN": prn}, {"$set": updates})
    log_info("Student Updated")

def display_students(sender, data):
    delete_item("Student List", children_only=True)
    students = db.students.find()
    for student in students:
        add_text(f"PRN: {student['PRN']}, Name: {student['NAME']}, Email: {student['EMAIL']}, Batch: {student['BATCH']}, Mobile: {student.get('MOBILE', 'N/A')}", parent="Student List")

db = connect_to_mongodb()

with window("Main Window", width=600, height=300):
    add_input_text("PRN", label="PRN")
    add_input_text("Name", label="Name")
    add_input_text("Email", label="Email")
    add_input_text("Batch", label="Batch")
    add_input_text("Mobile", label="Mobile")
    add_button("Add Student", callback=add_student)
    add_button("Delete Student", callback=delete_student)
    add_button("Update Student", callback=update_student)
    add_button("Show Students", callback=display_students)
    add_logger("Log", log_level=1)
    with child("Student List", autosize_x=True, autosize_y=True):
        pass

start_dearpygui(primary_window="Main Window")
