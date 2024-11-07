import os
import matplotlib.pyplot as plt
from datetime import datetime, timedelta
import pandas as pd

def read_log_files(directory):
    data = []
    for filename in os.listdir(directory):
        if filename.endswith(".log"):
            with open(os.path.join(directory, filename), 'r') as file:
                start_time, end_time = None, None
                for line in file:
                    if line.startswith("Start time:"):
                        parts = line.strip().split(" ")
                        start_time = datetime.strptime(parts[2] + " " + parts[3], '%Y-%m-%d %H:%M:%S')
                    if line.startswith("End time:"):
                        parts = line.strip().split(" ")
                        end_time = datetime.strptime(parts[2] + " " + parts[3], '%Y-%m-%d %H:%M:%S')
                if start_time and end_time:
                    duration = (end_time - start_time).total_seconds() / 3600  # Convert seconds to hours
                    data.append((start_time.date(), duration))
    return data

def summarize_daily_durations(data):
    df = pd.DataFrame(data, columns=['date', 'duration'])
    daily_summary = df.groupby('date')['duration'].sum()
    daily_summary_hours = daily_summary.round(3)  # Round to three decimal places
    daily_summary_hms = daily_summary.apply(lambda x: str(timedelta(hours=x)))
    summary_df = pd.DataFrame({
        'Date': daily_summary.index,
        'Total Duration (hours)': daily_summary_hours,
        'Total Duration (H:M:S)': daily_summary_hms
    })
    summary_df.to_markdown('./log/0summary.md', index=False)
    return summary_df

def visualize_time_data(daily_summary):
    daily_summary.set_index('Date')['Total Duration (hours)'].plot(kind='bar')
    plt.xlabel('Date')
    plt.ylabel('Total Duration (hours)')
    plt.title('Total Duration by Day')
    plt.show()

if __name__ == "__main__":
    log_directory = './log/'
    data = read_log_files(log_directory)
    daily_summary = summarize_daily_durations(data)
    visualize_time_data(daily_summary)
