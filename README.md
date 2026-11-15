# Database Lab 4

## Team Members
* Takla Hany Shaker Said - ID: 2304033

## Technology Stack
* **Back End:** Python (Flask)
* **Front End:** HTML, CSS, JavaScript
* **Database:** MySQL (PyMySQL)

## Deliverables Structure
* `problem1_DDL.sql` & `problem1_DML.sql`: Extended COMPANY database schema (5 tables) and seed data.
* `problem2_DDL.sql` & `problem2_DML.sql`: Extended Library database schema (6 tables with `ON DELETE CASCADE`) and seed data.
* `problem2_Queries.sql`: Standalone SQL queries for website pages F2.1 - F2.6.
* `website/`: Flask application containing Lab 2 (To-Do), Lab 3 (Library CRUD), and Lab 4 (Library Search & Reports F2.1 - F2.6).

## How to Run the Website
1. Navigate to the project root folder.
2. Create and activate the Conda environment: `conda create -n lab4-flask python=3.11 -y` and `conda activate lab4-flask`.
3. Install dependencies: `pip install -r requirements.txt`.
4. Build and seed the Problem 1 database:
   * `mysql -u root -p < problem1_DDL.sql`
   * `mysql -u root -p < problem1_DML.sql`
5. Build and seed the Problem 2 (`library`) database:
   * `mysql -u root -p < problem2_DDL.sql`
   * `mysql -u root -p < problem2_DML.sql`
6. Navigate into the `website/` folder.
7. Ensure `.env` is configured with your MySQL credentials.
8. Start the server: `flask run`.
9. Open `http://127.0.0.1:5000/search` in your web browser and use the footer links to navigate between F2.1 - F2.6.

## Features Built
* **Problem 2 (F2.1 - F2.6):** Implemented the 6-table Library schema, seed data, and web pages for book search, full catalogue, category/author/price reports, loan status tracking, most-borrowed rankings, and author-publisher country matching.
* **Problem 2 (Bonus):** Used prepared statements (`%s` placeholders) in the F2.1 search query.