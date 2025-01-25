
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

### Running the Development Server

Start the Flask development server:
```bash
uvicorn app.main:app --reload
```

By default, the server will run on [http://127.0.0.1:8000](http://127.0.0.1:8000).

## API Endpoints

### `/api/default-trends` [GET]
- **Description**: Returns yearly trends of loan defaults.
- **Query Parameters**:
  - `start_year`: (optional) Filter results starting from this year.
  - `end_year`: (optional) Filter results ending at this year.
- **Response**: JSON object containing default trends by year.

### `/api/loan-distribution` [GET]
- **Description**: Returns the distribution of loan amounts.
- **Response**: JSON object containing loan amount ranges and counts.

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
