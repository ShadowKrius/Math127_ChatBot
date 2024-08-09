import fitz  # PyMuPDF
import csv
import io
from PIL import Image

# Open the PDF file
pdf_document = '/Users/aryanjoshi/Downloads/Question 4 of 10 - HW 1.1.pdf'  
# Replace with your actual PDF file path
document = fitz.open(pdf_document)

data = []

# Iterate through each page
for page_num in range(document.page_count):
    page = document.load_page(page_num)
    text = page.get_text("text").strip()
    
    # Extract images
    image_list = page.get_images(full=True)
    images = []
    for img_index, img in enumerate(image_list):
        xref = img[0]
        base_image = document.extract_image(xref)
        image_bytes = base_image["image"]
        image = Image.open(io.BytesIO(image_bytes))
        image_filename = f"page_{page_num + 1}_img_{img_index + 1}.png"
        image.save(image_filename)  # Save the image
        images.append(image_filename)
    
    # Assuming the text contains chapter and section info
    # Here we simply append the text and image filenames to the data list
    data.append([page_num + 1, text, ", ".join(images)])

# Save to CSV
with open('questions.csv', 'w', newline='') as file:
    writer = csv.writer(file)
    writer.writerow(["page_number", "question_text", "image_filenames"])
    writer.writerows(data)

print("Extraction complete. Data saved to questions.csv")

