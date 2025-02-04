import pandas as pd
import roman
import re
from py_pdf_parser.loaders import load


class ExamExtractor(object):

    def __init__(self, exam_year, exam_type, cc_year, filename):
        self.exam_year = exam_year
        self.exam_type = exam_type
        self.cc_year = cc_year
        self.filename = filename
        self.pdf_data = pd.DataFrame(columns=["row"])
        self.points_data = pd.DataFrame(columns=["exc_numb", "points"])
        self.topic_count = pd.DataFrame(columns=["exc_numb", "topic_count"])
        self.exam_data = pd.DataFrame(columns=["exc_numb", "req_id"])

    def get_regex(self, func: str):
        if self.exam_year in range(2015, 2021):
            regex_dict = {
                "get_topic_points": r"(?:(?:(?:G|SP)?\d\d?\.\d\d?(?:, (?:G|SP)?\d\d?\.\d\d?)?)\)|Zadanie)",
                "extract_points": r"Zadanie (\d\d?)\. \(0[–-−](\d)\)",
                "get_ct_data": r"((?:G|SP)?\d\d?\.\d\d?(?:|, (?:G|SP)?\d\d?\.\d\d?)?)\)"
            }
        else:
            regex_dict = {
                "get_topic_points": r"(?:(?:I|II|III|IV|V|VI|VII|VIII|IX|X|XI|XII)\.\d\d?\)|"
                                    r"XIII\)|"
                                    r"Zadanie)",
                "extract_points": r"Zadanie (\d\d?.*)\. \(0[–-−](\d)\)",
                "get_ct_data_1": r"Zadanie (\d\d?.*)\. \(",
                "get_ct_data_2": r"((?:I|II|III|IV|V|VI|VII|VIII|IX|X|XI|XII|XIII)(?:\.\d\d?)?)\)"
            }

        return regex_dict[func]


    def make_pdf_data(self, parsed_pdf):
        self.pdf_data["row"] = [row.text() for row in parsed_pdf.elements]

    def clean_pdf_data(self):
        self.pdf_data["row"] = (self.pdf_data["row"].str.replace("\n", "")
                                .str.replace(r" +", " ", regex=True))

    def slice_pdf_data(self):
        try:
            end_index = self.pdf_data[self.pdf_data["row"].str.contains("dyskalkulią")].index.values[0]
            self.pdf_data = self.pdf_data.iloc[:end_index, :]
        except IndexError:
            pass


    def get_topic_points(self):
        self.pdf_data = self.pdf_data[
            self.pdf_data["row"].str.contains(self.get_regex("get_topic_points"), regex=True)]


    def extract_points(self):
        self.points_data[["exc_numb", "points"]] = self.pdf_data["row"].str.extract(self.get_regex("extract_points"))
        self.points_data.dropna(inplace=True)
        self.points_data.reset_index(drop=True, inplace=True)
        self.points_data["points"] = self.points_data["points"].astype(int)


    def get_ct_data(self):
        exc_list = []
        exc_count = 0

        if self.cc_year == 2023:
            for row in self.pdf_data["row"].values:
                if "Zadanie" in row:
                    exc_list.append(re.findall(self.get_regex("get_ct_data_1"), row)[0])
                if ct := re.findall(self.get_regex("get_ct_data_2"), row):
                    for chapter_topic in ct:
                        self.exam_data.loc[self.exam_data.size, :] = exc_list[-1], chapter_topic
        else:
            for row in self.pdf_data["row"].values:
                if "Zadanie" in row:
                    exc_count += 1
                if ct := re.findall(self.get_regex("get_ct_data"), row):
                    for chapter_topic in ct:
                        self.exam_data.loc[self.exam_data.size, :] = exc_count, chapter_topic

        self.exam_data.dropna(inplace=True)
        self.exam_data.reset_index(inplace=True, drop=True)


    def extract_ct(self):
        numbers = []
        ctopics = []

        for n, ct in enumerate(self.exam_data["req_id"].values):
            if ", "in ct:
                for single_ct in ct.split(", "):
                    ctopics.append(single_ct)
                    numbers.append(self.exam_data.loc[n, "exc_numb"])
            else:
                ctopics.append(ct)
                numbers.append(self.exam_data.loc[n, "exc_numb"])

        self.exam_data = pd.DataFrame(
            {
                "exc_numb": numbers,
                "req_id": ctopics
            }
        )

    def add_types(self):
        self.exam_data["school_type"] = ["primary" if "SP" in ct else "middle" if "G" in ct else "high" for ct in self.exam_data["req_id"]]
        self.exam_data["req_id"] = self.exam_data["req_id"].str.replace("SP", "").str.replace("G", "")

    def get_exc_size(self):
        for e_numb in self.exam_data["exc_numb"].values:
            self.topic_count.loc[self.topic_count.size, :] = e_numb, self.exam_data[self.exam_data["exc_numb"] == e_numb]["exc_numb"].count()

        self.topic_count.drop_duplicates(inplace=True)
        self.topic_count.reset_index(inplace=True, drop=True)
        self.topic_count["topic_count"] = self.topic_count["topic_count"].astype(int)

    def get_part_points(self):
        self.points_data["exc_numb"] = self.points_data["exc_numb"].astype(str)
        self.topic_count["exc_numb"] = self.topic_count["exc_numb"].astype(str)

        self.points_data = self.points_data.join(self.topic_count.set_index("exc_numb"), on="exc_numb", validate="many_to_one")
        self.points_data["points"] = self.points_data["points"] / self.points_data["topic_count"]

        self.points_data.drop(columns=["topic_count"], inplace=True)

    def merge_points_ct(self):
        self.exam_data["exc_numb"] = self.exam_data["exc_numb"].astype(str)

        self.exam_data = self.exam_data.join(self.points_data.set_index("exc_numb"), on="exc_numb")

        self.exam_data["points"] = round(self.exam_data["points"], 2)

    def add_info(self):
        self.exam_data["req_year"] = self.cc_year
        self.exam_data["exam_year"] = self.exam_year
        self.exam_data["exam_type"] = self.exam_type
        self.exam_data.index.rename("id", inplace=True)

    def clean_romans(self):
        def to_roman(r):
            try:
                return str(roman.fromRoman(r.split(".")[0])) + "." + r.split(".")[1]
            except IndexError:
                return str(roman.fromRoman(r))

        self.exam_data["req_id"] = [to_roman(req) for req in self.exam_data["req_id"].values]

    def get_data(self):
        self.make_pdf_data(load(f"PDF/Exams/{self.filename}.pdf"))
        self.clean_pdf_data()
        self.slice_pdf_data()
        self.get_topic_points()

        self.extract_points()
        self.get_ct_data()
        self.extract_ct()
        self.add_types()
        self.get_exc_size()
        self.get_part_points()
        self.merge_points_ct()
        self.add_info()
        if self.cc_year == 2023:
            self.clean_romans()

