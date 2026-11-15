USE library;

-- 4 Authors
INSERT INTO AUTHOR (name, country) VALUES
('AUTHOR 1', 'Egypt'),
('AUTHOR 2', 'Egypt'),
('AUTHOR 3', 'UK'),
('AUTHOR 4', 'USA');

-- 3 Publishers
INSERT INTO PUBLISHER (name, country) VALUES
('PUBLISHER 1', 'Egypt'),
('PUBLISHER 2', 'UK'),
('PUBLISHER 3', 'Germany');

-- 3 Categories
INSERT INTO CATEGORY (name) VALUES
('CATEGORY 1'),
('CATEGORY 2'),
('CATEGORY 3');

-- 10 Books
INSERT INTO BOOK (title, price, publish_year, author_id, publisher_id, category_id) VALUES
('BOOK 1', 15.00, 2020, 1, 1, 1),
('BOOK 2', 18.50, 2021, 1, 2, 1),
('BOOK 3', 25.00, 2022, 1, 1, 2),
('BOOK 4', 16.00, 2019, 2, 1, 2),
('BOOK 5', 30.00, 2020, 2, 3, 2),
('BOOK 6', 45.00, 2021, 2, 2, 3),
('BOOK 7', 20.00, 2023, 3, 2, 3),
('BOOK 8', 50.00, 2022, 3, 3, 1),
('BOOK 9', 12.00, 2018, 3, 1, 3),
('BOOK 10', 60.00, 2024, 3, 3, 1);

-- 5 Members
INSERT INTO MEMBER (name, email, join_date) VALUES
('MEMBER 1', 'member1@test.com', '2025-01-10'),
('MEMBER 2', 'member2@test.com', '2025-02-15'),
('MEMBER 3', 'member3@test.com', '2025-03-20'),
('MEMBER 4', 'member4@test.com', '2025-04-25'),
('MEMBER 5', 'member5@test.com', '2025-05-30');

-- 12 Loans 
INSERT INTO LOAN (book_id, member_id, loan_date, return_date) VALUES
(1, 1, '2026-01-05', '2026-01-15'),
(1, 2, '2026-01-20', '2026-01-30'),
(1, 3, '2026-02-01', '2026-02-10'),
(1, 4, '2026-02-15', NULL),
(2, 1, '2026-01-10', '2026-01-20'),
(2, 2, '2026-02-05', '2026-02-15'),
(2, 1, '2026-03-01', NULL),
(3, 1, '2026-01-12', '2026-01-22'),
(3, 3, '2026-02-12', '2026-02-22'),
(4, 1, '2026-02-18', '2026-02-28'),
(5, 2, '2026-03-05', '2026-03-15'),
(6, 4, '2026-03-10', NULL);