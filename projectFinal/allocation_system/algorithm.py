#Algorithm for the case of number of students higher than 
import math
def stable_matching(students_preferences, teachers_preferences):
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
                    least_preferred_student = current_students.pop(0)
                    teachers_assigned[teacher].append(student)
                    proposals[student] = teacher
                    proposals[least_preferred_student] = None
                    students_proposals[least_preferred_student] += 1
            if None not in proposals.values():
                break
    return proposals

# Example data
students_preferences = {
    'alice.johnson': ['John  ', 'Emily Johnson', 'Sarah Brown', 'Samantha Clark'],
    'bob.smith': ['Samantha Clark', 'John Smith', 'Sarah Brown', 'Emily Johnson'],
    'emma.davis': ['Emily Johnson', 'Sarah Brown', 'John Smith', 'Samantha Clark'],
    'sophia.brown': ['Emily Johnson', 'Sarah Brown', 'Samantha Clark', 'John Smith'],
    'johndoe': ['Emily Johnson', 'Sarah Brown', 'John Smith', 'Samantha Clark'],
    'janesmith': ['Samantha Clark', 'Sarah Brown', 'Emily Johnson', 'John Smith'],
    'davidw': ['Emily Johnson', 'John Smith', 'Samantha Clark', 'Sarah Brown']
}

teachers_preferences = {
    'johnsmith': ['Bob Smith', 'Alice Johnson', 'David Wilson', 'Jane Smith', 'Emma Davis', 'John Doe', 'Sophia Brown'],
    'emily.johnson': ['John Doe', 'Sophia Brown', 'Jane Smith', 'Alice Johnson', 'David Wilson', 'Bob Smith', 'Emma Davis'],
    'sarah.brown': ['Alice Johnson', 'Bob Smith', 'Emma Davis', 'Sophia Brown', 'David Wilson', 'Jane Smith', 'John Doe'],
    'sam.clark': ['Alice Johnson', 'Bob Smith', 'Emma Davis', 'Sophia Brown', 'John Doe', 'Jane Smith', 'David Wilson']
}


# Run the algorithm
matching = stable_matching(students_preferences, teachers_preferences)
print(matching)
