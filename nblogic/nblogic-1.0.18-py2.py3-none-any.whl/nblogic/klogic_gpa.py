import mechanicalsoup
import json
import re
import art
import sys
import getpass


class KLOGIC:
    def __init__(self, apiMode=False):
        self.browser = mechanicalsoup.StatefulBrowser()
        self.result_all = dict()
        self.user_info = dict()
        self.grade_info = list()
        self.term_info = dict()
        self.student_bio = dict()
        self.username = ''
        self.program_id = None
        self.status = False
        self.apiMode = apiMode
        self.language = "TH"
        if self.apiMode:
            self.language = "EN"
        if not self.apiMode:
            self.welcome()

        self.word_mapping = {
            "COURSES_LIST": {
                "EN": "Courses_list",
                "TH": "รายวิชา"
            },
            "SEMESTER": {
                "EN": "Semester",
                "TH": "ประจำภาค"
            },
            "CUMULATIVE": {
                "EN": "Cumulative",
                "TH": "สะสม"
            },
            "AVERAGE_SCORE": {
                "EN": "Average_Score",
                "TH": "คะแนนฉลี่ย"
            },
            "REGISTERED_CREDIT": {
                "EN": "Registered_Credit",
                "TH": "หน่วยกิตที่ลง"
            },
            "ACHIEVE_CREDIT": {
                "EN": "Achieve_Credit",
                "TH": "หน่วยกิตที่ได้"
            },
            "TOTAL_SCORE": {
                "EN": "Total_Score",
                "TH": "แต้มระดับคะแนน"
            },
            "STATUS": {
                "EN": "Status",
                "TH": "สถานภาพ"
            },
            "USER_INFORMATION": {
                "EN": "User_Information",
                "TH": "รายละเอียดผู้ใช้งาน"
            },
            "USER_GRADE": {
                "EN": "User_Grade",
                "TH": "ผลการเรียน"
            },
            "USER_BIO": {
                "EN": "User_Bio",
                "TH": "ประวัตินักศึกษา"
            },
            "USER": {
                "EN": "User",
                "TH": "ผู้ใช้งาน"
            },
            "TIME": {
                "EN": "Time",
                "TH": "เวลา"
            },
            "CURRENTSEMESTER": {
                "EN": "Current_Semester",
                "TH": "ภาค/ปีการศึกษาปัจจุบัน"
            },
            "CURRENTSEMESTERWORK": {
                "EN": "Current_Work_Semester",
                "TH": "ปีการศึกษาที่ทำงานอยู่"
            },
            "STUDENT_ID": {
                "EN": "Student_ID",
                "TH": "เลขประจำตัว"
            },
            "STUDENT_NAME": {
                "EN": "Name",
                "TH": "ชื่อ"
            },
            "STUDENT_MAJOR": {
                "EN": "Major",
                "TH": "สาขา"
            },
            "STUDENT_DEPARTMENT": {
                "EN": "Department",
                "TH": "ภาควิชา"
            },
            "STUDENT_FACULTY": {
                "EN": "Faculty",
                "TH": "คณะ"
            },
            "COURSE_ID": {
                "EN": "Course_ID",
                "TH": "รหัสวิชา"
            },
            "COURSE_NAME": {
                "EN": "Course_Name",
                "TH": "ชื่อวิชา"
            },
            "COURSE_CREDIT": {
                "EN": "Course_Credit",
                "TH": "หน่วยกิต"
            },
            "COURSE_SECTION": {
                "EN": "Course_Section",
                "TH": "ตอนเรียน"
            },
            "COURSE_GRADE": {
                "EN": "Course_Grade",
                "TH": "เกรด"
            },
        }

    def welcome(self):
        art.tprint("KLOGIC")
        print("*----- Welcome to KLOGIC GPA Reporter -----*")

    def current_page(self):
        print("Page:", self.browser.get_url())

    def remove_xa(self, text):
        return text.replace("\xa0", "")

    def authentication(self, userName=None, passWord=None):
        self.klogic_site()
        if userName and passWord:
            username = userName
            password = passWord
        else:
            username = input("Username: ")
            password = getpass.getpass('Password: ')
        # password = input("Password: ")

        self.browser.select_form('form[action="/kris/index.jsp"]')

        self.browser["username"] = username
        self.browser["password"] = password

        # print(browser.get_current_form().print_summary())

        self.browser.submit_selected()

        page = self.browser.get_current_page()
        td_all = page.find_all("td", align="center", colspan="2")
        td_all_filter = [texts.text.strip() for texts in td_all]
        # print(td_all_filter)
        if ('รหัสผ่านไม่ถูกต้อง' in td_all_filter):
            return False

        self.username = username
        self.status = True
        return True

    def get_user_information(self, tables):

        user_td = tables[0].find_all("td")
        # print(user_td)
        self.user_info[self.word_mapping["USER"][self.language]] = re.search(r"(?<!\d)\d{13}(?!\d)",
                                                                             user_td[0].text).group(0)
        self.user_info[self.word_mapping["TIME"][self.language]] = user_td[1].text.replace("\xa0", "")
        self.user_info[self.word_mapping["CURRENTSEMESTER"][self.language]] = re.search(r"(?<!\d)\d{1,2}/\d{4}(?!\d)",
                                                                                        user_td[2].text).group(0)
        self.user_info[self.word_mapping["CURRENTSEMESTERWORK"][self.language]] = re.search(
            r"(?<!\d)\d{1,2}/\d{4}(?!\d)", user_td[3].text).group(0)
        # print(user_info)

        tables = tables[1:]

        user_td2 = tables[0].find_all("td")
        # print(user_td2)
        self.user_info[self.word_mapping["STUDENT_ID"][self.language]] = re.search(r"(?<!\d)\d{13}(?!\d)",
                                                                                   user_td2[0].text).group(0)
        self.user_info[self.word_mapping["STUDENT_NAME"][self.language]] = user_td2[1].text.replace("\xa0", "").replace(
            "ชื่อ", "").replace("\r\n", "")

        user_td3 = tables[1].find_all("td")
        # print(user_td3)

        self.user_info[self.word_mapping["STUDENT_MAJOR"][self.language]] = user_td3[0].text.replace("สาขา",
                                                                                                     "").replace("\xa0",
                                                                                                                 "")
        self.user_info[self.word_mapping["STUDENT_DEPARTMENT"][self.language]] = user_td3[1].text.replace("ภาควิชา",
                                                                                                          "").replace(
            "\xa0", "")
        self.user_info[self.word_mapping["STUDENT_FACULTY"][self.language]] = user_td3[2].text.replace("คณะ",
                                                                                                       "").replace(
            "\xa0", "")

        if not self.apiMode:
            print("*----- Get User information SUCCEED -----*")

    def get_grade_information(self, tables):
        # print("Grade Tables:", tables)
        for tb in tables:
            # print(tb)
            # break
            first_term = tb
            # print(first_term)
            ft_tr = first_term.find_all("tr")
            # print(ft_tr[2])
            # print(ft_tr[1:])
            ft = ft_tr[0].text.replace("\xa0", "")
            term_info = dict()
            term_info[ft] = {self.word_mapping["COURSES_LIST"][self.language]: []}
            self.term_info[ft] = {self.word_mapping["COURSES_LIST"][self.language]: []}
            # term_info = [{ft: {"รายวิชา": []}}]

            for tr in ft_tr[2:]:
                try:
                    ft_tr2_td = tr.find_all("td")
                    # print(ft_tr2_td)
                    course_info = {}
                    course_id = re.search(r"(?<!\d)\d{9}(?!\d)", ft_tr2_td[0].text).group(0)
                    course_info[self.word_mapping["COURSE_ID"][self.language]] = course_id
                    course_info[self.word_mapping["COURSE_NAME"][self.language]] = ft_tr2_td[0].text.replace(course_id,
                                                                                                             "").replace(
                        "\xa0", "").strip()
                    course_info[self.word_mapping["COURSE_CREDIT"][self.language]] = ft_tr2_td[1].text.strip()
                    course_info[self.word_mapping["COURSE_SECTION"][self.language]] = ft_tr2_td[2].text.strip()
                    course_info[self.word_mapping["COURSE_GRADE"][self.language]] = ft_tr2_td[3].text.strip()
                    # print(course_info)
                    term_info[ft][self.word_mapping["COURSES_LIST"][self.language]].append(course_info)
                    self.term_info[ft][self.word_mapping["COURSES_LIST"][self.language]].append(course_info)
                    # print(term_info)
                except:
                    # print(tr.find_all("td"))
                    result = tr.find_all("td")
                    # print(result)
                    result_first_row = result[0].find_all("td")
                    # print(result_first_row[6:])
                    result_first_row = result_first_row[6:]
                    term_info[ft][self.word_mapping["SEMESTER"][self.language]] = {
                        self.word_mapping["AVERAGE_SCORE"][self.language]: self.remove_xa(result_first_row[0].text),
                        self.word_mapping["REGISTERED_CREDIT"][self.language]: self.remove_xa(result_first_row[1].text),
                        self.word_mapping["ACHIEVE_CREDIT"][self.language]: self.remove_xa(result_first_row[2].text),
                        self.word_mapping["TOTAL_SCORE"][self.language]: self.remove_xa(result_first_row[3].text)}
                    self.term_info[ft][self.word_mapping["SEMESTER"][self.language]] = {
                        self.word_mapping["AVERAGE_SCORE"][self.language]: self.remove_xa(result_first_row[0].text),
                        self.word_mapping["REGISTERED_CREDIT"][self.language]: self.remove_xa(result_first_row[1].text),
                        self.word_mapping["ACHIEVE_CREDIT"][self.language]: self.remove_xa(result_first_row[2].text),
                        self.word_mapping["TOTAL_SCORE"][self.language]: self.remove_xa(result_first_row[3].text)}
                    result_first_row = result_first_row[5:]
                    # print(result_first_row)
                    term_info[ft][self.word_mapping["CUMULATIVE"][self.language]] = {
                        self.word_mapping["AVERAGE_SCORE"][self.language]: self.remove_xa(result_first_row[0].text),
                        self.word_mapping["REGISTERED_CREDIT"][self.language]: self.remove_xa(result_first_row[1].text),
                        self.word_mapping["ACHIEVE_CREDIT"][self.language]: self.remove_xa(result_first_row[2].text),
                        self.word_mapping["TOTAL_SCORE"][self.language]: self.remove_xa(result_first_row[3].text)}
                    self.term_info[ft][self.word_mapping["CUMULATIVE"][self.language]] = {
                        self.word_mapping["AVERAGE_SCORE"][self.language]: self.remove_xa(result_first_row[0].text),
                        self.word_mapping["REGISTERED_CREDIT"][self.language]: self.remove_xa(result_first_row[1].text),
                        self.word_mapping["ACHIEVE_CREDIT"][self.language]: self.remove_xa(result_first_row[2].text),
                        self.word_mapping["TOTAL_SCORE"][self.language]: self.remove_xa(result_first_row[3].text)}
                    term_info[ft][self.word_mapping["STATUS"][self.language]] = result[-1].text.strip()
                    self.term_info[ft][self.word_mapping["STATUS"][self.language]] = result[-1].text.strip()
                    break
            # print(term_info)
            if not self.apiMode:
                print("*------Get info for TERM:", ft, "SUCCEED ------*")
            self.grade_info.append(term_info)

    def get_information(self):
        if self.status:
            self.klogic_site()
            self.browser.follow_link("grade.jsp")
        else:
            if not self.apiMode:
                print("*----- Unauthorized: Please log in -----*")
            while self.authentication():
                pass
            self.browser.follow_link("grade.jsp")
        # current_page()
        page = self.browser.get_current_page()
        # print(page)

        tables = page.find_all("table")
        tables = tables[7:]

        self.get_user_information(tables)

        # print(user_info)

        # for td in tables[0]:
        #     print(td)
        # print(td.find("td"))
        # user_info[]

        tables = tables[3:]
        tables = tables[::2]

        self.get_grade_information(tables)
        # print(tables[::2])
        self.result_all[self.word_mapping["USER_INFORMATION"][self.language]] = self.user_info
        # self.result_all["ผลการเรียน"] = self.grade_info
        self.result_all[self.word_mapping["USER_GRADE"][self.language]] = self.term_info

    def get_bio(self):
        import re
        if self.status:
            self.klogic_site()
            self.browser.follow_link("student_bio.jsp")
        else:
            if not self.apiMode:
                print("*----- Unauthorized: Please log in -----*")
            while self.authentication():
                pass
            self.browser.follow_link("student_bio.jsp")

        page = self.browser.get_current_page()
        tables = page.find_all("table", align="center", width="100%")
        first_table = tables[0]
        first_table_tr = first_table.find_all("tr")
        for row in first_table_tr[1:]:
            row_td = row.find_all("td")
            self.student_bio[row_td[0].text.strip()] = row_td[1].text.strip()
            # print("{}: {}".format(row_td[0].text.strip(), row_td[1].text.strip()))
        program_id = re.findall("\(([^)]+)\)", self.student_bio["หลักสูตร"])
        self.student_bio["Program_ID"] = program_id[0]
        self.user_info["Program_ID"] = program_id[0]
        second_table = tables[1]
        second_table_tr = second_table.find_all("tr")
        for row in second_table_tr:
            row_td = row.find_all("td")
            self.student_bio[row_td[0].text.strip()] = row_td[1].text.strip()
            # print("{}: {}".format(row_td[0].text.strip(), row_td[1].text.strip()))

        third_table = tables[2]
        third_table_tr = third_table.find_all("tr")
        for row in third_table_tr[1:]:
            row_td = row.find_all("td")
            self.student_bio[row_td[0].text.strip()] = row_td[1].text.strip()
            # print("{}: {}".format(row_td[0].text.strip(), row_td[1].text.strip()))

        forth_table = tables[3]
        forth_table_tr = forth_table.find_all("tr")
        # print(forth_table_tr)
        for row in forth_table_tr[1:]:

            row_td = row.find_all("td")
            # print(row_td)
            # if(row_td[0].text == ""):
            #     self.student_bio["ที่อยู่(ต่อ)"] = row_td[1].text.strip()
            # else:
            # print("Length:", len(row_td))
            if len(row_td) == 6:
                self.student_bio[row_td[0].text.strip()] = row_td[1].text.strip()
                self.student_bio[row_td[2].text.strip()] = row_td[3].text.strip()
                self.student_bio[row_td[4].text.strip()] = row_td[5].text.strip()
            else:
                if (row_td[0].text == ""):
                    self.student_bio["ที่อยู่(ต่อ)"] = row_td[1].text.strip()
                else:
                    self.student_bio[row_td[0].text.strip()] = row_td[1].text.strip()

        fifth_table = tables[4]
        fifth_table_tr = fifth_table.find_all("tr")
        for row in fifth_table_tr:
            row_td = row.find_all("td")

            self.student_bio[row_td[0].text.strip()] = row_td[1].text.strip()

        sixth_table = tables[5]
        sixth_table_tr = sixth_table.find_all("tr")
        # print(sixth_table_tr[0])

        # print("ROW:",row)
        row_td = sixth_table_tr[0].find_all("td")
        # print(row_td)
        self.student_bio[row_td[0].text.strip()] = row_td[1].text.strip()
        # print("{}: {}".format(row_td[0].text.strip(), row_td[1].text.strip()))
        del self.student_bio[""]
        self.result_all[self.word_mapping["USER_BIO"][self.language]] = self.student_bio

        if not self.apiMode:
            print("*-------- Get Student Bio SUCCEED -------*")

    def get_program_course(self):
        if self.status:
            self.klogic_site()
            self.browser.follow_link("completion.jsp")
        else:
            if not self.apiMode:
                print("*----- Unauthorized: Please log in -----*")
            while self.authentication():
                pass
            self.browser.follow_link("completion.jsp")

        # current_page()
        all_course = list()
        attemp = list()
        attemp_with_credit = list()
        unknown_credit = list()
        update_course = list()
        page = self.browser.get_current_page()
        # print(page)

        tables = page.find_all("table")  # Get all tables

        self.get_user_information(tables[7:])
        self.get_bio()

        tables = tables[11:]  # Start at useful data table

        tables_td_4 = tables[0].find_all("td", colspan="4")  # Find table that data within
        # print(tables_td_4[0])
        for tr in tables_td_4:
            tables_td_4_tr = tr.find_all("tr")
            for td in tables_td_4_tr:
                tables_td_4_tr_td = td.find_all("td")
                result = [x.text.replace("\n", "").strip() for x in tables_td_4_tr_td]
                # print(result)
                if len(result[0].split(" ")) == 2:
                    # Unknown credit
                    course_id = result[0].split(" ")[0]
                    course_credit = ""
                    course_name = result[0].replace(course_id, "").strip()
                    all_course.append({"Course_id": course_id, "Name": course_name, "Credit_points": course_credit
                                       })
                    unknown_credit.append({"Course_id": course_id, "Name": course_name, "Credit_points": course_credit
                                       })

                else:
                    course_id = result[0].split(" ")[0]
                    course_credit = result[0].split(" ")[-1]
                    course_credit_only = result[0].split(" ")[-1].split("(")[0]
                    course_name = result[0].replace(course_id, "").replace(course_credit, "").strip()
                    all_course.append({"Course_id": course_id, "Name": course_name, "Credit_points": course_credit_only
                                       })
                if result[-1] != '' and result[-2] != '' and result[-3] != '':
                    # Achieve grade
                    semester = result[-1].split("/")[0]
                    year = str(int(result[-1].split("/")[1])-543)
                    grade = result[-2]
                    credit = result[-3]
                    attemp.append({"Student_id": self.username, "Course_id": course_id, "Year": year,
                                   "Semester": semester, "Grade": grade})
                    attemp_with_credit.append({"Student_id": self.username, "Course_id": course_id, "Year": year,
                                   "Semester": semester, "Grade": grade, "Credit_points": credit})

        # print(all_course)
        # print(len(all_course))
        # print(attemp)
        # print(len(attemp))
        # print(unknown_credit)
        # print(self.username)

        for course in unknown_credit:
            for attemp_ in  attemp_with_credit:
                # print(course['Course_id'], attemp_['Course_id'])
                if(attemp_["Course_id"] == course['Course_id'] and attemp_["Credit_points"]):
                    update_course.append({"Course_id": attemp_['Course_id'], "Credit_points": attemp_['Credit_points']})
        for course_u in update_course:
            for course_a in all_course:
                if course_u["Course_id"] == course_a["Course_id"]:
                    course_a["Credit_points"] = course_u["Credit_points"]

        self.all_course = all_course
        self.attemp = attemp
        self.update_course = update_course
        self.full_course = {"User_info": self.user_info,"all_course": all_course, "attemp": attemp}
        # with open('course_dict_sql_klogic.json', 'w+', encoding='utf8') as outfile:
        #     json.dump(all_course, outfile, indent=4, ensure_ascii=False)
        # with open('course_dict_sql_attemp_klogic.json', 'w+', encoding='utf8') as outfile:
        #     json.dump(attemp, outfile, indent=4, ensure_ascii=False)
        # with open('course_dict_sql_update_course_klogic.json', 'w+', encoding='utf8') as outfile:
        #     json.dump(update_course, outfile, indent=4, ensure_ascii=False)
        # with open('course_dict_full_course_klogic.json', 'w+', encoding='utf8') as outfile:
        #     json.dump(self.full_course, outfile, indent=4, ensure_ascii=False)


    def get_course_bot(self):
        browser = mechanicalsoup.StatefulBrowser(soup_config={'features': 'html.parser'})
        # self.tess_site()
        browser.open("http://klogic.kmutnb.ac.th:8080/kris/tess/dataQuerySelector.jsp?query=openSectionTab")
        page = browser.get_current_page()
        options = page.find_all("option")[1:]
        options_dict_dept = dict()
        options_dict_fac = dict()
        # options_dict_fac = [{option["value"]: option.text.replace(option["value"], "").replace(
        #     "\n", "").replace("\t", "").strip()} for option in options if len(option["value"]) == 2]
        # options_dict_dept = [{option["value"]: option.text.replace(option["value"], "").replace(
        #     "\n", "").replace("\t", "").strip()} for option in options if len(option["value"]) > 2]
        for option in options:

            if len(option["value"]) == 2:
                options_dict_fac[option["value"]] = option.text.replace(option["value"], "").replace("\n", "")\
                    .replace("\t", "").strip()
            else:
                options_dict_dept[option["value"]] = option.text.replace(option["value"], "").replace("\n", "") \
                    .replace("\t", "").strip()

        del options_dict_dept['']
        # print(options_dict_fac)

        print(options_dict_dept)
        new_options_dict = dict()
        for fac in options_dict_fac:
            dept_list = list()
            for dept in options_dict_dept:
                if dept[:2] == fac:
                    dept_list.append({dept: options_dict_dept[dept]})
            new_options_dict[fac] = {"name": options_dict_fac[fac], "depts": dept_list}

        # print(new_options_dict)
        # with open('new_options_dict.json', 'w+', encoding='utf8') as outfile:
        #     json.dump(new_options_dict, outfile, indent=4, ensure_ascii=False)

        course_dict = dict()
        course_dict_sql = list()
        program_list = list()
        # fucking loop
        for fac, val in new_options_dict.items():
            # print(fac, val["depts"])
            print("Faculty:", fac, val["name"])
            for dept in val["depts"]:
                print("Department:", dept, fac)
                # print(selected_form.print_summary())
                forms = page.find_all("form")

                selected_form = browser.select_form(forms[0])

                selected_form.set("facCode", fac)
                # print("-----------------------------")
                browser.submit_selected()
                # selected_form.print_summary()
                # print("-----------------------------")
                page = browser.get_current_page()
                forms = page.find_all("form")
                selected_form = browser.select_form(forms[0])
                selected_form.set("deptCode", dept)
                # print("*****************************")
                #
                # selected_form.print_summary()
                # print("*****************************")
                browser.submit_selected()
                # selected_form.print_summary()
                page = browser.get_current_page()
                programs = page.find_all("option")

                # Get all programs
                programs_value = dict()
                for program in programs[len(options_dict_fac) + 3 + len(val["depts"]):]:
                    # print(major["value"])
                    programs_value[program["value"]] = program.text.replace("\n", "").replace("\t", "").strip()
                    program_list.append({"Name": programs_value[program["value"]]
                                        .replace(program["value"], "").strip(),
                                         "Program_id": program["value"], "Faculty": val["name"],
                                         "Department": list(dept.values())[0]})
                    # print(list(dept.values())[0])
                    print({"Name": programs_value[program["value"]]
                                        .replace(program["value"], "").strip(),
                                         "Program_id": program["value"], "Faculty": val["name"],
                                         "Department": list(dept.values())[0]})

                # Get all courses in programs
                for program in programs_value:
                    forms = page.find_all("form")
                    selected_form = browser.select_form(forms[-1])

                    selected_form.set("currCode", program)
                    browser.submit_selected()
                    page = browser.get_current_page()
                    all_tables = page.find_all("table")
                    data_table = all_tables[5]

                    course_table = data_table.find_all("tr", bgcolor="#EA98FF")

                    for course in course_table:
                        course_td = course.find("td")
                        course_id = course_td.text.split(" ")[0].replace("\n", "")
                        course_credit = course_td.text.split(" ")[-1].replace("\n", "")
                        course_credit_only = course_td.text.split(" ")[-1].split("(")[0]
                        course_name = course_td.text.replace(course_id + " ", "").replace(
                            " " + course_credit, "").replace("\n", "")
                        # print(course_td.text)
                        course_dict[course_id] = {"course_name": course_name, "course_credit": course_credit_only}
                        course_dict_sql.append(
                            {"Course_id": course_id, "Name": course_name, "Credit_points": course_credit_only,
                             "Program": program})
                    print(program, "complete!")

        print(new_options_dict)

        # with open('course_dict_full_sql.json', 'w+', encoding='utf8') as outfile:
        #     json.dump(course_dict_sql, outfile, indent=4, ensure_ascii=False)
        with open('program_full_sql.json', 'w+', encoding='utf8') as outfile:
            json.dump(program_list, outfile, indent=4, ensure_ascii=False)


    def get_program_course_for_current_semester(self):
        fac = "01"
        dept = fac + "01"
        program = "59010124"
        browser = mechanicalsoup.StatefulBrowser(soup_config={'features': 'html.parser'})
        # self.tess_site()
        browser.open("http://klogic.kmutnb.ac.th:8080/kris/tess/dataQuerySelector.jsp?query=openSectionTab")
        page = browser.get_current_page()
        forms = page.find_all("form")
        selected_form = browser.select_form(forms[0])
        selected_form.set("facCode", fac)
        selected_form.set("deptCode", dept)
        # selected_form.print_summary()
        browser.submit_selected()
        page = browser.get_current_page()
        forms = page.find_all("form")
        selected_form = browser.select_form(forms[-1])

        selected_form.set("currCode", program)
        browser.submit_selected()
        page = browser.get_current_page()
        all_tables = page.find_all("table")
        data_table = all_tables[5]

        course_table = data_table.find_all("tr", bgcolor="#EA98FF")
        course_dict = dict()
        course_dict_sql = list()
        for course in course_table:
            course_td = course.find("td")
            course_id = course_td.text.split(" ")[0].replace("\n", "")
            course_credit = course_td.text.split(" ")[-1].replace("\n", "")
            course_name = course_td.text.replace(course_id+" ", "").replace(
                " "+course_credit, "").replace("\n", "")
            # print(course_td.text)
            course_dict[course_id] = {"course_name": course_name, "course_credit": course_credit}
            course_dict_sql.append({"Course_id": course_id, "Name": course_name, "Credit_points": course_credit,
                                    "Program": "59010126"})
        print(course_dict_sql)
        with open('course_dict_sql.json', 'w+', encoding='utf8') as outfile:
            json.dump(course_dict_sql, outfile, indent=4, ensure_ascii=False)
        # first_link = self.browser.links()[-1]
        # browser.follow_link(first_link)
        # self.browser.follow_link("dataQuerySelector.jsp?query=teachTab")
        # page = browser.get_current_page()
        # self.current_page()
        # print(forms)

    def gradedb(self):
        if self.term_info:
            import pandas as pd
            db = pd.DataFrame(columns=['Course Id', 'Course Name', 'Year', 'Semester', 'Credit', 'Section',
                                       'Grade', 'Grade(Score)'])
            grade_table = {
                'A': 4,
                'B+': 3.5,
                'B': 3,
                'C+': 2.5,
                'C': 2,
                'D+': 1.5,
                'D': 1,
                'F': 0
            }
            for term in self.term_info:
                year_split = term.split(" ")  # Extract the selected term
                year = year_split[1]  # Get the year
                semester = year_split[3]  # Get the semester
                for row in self.term_info[term][self.word_mapping["COURSES_LIST"][self.language]]:
                    db = db.append({'Course Id': row[self.word_mapping["COURSE_ID"][self.language]],
                                    'Course Name': row[self.word_mapping["COURSE_NAME"][self.language]], 'Year': year,
                                    'Semester': semester,
                                    'Credit': row[self.word_mapping["COURSE_CREDIT"][self.language]],
                                    'Section': row[self.word_mapping["COURSE_SECTION"][self.language]],
                                    'Grade': row[self.word_mapping["COURSE_GRADE"][self.language]],
                                    'Grade(Score)': grade_table[row[self.word_mapping["COURSE_GRADE"][self.language]]]},
                                   ignore_index=True)

            return db
        else:
            if not self.apiMode:
                print("No term information!")
                print("Getting information...")
            self.get_information()
            return self.gradedb()

    def klogic_site(self):
        self.browser.open("http://klogic2.kmutnb.ac.th:8080/kris/index.jsp")

    def icit_site(self):
        self.browser.open("http://grade-report.icit.kmutnb.ac.th/auth/signin")

    def tess_site(self):
        self.browser.open("http://klogic.kmutnb.ac.th:8080/kris/tess/dataQuerySelector.jsp")

    def generate_json(self):

        with open('report_{}.json'.format(self.username), 'w+', encoding='utf8') as outfile:
            json.dump(self.result_all, outfile, indent=4, ensure_ascii=False)

        if not self.apiMode:
            print("*----- Generate JSON report for user => {} COMPLETE -----*".format(self.username))

    def json(self, language="TH", var="result"):
        if language == "EN":
            if var == "result":
                return json.dumps(self.translate(), ensure_ascii=False).encode("utf8")
        else:
            if var == "result":
                return json.dumps(self.result_all, ensure_ascii=False).encode("utf8")
            elif var == "all_course":
                return json.dumps(self.all_course, ensure_ascii=False).encode("utf8")
            elif var == "attemp":
                return json.dumps(self.attemp, ensure_ascii=False).encode("utf8")
            elif var == "update_course":
                return json.dumps(self.update_course, ensure_ascii=False).encode("utf8")
            elif var == "full_course":
                return json.dumps(self.full_course, ensure_ascii=False).encode("utf8")

    def translate(self):
        from copy import deepcopy
        # print(self.result_all['User Bio'])
        # print(self.result_all.keys())

        # keys = [*self.result_all['User Bio']]
        # keys = map(lambda x: self.language_mapper(x), keys)
        translated_bio = dict()

        for key, value in self.result_all['User_Bio'].items():
            translated_bio[self.language_mapper(key)] = value
        # print(translated_bio)

        # print(self.result_all['User Grade'])
        translated_grade = {}
        for key, value in self.result_all['User_Grade'].items():
            # print(key)
            tg = key.replace("ปีการศึกษา", "Year").replace("ภาคการศึกษาที่", "Semester")
            translated_grade[tg] = value
        # print(translated_grade)

        result_all = deepcopy(self.result_all)
        result_all['User_Bio'] = translated_bio
        result_all['User_Grade'] = translated_grade
        result_all['User_Summary'] = self.full_course
        return result_all


    def language_mapper(self, word):
        word_list = {
            "เลขประจำตัว": "Student_ID",
            "ชื่อภาษาไทย": "Thai_Name",
            "ชื่อภาษาอังกฤษ": "English_Name",
            "เพศ": "Sex",
            "ระดับ": "Degree",
            "สาขา": "Major",
            "ประเภทนักศึกษา": "Student_Type",
            "หลักสูตร": "Program",
            "แผน": "Program2",
            "วิชาเอก": "Main_Course",
            "ปีที่เข้า": "Year_Enrolled",
            "วิทยาเขต": "Campus",
            "เลขที่บัญชี": "Account_Number",
            "สถานะนักศึกษา": "Student_Status",
            "ชั้นปีที่": "Year",
            "บัตรประชาชน": "ID_Card",
            "วันเกิด": "Birth_Date",
            "ภูมิลำเนา": "Home_Town",
            "ส่วนสูง": "Height",
            "น้ำหนัก": "Weight",
            "กลุ่มเลือด": "Blood_Group",
            "เป็นบุตรคนที่": "Is_the_child_of",
            "จากจำนวนทั้งหมด": "From_total",
            "ที่อยู่ *": "Address",
            "ที่อยู่(ต่อ)": "Address_",
            "โทรศัพท์": "Telephone",
            "อาศัยอยู่กับ": "Live_with",
            "ค่าใช้จ่ายต่อเดือน": "Expense",
            "ได้รับอุปการะด้านการเงินจาก": "Funded_by",
            "Program_ID": "Program_ID"
        }
        return word_list[word]


if __name__ == "__main__":
    klogic = KLOGIC(apiMode=True)
    username = ""
    password = ""
    # klogic.get_course_bot()
    # klogic.current_page()
    # if klogic.authentication(username, password):
    #     klogic.get_program_course()
        # print(json.loads(klogic.json(var="all_course")))
        # print(json.loads(klogic.json(var="update_course")))
        # print(json.loads(klogic.json(var="attemp")))
        # print(json.loads(klogic.json(var="full_course")))
        # klogic.get_bio()
        # klogic.get_information()
        # print(json.loads(klogic.json(language="EN")))

