"""
Photo utilities for downloading and saving photos from Telegram
"""
from pathlib import Path
from aiogram import Bot
from aiogram.types import PhotoSize


async def download_photo(bot: Bot, photo: PhotoSize, folder: str = "photos") -> str:
    """
    Download photo from Telegram and save to local storage
    
    Args:
        bot: Bot instance
        photo: PhotoSize object from Telegram
        folder: Folder name to save photos (default: "photos")
    
    Returns:
        Relative path to saved photo (e.g., "photos/shop_123_photo.jpg")
    """
    # Get project root directory
    project_root = Path(__file__).resolve().parent.parent.parent.parent
    storage_dir = project_root / "storage" / folder
    storage_dir.mkdir(parents=True, exist_ok=True)
    
    # Get file info from Telegram
    file_info = await bot.get_file(photo.file_id)
    
    # Generate unique filename
    # Format: {type}_{id}_{timestamp}.jpg
    import time
    timestamp = int(time.time())
    file_extension = file_info.file_path.split('.')[-1] if '.' in file_info.file_path else 'jpg'
    filename = f"{folder}_{timestamp}_{photo.file_id[:10]}.{file_extension}"
    
    # Full path to save file
    file_path = storage_dir / filename
    
    # Download file
    await bot.download_file(file_info.file_path, str(file_path))
    
    # Return relative path from project root (for database storage)
    relative_path = f"storage/{folder}/{filename}"
    
    return relative_path


def get_photo_path(relative_path: str) -> Path:
    """
    Get full path to photo file
    
    Args:
        relative_path: Relative path stored in database (e.g., "storage/photos/shop_123.jpg")
    
    Returns:
        Path object to photo file
    """
    project_root = Path(__file__).resolve().parent.parent.parent.parent
    return project_root / relative_path


def photo_exists(relative_path: str) -> bool:
    """
    Check if photo file exists
    
    Args:
        relative_path: Relative path stored in database
    
    Returns:
        True if file exists, False otherwise
    """
    if not relative_path:
        return False
    
    photo_path = get_photo_path(relative_path)
    return photo_path.exists()

