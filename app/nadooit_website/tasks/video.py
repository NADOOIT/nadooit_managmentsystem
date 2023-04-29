import json
from celery import shared_task
from nadooit_website.models import (
    Video,
    VideoResolution,
)
from django.db.models import Count
import os


from moviepy.editor import VideoFileClip
import gzip
import shutil

from moviepy.editor import ffmpeg_tools


def create_hls_files(input_path, output_path, resolution, segment_duration=4):
    hls_output_path = os.path.splitext(output_path)[0] + f"_{resolution}p_hls"
    os.makedirs(hls_output_path, exist_ok=True)
    playlist_file = os.path.join(hls_output_path, f"playlist_{resolution}p.m3u8")

    width = -1
    height = resolution
    bitrate = "1000k"
    gop_size = segment_duration * 30

    ffmpeg_tools.ffmpeg_extract_subclip(
        input_path,
        0,
        -1,
        targetname=playlist_file,
        codec="libx264",
        bitrate=bitrate,
        vf=f"scale={width}:{height}",
        gop_size=gop_size,
        hls_time=segment_duration,
        hls_playlist_type="vod",
        format="hls",
    )

    return hls_output_path


def convert_to_mp4(input_path, output_path):
    clip = VideoFileClip(input_path)
    clip.write_videofile(output_path, codec="libx264")


def reduce_bitrate(input_path, output_path, bitrate, crf, preset):
    ffmpeg_command = f"ffmpeg -i {input_path} -b:v {bitrate} -crf {crf} -preset {preset} {output_path}"
    subprocess.run(ffmpeg_command, shell=True, check=True)


def compress_video(input_path, output_path):
    with open(input_path, "rb") as src_file:
        with gzip.open(output_path, "wb") as dest_file:
            shutil.copyfileobj(src_file, dest_file)


def scale_video(input_path, output_path, resolution):
    clip = VideoFileClip(input_path)
    height = resolution
    scaled_clip = clip.resize(
        height=height
    )  # This will maintain the original aspect ratio
    scaled_clip.write_videofile(output_path, codec="libx264")


import os
import subprocess

from django.core.exceptions import ObjectDoesNotExist


def process_video(input_path, output_path, resolution, bitrate, crf, preset):
    try:
        temp_path = input_path

        scaled_output_path = os.path.splitext(output_path)[0] + f"_{resolution}p.mp4"
        scale_video(temp_path, scaled_output_path, resolution)

        reduced_output_path = os.path.splitext(scaled_output_path)[0] + "_reduced.mp4"
        reduce_bitrate(scaled_output_path, reduced_output_path, bitrate, crf, preset)
        os.remove(scaled_output_path)
        os.rename(reduced_output_path, scaled_output_path)

        # Create HLS files and playlist for the current resolution
        video_name = os.path.splitext(os.path.basename(input_path))[0]

        hls_output_path = f"/vol/web/media/hls_playlists/{video_name}_{resolution}p"
        os.makedirs(hls_output_path, exist_ok=True)
        hls_playlist_path = os.path.join(hls_output_path, "index.m3u8")
        ffmpeg_command = f"ffmpeg -i {scaled_output_path} -profile:v high444 -level 4.2 -start_number 0 -hls_time 10 -hls_list_size 0 -f hls {hls_playlist_path}"
        subprocess.run(ffmpeg_command, shell=True, check=True)
    except Exception as e:
        print(f"Error occurred during video processing: {e}")
        if os.path.exists(scaled_output_path):
            os.remove(scaled_output_path)
        if os.path.exists(reduced_output_path):
            os.remove(reduced_output_path)
        raise e


@shared_task
def create_streaming_files_task(video_id):
    from django.db import connections
    from django.core.files import File

    try:
        video = Video.objects.get(id=video_id)
    except ObjectDoesNotExist:
        print(f"Video with id {video_id} does not exist")
        return

    connections.close_all()
    input_path = video.original_file.path

    print("Input path:", input_path)
    print("Video ID:", video_id)
    output_path = os.path.splitext(input_path)[0] + ".mp4"
    print("Output path:", output_path)

    # Convert to mp4 format if necessary
    temp_path = input_path
    if not input_path.lower().endswith(".mp4"):
        temp_path = os.path.splitext(input_path)[0] + "_temp.mp4"
        convert_to_mp4(input_path, temp_path)
        input_path = temp_path

    # Load the JSON configuration file
    try:
        with open("video_config.json") as config_file:
            config = json.load(config_file)
    except Exception as e:
        print(f"Error loading configuration file: {e}")
        return

    video_name = os.path.splitext(os.path.basename(input_path))[0]
    print("Video name:", video_name)

    # Now use the configurations from the file
    try:
        for resolution_config in config["resolutions"]:
            resolution = resolution_config["resolution"]
            bitrate = resolution_config["bitrate"]
            crf = resolution_config["crf"]
            preset = resolution_config["preset"]

            process_video(input_path, output_path, resolution, bitrate, crf, preset)

            # Save the processed video file
            scaled_output_path = (
                os.path.splitext(output_path)[0] + f"_{resolution}p.mp4"
            )
            with open(scaled_output_path, "rb") as transcoded_file:
                connections["default"].connect()
                video_resolution = VideoResolution.objects.create(
                    video=video, resolution=resolution
                )
                video_resolution.video_file.save(
                    os.path.basename(scaled_output_path),
                    File(transcoded_file),
                    save=True,
                )

            # Save the HLS playlist file
            hls_playlist_path = (
                f"/vol/web/media/hls_playlists/{video_name}_{resolution}p/index.m3u8"
            )
            with open(hls_playlist_path, "rb") as playlist_file:
                connections["default"].connect()
                video_resolution.hls_playlist_file.save(
                    f"{video_name}_{resolution}p/index.m3u8",
                    File(playlist_file),
                    save=True,
                )

            # Delete the processed video file
            if os.path.exists(scaled_output_path):
                os.remove(scaled_output_path)
    except Exception as e:
        print(f"Error occurred during file saving or processing: {e}")
        if os.path.exists(input_path):
            os.remove(input_path)
        if os.path.exists(output_path):
            os.remove(output_path)
        raise e
    finally:
        if os.path.exists(temp_path) and temp_path != input_path:
            os.remove(temp_path)
