from datetime import datetime, timedelta
import whisper
import sys


def _format_delta_time(seconds):
    delta = timedelta(seconds=seconds)
    # Format in "0:00:00.xxx"
    formatted_time = "{:0>2}:{:0>2}:{:06.3f}".format(
        delta.seconds // 3600, (delta.seconds % 3600) // 60, delta.total_seconds() % 60
    )
    return formatted_time

def make_subs(filename):
    print("Generating subtitles...")
    
    model = whisper.load_model("base")
    result = model.transcribe(filename, language="en", fp16=False, verbose=True)

    # Generate the .vtt file
    vtt_file = filename + '.vtt'
    with open(vtt_file, "w") as file:
        file.write('WEBVTT' + '\n' + '\n')
        for index, segment in enumerate(result['segments']):
            file.write(str(index + 1) + '\n')

            start = _format_delta_time(segment['start'])
            end = _format_delta_time(segment['end'])

            file.write(str(start) + ' -->  ' + str(end) + '\n')
            file.write(segment['text'].strip() + '\n')
            file.write('\n')
    
    return vtt_file
