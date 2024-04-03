import argparse
import subprocess
import os
import logging

# Setup logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s [%(levelname)s] %(message)s')

def get_subtitle_streams(file_path, languages=None):
    """Returns the indexes of the first subtitle stream for each specified language."""
    cmd = ['ffprobe', '-v', 'error', '-select_streams', 's', '-show_entries',
           'stream=index:stream_tags=language', '-of', 'csv=p=0', file_path]
    result = subprocess.run(cmd, text=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    streams = [line.split(',') for line in result.stdout.splitlines()]

    # Extract language streams
    if languages is None:
        # Return all available languages
        if not streams:
            lang_streams
        else:
            lang_streams = { lang : stream for stream, lang in streams }
    else:
        # Filter streams by specified languages
        lang_streams = {lang: next((stream[0] for stream in streams if stream[1] == lang), None) for lang in languages}

    return lang_streams

def extract_media(file_path, languages=None):

    if languages is None:
        subtitle_streams = get_subtitle_streams(file_path, languages)
        logging.info(f'{file_path} contains these subtitles: {sorted(set(subtitle_streams.keys()))}')
        return

    base_name = os.path.splitext(file_path)[0]
    video_output = f'{base_name}.mp4'
    if len(languages) == 1:
        subtitle_outputs = {lang: f'{base_name}.srt' for lang in languages}
    else:
        subtitle_outputs = {lang: f'{base_name}_{lang}.srt' for lang in languages}

    # Extract MP4 video
    logging.info(f'Extracting video to {video_output}')
    subprocess.run(['ffmpeg', '-v', 'error', '-i', file_path, '-c', 'copy', '-map', '0:v:0', '-map', '0:a?', video_output])

    # Get subtitle streams
    subtitle_streams = get_subtitle_streams(file_path, languages)

    # Extract subtitles
    for lang, stream_index in subtitle_streams.items():
        if stream_index:
            logging.info(f'Extracting {lang} subtitles to {subtitle_outputs[lang]}')
            subprocess.run(['ffmpeg', '-v', 'error', '-i', file_path, '-map', f'0:{stream_index}', '-c', 'copy', subtitle_outputs[lang]])
        else:
            logging.warning(f'No subtitle stream found for {lang} in {file_path}')

def main():
    parser = argparse.ArgumentParser(description="Extract MP4 and subtitles from MKV files.")
    parser.add_argument('files', nargs='+', help='MKV file(s) to process.')
    parser.add_argument('-l', '--languages', '--lang', nargs='+', help='Subtitle languages to extract (ISO 639-2 codes). If only one language is extracted, then the output file will have the same name as the video file. Otherwise `_lang` will be appended to the name.')

    args = parser.parse_args()

    for mkv_file in args.files:
        if not os.path.isfile(mkv_file):
            logging.error(f'File not found: {mkv_file}')
            continue
        extract_media(mkv_file, args.languages)

if __name__ == '__main__':
    main()


