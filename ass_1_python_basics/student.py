class Student:
    def __init__(self,name,roll_number,classroom,teacher,email,attendance):
        self.attendance = attendance
        self.name = name
        self.roll_number = roll_number
        self.classroom = classroom
        self.teacher = teacher
        self.email = email
 
    def display(self):
        print("name: ",self.name)
        print("roll_number: ",self.roll_number)
        print("classroom: ",self.classroom)
        print("teacher: ",self.teacher)
        print("email: ",self.email)
        print("attendance: ",self.attendance)
    
# ram = Student(80,7.0,"ram setu",102,6403,"shriram sane","ram@gmail.com")

# print(ram.attendance,ram.grades,ram.name,ram.email)
# ram.display()

class StudentManagementSystem:
    def __init__(self):
        self.student =[]

    def addStudent(self):
        name = (input("Enter name: "))
        roll_number = int(input("roll_number: "))
        classroom = int(input(" classroom: "))
        teacher = (input("teacher: "))
        email = (input(" email: "))
        attendance = int(input("attendance : "))
        std = Student(name,roll_number,classroom,teacher,email,attendance)
        self.student.append(std)

    def view_student(self):
        # print(self.student)
         for std in self.student:
            std.display()
            print("------------------")
    
system = StudentManagementSystem()
system.addStudent()
system.addStudent()
system.view_student()