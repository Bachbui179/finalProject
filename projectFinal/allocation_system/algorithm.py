#Algorithm for the case of number of students higher than 
import math
students_preferences = {
    'Alice Johnson': ['John Smith', 'Emily Johnson', 'Sarah Brown', 'Samantha Clark'],
    'Bob Smith': ['Samantha Clark', 'John Smith', 'Sarah Brown', 'Emily Johnson'],
    'Emma Davis': ['Emily Johnson', 'Sarah Brown', 'John Smith', 'Samantha Clark'],
    'Sophia Brown': ['Emily Johnson', 'Sarah Brown', 'Samantha Clark', 'John Smith'],
    'John Doe': ['Emily Johnson', 'Sarah Brown', 'John Smith', 'Samantha Clark'],
    'Jane Smith': ['Samantha Clark', 'Sarah Brown', 'Emily Johnson', 'John Smith'],
    'David Wilson': ['Emily Johnson', 'John Smith', 'Samantha Clark', 'Sarah Brown']
}

teachers_preferences = {
    'John Smith': ['Bob Smith', 'Alice Johnson', 'David Wilson', 'Jane Smith', 'Emma Davis', 'John Doe', 'Sophia Brown'],
    'Emily Johnson': ['John Doe', 'Sophia Brown', 'Jane Smith', 'Alice Johnson', 'David Wilson', 'Bob Smith', 'Emma Davis'],
    'Sarah Brown': ['Alice Johnson', 'Bob Smith', 'Emma Davis', 'Sophia Brown', 'David Wilson', 'Jane Smith', 'John Doe'],
    'Samantha Clark': ['Alice Johnson', 'Bob Smith', 'Emma Davis', 'Sophia Brown', 'John Doe', 'Jane Smith', 'David Wilson']
}

    
max_students_per_teacher = math.ceil(len(students_preferences)/len(teachers_preferences))
teachers_assigned = {teacher: [] for teacher in teachers_preferences}
students_proposals = {student: 0 for student in students_preferences}
proposals = {student: None for student in students_preferences}
while None in proposals.values():
    for student in students_preferences:
        if proposals[student] is None:
            teacher = students_preferences[student][students_proposals[student]]
            if len(teachers_assigned[teacher]) < max_students_per_teacher:
                teachers_assigned[teacher].append(student)
                proposals[student] = teacher
            else:
                current_students = teachers_assigned[teacher]
                current_students.sort(key=lambda x: teachers_preferences[teacher].index(x))
                least_preferred_student = current_students[-1]
                
                if teachers_preferences[teacher].index(student) < teachers_preferences[teacher].index(least_preferred_student):
                    # Replace the least preferred student with the current student
                    teachers_assigned[teacher].remove(least_preferred_student)
                    teachers_assigned[teacher].append(student)
                    proposals[student] = teacher
                    proposals[least_preferred_student] = None
                    students_proposals[least_preferred_student] += 1
                else:
                    # If the teacher prefers all current students over the proposing student, increment proposal count
                    students_proposals[student] += 1

print(proposals)

# Example data



# Run the algorithm
