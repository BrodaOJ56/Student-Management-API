def get_grade(score):
    """ Convert a score to corresponding grade """
    if score < 100 and score > 89:
        return 'A'
    elif score < 90 and score > 79:
        return 'B'
    elif score < 80 and score > 69:
        return 'C'
    elif score < 70 and score > 59:
        return 'D'
    elif score < 60 and score > 49:
        return 'E'
    elif score < 50 :
        return 'F'    
    else:
        return 'F'

def convert_grade_to_gpa(grade):
    """Convert a grade to the corresponding point value """
    if grade == 'A':
        return 4.0
    elif grade == 'B':
        return 3.3
    elif grade == 'C':
        return 2.3
    elif grade == 'D':
        return 1.3
    else:
        return 0.0