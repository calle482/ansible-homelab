import glob
import os
import sys
import shutil
import subprocess

if __name__ == '__main__':
    current_directory = os.getcwd()
    # change these for other extensions as needed
    VIDEO_EXTS = ['.mkv', '.mp4']
    SUBTITLE_EXTENSIONS = ['.en.srt', '.sv.srt']

    for root, dirs, files in os.walk(current_directory):
        for video_ext in VIDEO_EXTS:
            for video_file in glob.glob(os.path.join(root, '*' + video_ext)):
                base = os.path.splitext(video_file)[0]

                for subtitle_ext in SUBTITLE_EXTENSIONS:
                    srt_file = base + subtitle_ext
                    synced_srt_file = base + '.default' + subtitle_ext

                    if not os.path.exists(srt_file):
                        continue  # Skip if subtitle file doesn't exist

                    print(f'Syncing {video_file} - {subtitle_ext[1:3].upper()} subtitles')

                    # Construct the autosubsync command with the parallelism option
                    autosubsync_cmd = [
                        'autosubsync',
                        '--parallelism',
                        '24',
                        video_file,
                        srt_file,
                        synced_srt_file
                    ]

                    try:
                        # Execute the autosubsync command using subprocess
                        subprocess.run(autosubsync_cmd, check=True)
                    except subprocess.CalledProcessError:
                        print('Low-quality fit detected. Skipping to the next file.')
                        continue

                    # Move the original subtitle file to the backup directory
                    backup_dir = os.path.join(root, 'subs_backup')
                    os.makedirs(backup_dir, exist_ok=True)
                    backup_srt_file = os.path.join(backup_dir, os.path.basename(srt_file))
                    shutil.move(srt_file, backup_srt_file)

                    # Rename the synced subtitle file
                    new_srt_file = base + subtitle_ext
                    if os.path.exists(synced_srt_file):
                        os.rename(synced_srt_file, new_srt_file)

                    print(f'Syncing complete for {video_file} - {subtitle_ext[1:3].upper()} subtitles')
