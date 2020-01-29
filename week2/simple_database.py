import xml.etree.ElementTree as ET
import sqlite3
from sqlite3 import Error


def create_memory_connection():
    conn = None
    try:
        conn = sqlite3.connect(':memory:')
        # conn = sqlite3.connect('C:\\sqlite\\db\\python_db.db')
        return conn
    except Error as e:
        print(e)

    return conn


def list_doctors_by_speciality(conn):
    cursor = conn.cursor()
    cursor.execute("SELECT Speciality, Doctor_Name FROM Doctor ORDER BY Speciality")
    doctors = cursor.fetchall()
    doc_speciality = ''
    for row in doctors:
        if doc_speciality != row[0]:
            print(row[0], ":")
            doc_speciality = row[0]
        print(" ", row[1])
    cursor.close()


def create_test_tables(conn):
    try:
        cursor = conn.cursor()
        sql_hospital_table = """ CREATE TABLE IF NOT EXISTS Hospital (
            Hospital_Id UNSIGNED BIG INT primary key,
            Hospital_Name TEXT NOT NULL,
            Bed_Count INTEGER
        ); """
        cursor.execute(sql_hospital_table)

        sql_doctor_table = """ CREATE TABLE IF NOT EXISTS Doctor (
                    Doctor_Id UNSIGNED BIG INT primary key,
                    Doctor_Name TEXT NOT NULL,
                    Hospital_Id INTEGER NOT NULL,
                    Joining_Date DATE NOT NULL,
                    Speciality TEXT,
                    Salary INTEGER,
                    Experience INTEGER
                ); """
        cursor.execute(sql_doctor_table)
        cursor.close()

    except Error as e:
        print(e)


def fill_test_tables(conn):
    cursor = conn.cursor()
    # uncomment if you use db file instead of memory
    # I am too lazy to check if the tables are empty
    # cursor.execute("DELETE FROM Hospital")
    # conn.commit()
    # cursor.execute("DELETE FROM Doctor")
    # conn.commit()
    hospital_data = [('1', 'Mayo Clinic', '200'),
                     ('2', 'Cleveland Clinic', '400'),
                     ('3', 'Johns Hopkins', '1000'),
                     ('4', 'UCLA Medical Center', '1500')]

    cursor.executemany("INSERT INTO Hospital VALUES (?,?,?)", hospital_data)
    conn.commit()

    doctor_data = [('101', 'David', '1', '2005-02-10', 'Pediatric', '40000', 'NULL'),
                   ('102', 'Michael', '1', '2018-07-23', 'Oncologist', '20000', 'NULL'),
                   ('103', 'Susan', '2', '2016-05-19', 'Garnacologist', '25000', 'NULL'),
                   ('104', 'Robert', '2', '2017-12-28', 'Pediatric ', '28000', 'NULL'),
                   ('105', 'Linda', '3', '2004-06-04', 'Garnacologist', '42000', 'NULL'),
                   ('106', 'William', '3', '2012-09-11', 'Dermatologist', '30000', 'NULL'),
                   ('107', 'Richard', '4', '2014-08-21', 'Garnacologist', '32000', 'NULL'),
                   ('108', 'Karen', '4', '2011-10-17', 'Radiologist', '30000', 'NULL')]
    cursor.executemany("INSERT INTO Doctor VALUES (?,?,?,?,?,?,?)", doctor_data)
    conn.commit()
    cursor.close()


def print_db_version(conn):
    cursor = conn.cursor()
    cursor.execute("SELECT sqlite_version()")
    rows = cursor.fetchall()
    for row in rows:
        print(row)
    cursor.close()


def show_doctors_by_given_hospital(conn):
    cursor = conn.cursor()
    cursor.execute("SELECT DISTINCT Hospital_Name FROM Hospital")
    rows = cursor.fetchall()
    print("Hospitals: ")
    for row in rows:
        print(" ", row[0])
    hospital = input("Type a hospital name, please:")
    sql = """SELECT Doctor.Doctor_Name 
                   FROM Doctor, Hospital where 
                   Hospital.Hospital_Name='{0}'
                   AND
                   Doctor.Hospital_Id = Hospital.Hospital_Id""".format(hospital)
    cursor.execute(sql)
    doctors = cursor.fetchall()
    for doctor in doctors:
        print(" ", doctor[0])

    cursor.close()


def update_experience(conn):
    cursor = conn.cursor()
    cursor.execute("UPDATE Doctor SET Experience=(strftime('%Y', 'now') - strftime('%Y', Joining_Date));")
    cursor.execute("SELECT Doctor_Name, Experience FROM Doctor")
    rows = cursor.fetchall()
    for row in rows:
        print(row[0], " ", row[1])
    cursor.close()


def export_doctors_xml(conn):
    cursor = conn.cursor()
    xml_root = ET.Element("Envelope", xmlns="http://schemas.xmlsoap.org/soap/envelope/")
    xml_body = ET.SubElement(xml_root, "Body")
    xml_doctors = ET.SubElement(xml_body, "Doctors")
    cursor.execute("SELECT Doctor_Id, Doctor_Name, Speciality, Salary FROM Doctor")
    rows = cursor.fetchall()
    for row in rows:
        xml_doctor = ET.SubElement(xml_doctors, "Doctor")
        ET.SubElement(xml_doctor, "Doctor_ID").text = str(row[0])
        xml_personal_data = ET.SubElement(xml_doctor, "Personal_Data")
        ET.SubElement(xml_personal_data, "Name").text = row[1]
        ET.SubElement(xml_personal_data, "Speciality").text = row[2]
        ET.SubElement(xml_personal_data, "Salary").text = str(row[3])

    tree = ET.ElementTree(xml_root)
    tree.write("C:\\sqlite\\db\\doctors.xml", encoding="UTF-8", xml_declaration=True)
    cursor.close()


def main():
    # create a database connection
    conn = create_memory_connection()

    # create tables
    if conn is not None:
        print_db_version(conn)
        create_test_tables(conn)
        fill_test_tables(conn)
        list_doctors_by_speciality(conn)
        show_doctors_by_given_hospital(conn)
        update_experience(conn)
        export_doctors_xml(conn)
        conn.close()
    else:
        print("Error! cannot create the database connection.")
        return


if __name__ == '__main__':
    main()
