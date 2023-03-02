

def start_server():
    import sys, subprocess
    subprocess.call(['uvicorn', 'src.server.server:app', '--reload', '--port' , '9000'])


if __name__ == "__main__":
    try:
        start_server()
    except Exception as e:
        raise e