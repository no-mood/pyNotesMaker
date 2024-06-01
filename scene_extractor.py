import subprocess
import re
from datetime import datetime, timedelta
from collections import namedtuple

FrameTime = namedtuple('FrameTime', ['start', 'end'])

def _get_video_duration(filename):
    result = subprocess.run(["ffmpeg", "-i", filename], stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
    match = re.search(r"Duration: (\d+:\d+:\d+\.\d+)", result.stderr)
    if match:
        return match.group(1)
    else:
        return None

def _extract_scenes(filename, threshold, time_file = "tmp/time.txt"):
    # ffmpeg -i inputvideo.mp4 -filter_complex "[0:v]select='eq(n,0)+gt(scene,0.1)',metadata=print:file=time.txt" -vsync vfr img%03d.png
    
    frame_name = "tmp/frames/%05d.jpg"
    command = [
        "ffmpeg", "-i", filename,
        "-filter:v", f"select='gt(scene,{threshold})',showinfo",
        "-vsync", "0", frame_name,
        "-f", "null", 
        "-",
    ]
    command = [
        "ffmpeg", "-i", filename,
        "-filter_complex", f"[0:v]select='eq(n\,0)+gt(scene,{threshold})',metadata=print:file={time_file}",
        "-vsync", "vfr", 
        frame_name,
    ]
    subprocess.run(command)
    return time_file


def _get_frames(time_file):
    frame_dict = {}

    prev_frame, prev_time = None, None

    with open(time_file, 'r') as file:
        for line in file:
            match = re.search(r'frame:(\d+).*pts_time:(\d+\.?\d*)', line)
            if match:
                frame, pts_time = match.groups()
                frame_key = "%05d.jpg" % (int(frame) + 1)  # Add 1 to the frame number because jpgs start from 1
                if prev_frame is not None and prev_time is not None:
                    frame_dict[prev_frame] = FrameTime(float(prev_time), float(pts_time))
                prev_frame, prev_time = frame_key, pts_time

        # Handle the last frame
        if prev_frame is not None and prev_time is not None:
            frame_dict[prev_frame] = FrameTime(float(prev_time), "end")

    return frame_dict


def convert_to_datetime(frame_dict, duration):
    datetime_dict = {}

    # Convert duration string to timedelta
    duration = datetime.strptime(duration, "%H:%M:%S.%f").time()
    duration = timedelta(hours=duration.hour, minutes=duration.minute, seconds=duration.second, microseconds=duration.microsecond)

    for frame, frame_time in frame_dict.items():
        start_time = timedelta(seconds=frame_time.start)
        if frame_time.end == "end":
            end_time = duration
        else:
            end_time = timedelta(seconds=frame_time.end)
        datetime_dict[frame] = FrameTime(start_time, end_time)

    return datetime_dict



def extract_frames(filename, threshold, time_file = "tmp/time.txt"):
    print("Extracting scene...")
    
    duration = _get_video_duration(filename)
    time_file = _extract_scenes(filename, threshold, time_file = time_file)
    frame_dict = _get_frames(time_file)
    frame_dict = convert_to_datetime(frame_dict, duration)
    
    # print("Frame dict: ", frame_dict)
    return frame_dict
