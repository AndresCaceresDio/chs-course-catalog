# Taskly

## Description

Taskly is a comprehensive task management website designed to go beyond the functionality of traditional to-do lists. It allows users to register an account, log in, and securely manage their tasks with various features. Users can:

- Add tasks with details such as title, description, due date and time, category, and priority.
- View tasks in a table format upon logging in.
- Create and manage task categories.
- Assign tasks to categories or change their categories.
- Mark tasks as complete and view the history of completed tasks.
- Change their password and log out.

## Installation Instructions

To set up and run the Taskly website locally, follow these steps:

1. **Clone the repository:**
    ```bash
    git clone https://github.com/Matiasjcd/taskly.git
    cd Taskly
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
    Ensure `taskLy.db` is in the project directory. This database contains user tasks and information.

5. **Run the application:**
    ```bash
    flask run
    ```
    The application will be available at `http://127.0.0.1:5000`.

## Usage

Taskly provides a robust task management system with various features. Here’s how to use it:

1. **Register an Account:**
    - Navigate to the register page (`/register`).
    - Enter a valid username and password to create an account.

2. **Log In:**
    - Navigate to the login page (`/login`).
    - Enter your credentials to access your account.

3. **Manage Tasks:**
    - **Add Tasks:** Go to the add tasks page (`/add-tasks`) to create new tasks with relevant details.
    - **View Tasks:** Your tasks are displayed on the default homepage upon logging in.
    - **Manage Tasks:** Navigate to the manage tasks page (`/manage-tasks`) to remove tasks, change their category, or mark them as complete.

4. **Manage Categories:**
    - **Add/Remove Categories:** Use the manage categories page (`/manage-categories`) to create new categories or delete existing ones.
    - **Change Task Category:** Assign tasks to different categories using the change category page (`/change-category`).

5. **View History:**
    - See your history of completed tasks on the history page (`/history`).

6. **Account Management:**
    - **Change Password:** Use the change password page (`/change-password`) to update your password.
    - **Log Out:** Log out of your account at any time.

## Dependencies

This project requires the following modules, as listed in `requirements.txt`:
- Flask
- SQLite (normally a built-in library for Python)
- Other dependencies as required

## Contact Information

For any questions or feedback, please contact matiascaceresd@gmail.com.
