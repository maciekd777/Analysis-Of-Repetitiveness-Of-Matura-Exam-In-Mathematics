import pandas as pd

class DataStorage(object):
    old_exams = pd.DataFrame()
    new_exams = pd.DataFrame()
    old_perc = pd.DataFrame()
    new_perc = pd.DataFrame()

    @classmethod
    def concat_exam_results(cls, exam):
        if exam.cc_year == 2015:
            cls.old_exams = pd.concat([cls.old_exams, exam.exam_data], ignore_index=True)
        else:
            cls.new_exams = pd.concat([cls.new_exams, exam.exam_data], ignore_index=True)

    @classmethod
    def concat_perc_results(cls, perc):
        if perc.cc_year == 2015:
            cls.old_perc = pd.concat([cls.old_perc, perc.perc_data], ignore_index=True)
        else:
            cls.new_perc = pd.concat([cls.new_perc, perc.perc_data], ignore_index=True)

    @classmethod
    def save_all(cls):
        for df in [cls.old_exams, cls.new_exams, cls.old_perc, cls.new_perc]:
            df.index.rename("id", inplace=True)

        cls.old_exams.to_csv(f"CSV/Exams/old_exams.csv")
        cls.new_exams.to_csv(f"CSV/Exams/new_exams.csv")
        cls.old_perc.to_csv(f"CSV/Perc/old_perc.csv")
        cls.new_perc.to_csv(f"CSV/Perc/new_perc.csv")