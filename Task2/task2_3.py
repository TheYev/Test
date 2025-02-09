import re
import argparse
from collections import Counter


LOG_PATTERN = re.compile(r'(?P<ip>[\d\.]+) - - \[.*\] "[A-Z]+ (?P<url>\S+) [^"]+" (?P<status>\d{3}) (?P<size>\d+|-)')

def parse_log(file_path):
    ip_counter = Counter()
    status_counter = Counter()
    total_size = 0
    count = 0
    
    with open(file_path, 'r', encoding='utf-8') as file:
        for line in file:
            match = LOG_PATTERN.match(line)
            if match:
                data = match.groupdict()
                ip_counter[data['ip']] += 1
                status_counter[data['status']] += 1
                
                if data['size'].isdigit():
                    total_size += int(data['size'])
                    count += 1
    
    return ip_counter, status_counter, total_size, count

def analyze_log(file_path):
    ip_counter, status_counter, total_size, count = parse_log(file_path)
    
    print("Top 5 IP addresses with most requests:")
    for ip, freq in ip_counter.most_common(5):
        print(f"{ip}: {freq} requests")
    
    print("\nMost frequent errors (4xx and 5xx):")
    for status, freq in status_counter.items():
        if status.startswith('4') or status.startswith('5'):
            print(f"Status {status}: {freq} times")
    
    avg_size = total_size / count if count else 0
    print(f"\nAverage response size: {avg_size:.2f} bytes")

def main():
    parser = argparse.ArgumentParser(description="Analyze Nginx log files.")
    parser.add_argument("logfile", help="Path to the log file")
    args = parser.parse_args()
    analyze_log(args.logfile)

if __name__ == "__main__":
    main()
