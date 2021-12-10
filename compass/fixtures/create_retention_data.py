import json
import random

with open("retention_data.json", "r") as retention_file:
    cleaned_students = []
    for stu_dict in students:
        stu_dict["student_fk"] = #1-100
        stu_dict["fields"]["priority"] = random.uniform(-5.0, 5.0)
        stu_dict["fields"]["sign_ins"] = random.uniform(-5.0, 5.0)
        stu_dict["fields"]["activity"] = random.uniform(-5.0, 5.0)
        stu_dict["fields"]["assignments"] = random.uniform(-5.0, 5.0)
        stu_dict["fields"]["grades"] = random.uniform(-5.0, 5.0)
        cleaned_students.append(stu_dict)
with open("retention_data_fixed.json", "w") as retention_file_fixed:
    retention_file_fixed.write(json.dumps(cleaned_students, indent=1))
