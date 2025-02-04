
# Analysis of Repetitiveness of Matura Math Exam

This project is about analysing repetitiveness of tasks on Poland's Matura exam in mathematics. Here, on GitHub, I would like to share the code that was used to extract data, manipulate data, and create visuals. For more information about the project, head to it's page on Notion.

## Authors

- [@maciekd777](https://github.com/maciekd777)

## Tech Stack

**Data extraction:** Pandas, Py-Pdf-Parser, Excel

**Data manipulation:** Pandas, NumPy, Power BI

**Data visualization:** Matplotlib, Seaborn, Power BI

## Data Sources

All files in `PDF` folder are cropped files that originally were collected from following sources:

* Files: `2015.pdf`, `2016.pdf`, `2017.pdf`, `2018.pdf`, `2019.pdf`, `2020.pdf`, `2023.pdf`, `2024.pdf` from [cke.gov.pl](cke.gov.pl)
* Files: `2023_add.pdf`, `2024_add.pdf`, `2023_makeup.pdf` from [arkusze.pl](arkusze.pl)

All PDF files in `XL` folder are cropped files that originally were collected from [cke.gov.pl](cke.gov.pl), changed to XLSX files, and prepare in Excel for future extraction and analysis.

## Data Extraction

Entire extraction process was done in Python, mostly using Pandas, Py-Pdf-Parser, and Regular Expression modules. The entire code is available in following files: `main.py`, `DataStorage.py`, `ExamExtractor.py`, and `PercExtractor.py`.

## 

## Badges

[![MIT License](https://img.shields.io/badge/License-MIT-green.svg)](https://choosealicense.com/licenses/mit/)
