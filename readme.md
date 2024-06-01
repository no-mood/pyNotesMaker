# pyNotesMaker

pyNotesMaker is a Python-based tool that matches video scenes with corresponding text from a PDF file. It uses scene detection to extract frames from a video, matches these frames with the text, and outputs the results to a file.

## Installation

Clone the repository to your local machine:

```bash
git clone https://github.com/yourusername/pyNotesMaker.git
```

Navigate to the project directory:

```
cd pyNotesMaker
```

Install the required packages:

```bash
pip install -r requirements.txt
```

Or, if you're a Nix user, you can use the provided `flake.nix` file to create a development environment:

```bash
nix develop flake.nix
```

## Usage
You can run pyNotesMaker from the command line with the following arguments:

```bash
python main.py -v <video_file> -p <pdf_file> -o <output_file> [-s <subs_file>] [-t <threshold>]
```

```bash
-v, --video: (Required) The video file to process.
-p, --pdf: (Required) The PDF file to match with the video scenes.
-o, --output: (Required) The file to output the results to.
-s, --subs: (Optional) The subtitles file. If not provided, subtitles will be generated from the video file.
-t, --threshold: (Optional) The threshold for scene detection. If not provided, a default value of 0.05 will be used.
`````

### Example
```bash
python main.py -v my_video.mp4 -p my_pdf.pdf -o output.txt
```


## License
This project is licensed under the
[MIT](https://choosealicense.com/licenses/mit/) license.