import os
from fpdf import FPDF

DATA_DIR = os.path.join(os.path.dirname(__file__), "data")
os.makedirs(DATA_DIR, exist_ok=True)

policies = {
    "it_security_policy.pdf": [
        "IT Security and Acceptable Use Policy",
        "1. Device Usage: Employees must only use company-issued devices for work. Personal devices must be enrolled in the MDM program before accessing corporate networks.",
        "2. Password Policy: Passwords must be at least 14 characters long, contain a mix of uppercase, lowercase, numbers, and symbols, and be rotated every 90 days. Sharing passwords is strictly prohibited and grounds for immediate termination.",
        "3. Software Installation: Employees are not permitted to install unapproved third-party software on company laptops. All software requests must go through the IT service desk.",
        "4. Data Protection: Confidential client data must never be stored on local hard drives. All sensitive data must be stored in the approved cloud storage provider (Google Workspace or AWS).",
        "5. Phishing & Training: All employees must complete the quarterly security awareness training. Failing to complete the training within the 30-day window will result in temporary suspension of network access."
    ],
    "employee_benefits_policy.pdf": [
        "Employee Benefits and Perks Policy",
        "1. Health Insurance: The company covers 100% of health, dental, and vision insurance premiums for employees, and 80% for dependents. Coverage starts on the first day of employment.",
        "2. Educational Stipend: Employees are eligible for a $2,000 annual stipend for continuous education, including courses, certifications, and conferences. Approval from a direct manager is required before purchasing.",
        "3. Wellness Budget: A monthly wellness stipend of $100 is provided. This can be used for gym memberships, mental health apps, or fitness equipment. It does not roll over to the next month.",
        "4. 401(k) Matching: The company provides a 100% match on the first 4% of employee contributions, and a 50% match on the next 2%. Vesting is immediate.",
        "5. Parental Leave: Primary caregivers receive 16 weeks of fully paid parental leave, and secondary caregivers receive 8 weeks. This applies to birth, adoption, and foster placements."
    ],
    "anti_harassment_policy.pdf": [
        "Anti-Harassment and Non-Discrimination Policy",
        "1. Zero Tolerance: The company has a zero-tolerance policy for any form of harassment, discrimination, or bullying based on race, gender, sexual orientation, religion, age, disability, or any other protected class.",
        "2. Reporting Procedure: Any employee who witnesses or experiences harassment should immediately report it to their manager, Human Resources, or the anonymous whistleblowing hotline at 1-800-555-0199.",
        "3. Investigation Process: All reports will be investigated promptly and confidentially. The company will take appropriate disciplinary action, up to and including termination, for any employee found to have violated this policy.",
        "4. Retaliation: Retaliation against any employee who makes a good-faith report of harassment is strictly prohibited and is itself a terminable offense.",
        "5. Mandatory Training: All employees must attend an annual anti-harassment training workshop. Managers must attend an additional leadership training session focusing on conflict resolution and bias mitigation."
    ]
}

class PDF(FPDF):
    def header(self):
        self.set_font('Arial', 'B', 15)
        self.cell(0, 10, 'Corporate HR Policy Document', 0, 1, 'C')
        self.ln(10)
        
    def footer(self):
        self.set_y(-15)
        self.set_font('Arial', 'I', 8)
        self.cell(0, 10, f'Page {self.page_no()}', 0, 0, 'C')

for filename, lines in policies.items():
    pdf = PDF()
    pdf.add_page()
    pdf.set_font("Arial", size=12)
    
    # Title
    pdf.set_font("Arial", 'B', 16)
    pdf.cell(0, 10, lines[0], 0, 1, 'L')
    pdf.ln(5)
    
    # Body
    pdf.set_font("Arial", size=12)
    for line in lines[1:]:
        pdf.multi_cell(0, 8, line)
        pdf.ln(3)
        
    filepath = os.path.join(DATA_DIR, filename)
    pdf.output(filepath)
    print(f"Generated {filepath}")
