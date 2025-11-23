def display_instruction():
    """Display menu options."""

    print('''
--- Student Grade Analyzer ---
1. Add a new student
2. Add grades for a student
3. Generate a full report
4. Find the top student
5. Exit program
    ''')


def add_student():
    """Add a new student to the list."""

    name = input("Enter student name: ").strip()
    if any(name.lower() == student["name"].lower() for student in students):
        print("You have already been added to the list.")
    else:
        student_dict = {"name": name, "grades": []} 
        students.append(student_dict)


def add_grades():
    """Add grades for a student from the list."""

    name = input("Enter student name: ").strip()
    for student in students:
        if name.lower() == student["name"].lower():
            while True:
                try:
                    grade = input("Enter a grade (or 'done' to finish): ")
                    if grade.lower() == "done":
                        break
                    elif 0 <= int(grade) <= 100:
                        student["grades"].append(int(grade))
                    else:
                        print("Invalid input. Please enter one number from 0 to 100 (or 'done' to finish).")  
                except ValueError:
                    print("Invalid input. Please enter one number from 0 to 100 (or 'done' to finish).")
            break
    else:
        print("Sorry, you have not been found on the list of students")


def calculate_average_grade(grades):
    """Calculate an average grade or return None if there are no grades."""

    if len(grades) != 0:
        avg = round(sum(grades) / len(grades), 1)
        return avg
    else:
        return None 


def show_report():
    """Generate a full report with average grades."""

    average_grades = []
    print("--- Student Report ---")
    for student in students:
        average = calculate_average_grade(student["grades"])
        if average is not None:
            average_grades.append(average)
            print(f"{student['name']}'s average grade is {average}.")
        else:
            print(f"{student['name']}'s average grade is N/A.")
    if len(students) == 0:
        print("There are no students on the list yet.") 
    elif len(average_grades) == 0:
        print("There are no grades on the list yet.")
    else:
        print(f'''-------------------------
Max Average: {max(average_grades)}
Min Average: {min(average_grades)}
Overall Average: {round(sum(average_grades) / len(average_grades), 1)}
              ''')


def find_best_student():
    """Find the student with the highest average grade."""

    if len(students) == 0:
        print("There are no students on the list yet.")
    elif all(len(student["grades"]) == 0 for student in students):
        print("There are no grades on the list yet.")
    else:
        best_student = max(students, key=lambda student: calculate_average_grade(student["grades"]) or 0)
        best_student_grades = calculate_average_grade(best_student["grades"])
        print(f"The student with the highest average is {best_student['name']} with a grade of {best_student_grades}")
        

students = []

while True:
    display_instruction()
    try:
        choice = int(input("Enter your choice: "))
    except ValueError:
        print("Invalid input. Please enter a number.")
        continue
    if choice == 5:
        break
    elif choice == 1:
        add_student()
    elif choice == 2:
        add_grades()
    elif choice == 3:
        show_report()
    elif choice == 4:
        find_best_student()
    else:
        print("Please enter a number from 1 to 5.")
    