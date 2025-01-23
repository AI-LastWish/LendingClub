-- Create a table for Lending Club Loans data
CREATE TABLE lending_club_loans (
    loan_amnt DECIMAL(10, 2),
    funded_amnt DECIMAL(10, 2),
    term VARCHAR(50),
    int_rate DECIMAL(10, 4),  -- To account for more precise interest rates
    installment DECIMAL(10, 2),
    grade VARCHAR(5),
    sub_grade VARCHAR(5),
    emp_title TEXT,
    emp_length VARCHAR(50),
    home_ownership VARCHAR(50),
    annual_inc DECIMAL(15, 2),
    verification_status VARCHAR(50),
    pymnt_plan CHAR(1),
    url TEXT,
    "desc" TEXT,  -- Escaping the reserved keyword
    purpose VARCHAR(50),
    title TEXT,
    zip_code VARCHAR(10),
    addr_state VARCHAR(10),
    dti DECIMAL(10, 2),
    delinq_2yrs INT,
    earliest_cr_line VARCHAR(50),
    inq_last_6mths INT,
    mths_since_last_delinq INT,
    mths_since_last_record INT,
    open_acc INT,
    pub_rec INT,
    revol_bal DECIMAL(15, 2),
    revol_util DECIMAL(10, 4),  -- More precise utilization
    total_acc INT,
    initial_list_status CHAR(1),
    mths_since_last_major_derog INT,
    policy_code INT,
    is_bad BOOLEAN
);

SELECT table_name
FROM information_schema.tables
WHERE table_name = 'lending_club_loans';