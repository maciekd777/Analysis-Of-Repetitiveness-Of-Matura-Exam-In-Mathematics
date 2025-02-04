from Data_Extractor.ExamExtractor import ExamExtractor
from Data_Extractor.PercExtractor import PercExtractor
from Data_Extractor.DataStorage import DataStorage

EXAMS = [[exam_year, "main", 2015, f"{exam_year}"] for exam_year in range (2015, 2021)]
EXAMS.extend([
    [2023, "main", 2023, "2023"],
    [2023, "additional", 2023, "2023_add"],
    [2024, "main", 2023, "2024"],
    [2024, "additional", 2023, "2024_add"],
    [2024, "make-up", 2023, "2024_makeup"]
])

def main():
    for exam_year, exam_type, cc_year, filename in EXAMS:

        exam = ExamExtractor(exam_year, exam_type, cc_year, filename)
        exam.get_data()
        DataStorage.concat_exam_results(exam)

        if exam_type == "main":
            perc = PercExtractor(exam_year, cc_year, filename)
            perc.get_perc()
            DataStorage.concat_perc_results(perc)

    DataStorage.save_all()


if __name__ == "__main__":
    main()