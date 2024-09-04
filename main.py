import subprocess

def main():
    # Define the path to the send_audio.py script
    script_path = "backend/streaming_server/send_audio.py"
    
    try:
        # Run the script using subprocess
        result = subprocess.run(['python', script_path], capture_output=True, text=True)
        
        # Print the output and errors
        print("Output:\n", result.stdout)
        print("Errors:\n", result.stderr)
        
        # Check if the script executed successfully
        if result.returncode == 0:
            print("Script ran successfully.")
        else:
            print("Script encountered an error.")
            
    except Exception as e:
        print(f"An error occurred while running the script: {e}")

if __name__ == "__main__":
    main()