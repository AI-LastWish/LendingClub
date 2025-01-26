
# LendingClub Backend

This is the backend service for the LendingClub data analysis and visualization project. It is built with Python, leveraging Flask for API endpoints and pandas for data analysis.

## Getting Started

### Prerequisites

To run this project locally, ensure you have the following installed:
- Python 3.8 or later
- pip (Python package manager)
- virtualenv (optional but recommended)

### Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/AI-LastWish/LendingClub.git
   cd LendingClub
   ```
2. Create and activate a virtual environment (optional but recommended):
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```
3. Install dependencies:
   ```bash
   pip install -r app/requirements.txt
   ```
4. Configure environment variables:
   Rename the .example-env to .env and add your key

### Running the Development Server

Start the Flask development server:
```bash
uvicorn app.main:app --reload
```

By default, the server will run on [http://127.0.0.1:8000](http://127.0.0.1:8000).

## API Endpoints

### `api/data_analysis/loan-distribution` [GET]
- **Description**: Fetches the distribution of loan amounts.
- **Response**: JSON object containing loan amount ranges and counts.
- **Error Response**: Returns a 500 status code if the loan distribution data is not available in the cache.

### `/api/data_analysis/grade-defaults` [GET]
- **Description**: Fetches the default rates by loan grade.
- **Response**: JSON object containing default rates by grade.
- **Error Response**: Returns a 500 status code if grade defaults data is not available in the cache.

### `/api/data_analysis/state-defaults` [GET]
- **Description**: Fetches the default rates by state.
- **Response**: JSON object containing default rates by state.
- **Error Response**: Returns a 500 status code if state defaults data is not available in the cache.

### `/api/data_analysis/risk-factors` [GET]
- **Description**: Fetches analysis of risk factors influencing loan defaults.
- **Response**: JSON object containing risk factors and their impact.
- **Error Response**: Returns a 500 status code if risk factors data is not available in the cache.

### `/api/data_analysis/temporal-trends` [GET]
- **Description**: Fetches temporal trends of loan defaults over time.
- **Response**: JSON object containing temporal trends data.
- **Error Response**: Returns a 500 status code if temporal trends data is not available in the cache.

### `/api/data_analysis/report` [GET]
- **Description**: Fetches the final analysis report.
- **Response**: JSON object containing the final report summary and details.
- **Error Response**: Returns a 500 status code if the final report is not available in the cache.

---

## Methodology

The backend processes LendingClub loan data to generate insights. Key steps include:

1. **Data Ingestion**:
   - Reads data from CSV files or a database.

2. **Analysis**:
   - Processes data using pandas to calculate trends and distributions.
   - Identifies correlations between borrower attributes and loan defaults.

3. **API Exposure**:
   - Exposes the results via RESTful API endpoints for frontend consumption.

---

## Results and Insights

### Key Findings
1. **Default Trends**:
   - Loan defaults peaked during economic downturns (e.g., 2008-2009).
   - Default rates have declined since 2015 due to stricter lending policies.

2. **Loan Distribution**:
   - Most loans are between $5,000 and $15,000, with an average of $11,035.

3. **Actionable Insights**:
   - Strengthen risk models during economic uncertainty.
   - Focus on borrower attributes (e.g., income and credit history) to predict defaults.

---

## Contribution Guidelines

We welcome contributions to improve this project! To contribute:
1. Fork the repository.
2. Create a feature branch:
   ```bash
   git checkout -b feature/your-feature-name
   ```
3. Make your changes and commit them:
   ```bash
   git commit -m "Description of your changes"
   ```
4. Push the branch and open a pull request.

---

## License

This project is licensed under the MIT License. See the LICENSE file for more details.
