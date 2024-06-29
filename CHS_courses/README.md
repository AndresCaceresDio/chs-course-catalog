# CHS Courses

## Description
CHS Courses is a website that provides a searchable database of a certain high school's course catalog. The catalog is displayed in a table and can be searched based on the following criteria:
- Title of the course
- Level of the course (AP, G/T, Honors, Regular)
- Subject (Math, English, CTE, etc.)
- Grade levels eligible to take the course
- Unique code of the course

All of this information is displayed in the table, making it easy to find and explore courses.

## Installation Instructions

To set up and run the CHS Courses website locally, follow these steps:

1. **Clone the repository:**
    ```bash
    git clone https://github.com/yourusername/CHS_courses.git
    cd CHS_courses
    ```

2. **Set up a virtual environment (optional but recommended):**
    ```bash
    python -m venv venv
    source venv/bin/activate  # On Windows, use `venv\Scripts\activate`
    ```

3. **Install the required modules:**
    ```bash
    pip install -r requirements.txt
    ```

4. **Set up the database:**
    Ensure that `courses.db` is in the project directory. This file contains the high school's course catalog.

5. **Run the application:**
    ```bash
    flask run
    ```
    The application will be available at `http://127.0.0.1:5000`.

## Usage

To use the CHS Courses website:

1. Start the Flask server by running the `flask run` command as described above.
2. Open your web browser and navigate to `http://127.0.0.1:5000`.
3. You will see a table displaying the course catalog.
4. Use the search functionality to filter courses based on title, level, subject, grade levels, or course code.

## Dependencies

This project requires the following modules, as listed in `requirements.txt`:
- Flask
- SQLite (normally a built-in library for Python)

## Contact Information

For any questions or feedback, please contact matiascaceresd@gmail.com.
