from glob import glob


def check_file_exists(filepath: str) -> bool:
    
    """
    check exists file 
    
    if file exist -> return True
    else -> False
    """
    if len(glob(filepath)) > 0:
        return True

    return False
