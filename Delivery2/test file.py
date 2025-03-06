import pandas as pd
import matplotlib.pyplot as plt

# Define sample data following the template
data = {
    "user_prompt": [
        "I have just been on an international flight",
        "Is it safe to travel with a newborn?",
        "What are the risks of air travel for infants?",
        "Can I bring baby formula on a flight?",
        "How soon can a baby fly after birth?",
        "Are there any vaccines needed for infants before flying?",
        "What precautions should I take when flying with a newborn?",
        "Can cabin pressure affect a baby’s ears?",
        "Is a passport required for an infant on an international flight?",
        "What should I pack when flying with an infant?",
        "How can I keep my baby calm during a flight?"
    ],
    "url_to_check": [
        "https://www.mayoclinic.org/healthy-lifestyle/infant-and-toddler-health/expert-answers/air-travel-with-infant/faq-20058539",
        "https://www.cdc.gov/travel/page/infants",
        "https://www.aap.org/en-us/advocacy-and-policy/aap-health-initiatives/healthy-children/Pages/Air-Travel-Safety-for-Infants.aspx",
        "https://www.tsa.gov/travel/security-screening/whatcanibring/items/baby-formula",
        "https://www.faa.gov/travelers/fly-children",
        "https://www.who.int/travel-advice/vaccination-for-infants",
        "https://www.healthychildren.org/English/safety-prevention/on-the-go/Pages/Flying-with-Babies-and-Toddlers.aspx",
        "https://www.enthealth.org/be_ent_smart/air-travel-and-your-ears/",
        "https://travel.state.gov/content/travel/en/passports/requirements/minor.html",
        "https://www.parents.com/baby/travel/baby-travel-checklist/",
        "https://www.verywellfamily.com/how-to-keep-baby-calm-during-flight-5202824"
    ],
    "func_rating": [3, 4, 3, 5, 4, 4, 3, 4, 5, 4, 3],
    "custom_rating": [4, 5, 3, 5, 4, 5, 4, 4, 5, 5, 4]
}

# Create a DataFrame
df = pd.DataFrame(data)

# Save as CSV file
csv_file_path = "url_validation_data.csv"
df.to_csv(csv_file_path, index=False)

# Create an image of the DataFrame
fig, ax = plt.subplots(figsize=(12, 4))
ax.axis('tight')
ax.axis('off')
table = ax.table(cellText=df.values, colLabels=df.columns, cellLoc='center', loc='center')

# Save the table as an image
image_path = "url_validation_table.png"
plt.savefig(image_path, dpi=300, bbox_inches='tight')

# Generate a test script
test_script_content = """
from deliverable2 import *

# Instantiate the URLValidator class
validator = URLValidator()

# Define test cases
test_cases = [
    ("I have just been on an international flight", "https://www.mayoclinic.org/healthy-lifestyle/infant-and-toddler-health/expert-answers/air-travel-with-infant/faq-20058539"),
    ("Is it safe to travel with a newborn?", "https://www.cdc.gov/travel/page/infants"),
    ("What are the risks of air travel for infants?", "https://www.aap.org/en-us/advocacy-and-policy/aap-health-initiatives/healthy-children/Pages/Air-Travel-Safety-for-Infants.aspx"),
]

# Run the validation
for prompt, url in test_cases:
    result = validator.rate_url_validity(prompt, url)
    print(f"User Prompt: {prompt}\nURL: {url}\nResult: {result}\n{'-'*50}")
"""

# Save the test script file
test_file_path = "test_url_validation.py"
with open(test_file_path, "w") as file:
    file.write(test_script_content)
