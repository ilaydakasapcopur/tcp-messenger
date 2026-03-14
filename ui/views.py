def show_log_details(log_entry):
    print("\n--- Message Parameters ---")
    for key, value in log_entry['params'].items():
        print(f"{key.capitalize()}: {value}")

def list_logs(logs):
    print(f"\n{'ID':<5} | {'Timestamp':<20} | {'Type':<10}")
    print("-" * 40)
    for idx, log in enumerate(logs):
        print(f"{idx:<5} | {log['timestamp']:<20} | {log['type']:<10}")