#!/usr/bin/env python3
"""
iCloud Photo Delta Analyzer
Compares iCloud photos with local backup directories and generates a CSV of missing files.
"""

import os
import csv
from pathlib import Path
from datetime import datetime
from pyicloud import PyiCloudService


def authenticate_icloud(username, password):
    """Authenticate with iCloud and handle 2FA if needed."""
    print(f"Authenticating with iCloud as {username}...")
    api = PyiCloudService(username, password)
    
    if api.requires_2fa:
        print("Two-factor authentication required.")
        code = input("Enter the 2FA code you received: ")
        result = api.validate_2fa_code(code)
        print(f"2FA validation result: {'Success' if result else 'Failed'}")
        
        if not result:
            raise Exception("Failed to authenticate with 2FA")
    
    print("Successfully authenticated!")
    return api


def get_icloud_photos(api):
    """Retrieve all photos from iCloud with metadata."""
    print("Fetching iCloud photo library...")
    photos = []
    
    for photo in api.photos.all:
        photo_data = {
            'filename': photo.filename,
            'created': photo.created,
            'asset_id': photo.asset_id,
            'size': getattr(photo, 'size', 'N/A')
        }
        photos.append(photo_data)
    
    print(f"Found {len(photos)} photos in iCloud")
    return photos


def scan_local_directories(directory_paths):
    """Scan local directories for existing photo files."""
    print(f"Scanning local directories: {directory_paths}")
    local_files = set()
    
    for dir_path in directory_paths:
        path = Path(dir_path)
        if not path.exists():
            print(f"Warning: Directory not found - {dir_path}")
            continue
        
        # Recursively find all files
        for file_path in path.rglob('*'):
            if file_path.is_file():
                local_files.add(file_path.name)
    
    print(f"Found {len(local_files)} files in local directories")
    return local_files


def calculate_delta(icloud_photos, local_files):
    """Find photos in iCloud that don't exist locally."""
    print("Calculating delta...")
    missing_photos = []
    
    for photo in icloud_photos:
        if photo['filename'] not in local_files:
            missing_photos.append(photo)
    
    print(f"Found {len(missing_photos)} photos not backed up locally")
    return missing_photos


def export_to_csv(missing_photos, output_file='missing_photos.csv'):
    """Export missing photos to CSV."""
    print(f"Exporting to {output_file}...")
    
    with open(output_file, 'w', newline='', encoding='utf-8') as csvfile:
        fieldnames = ['filename', 'created', 'asset_id', 'size']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        
        writer.writeheader()
        for photo in missing_photos:
            writer.writerow(photo)
    
    print(f"CSV exported successfully: {output_file}")


def main():
    """Main execution flow."""
    print("=== iCloud Photo Delta Analyzer ===\n")
    
    # Configuration
    icloud_username = input("Enter your iCloud email: ")
    icloud_password = input("Enter your iCloud password: ")
    
    local_dirs_input = input("Enter local backup directories (comma-separated): ")
    local_dirs = [d.strip() for d in local_dirs_input.split(',')]
    
    # Step 1: Authenticate
    api = authenticate_icloud(icloud_username, icloud_password)
    
    # Step 2: Get iCloud photos
    icloud_photos = get_icloud_photos(api)
    
    # Step 3: Scan local directories
    local_files = scan_local_directories(local_dirs)
    
    # Step 4: Calculate delta
    missing_photos = calculate_delta(icloud_photos, local_files)
    
    # Step 5: Export results
    if missing_photos:
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        output_file = f'missing_photos_{timestamp}.csv'
        export_to_csv(missing_photos, output_file)
        
        print(f"\n✓ Analysis complete!")
        print(f"✓ {len(missing_photos)} files need to be backed up")
        print(f"✓ List saved to: {output_file}")
    else:
        print("\n✓ All iCloud photos are backed up locally!")


if __name__ == "__main__":
    main()
