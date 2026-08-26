#!/usr/bin/env python3
"""Test script to verify download works."""

import subprocess
import tempfile
import os
import glob

def test_spotdl():
    """Test spotdl download."""
    test_url = "https://open.spotify.com/track/4iV5W9uYEdYUVa79Axb7Rh"
    temp_dir = tempfile.mkdtemp()
    
    print(f"Testing spotdl with: {test_url}")
    print(f"Temp dir: {temp_dir}")
    
    try:
        result = subprocess.run(
            ['spotdl', 'download', test_url, '--output', temp_dir],
            capture_output=True,
            text=True,
            timeout=120
        )
        
        print(f"Return code: {result.returncode}")
        print(f"stdout: {result.stdout}")
        if result.stderr:
            print(f"stderr: {result.stderr}")
        
        audio_files = []
        for ext in ['*.mp3', '*.m4a', '*.opus', '*.ogg', '*.wav']:
            audio_files.extend(glob.glob(os.path.join(temp_dir, ext)))
        
        if audio_files:
            print(f"\n✅ Success! Found {len(audio_files)} file(s):")
            for f in audio_files:
                size = os.path.getsize(f)
                print(f"  - {os.path.basename(f)} ({size} bytes)")
        else:
            print("\n❌ No audio files found!")
            
    except Exception as e:
        print(f"❌ Error: {e}")
    finally:
        import shutil
        shutil.rmtree(temp_dir, ignore_errors=True)

def test_ytdlp():
    """Test yt-dlp download."""
    test_url = "https://www.youtube.com/watch?v=dQw4w9WgXcQ"
    temp_dir = tempfile.mkdtemp()
    
    print(f"\nTesting yt-dlp with: {test_url}")
    print(f"Temp dir: {temp_dir}")
    
    try:
        output_template = os.path.join(temp_dir, '%(title)s.%(ext)s')
        
        result = subprocess.run(
            [
                'yt-dlp',
                '-x',
                '--audio-format', 'mp3',
                '-o', output_template,
                '--no-playlist',
                test_url
            ],
            capture_output=True,
            text=True,
            timeout=120
        )
        
        print(f"Return code: {result.returncode}")
        print(f"stdout: {result.stdout}")
        if result.stderr:
            print(f"stderr: {result.stderr}")
        
        audio_files = []
        for ext in ['*.mp3', '*.m4a', '*.opus', '*.ogg', '*.wav', '*.webm']:
            audio_files.extend(glob.glob(os.path.join(temp_dir, ext)))
        
        if audio_files:
            print(f"\n✅ Success! Found {len(audio_files)} file(s):")
            for f in audio_files:
                size = os.path.getsize(f)
                print(f"  - {os.path.basename(f)} ({size} bytes)")
        else:
            print("\n❌ No audio files found!")
            
    except Exception as e:
        print(f"❌ Error: {e}")
    finally:
        import shutil
        shutil.rmtree(temp_dir, ignore_errors=True)

if __name__ == '__main__':
    print("🎵 Testing Download Methods")
    print("=" * 40)
    
    test_spotdl()
    test_ytdlp()
