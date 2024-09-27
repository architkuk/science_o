import csv
import random
from collections import defaultdict

# Constants
MAX_VARSITY = 15
EVENTS = {
    'Period 1': ['Air Trajectory', 'Disease Detectives', 'Fossils', 'Meteorology',
                  'Metric Mastery', 'Microbe Mission', 'Experimental Design', 'Mission Possible'],
    'Period 2': ['Codebusters', 'Crimebusters', 'Helicopter', 'Reach for the Stars',
                  'Road Scholar', 'Tower', 'Optics', 'Ecology'],
    'Period 3': ['Anatomy', 'Dynamic Planet', 'Entomology', 'Potions', 
                  'Scrambler', 'Wind Power', 'Write it Do it']
}

LOCATIONS = ['North Charlotte', 'South Charlotte', 'Waxhaw']

# Read student data from CSV
def read_students(file_path):
    students = []
    with open(file_path, newline='') as csvfile:
        reader = csv.reader(csvfile)
        first = True
        for row in reader:
            if first:
                first = False
                continue
            if row:  # Ensure row is not empty
                breakpoint()
                students.append({
                    'name': row[0],
                    'grade': int(row[1]),
                    'location': row[2],
                    'choices': {
                        'Period 1': row[3],
                        'Period 2': row[4],
                        'Period 3': row[5]
                    }
                })
    return students

def assign_students(students):
    assigned = defaultdict(list)
    lottery = []
    waiting_list = []

    eighth_graders = [s for s in students if s['grade'] == 8]
    seventh_graders = [s for s in students if s['grade'] == 7]
    sixth_graders = [s for s in students if s['grade'] == 6]

    prioritized = eighth_graders + [s for s in seventh_graders if s.get('previous_participation')] + sixth_graders + [s for s in seventh_graders if s not in seventh_graders]

    if len(prioritized) > MAX_VARSITY:
        lottery = random.sample(prioritized, MAX_VARSITY)
    else:
        lottery = prioritized

    event_assignments = defaultdict(list)

    for student in lottery:
        for period, event in student['choices'].items():
            if event in EVENTS[period] and len(event_assignments[event]) < 2:
                event_assignments[event].append(student)
                break
        else:
            waiting_list.append(student)  # No assignment made

    return event_assignments, waiting_list

def main(csv_file):
    students = read_students(csv_file)
    event_assignments, waiting_list = assign_students(students)

    for event, assigned_students in event_assignments.items():
        print(f"{event}: {[student['name'] for student in assigned_students]}")

    print("\nJV Team:")
    for student in waiting_list:
        print(student['name'])

if __name__ == '__main__':
    main('students.csv')
