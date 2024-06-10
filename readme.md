# pyNotesMaker

This tool is designed to transcribe university lectures from a video where slides are shown.

The tool performs the following steps:

1. **Frame Extraction**: The tool uses `ffmpeg` to extract distinct frames from the video based on a certain threshold. This is particularly useful for videos that display presentation slides, as the threshold can be set to a low level to capture only the slide changes. The tool saves both the frame images and their timings.

2. **Text Extraction**: The tool extracts text from each frame using Optical Character Recognition (OCR) and associates each frame with a page of a PDF (passed from the command line).

3. **Subtitle Association**: The tool associates the subtitles with the PDF pages based on timing, and generates a LaTeX file containing a custom environment with the page name and text block.

The generated file can be used in a document as follows:

<details>
  <summary>Example of output.tex</summary>
  
```latex
\begin{slide}{1}
	Lorem ipsum dolor sit amet, consectetur adipiscing elit. Vivamus lacinia odio vitae vestibulum vestibulum. Cras venenatis euismod malesuada. Nullam ac erat ante. Quisque ultricies lorem nec ligula sagittis, at ullamcorper velit ultricies. Nam vel urna quis velit ullamcorper varius. Mauris vel augue sed quam dignissim commodo et eget nisl. Suspendisse potenti. Proin sit amet diam eget mi facilisis lacinia. Fusce elementum, nulla ac vulputate sagittis, justo lorem ultricies libero, id malesuada nulla elit in metus. Praesent tincidunt sem vel bibendum venenatis.
\end{slide}

\begin{slide}{2}
	Praesent scelerisque, quam a ullamcorper malesuada, metus nulla commodo nulla, vitae ultrices lacus purus nec erat. Suspendisse potenti. Etiam tristique eros in magna feugiat, non elementum nisl scelerisque. Vivamus in diam volutpat, fringilla metus vel, condimentum turpis. Cras tincidunt purus quis urna bibendum, non condimentum est egestas. Ut non orci libero. Phasellus tempor enim ut risus vehicula, vel dignissim justo scelerisque. Nulla facilisi.
\end{slide}

\begin{slide}{3}
	Curabitur eget justo nisi. Aliquam erat volutpat. Donec suscipit lorem ac quam porttitor, sit amet consectetur libero sodales. Sed tincidunt urna vel nunc facilisis, nec laoreet velit lacinia. Maecenas vehicula magna a efficitur tincidunt. Nullam ac tortor ut dolor auctor feugiat id nec justo. Morbi sodales, odio sed fringilla lacinia, arcu ex dapibus risus, eu dictum lectus quam eu nulla. Suspendisse euismod risus nec risus venenatis, et venenatis arcu blandit. Praesent ultricies lectus id orci tincidunt venenatis.
\end{slide}
```
  
</details>


<details>
  <summary>Example of main.tex</summary>

```latex
\documentclass[8pt]{beamer}
\title{pyNotesMaker}
\author{Your name}
\institute{Your institute}
\date{\today}

% This is the custom environment used by pyNotesMaker
\newenvironment{slide}[1]{%
\begin{frame}[t, plain, noframenumbering]
\centering
\includegraphics[page = #1,width =\textwidth]{\slides}
}{%
\end{frame}
}

\begin{document}

\def\slides{slides/01-Chapter1.pdf}
\include{output}


\end{document}
```

</details>

## Installation

Clone the repository to your local machine, then navigate to the project directory:


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
python main.py -v <video_file> -d <pdf_file> [-o <output_file>] [-s <subs_file>] [-t <threshold>]
```

```bash
-v, --video: (Required) The Video file to process.
-d, --pdf: (Required) The PDF Document to match with the video scenes.
-o, --output: (Optional) The file to Output the results to. If not provided, the default will the output.tex in the output/ directory.
-s, --subs: (Optional) The Subtitles file. If not provided, subtitles will be generated from the video file.
-t, --threshold: (Optional) The Threshold for scene detection. If not provided, a default value of 0.05 will be used.
```

### Example

```bash
python main.py -v my_video.mp4 -d my_pdf.pdf -o output.tex
```

## License

This project is licensed under the
[MIT](https://choosealicense.com/licenses/mit/) license.
