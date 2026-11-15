USE company;

-- Insert Employees
INSERT INTO EMPLOYEE (ssn, fname, lname, bdate, address, gender, salary, super_ssn, Dno) VALUES
(1, 'fname 1', 'lname 1', '1999-09-09', 'address 1, Alexandria', 'M', 5000.00, NULL, NULL),
(2, 'fname 2', 'lname 2', '1999-09-09', 'address 2, Alexandria', 'F', 6000.00, NULL, NULL),
(3, 'fname 3', 'lname 3', '1999-09-09', 'address 3, Cairo', 'M', 5500.00, 2, NULL),
(4, 'fname 4', 'lname 4', '1999-09-09', 'address 4, Alexandria', 'M', 4500.00, 1, NULL),
(5, 'fname 5', 'lname 5', '1999-09-09', 'address 5, Cairo', 'F', 3500.00, 1, NULL),
(6, 'fname 6', 'lname 6', '1999-09-09', 'address 6, Alexandria', 'M', 2500.00, 4, NULL);

-- Insert Departments
INSERT INTO DEPARTMENT (Dnumber, Dname, mgr_ssn, mgr_start_date) VALUES
(10, 'Dname 1', 1, '2020-01-01'),
(20, 'Dname 2', 2, '2020-01-01'),
(30, 'Dname 3', 3, '2020-01-01');

-- Assign Employees to Departments
UPDATE EMPLOYEE SET Dno = 10 WHERE ssn IN (1, 4, 5, 6);
UPDATE EMPLOYEE SET Dno = 20 WHERE ssn IN (2, 3);

-- Insert Projects
INSERT INTO PROJECT (Pnumber, Pname, Plocation, Dno) VALUES
(100, 'Pname 1', 'Plocation 1', 10),
(200, 'Pname 2', 'Plocation 2', 20),
(300, 'Pname 3', 'Plocation 3', 10),
(400, 'Pname 4', 'Plocation 4', 30);

-- Insert 8 WORKS_ON
INSERT INTO WORKS_ON (essn, Pno, hours) VALUES
(1, 100, 10.00),
(1, 200, 15.00),
(2, 200, 20.00),
(3, 200, 10.00),
(4, 100, 15.00),
(4, 300, 10.00),
(5, 100, 10.00),
(6, 300, 5.00);

-- Insert 3 DEPENDENT
INSERT INTO DEPENDENT (essn, dependent_name, gender, bdate, relationship) VALUES
(1, 'Dependent 1', 'M', '2020-01-01', 'Son'),
(1, 'Dependent 2', 'F', '2022-05-10', 'Daughter'),
(2, 'Dependent 3', 'F', '1998-03-15', 'Wife');