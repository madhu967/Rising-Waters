import os
import glob
import markdown
from fpdf import FPDF

# Create a PDF class with basic styling
class PDF(FPDF):
    def header(self):
        self.set_font('helvetica', 'B', 12)
        self.cell(0, 10, 'Rising Waters - Project Documentation', border=False, ln=1, align='C')
        self.ln(10)

    def footer(self):
        self.set_y(-15)
        self.set_font('helvetica', 'I', 8)
        self.cell(0, 10, f'Page {self.page_no()}', border=False, align='C')

def generate_pdf_from_md(md_file_path, pdf_file_path):
    with open(md_file_path, 'r', encoding='utf-8') as f:
        md_text = f.read()

    # Convert Markdown to HTML
    html_text = markdown.markdown(md_text, extensions=['tables'])

    pdf = PDF()
    pdf.add_page()
    pdf.set_font("helvetica", size=12)
    # write_html parses basic HTML and translates it to FPDF elements
    pdf.write_html(html_text)
    pdf.output(pdf_file_path)

if __name__ == "__main__":
    base_dir = os.path.dirname(os.path.abspath(__file__))
    
    # Iterate over directories starting with a number
    for folder in os.listdir(base_dir):
        folder_path = os.path.join(base_dir, folder)
        if os.path.isdir(folder_path) and folder[0].isdigit():
            # Find the markdown file in the folder
            md_files = glob.glob(os.path.join(folder_path, "*.md"))
            for md_file in md_files:
                base_name = os.path.basename(md_file).replace('.md', '.pdf')
                pdf_path = os.path.join(folder_path, base_name)
                print(f"Generating PDF for {md_file} -> {pdf_path}")
                try:
                    generate_pdf_from_md(md_file, pdf_path)
                    print(f"Successfully generated {pdf_path}")
                except Exception as e:
                    print(f"Failed to generate {pdf_path}: {e}")
