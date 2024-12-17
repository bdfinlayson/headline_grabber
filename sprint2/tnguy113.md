# Sprint 2

## Table of Contents

- [Sprint 2](#sprint-2)
  - [Table of Contents](#table-of-contents)
  - [Group Basic Information](#group-basic-information)
  - [Individual Reflection](#individual-reflection)
    - [1. What you planned to do?](#1-what-you-planned-to-do)
    - [2. What you did not do?](#2-what-you-did-not-do)
    - [3. What problems you encountered?](#3-what-problems-you-encountered)
    - [4. Issues completed](#4-issues-completed)
    - [5. Files you worked on](#5-files-you-worked-on)
    - [6. What you accomplished?](#6-what-you-accomplished)
      - [HG32 - Add some unit test for Reu scrapping](#hg32---add-some-unit-test-for-reu-scrapping)
      - [HG31 - Add display report unit test cases](#hg31---add-display-report-unit-test-cases)
      - [HG38 - Add keywords option](#hg38---add-keywords-option)

## Group Basic Information

- GitHub repository: [Link](https://github.com/bdfinlayson/headline_grabber)
- Project Board: [Link](https://github.com/orgs/COSC540-HeadlineGrabber/projects/1/views/3)

 | Name               | GitHub Id   | Group Name       |
 | ------------------ | ----------- | ---------------- |
 | Ton That Tu Nguyen | tonthattuit | Headline Grabber |

## Individual Reflection

### 1. What you planned to do?

- Increase the unit test coverage
- Implement improvement for application

### 2. What you did not do?

- Initialize the desktop UI for this project.

### 3. What problems you encountered?

- Failed unit test cases because of new implementation.
- Failed unit test cases because of resolve conflicts mistake when merging code changes.
  
### 4. Issues completed

- [HG32 - Add some unit test for Reu scrapping](https://github.com/bdfinlayson/headline_grabber/pull/24)
- [HG31 - Add display report unit test cases](https://github.com/bdfinlayson/headline_grabber/pull/28)
- [HG38 - Add keywords option](https://github.com/bdfinlayson/headline_grabber/pull/33)

### 5. Files you worked on

- [HG32 - Add some unit test for Reu scrapping](https://github.com/bdfinlayson/headline_grabber/pull/24)
  - src/headline_grabber/pipeline_steps/scrape_text.py
  - tests/headline_grabber/pipeline_steps/scrape_text_test.py
  - tests/headline_grabber/pipeline_steps/test_data/reu.html
  - tests/headline_grabber/pipeline_steps/test_data/scrape_text_data.py

---

- [HG31 - Add display report unit test cases](https://github.com/bdfinlayson/headline_grabber/pull/28)
  - src/headline_grabber/pipeline_steps/display_report.py
  - tests/headline_grabber/pipeline_steps/display_report_test.py
  - tests/headline_grabber/pipeline_steps/scrape_text_test.py
  - tests/headline_grabber/pipeline_steps/test_data/display_report_data.py

---

- [HG38 - Add keywords option](https://github.com/bdfinlayson/headline_grabber/pull/33)
  - pyproject.toml
  - requirements.txt
  - src/headline_grabber/__main__.py
  - src/headline_grabber/models/user_preferences.py
  - src/headline_grabber/pipeline_steps/scrape_text.py
  - src/headline_grabber/validators/click/option_validator.py

### 6. What you accomplished?

#### HG32 - Add some unit test for Reu scrapping

- Get back the code for ScrapTextException for fixing the issue of resolve conflict.
- Add Reu test data
- Add Unit tests for Reu

#### HG31 - Add display report unit test cases

- Update display_report.py: using static method for some functions
- Add unit test for display_report.py
- Update some function name for scrap_text_test.

#### HG38 - Add keywords option

- Add new --keyworks or -k option
- Update dependency for the application.
