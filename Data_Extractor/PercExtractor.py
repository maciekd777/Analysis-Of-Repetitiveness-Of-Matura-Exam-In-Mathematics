import pandas as pd
import roman

EXTRACT_2023 = r"([IVX][IVX]?[IVX]?[IVX]?(?:\.\d\d?)?)\)"
EXTRACT_2015 =  r"((?:G|SP)?\d\d?\.\d\d?(?:|, (?:G|SP)?\d\d?\.\d\d?)?)\)"

class PercExtractor(object):

    def __init__(self, exam_year, cc_year, filename):
        self.exam_year = exam_year
        self.cc_year = cc_year
        self.xl_data = pd.read_excel(f"XL/Perc/{filename}.xlsx")
        self.perc_data = pd.DataFrame(columns=["req_id"])

    def clean_xl(self):
        self.xl_data["requirement"] = (self.xl_data["requirement"].str.replace("\n", "")
                                        .str.replace(r" +", " ", regex=True))

    def get_ct(self):
        self.perc_data["req_id"] = self.xl_data["requirement"].str.extractall(EXTRACT_2015 if self.cc_year == 2015 else EXTRACT_2023)

        try:
            self.perc_data.reset_index(inplace=True)
            self.perc_data.drop(columns=["match"], inplace=True)
            self.perc_data.rename(columns={"level_0": "id"}, inplace=True)
        except KeyError:
            pass

        self.perc_data.set_index("id", inplace=True)
        self.perc_data = self.perc_data.join(self.xl_data[["perc", "exc_numb"]])
        self.perc_data["perc"] = self.perc_data["perc"] / 100


    def clean_data(self):
        def to_roman(r):
            try:
                return str(roman.fromRoman(r.split(".")[0])) + "." + r.split(".")[1]
            except IndexError:
                return str(roman.fromRoman(r))

        self.perc_data["school_type"] = ["primary" if "SP" in ct else "middle" if "G" in ct else "high" for ct in self.perc_data["req_id"]]
        self.perc_data["req_id"] = self.perc_data["req_id"].str.replace("SP", "").str.replace("G", "")
        self.perc_data["req_year"] = self.cc_year
        self.perc_data["exam_year"] = self.exam_year
        self.perc_data["exam_type"] = "main"
        self.perc_data.index.rename("id", inplace=True)

        if self.cc_year == 2023:
            self.perc_data["req_id"] = [to_roman(req) for req in self.perc_data["req_id"].values]



    def get_perc(self):
        self.clean_xl()
        self.get_ct()
        self.clean_data()