# Hink Pinks 

## Description 
Hink Pinks is a fun and engaging website that generates a type of riddle known as a Hink pink. A Hink pink is a riddle with two rules: the answer must include two words that rhyme perfectly, and neither of those two words are present in the riddle. For example: 

**Riddle:** A late festival -->
**Answer:** Tardy party 

Currently, the riddles are hard-coded, but future plans include implementing a database to store and manage an expanding collection of riddles. 

## Installation Instructions 

To set up and run the Hink Pinks website locally, follow these steps: 

1. **Clone the repository:**
    ```bash
    git clone https://github.com/Matiasjcd/hink_pinks.git
    cd Hink_Pinks
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
    
4. **Run the application:**
    ```bash
    flask run
    ```
    The application will be available at `http://127.0.0.1:5000`.

## Usage 

To use the Hink Pinks website: 

1. Start the Flask server by running the `flask run` command as described above.
2. Open your web browser and navigate to `http://127.0.0.1:5000`.
3. The website will display a daily Hink Pink riddle.
4. Enter your guess in the input fields provided. The website will indicate whether your guess is correct or not.
5. A new riddle will be available each day.

## Dependencies 

This project requires the following modules, as listed in `requirements.txt`: 
- Flask
- datetime (normally a built-in library for Python)

## Contact Information 

For any questions or feedback, please contact matiascaceresd@gmail.com.




















