# QuizBowl

## Description

QuizBowl is a project focused on analyzing a dataset of QuizBowl question categories. The primary output is a spreadsheet that contains detailed statistical information about these categories, derived from the QANTA 2021 training dataset.

### Spreadsheet Details

Each column in the spreadsheet provides specific insights about the question categories:

1. **Category Name**: The name of the question category.
2. **Number of Appearances**: The number of years the category has appeared in the dataset.
3. **First Appearance**: The first year the category appeared.
4. **Last Appearance**: The last year the category appeared (data ranges from 1997 to 2020).
5. **Relative Frequency Distribution**: Statistical information about how often the category appeared, e.g., a mean of 9.74% means the category represented 9.74% of questions on average during its active years.
6. **Model**: The name of the model that best fits the category's frequency distribution (e.g., Linear).
7. **Regression Equation**: The equation of the best-fit model.
8. **Correlation Coefficient**: The correlation coefficient of the model.
9. **Group**: The overall pattern of the category's frequency distribution (e.g., Constant, Periodic, Sudden onset/offset).
10. **Predicted Frequency (2021)**: The predicted frequency for 2021 using ARIMA.
11. **Data**: The frequency data for the category as a list of coordinate points (year, percentage).

## Installation Instructions

To set up and run the analysis tools for the QuizBowl project, follow these steps:

1. **Clone the repository:**
    ```bash
    git clone https://github.com/Matiasjcd/QuizBowl.git
    cd QuizBowl
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

4. **Prepare the dataset:**
    Ensure your dataset is properly formatted and accessible. The dataset should be similar in structure to the QANTA 2021 training dataset.

## Usage

To generate the QuizBowl question category analysis spreadsheet:

1. **Perform Statistical Analysis:**
    ```bash
    python statistical_analysis.py
    ```

2. **Find Frequency Data:**
    ```bash
    python frequency_finder.py
    ```

3. **Optimize R-squared Value:**
    ```bash
    python optimize_rsq.py
    ```

4. **Find ARIMA:**
    ```bash
    python find_ARIMA.py
    ```

This series of scripts will generate a comprehensive analysis of the question categories, similar to the provided example spreadsheet.

## Dependencies

This project requires the following modules, as listed in `requirements.txt`:
- statsmodels
- pandas
- numpy
- scipy

## Contact Information

For any questions or feedback, please contact matiascaceresd@gmail.com.
