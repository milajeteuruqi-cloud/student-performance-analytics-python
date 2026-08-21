import csv
import json
from pathlib import Path

DATA_FILE = Path(__file__).with_name("students.csv")
REPORT_FILE = Path(__file__).with_name("report.json")

SUBJECTS = ("python", "ict", "math")


def load_students(path=DATA_FILE):
    """Read student scores from CSV and convert score fields to integers."""
    students = []
    with open(path, newline="", encoding="utf-8") as file:
        reader = csv.DictReader(file)
        for row in reader:
            student = {"name": row["name"]}
            for subject in SUBJECTS:
                score = int(row[subject])
                if not 0 <= score <= 100:
                    raise ValueError(f"Invalid {subject} score for {row['name']}")
                student[subject] = score
            students.append(student)
    return students


def student_average(student):
    return round(sum(student[s] for s in SUBJECTS) / len(SUBJECTS), 2)


def subject_averages(students):
    return {
        subject: round(sum(s[subject] for s in students) / len(students), 2)
        for subject in SUBJECTS
    }


def build_report(students):
    ranked = []
    for student in students:
        ranked.append({
            "name": student["name"],
            "average": student_average(student),
            "status": "Pass" if student_average(student) >= 60 else "Needs support",
        })

    ranked.sort(key=lambda item: item["average"], reverse=True)
    return {
        "class_size": len(students),
        "top_student": ranked[0]["name"] if ranked else None,
        "subject_averages": subject_averages(students),
        "students": ranked,
    }


def save_report(report, path=REPORT_FILE):
    with open(path, "w", encoding="utf-8") as file:
        json.dump(report, file, indent=2, ensure_ascii=False)


def print_summary(report):
    print("STUDENT PERFORMANCE REPORT")
    print("-" * 48)
    for row in report["students"]:
        print(f"{row['name']:<12} {row['average']:>6.2f}  {row['status']}")
    print("\nTop student:", report["top_student"])
    print("Subject averages:", report["subject_averages"])


def main():
    students = load_students()
    report = build_report(students)
    save_report(report)
    print_summary(report)


if __name__ == "__main__":
    main()
