# Acronymaker

## Description

Acronymaker is a sophisticated program designed to generate mnemonic acronyms based on user input. It performs millions of permutations at breakneck speeds using `itertools`, ensuring that the resulting mnemonic acronyms are valid words. The program offers several customizable options:

- **Order Preservation**: Users can choose whether to preserve the order of words in the acronym.
- **Language Selection**: Users can select the language in which the acronym should be generated.
- **Shuffling**: Users can shuffle the word order for different permutations while preserving the order.
- **Synonym Integration**: Users can input synonyms for their words, and Acronymaker will use these to create mnemonic acronyms.

The output is a list of valid mnemonic acronyms, along with details on any synonyms used in the generation process.

## Installation Instructions

To set up and run the Acronymaker program locally, follow these steps:

1. **Clone the repository:**
    ```bash
    git clone https://github.com/Matiasjcd/Acronymaker.git
    cd Acronymaker
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

4. **Set up the database (if any):**
    Ensure that any required database files are correctly set up and accessible.

5. **Run the application:**
    ```bash
    flask run
    ```
    The application will be available at `http://127.0.0.1:5000`.

## Usage

Using the Acronymaker website is straightforward:

1. **Language Selection:**
    - Choose the desired language from the dropdown menu.

2. **Input Words and Synonyms:**
    - Enter the words for which you want to generate acronyms.
    - Optionally, enter synonyms for these words.

3. **Order and Shuffling Options:**
    - Select whether to preserve the order of words in the acronym.
    - If preserving order, you can choose to shuffle the words for different permutations.

4. **Generate Acronyms:**
    - Click the "Generate" button.
    - The program will display the first 30 mnemonic acronyms along with information on any synonyms used.
    - If more acronyms are available, click "Load More" to display additional results.

## Dependencies

This project requires the following modules, as listed in `requirements.txt`:
- Flask
- Pyspellchecker
- Itertools
- Other dependencies as required

## Contact Information

For any questions or feedback, please contact matiascaceresd@gmail.com.
