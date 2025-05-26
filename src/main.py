import uvicorn
import argparse

def main():
    parser = argparse.ArgumentParser(description="Run the FastAPI server")
    parser.add_argument("-port", type=int, default=8000, help="Port number the server should listen on")
    args = parser.parse_args()

    uvicorn.run("fast:app", host="127.0.0.1", port=args.port, log_level="info")

if __name__ == "__main__":
    main()

