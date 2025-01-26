
# LendingClub Frontend

This is a [Next.js](https://nextjs.org) project designed to visualize insights and trends from LendingClub loan data, with an emphasis on user-friendly, interactive, and insightful visualizations. The application supports interactive data exploration, enabling users to analyze loan characteristics and default trends effectively.

## Objective

This project aims to provide an interactive platform for exploring the LendingClub Loans dataset. The visualizations and insights generated help identify trends, such as loan distributions, default rates, and risk factors, while supporting decision-making for risk assessments and loan recommendations.

---

## Key Features

- **Dynamic Visualizations**:
  - Histograms for loan distributions.
  - Bar charts for categorical loan trends.
  - Line charts for temporal trends.
  - Heatmaps for correlation analysis.

- **Interactive Filtering**:
  - Users can filter results by timeframes, loan grades, and states.

- **Scalable Frontend Architecture**:
  - Built with Next.js 15 and React components for modularity.
  - Styled with Tailwind CSS for a modern, responsive UI.

- **API Integration**:
  - Connects with backend APIs to fetch precomputed data for loan distributions, default rates, risk factors, and more.

---

## Prerequisites

Ensure you have the following installed:
- Node.js (v16 or later)
- A package manager: npm, yarn, or pnpm

---

## Installation and Setup

1. **Clone the repository**:
   ```bash
   git clone https://github.com/AI-LastWish/LendingClub-frontend.git
   cd LendingClub-frontend
   ```

2. **Install dependencies**:
   ```bash
   npm install
   # or
   yarn install
   # or
   pnpm install
   ```

3. **Run the development server**:
   ```bash
   npm run dev
   ```
   Visit [http://localhost:3000](http://localhost:3000) in your browser.

4. **Build for production**:
   ```bash
   npm run build
   ```
   This generates an optimized production build in the `.next` directory.

---

## Methodology

The application visualizes insights from the LendingClub dataset using the following steps:

1. **Data Analysis**:
   - Analyze the distribution of loan amounts and default trends.
   - Highlight state-wise and grade-wise default rates.
   - Identify risk factors contributing to defaults.

2. **Visualization Design**:
   - Create intuitive visualizations (e.g., bar charts, histograms, and line plots).
   - Ensure accessibility with responsive layouts and tooltips for data points.

3. **API Integration**:
   - Fetch precomputed insights using dedicated endpoints like `/api/data_analysis/loan-distribution`, `/api/data_analysis/grade-defaults`, and others.

4. **Interactivity**:
   - Implement dynamic filters for exploring trends across years, grades, and states.

---

## Key Insights

### 1. Default Trends
- Significant spikes in defaults were observed during economic recessions, e.g., 2008.
- Improved lending practices reduced defaults after 2015.

### 2. Loan Distribution
- Loan amounts range between $500 and $35,000.
- 50% of loans are below $9,600.

### 3. Risk Identification
- High default rates are correlated with specific grades and states.
- Tailored lending policies can mitigate risks.

---

## API Endpoints

### `/api/data_analysis/loan-distribution` [GET]
- **Description**: Fetches loan amount distribution.
- **Response**: JSON object with loan ranges and counts.

### `/api/data_analysis/grade-defaults` [GET]
- **Description**: Fetches grade-wise default analysis.
- **Response**: JSON object with default rates by grade.

### `/api/data_analysis/state-defaults` [GET]
- **Description**: Fetches state-wise default analysis.
- **Response**: JSON object with default rates by state.

### `/api/data_analysis/risk-factors` [GET]
- **Description**: Fetches analysis of risk factors.
- **Response**: JSON object with risk factor impacts.

### `/api/data_analysis/temporal-trends` [GET]
- **Description**: Fetches temporal trends of defaults.
- **Response**: JSON object with year-by-year trends.

### `/api/data_analysis/report` [GET]
- **Description**: Fetches the final analysis report.
- **Response**: JSON object summarizing findings.

---

## Deployment

The application is deployed via [Vercel](https://vercel.com). For deployment:
1. Link the repository to a Vercel project.
2. Follow [Next.js deployment documentation](https://nextjs.org/docs/app/building-your-application/deploying).

---

## Contribution

We welcome contributions to enhance this project! To contribute:
1. Fork the repository.
2. Create a feature branch:
   ```bash
   git checkout -b feature/your-feature-name
   ```
3. Commit and push your changes.
4. Open a pull request for review.

---

## License

This project is licensed under the MIT License. See the LICENSE file for details.
