# Development Log - TimeKeeper, the Python app usage monitor

## 2025-09-5 - *Project Setup*
- [x] Done
    - [x] Created Github repository
    - [x] Set up some basic project structure
    - [x] Installed psutil
    - [x] Basic process detection working
- [ ] To_do
    - [ ] Set up SqLite database
    - [ ] Filter the actual apps
    - [ ] Sniff some other Github repos for folder strutucre

### to Study
- Markdown Basic Sintax - [https://www.markdownguide.org/basic-syntax/]
- Github folder strutcure - [https://github.com/streamlit/streamlit] / [https://github.com/psf/requests]

## 2025-09-06 - *Filter*
- [x] Done
    - [x] Filter out some of the system processses
    - [x] Refine Filter

- [ ] To_do
    - [ ] Differentiate between background and active processes
    - [ ] Set up SqLite db

## 2025-09-08 - *Architecture Refactoring*
- [x] Done
    - [x] Switch the functions to their own class
    - [x] Differentiate between background and active processes

- [ ] To_do
    - [ ] Complete the Facate pattern
    - [ ] Set up SqLite db
    - [ ] Refine Filter

- ### Lerning Goals
    - To Read 
        - Design Patterns: elements of reusable object-oriented software
        - Clean Code: A Handbook of Agile Software Craftsmanship
        - Clean Architecture: A Craftsman's Guide to Software Structure and Design: A Craftsman's Guide to Software Structure and Design
    - To Research
        - SOLID
        - Python Design Patterns

## 2025-09-10 - *Architecture Refactoring*
- [x] Done
    - [x] Complete the Architecture Refactoring
    - [x] Refine Filter
- [ ] To_do
    - [ ] Set up SqLite db
    
- ### Lerning Goals
    - To Read 
        - The Pragmatic Programmer
    - To Research
        - SQlite
        - Window Enumeration on Linux / MacOS

## 2025-09-11 - *Setup Database*
- [x] Done
    - [x] Plan New APP flow
    - [x] Set up Sqlite db
- [ ] To_do
    - [ ] Integrate Database with the app main cycle
    - [ ] Make app more user-interactive

---
## Break for exam
---

## 2025-09-23 - *Integrate Database*
- [x] Done
    - [x] Integrate Database with the app main life cycle
    - [x] Refactorated filter logic
- [ ] To_do
    - [ ] Integrate the database with the filter
    - [ ] Refactor filter logic - add more filters
- [ ] Descarted (for now)
    - [x] Make app more user-interactive

## 2025-09-23 - *Upgrade Database*
- [x] Done
    - [x] Add a get_running_time by month method
    - [x] Add a get_running_time by week method
- [ ] To_do
    - [ ] Integrate the database with the filter
    - [ ] Refactor filter logic - add more filters or change it to categorizer instead

## 2025-09-24 - *Categorizer*
- [x] Done
    - [x] Add a ProcesssCategorizer class
    - [x] Refactor ProcessFilter class
    - [x] Refactor Database class 
- [ ] To_do
    - [ ] Add a ProcessEnricher class
        > It will work as a way to start using persistent running time data from the databse instead of now / create_time
    - [ ] Plan about UX (CLI - for now)

## 2025-09-30 - *Enricher*
- [x] Done
    -[x] Add a ProccessEnricher
    -[x] Modify ProcessSorter and ProcessRenderer classes to work along with the enriched_processes
- [ ] To_do
    - [ ] Add more time related consistent data related to running_time

## 2025-10-07 - *Week And Month Running Time*
- [x] Done
    -[x] Add week and month running time to the ProcessEnricher
    -[x] Modify ProcessRenderer to render the week and month running time
- [ ] To_do
    - [ ] Threading
    - [ ] Add more time related consistent data related to running_time
    - [ ] Refactor Monitor and ProcessRenderer
    - [ ] Refactor the life cycle of the application
        > Add More interative options like, See Running Processes, See Background Processes, See Apps, Sort Apss by - TodayRT, WeekRT, name, user, i.e

## 2025-10-22 - *Major Categorizer Update*
- [x] Done
    -[x] Updated process_categorizer
    -[x] Created a process_window_checker for better responsability distribuiton
- [ ] To_do (*Everything from last time*)
    - [ ] Threading
    - [ ] Add more time related consistent data related to running_time
    - [ ] Refactor Monitor and ProcessRenderer
    - [ ] Refactor the life cycle of the application
