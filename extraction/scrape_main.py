from scrape_ktu_announcements import scrape
import pandas as pd
from docx import Document

# Scrape the data and store it in the 'notification' variable
notification = scrape()
print(notification)

# Create a DataFrame from the scraped data
df = pd.DataFrame(notification)

# Create a new Word document
doc = Document()

# Write the DataFrame contents to the Word document
doc.add_paragraph(df.to_string())

# Save the Word document
doc.save('announcements.docx')
print("Data written to announcements.docx successfully.")
