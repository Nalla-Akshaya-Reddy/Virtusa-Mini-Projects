-- Most Consulted Doctors
SELECT d.name, COUNT(*) AS total_patients
FROM Doctors d
JOIN Appointments a ON d.doctor_id = a.doctor_id
GROUP BY d.name;

-- Total Revenue Per Month
SELECT EXTRACT(MONTH FROM a.dateofTreat) AS month_num, 
       SUM(t.cost) AS revenue
FROM Appointments a
JOIN Treatments t ON a.patient_id = t.patient_id
GROUP BY EXTRACT(MONTH FROM a.dateofTreat)
ORDER BY month_num;

-- Most Common Diseases
SELECT diagnosis, COUNT(*) AS count
FROM Treatments
GROUP BY diagnosis
ORDER BY count DESC;

-- Patient Visit Frequency
SELECT patient_id, COUNT(*) AS visits
FROM Appointments
GROUP BY patient_id;

-- Doctor Performance
SELECT d.name, COUNT(*) AS patients, SUM(t.cost) AS revenue
FROM Doctors d
JOIN Appointments a ON d.doctor_id = a.doctor_id
JOIN Treatments t ON a.patient_id = t.patient_id
GROUP BY d.name;
