INSERT INTO Patients VALUES (1, 'Akshaya', 21, 'Female');
INSERT INTO Patients VALUES (2, 'Rahul', 35, 'Male');

INSERT INTO Doctors VALUES (101, 'Dr. Sharma', 'Cardiology');
INSERT INTO Doctors VALUES (102, 'Dr. Reddy', 'Dermatology');

INSERT INTO Appointments VALUES (1, 1, 101, TO_DATE('26-03-2001', 'DD-MM-YYYY'));
INSERT INTO Appointments VALUES (2, 2, 101, TO_DATE('20-03-2001', 'DD-MM-YYYY'));
INSERT INTO Appointments VALUES (3, 1, 102, TO_DATE('22-03-2001', 'DD-MM-YYYY'));


INSERT INTO Treatments VALUES (1, 1, 'Heart Disease', 5000);
INSERT INTO Treatments VALUES (2, 2, 'Skin Allergy', 1500);
INSERT INTO Treatments VALUES (3, 1, 'Heart Disease', 7000);