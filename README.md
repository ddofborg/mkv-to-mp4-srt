# MKV to MP4 & SRT (subtitles) extractor

Extract MP4 and subtitles from an MKV file to separate files.


## Requirements

Binaries:

- ffmpeg

- ffprobe

To install, on:

- OSX use `brew install ffmpeg` (if [Homebrew](https://brew.sh/) is installed).
- Ubuntu use `sudo apt-get install ffmpeg`. 
- Fedora use `sudo dnf install ffmpeg`.
- RHEL use `sudo yum install ffmpeg ffmpeg-devel`.
- CentOS use `sudo dnf install ffmpeg ffmpeg-devel`.
- Windows, see [gyan.dev](https://www.gyan.dev/ffmpeg/builds/).

## Usage

    usage: mkv-to-mp4-srt.py [-h] [-l LANGUAGES [LANGUAGES ...]] files [files ...]

    Extract MP4 and subtitles from MKV files.

    positional arguments:
      files                 MKV file(s) to process.

    options:
      -h, --help            show this help message and exit
      -l LANGUAGES [LANGUAGES ...], --languages LANGUAGES [LANGUAGES ...]
                            Subtitle languages to extract (ISO 639-2 codes).


## Notes

- Output will be put in the same folder as the source, only with different extension. `.mp4.` for the video and `_{lang}.srt` for the subtitles.

- The video is not recompressed, just copied without quality loss.

- (not tested) If there is no MP4 video in the MKV file, the video will still be extracted as `.mp4`, but will need a different player.
