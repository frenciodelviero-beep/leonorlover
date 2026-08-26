#!/usr/bin/env python3
"""Test script to verify spotdl works correctly."""

import subprocess
import tempfile
import os
import glob

def test_spotdl():
    """Test if spotdl can download a track."""
    
    # Test URL (a popular track)
    test_url = "https://open.spotify.com/track/4iV5W9uYEdYUVa79Axb7Rh"
    
    # Create temp directory
    temp_dir = tempfile.mkdtemp()
    print(f"Temp directory: {temp_dir}")
    
    try:
        print(f"Testing spotdl with URL: {test_url}")
        
        # Run spotdl
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
        
        # Check for downloaded files
        audio_files = []
        for ext in ['*.mp3', '*.m4a', '*.opus', '*.ogg', '*.wav']:
            audio_files.extend(glob.glob(os.path.join(temp_dir, ext)))
        
        if audio_files:
            print(f"\n✅ Success! Found {len(audio_files)} audio file(s):")
            for f in audio_files:
                size = os.path.getsize(f)
                print(f"  - {os.path.basename(f)} ({size} bytes)")
        else:
            print("\n❌ No audio files found!")
            
    except subprocess.TimeoutExpired:
        print("❌ Download timed out!")
    except Exception as e:
        print(f"❌ Error: {e}")
    finally:
        # Cleanup
        import shutil
        shutil.rmtree(temp_dir, ignore_errors=True)

if __name__ == '__main__':
    test_spotdl()
