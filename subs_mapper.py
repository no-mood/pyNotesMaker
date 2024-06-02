import webvtt
from datetime import datetime, timedelta
import re

def _vtt_to_subs(vtt_file):
    subs = []
    for caption in webvtt.read(vtt_file):
        start = datetime.strptime(caption.start, '%H:%M:%S.%f') - datetime(1900, 1, 1)
        end = datetime.strptime(caption.end, '%H:%M:%S.%f') - datetime(1900, 1, 1)
        subs.append({'start': start.total_seconds(), 'end': end.total_seconds(), 'text': caption.text})
    return subs



def _find_page_for_time(time, page_dict):
    # Find the page with the closest start or end time to the given time
    # FIXME: This is not the most efficient way to do this but it works for now.
    # See the previous implementation and try to understand why sometimes "None" is returned.
    closest_page = None
    closest_diff = float('inf')

    for page, frame_time in page_dict.items():
        start_diff = abs(frame_time.start.total_seconds() - time)
        end_diff = abs(frame_time.end.total_seconds() - time)

        if start_diff < closest_diff:
            closest_diff = start_diff
            closest_page = page
        if end_diff < closest_diff:
            closest_diff = end_diff
            closest_page = page

    return closest_page



def _match_sub_to_pages(sub, page_dict):
    start_time = sub['start']
    end_time = sub['end']

    start_page = _find_page_for_time(start_time, page_dict)
    end_page = _find_page_for_time(end_time, page_dict)

    return (start_page, end_page, sub['text'])

def sanitize_latex(text):
    replacements = {
        '#': r'\#',
        '$': r'\$',
        '%': r'\%',
        '&': r'\&',
        '_': r'\_',
        '{': r'\{',
        '}': r'\}',
        '~': r'\textasciitilde{}',
        '^': r'\^{}',
    }
    for char, replacement in replacements.items():
        text = text.replace(char, replacement)

    # Replace backslashes, but not if they're followed by a non-alphanumeric character
    text = re.sub(r'\\(?=\w)', r'\textbackslash{}', text)

    return text


def _write_page_subs_to_file(page_subs, save_target):
    grouped_text = {}
    for start_page, end_page, text in page_subs: # Group text by start and end page, but use end page as key
        if end_page not in grouped_text:
            grouped_text[end_page] = text
        else:
            grouped_text[end_page] += ' ' + text

    # Write grouped text to file
    with open(save_target, 'w') as file:
        for end_page, text in grouped_text.items(): 
            sanitized_text = sanitize_latex(text)
            file.write(f"\\begin{{slide}}{{{end_page}}}\n\t{sanitized_text}\n\\end{{slide}}\n\n")



def match_subs_to_pages(vtt_file, page_dict, save_target):
    subs = _vtt_to_subs(vtt_file)
    page_subs = [_match_sub_to_pages(sub, page_dict) for sub in subs]
    _write_page_subs_to_file(page_subs, save_target)
    return save_target