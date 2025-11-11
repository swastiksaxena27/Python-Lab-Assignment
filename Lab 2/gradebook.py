# Name: Swastik Saxena
# Project Title: Gradebook Analyzer

import csv



def average(marks):
   
    if not marks:
        return 0
    total = sum(marks.values())
    return total / len(marks)

def median(marks):
    
    if not marks:
        return 0
    scores = sorted(marks.values())
    n = len(scores)
    if n % 2 == 0:
        mid = (scores[n//2 - 1] + scores[n//2]) / 2
    else:
        mid = scores[n//2]
    return mid

def highest(marks):
    
    if not marks:
        return 0
    return max(marks.values())

def lowest(marks):
    
    if not marks:
        return 0
    return min(marks.values())






def give_grades(marks):
    
    grades = {}
    for name, score in marks.items():
        if score >= 90:
            grades[name] = "A"
        elif score >= 80:
            grades[name] = "B"
        elif score >= 70:
            grades[name] = "C"
        elif score >= 60:
            grades[name] = "D"
        else:
            grades[name] = "F"
    return grades

def grade_count(grades): # counts grades
    count = {"A": 0, "B": 0, "C": 0, "D": 0, "F": 0}
    for g in grades.values():
        if g in count:
            count[g] += 1
    return count





def pass_fail(marks):
    passed = [name for name, score in marks.items() if score >= 40]
    failed = [name for name, score in marks.items() if score < 40]
    return passed, failed





def enter_marks():
    data = {}
    print("\nEnter student marks (type 'done' to stop).")
    while True:
        name = input("Student name: ")
        if name.lower() == "done":
            break
        mark = input("Enter mark: ")
        try:
            mark = int(mark)
            if 0 <= mark <= 100:
                data[name] = mark
            else:
                print("Please enter a number 0–100.")
        except:
            print("Invalid number.")
    return data







def load_csv(): 

    data = {}
    file = input("Enter CSV file name: ")
    try:
        with open(file, "r", newline="", encoding="utf-8") as f:
            reader = csv.reader(f)
            try:
                next(reader)  # skip header
            except StopIteration:
                print("Empty file.")
                return {}
            for row in reader:
                if len(row) >= 2:
                    name = row[0].strip()
                    try:
                        mark = int(row[1].strip())
                        data[name] = mark
                    except:
                        print(f"Skipping bad mark for {name}.")
                else:
                    print(f"Bad row: {row}")
        print(f"Loaded {len(data)} students.")
    except FileNotFoundError:
        print("File not found.")
    except Exception as e:
        print("Error:", e)
    return data






def print_table(marks, grades):
    print("\n--- Report Card ---")
    print("Name\t\tMarks\tGrade")
    print("----------------------------")
    for name in marks:
        print(f"{name}\t\t{marks[name]}\t{grades[name]}")





def analyze(marks):
    if not marks:
        print("No data to analyze.")
        return
    
    print("\nStats ")
    print("Average:", round(average(marks), 2))
    print("Median:", median(marks))
    print("Highest:", highest(marks))
    print("Lowest:", lowest(marks))

    grades = give_grades(marks)
    dist = grade_count(grades)

    print("\nGrade Counts")
    for g, c in dist.items():
        print(g, ":", c)

    passed, failed = pass_fail(marks)
    print("\nPass/fail")
    print("Passed:", len(passed), "-", ", ".join(passed) if passed else "None")
    print("Failed:", len(failed), "-", ", ".join(failed) if failed else "None")

    print_table(marks, grades)

def menu():
    print("\n---")
    print(" Welcome to gradebook ")
    print("---")
    print("1. Enter marks by hand")
    print("2. Load marks from csv")
    print("3. exit")

def main():
    while True:
        menu()
        choice = input("choose 1, 2, or 3: ")

        if choice == "1":
            data = enter_marks()
            analyze(data)
        elif choice == "2":
            data = load_csv()
            analyze(data)
        elif choice == "3":
            print("goodbye")
            break
        else:
            print("invalid choice.")

        if choice in ("1", "2"):
            input("Press enter to go back to menu.")

if __name__ == "__main__":
    main()