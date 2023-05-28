#!/usr/bin/python3
#
# -*- encoding: UTF-8
# (c) Yash Oswal | https://t.me/yashoswalyo
# 
# NOTE: it can mux only Hindi audios and keeps the first audio of input file
#  
# requirements:
# > python3 -m pip install -U ffmpeg-python
# 
# help:
# > python3 batch_mux.py -h


import argparse
import json
import os
import subprocess

import ffmpeg


def batch_mux(
    videolist: list,
    audiolist: list,
    delay,
    title,
    hiTitle,
    enTitle,
    output,
):
    title = title.strip() if title is not None else output
    hiTitle = hiTitle.strip()

    total_files = len(videolist)
    f=open('batchcmds.txt','w')
    print(total_files)
    for i in range(total_files):
        videofile = videolist[i]
        audiofile = audiolist[i]
        temp = title.format_map({"i": str(i + 1).zfill(2)})
        final_output = output.format_map({"i": str(i + 1).zfill(2)})
        videodata = ffmpeg.probe(videofile)
        muxcmd = []
        muxcmd.append("ffmpeg")
        muxcmd.append("-hide_banner")
        muxcmd.append("-i")
        muxcmd.append(videofile)
        muxcmd.append("-itsoffset")
        muxcmd.append(delay)
        muxcmd.append("-i")
        muxcmd.append(audiofile)
        muxcmd.append("-map")
        muxcmd.append("0:v:0")
        muxcmd.append("-map")
        muxcmd.append("1:a:0")
        muxcmd.append("-map")
        muxcmd.append("0:a:0")
        muxcmd.append("-disposition:a:1")
        muxcmd.append("0")
        muxcmd.append("-disposition:a:0")
        muxcmd.append("default")
        muxcmd.append("-max_interleave_delta")
        muxcmd.append("0")

        for stream in videodata.get("streams"):
            if (stream["codec_type"] == "subtitle") and (
                stream["tags"]["language"].lower() in ["eng", "en"]
            ):
                ind = stream["index"]
                muxcmd.append("-map")
                muxcmd.append(f"0:{ind}")
                muxcmd.append(f"-disposition:s:s:0")
                muxcmd.append(f"default")
            if (stream["codec_type"] == "audio") and (
                stream["tags"]["language"].lower() in ["eng", "en"]
            ):
                og_title = stream["tags"]["title"]

        muxcmd.append("-metadata:s:a:1")
        muxcmd.append("language=eng")
        muxcmd.append("-metadata:s:a:1")
        muxcmd.append(f"title={enTitle if enTitle is not None else og_title}")
        muxcmd.append("-metadata:s:a:0")
        muxcmd.append("language=hin")
        muxcmd.append("-metadata:s:a:0")
        muxcmd.append(f"title={hiTitle}")
        muxcmd.append("-metadata")
        muxcmd.append(f"title={temp}")
        muxcmd.append("-c")
        muxcmd.append("copy")
        muxcmd.append(final_output)

        process = subprocess.call(muxcmd,stdout=subprocess.DEVNULL,stdin=subprocess.PIPE)
        
        f.write(" ".join(muxcmd))
        f.write("\n")
        print(muxcmd)

        i += 1
    f.close()
    return 1


def main():
    parser = argparse.ArgumentParser(
        description="Batch Mux video and audio. Made by :- @yashoswalyo",
        epilog="Exported file will be stored in ./output folder in current directory",
    )
    req = parser.add_argument_group("Required")
    opt = parser.add_argument_group("Optional")
    req.add_argument(
        "-v",
        "--videos",
        metavar="PATH",
        help="Path to the video directory",
        type=str,
        required=True,
    )
    req.add_argument(
        "-a",
        "--audios",
        metavar="PATH",
        help="Path to the audio directory",
        type=str,
        required=True,
    )
    opt.add_argument(
        "-d",
        "--delay",
        type=float,
        help="ffmpeg option '-itsoffset delay' in seconds (default==0.000)",
    )
    opt.add_argument(
        "-t",
        "--title",
        metavar="STRING",
        help="Title of each video can have {i} substitution (e.g: --title='Stranger Things S01E{i}')",
        type=str,
    )
    req.add_argument(
        "-hi",
        "--hin-audio-title",
        metavar="STRING",
        help="Hindi audio title string",
        type=str,
    )
    opt.add_argument(
        "-en",
        "--eng-auido-title",
        metavar="STRING",
        help="English audio title string",
        type=str,
    )
    req.add_argument(
        "-o",
        "--output",
        metavar="STRING",
        help="File name string, supports {i} substitution (e.g: -o 'Stranger Things S04E{i} 1080p 10bit WEBRiP x265 [Hindi AAC 2.0 + ENGLISH AAC 2.0] ESub.mkv')",
        type=str,
        required=True,
    )

    args = parser.parse_args()
    argdict = args.__dict__
    print(json.dumps(argdict, indent=3))

    if argdict.get("video") is not None:
        video_directory = argdict.get("video")
        video_directory = (
            video_directory if video_directory.endswith("/") else video_directory + "/"
        )
        if not os.path.exists(video_directory):
            exit("Video Directory doesnt exist")

    if argdict.get("audio") is not None:
        audio_directory = argdict.get("audio")
        audio_directory = (
            audio_directory if audio_directory.endswith("/") else audio_directory + "/"
        )
        if not os.path.exists(audio_directory):
            exit("Audio Directory doesnt exist")
    vpaths = []
    for dirpath, dirnames, filenames in os.walk(video_directory):
        filenames.sort(key=str.casefold)
        for f in filenames:
            vpaths.append(os.path.join(dirpath, f))
    apaths = []
    for dirpath, dirnames, filenames in os.walk(audio_directory):
        filenames.sort(key=str.casefold)
        for f in filenames:
            apaths.append(os.path.join(dirpath, f))

    title = argdict.get("title", None)
    hiTitle = argdict.get("hin_audio_title", None)
    enTitle = argdict.get("eng_auido_title", None)
    output = argdict.get("output", None)
    delay = argdict.get("delay")
    delay = 0.0 if delay is None else delay
    delay = "{:.3f}".format(delay)

    try:
        diirname = os.path.dirname(output)
        if not os.path.exists(diirname):
            os.makedirs(diirname)
    except:
        pass
    print(diirname)
    batch_mux(vpaths, apaths, delay, title, hiTitle, enTitle, output)


if __name__ == "__main__":
    main()
