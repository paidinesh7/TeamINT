import sys
import os
import weasyprint

# =====================================================================
# RAINMATTER TEAM PDF COMPILER (WEASYPRINT)
# =====================================================================
# Usage:
#   python compile_to_pdf.py input_file.html [output_file.pdf]
# =====================================================================

def compile_html(input_html, output_pdf=None):
    if not os.path.exists(input_html):
        print(f"❌ Error: HTML file not found at: {input_html}")
        return False
        
    if not output_pdf:
        output_pdf = os.path.splitext(input_html)[0] + ".pdf"
        
    print(f"Compiling HTML to print-ready PDF using WeasyPrint...")
    print(f"  • Source: {input_html}")
    print(f"  • Target: {output_pdf}")
    
    try:
        os.makedirs(os.path.dirname(os.path.abspath(output_pdf)), exist_ok=True)
        weasyprint.HTML(filename=input_html).write_pdf(output_pdf)
        print(f"✅ Success! PDF successfully generated: {output_pdf}")
        return True
    except Exception as e:
        print(f"❌ PDF Compilation Failed: {e}")
        return False

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python compile_to_pdf.py <path_to_html_file> [optional_output_pdf_path]")
        sys.exit(1)
        
    src_html = sys.argv[1]
    dest_pdf = sys.argv[2] if len(sys.argv) > 2 else None
    compile_html(src_html, dest_pdf)
