import subprocess
import time
import sys
import os

def run_performance_test():
    print("Starting FastAPI server in background...")
    # Start uvicorn server in a separate process
    server_process = subprocess.Popen(
        [sys.executable, "-m", "uvicorn", "app.main:app", "--host", "127.0.0.1", "--port", "8000", "--log-level", "warning"],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE
    )
    
    # Wait for the server to start up
    time.sleep(2)
    
    # Check if server started successfully
    if server_process.poll() is not None:
        print("Error: FastAPI server failed to start.")
        stdout, stderr = server_process.communicate()
        print("Stdout:", stdout.decode())
        print("Stderr:", stderr.decode())
        sys.exit(1)
        
    print("FastAPI server started. Running Locust load test...")
    
    # Run Locust in headless mode
    os.makedirs("reports", exist_ok=True)
    locust_cmd = [
        sys.executable, "-m", "locust",
        "-f", "locustfile.py",
        "--headless",
        "-u", "10",            # 10 concurrent users
        "-r", "2",             # Spawn rate: 2 users per second
        "--run-time", "10s",   # Run for 10 seconds
        "--host", "http://127.0.0.1:8000",
        "--html", "reports/locust_report.html"
    ]
    
    try:
        result = subprocess.run(locust_cmd, capture_output=True, text=True)
        print("Locust execution completed.")
        print(result.stdout)
        if result.stderr:
            print("Locust warnings/errors:", result.stderr)
    except Exception as e:
        print("Error running Locust:", str(e))
    finally:
        print("Terminating FastAPI server...")
        server_process.terminate()
        try:
            server_process.wait(timeout=5)
            print("Server process terminated successfully.")
        except subprocess.TimeoutExpired:
            print("Server process did not terminate. Killing...")
            server_process.kill()
            server_process.wait()

if __name__ == "__main__":
    run_performance_test()
