### Requirements:
`python3 -m pip install -U ffmpeg-python`

### Help:
`python3 batch_mux.py --help`
```
usage: batch_mux.py [-h] -v PATH -a PATH [-d DELAY] [-t STRING] [-hi STRING] [-en STRING] -o STRING

Batch Mux video and audio. Made by :- @yashoswalyo

options:
  -h, --help            show this help message and exit

Required:
  -v PATH, --video PATH
                        Path to the video directory
  -a PATH, --audio PATH
                        Path to the audio directory
  -hi STRING, --hin-audio-title STRING
                        Hindi audio title string
  -o STRING, --output STRING
                        File name string, supports {i} substitution (e.g: -o 'Stranger Things S04E{i} 1080p 10bit WEBRiP x265    
                        [Hindi AAC 2.0 + ENGLISH AAC 2.0] ESub.mkv')

Optional:
  -d DELAY, --delay DELAY
                        ffmpeg option '-itsoffset delay' in seconds (default==0.000)
  -t STRING, --title STRING
                        Title of each video can have {i} substitution (e.g: --title='Stranger Things S01E{i}')
  -en STRING, --eng-auido-title STRING
                        English audio title string

Exported file will be stored in ./output folder in current directory
```

### Example command to batch mux hindi audios:
```
python3 batch_mux.py \
--videos ./videos_dir \
--audios ./hindi_audios_dir \
--hi-audio-title 'Hindi AAC 2.0 ~ RAGA' \
--output 'Stranger Things S04E{i} 480p NF WEB-DL [Hindi + English] x264 ESubs ~ RAGA ~ Pahe.in.mkv'
```
