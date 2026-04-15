# Hospital Management and Patient Analytics System

## Project Description
This project is a simple database system built using SQL to manage hospital data. It stores information about patients, doctors, appointments, and treatments.

Along with storing data, it also performs analysis to understand hospital operations such as doctor performance, patient visits, and revenue.



## What the Project Does

- Stores patient details like name, age, and gender  
- Maintains doctor information and specialization  
- Tracks appointments between patients and doctors  
- Records treatments and their costs  
- Performs analysis using SQL queries  



## Database Tables

Patients  
- patient_id  
- name  
- age  
- gender  

Doctors  
- doctor_id  
- name  
- specialization  

Appointments  
- appointment_id  
- patient_id  
- doctor_id  
- dateofTreat  

Treatments  
- treatment_id  
- patient_id  
- diagnosis  
- cost  


## Technologies Used

- SQL  
- Relational Database Concepts  


## How It Works

First, tables are created to store patients, doctors, appointments, and treatments.

Then, sample data is inserted into these tables.

After that, different SQL queries are used to analyze the data and get useful insights.



## Queries Performed

- Most Consulted Doctors  
  Finds which doctors handled the highest number of patients  

- Total Revenue Per Month  
  Calculates how much revenue was generated each month  

- Most Common Diseases  
  Identifies frequently occurring diseases  

- Patient Visit Frequency  
  Counts how many times each patient visited  

- Doctor Performance  
  Shows doctor performance based on number of patients and revenue  


## How to Run the Project

1. Open a SQL environment such as MySQL or Oracle  
2. Run the structure file to create tables  
3. Run the insert file to add data  
4. Run the queries file to see results  



## Output

The output will show:
- Doctor statistics  
- Monthly revenue  
- Disease frequency  
- Patient visit counts  
- Doctor performance  



## Conclusion

This project shows how SQL can be used not only to store data but also to analyze it. It helps in understanding hospital operations and making better decisions based on data.
