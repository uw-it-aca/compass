import json
import random

with open("student_data.json", "r") as student_file:
    students = eval(student_file.read())
    names_file = open("random_names.txt", "r")
    names = [name.strip() for name in names_file]
    cleaned_students = []
    for idx, stu_dict in enumerate(students):
        name = names.pop()
        first_name, last_name = name.split(", ")
        initials = first_name[0].lower() + last_name[0].lower()
        stu_dict["fields"]["uw_reg_id"] = ""
        stu_dict["fields"]["canvas_user_id"] = ""
        stu_dict["fields"]["student_name"] = name
        stu_dict["fields"]["student_preferred_first_name"] = first_name
        stu_dict["fields"]["student_preferred_middle_name"] = None
        stu_dict["fields"]["student_preferred_last_name"] = last_name
        net_id = "{}{}".format(initials, random.randint(1,999))
        stu_dict["fields"]["uw_net_id"] = net_id
        stu_dict["fields"]["student_email"] = "{}{}@uw.edu".format(net_id, random.randint(1,999))
        stu_dict["fields"]["external_email"] = "{}{}@gmail.com".format(net_id, random.randint(1,999))
        stu_dict["fields"]["student_number"] = random.randint(1000000, 2000000)
        stu_dict["fields"]["local_phone_number"] = "(206) {}-{}".format(random.randint(100,999), random.randint(1000,9999))
        stu_dict["fields"]["perm_addr_line1"] = "123 Salmon Way"
        stu_dict["fields"]["perm_addr_line2"] = "Apt. 3"
        stu_dict["fields"]["perm_addr_city"] = "Seattle"
        stu_dict["fields"]["perm_addr_state"] = "WA"
        stu_dict["fields"]["perm_addr_5digit_zip"] = "98102"
        stu_dict["fields"]["perm_addr_4digit_zip"] = "0021"
        stu_dict["fields"]["perm_addr_country"] = "USA"
        stu_dict["fields"]["perm_addr_postal_code"] = "98102-0021"
        special_program_code = random.choice(range(1, 84))
        stu_dict["fields"]["special_program"] = [special_program_code]
        stu_dict["fields"]["retention"] = idx
        stu_dict["fields"]["honors_program_code"] = 0
        stu_dict["fields"]["honors_program_ind"] = "N"
        stu_dict["fields"]["uw_reg_id"] = "9136CCB8F66711D5BE060004AC494FFE"
        stu_dict["fields"]["canvas_user_id"] = random.randint(10000, 90000)
        resident_code = random.choice(range(0,6))
        res_code_map = {
            0: "Unknown",
            1: "RESIDENT",
            2: "RESIDENT IMMIGRANT",
            3: "NONRESIDENT CITIZEN",
            4: "NONRESIDENT IMMIGRANT",
            5: "NONRESIDENT STUDENT VISA",
            6: "NONCITIZEN OTHER"
        }
        stu_dict["fields"]["resident_code"] = str(resident_code)
        stu_dict["fields"]["resident_desc"] = res_code_map[resident_code]
        class_code = random.choice(range(0,14))
        class_code_map = {
            0: "Pending",
            1: "Freshman",
            2: "Sophomore",
            3: "Junior",
            4: "Senior",
            5: "Post-Baccalaureate",
            6: "Non-Matriculated",
            7: "Invalid",
            8: "Graduate",
            11: "1st Year Professional	",
            12: "2nd Year Professional",
            13: "3rd Year Professional",
            14: "4th Year Professional"
        }
        stu_dict["fields"]["class_code"] = str(class_code)
        stu_dict["fields"]["class_desc"] = class_code_map.get(class_code, 1)
        campus_code = random.choice([0,1,2])
        campus_code_map = {
            0: "Seattle",
            1: "Bothell",
            2: "Tacoma"
        }
        stu_dict["fields"]["campus_code"] = campus_code
        stu_dict["fields"]["campus_desc"] = campus_code_map[campus_code]
        stu_dict["fields"]["registered_in_quarter"] = random.choice([True, False])
        cleaned_students.append(stu_dict)
with open("student_data_fixed.json", "w") as student_file_fixed:
    student_file_fixed.write(json.dumps(cleaned_students, indent=1))

