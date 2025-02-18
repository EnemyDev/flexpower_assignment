# FlexPower assignment
This repository contains the "Initial Research and Proof of Concept" for the FlexPower assignment from the link [Assignment](https://github.com/FlexPwr/QuantChallenge)

## Overview
### Exlanation docs
- Please find my explanation for each tasts, along with some research results in ```docs``` folder
### Tech Stack and Library Choices

**Python3**: 
- Python is chosen for its simplicity, and extensive library ecosystem, making it ideal for data analysis, and scientific computing tasks. Its readability and efficiency in handling data structures are perfect for this assignment.

**CSV instead of Database**:
- No database (other than trades.sqlite provided in assignment) was employed for this project because it remains in an early research state, serving as a Proof of Concept (POC). This approach simplifies data import and doesn't require additional infrastructure, keeping the focus on data analysis.

**Pandas**:
- For data manipulation and analysis. Pandas provides powerful data structures for handling structured data, while cleaning, transforming, and analyzing time series data provided.

**aiohttp**:
- Asynchronous HTTP Client/Server

**Matplotlib**:
- Matplotlib is a comprehensive library for creating static, and interactive visualizations in Python, allowing presentation of tasks, strategy performance, etc.

**Scikit-learn**:
- Although this project focused on basic strategy evaluation, scikit-learn could be used for predictive models or for clustering to find patterns in price movements.

**Seaborn**:
- Built on top of Matplotlib, Seaborn offers a advanced/simplified interface for drawing additional charting requirements

This selection of libraries provides an basic environment for data processing, analysis, and visualization, tailored to the needs of assignment.

## Structure
Repository containes 3 main folders
  - **data** folder holds data provided in assignment in *raw* sublfolder, while *processed* subfolder holds data generated whem rummimg code.
  - **src** folder holds solution code, as python module.
  - **docs** folder holds MD files with my explanation, and "fabulations"

## Running solution
In order to run the solution please execute ```python -m src.main``` from virtual-environment after installing all required modules from requirements.txt (```pip install -r requirements.txt```)
- The sollution will fullfill tasks except the last one and task 1.3
- Executing will provide both, printed results in terminal as well as generated interactive charts an files(csv and png)
- In order to run webserver solving task 1.3, please execute ```python -m src.server.main```