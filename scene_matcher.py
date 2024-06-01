import os
import pytesseract
from PIL import Image
from difflib import SequenceMatcher
from PyPDF2 import PdfReader
from thefuzz import fuzz

def _ocr_frame(frame_path):
    # Use OCR to get the text of the frame
    frame_text = pytesseract.image_to_string(Image.open(frame_path), config='--psm 6', lang='eng')
    return frame_text


def _get_pdf_pages_text(pdf_file):
    # Open the PDF file
    pdf_reader = PdfReader(pdf_file)

    # Get the text of each page
    pages_text = [page.extract_text() for page in pdf_reader.pages]
    return pages_text


def _match_frame_to_page(frame_text, pages_text, threshold=50):
    best_match = 0 + threshold # Start with a threshold to avoid false positives
    best_match_page = None

    for i, page_text in enumerate(pages_text):
        match = fuzz.ratio(frame_text, page_text) # Fuzzy search, better than plain SequenceMatcher
        #print(f"\tMatch coefficient with page {i+1}: {match}")  # Print match coefficient for debugging
        if match > best_match:
            best_match = match
            best_match_page = i + 1 # Add 1 because slides start from 1

    return best_match_page


def match_scenes(frame_dict, pdf_file):
    frame_to_page_map = {}
    pages_text = _get_pdf_pages_text(pdf_file)

    # OCR all frame_text at the beginning for efficiency
    frame_texts = {frame_filename: _ocr_frame("tmp/frames/" + frame_filename) for frame_filename in frame_dict.keys()}
    
    for frame_filename, frame_time in frame_dict.items():
        #print(f"Matching frame {frame_filename} to page...")
        frame_to_page_map[frame_filename] = _match_frame_to_page(frame_texts[frame_filename], pages_text) # O(n^2) complexity    
    
    # Replace keys in frame_dict with mapping from frame_to_page_map
    page_to_time_map = {frame_to_page_map[frame_filename]: frame_time for frame_filename, frame_time in frame_dict.items()}
    
    # Cleans the /tmp/frames directory
    for frame_filename in frame_dict.keys():
        os.remove("tmp/frames/" + frame_filename)

    return page_to_time_map