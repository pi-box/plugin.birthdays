#!/usr/bin/env python3
# -*- coding: UTF-8 -*-
"""
video_handler.py - Video Processing Module for Pi-Box Birthdays Plugin

This module is responsible for creating and processing birthday greeting videos.
It overlays text on a template video and generates personalized videos for birthday recipients.

Functionality:
1. Creates a text image with the recipient's name.
2. Converts the text image into a transparent MOV file.
3. Overlays the MOV file onto a template MP4 video.
4. Saves the final personalized video.

Dependencies:
- PIL (Pillow): For generating text images.
- ffmpeg: For video processing.
- os, subprocess: For file operations and command execution.

Usage:
This module is used by `pibox.birthdays.py` to generate birthday greeting videos.
"""

from PIL import Image, ImageDraw, ImageFont
import subprocess
import os

def create_text_image(text, font_path, output_path, width=600, height=200, font_size=100, color="#ffe462", angle=3.5):
    """
    Creates a PNG image with the given text, formatted properly.
    
    :param text: The text to be displayed on the image.
    :param font_path: Path to the font file.
    :param output_path: Path where the generated PNG will be saved.
    :param width: Width of the image.
    :param height: Height of the image.
    :param font_size: Font size of the text.
    :param color: Text color.
    :param angle: Rotation angle of the text.
    """
    font = ImageFont.truetype(font_path, font_size)
    text_layer = Image.new("RGBA", (width, height), (0, 0, 0, 0))
    draw = ImageDraw.Draw(text_layer)
    
    bbox = draw.textbbox((0, 0), text, font=font)
    text_x = (width - (bbox[2] - bbox[0])) // 2
    text_y = (height - (bbox[3] - bbox[1])) // 2
    
    draw.text((text_x, text_y), text, font=font, fill=color)
    rotated_layer = text_layer.rotate(angle, resample=Image.BICUBIC, center=(width // 2, height // 2))
    rotated_layer.save(output_path, "PNG")
    print(f"✅ Created text image: {output_path}")

def convert_png_to_mov(png_path, mov_path, duration=10):
    """
    Converts a PNG image to a transparent MOV video file.
    
    :param png_path: Path to the input PNG file.
    :param mov_path: Path to the output MOV file.
    :param duration: Duration of the generated video.
    """
    command = [
        "ffmpeg", "-loop", "1", "-t", str(duration), "-i", png_path,
        "-vf", "format=rgba", "-c:v", "qtrle", mov_path
    ]
    subprocess.run(command, check=True)
    print(f"✅ Converted {png_path} to {mov_path}")

def overlay_mov_on_video(video_path, overlay_mov, output_path, start_time=5, end_time=10, fade_in_duration=1, fade_out_duration=1, x=100, y=50):
    """
    Overlays a transparent MOV video onto another video with fade-in and fade-out effects.
    
    :param video_path: Path to the input video.
    :param overlay_mov: Path to the overlay MOV file.
    :param output_path: Path to the final output video.
    :param start_time: Start time of the overlay in seconds.
    :param end_time: End time of the overlay in seconds.
    :param fade_in_duration: Duration of the fade-in effect.
    :param fade_out_duration: Duration of the fade-out effect.
    :param x: X position of the overlay.
    :param y: Y position of the overlay.
    """
    fade_out_start = end_time - fade_out_duration
    command = [
        "ffmpeg", "-i", video_path, "-i", overlay_mov, "-filter_complex",
        f"[1:v]fade=t=in:st={start_time}:d={fade_in_duration}:alpha=1," \
        f"fade=t=out:st={fade_out_start}:d={fade_out_duration}:alpha=1[overlay];" \
        f"[0:v][overlay]overlay=x={x}:y={y}:enable='between(t,{start_time},{end_time})'",
        "-pix_fmt", "yuv420p", "-c:v", "libx264", "-c:a", "copy", output_path
    ]
    subprocess.run(command, check=True)
    print(f"✅ Created overlay video: {output_path}")

def create(assets_dir, caption, video_template, output_video):
    """
    Generates a personalized birthday video by overlaying text on a template.
    
    :param assets_dir: Directory containing assets such as fonts.
    :param caption: Name of the person to be displayed.
    :param video_template: Path to the template MP4 video.
    :param output_video: Path where the final video will be saved.
    """
    font_path = os.path.join(assets_dir, "AlmoniNeue-BoldAAA.ttf")
    png_file = os.path.join(assets_dir, "text.png")
    mov_file = os.path.join(assets_dir, "text.mov")
    start_time = 5.65
    end_time = 8.5
    fade_duration = 0.1

    # Step 1: Create text image
    hebrew_text = "ל" + caption
    create_text_image(hebrew_text, font_path, png_file)

    # Step 2: Convert PNG to MOV
    convert_png_to_mov(png_file, mov_file, duration=10)

    # Step 3: Overlay MOV on MP4
    if os.path.exists(output_video):
        os.remove(output_video)
    overlay_mov_on_video(video_template, mov_file, output_video, start_time=start_time, end_time=end_time, fade_in_duration=fade_duration, fade_out_duration=fade_duration, x=1085, y=487)

    # Step 4: Cleanup temporary files
    for file in [png_file, mov_file]:
        try:
            os.remove(file)
            print(f"🗑 Deleted temporary file: {file}")
        except FileNotFoundError:
            print(f"⚠️ File {file} not found for deletion.")
        except Exception as e:
            print(f"❌ Error deleting {file}: {e}")

    print(f"🎬 Video processing complete! Check {output_video}.")
