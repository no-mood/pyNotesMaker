import webvtt
from datetime import datetime, timedelta

def _vtt_to_subs(vtt_file):
    subs = []
    for caption in webvtt.read(vtt_file):
        start = datetime.strptime(caption.start, '%H:%M:%S.%f') - datetime(1900, 1, 1)
        end = datetime.strptime(caption.end, '%H:%M:%S.%f') - datetime(1900, 1, 1)
        subs.append({'start': start.total_seconds(), 'end': end.total_seconds(), 'text': caption.text})
    return subs



def _find_page_for_time(time, page_dict):
    return next((page for page, frame_time in page_dict.items() if frame_time.start.total_seconds() <= time < frame_time.end.total_seconds()), None)



def _match_sub_to_pages(sub, page_dict):
    start_time = sub['start']
    end_time = sub['end']

    start_page = _find_page_for_time(start_time, page_dict)
    end_page = _find_page_for_time(end_time, page_dict)

    return (start_page, end_page, sub['text'])



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
            # file.write(f"Page: {end_page}, Text: \n{text}\n\n")
            file.write(f"\\begin{{slide}}{{{end_page}}}\n{text}\n\\end{{slide}}\n\n")



def match_subs_to_pages(vtt_file, page_dict, save_target):
    subs = _vtt_to_subs(vtt_file)
    page_subs = [_match_sub_to_pages(sub, page_dict) for sub in subs]
    _write_page_subs_to_file(page_subs, save_target)
    return save_target