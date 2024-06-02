import argparse
import os
from scene_extractor import extract_frames
from scene_matcher import match_scenes
from subs_maker import make_subs
from subs_mapper import match_subs_to_pages
import shutil

def main():
    parser = argparse.ArgumentParser(description='Process some files.')
    parser.add_argument('-v', '--video', help='Video file', required=True)
    parser.add_argument('-p', '--pdf', help='PDF file', required=True)
    parser.add_argument('-s', '--subs', help='Subs file')
    parser.add_argument('-t', '--threshold', type=float, default=0.05, help='Threshold for scene detection')
    parser.add_argument('-o', '--output', help='Output file saved in "output/". Default is "output.tex".')
    args = parser.parse_args()

    working_dir = "tmp/"
    output_dir = "output/"
    os.makedirs(working_dir, exist_ok=True)
    os.makedirs(output_dir, exist_ok=True)
    

    video_file = args.video
    pdf_file = args.pdf
    subs_file = args.subs if args.subs else make_subs(filename = video_file) # If subs file is not provided, generate it
    threshold = args.threshold
    out_file = output_dir + (args.output if args.output else "output.tex") # If output file is not provided, save it as "output.tex"

    frame_dict = extract_frames(filename = video_file, threshold = threshold)
    page_dict = match_scenes(frame_dict = frame_dict, pdf_file = pdf_file)
    outfile = match_subs_to_pages(vtt_file = subs_file, page_dict = page_dict, save_target= out_file)

    # Asks user if they want to delete the frames
    delete_frames = input("Do you want to delete the created files? (Y/n): ")
    if delete_frames.lower() == "n":
            print(f"Frames saved to {working_dir}. Delete them manually before running the script again.")
    else:
        shutil.rmtree(working_dir)
    
    print(f"Output saved to {outfile}")
    print("Done")


if __name__ == "__main__":
    main()