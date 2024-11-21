import os
import matplotlib.pyplot as plt
from datetime import datetime, timedelta
import pandas as pd
import warnings

def ignore_warnings():
    warnings.filterwarnings("ignore")

ignore_warnings()

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
    daily_summary_hours = daily_summary.round(1)  # Round to one decimal place
    daily_summary_hms = daily_summary.apply(lambda x: str(timedelta(hours=x)))
    summary_df = pd.DataFrame({
        'Date': daily_summary.index,
        'Total Duration (hours)': daily_summary_hours,
        'Total Duration (H:M:S)': daily_summary_hms,
        'Percentage': daily_summary_hours  # Calculate percentage
    })
    summary_df.to_markdown('./log/0summary.md', index=False)
    
    # Calculate global total duration
    global_total_duration = daily_summary.sum()
    
    return summary_df, global_total_duration

def visualize_time_data(daily_summary, global_total_duration):
    ax = daily_summary.set_index('Date')['Total Duration (hours)'].plot(kind='bar')
    for i, v in enumerate(daily_summary['Percentage']):
        ax.text(i, daily_summary['Total Duration (hours)'][i] + 0.1, f"{v}", ha='center')
    
    # Calculate the second column of the title
    start_date = datetime(2024, 7, 7)
    end_date = datetime(2029, 7, 7)
    current_date = datetime.now()
    total_days = (end_date - start_date).days
    elapsed_days = (current_date - start_date).days
    percentage_time = (elapsed_days / total_days) * 100
    
    plt.xlabel('Date')
    plt.ylabel('Total Duration (hours)')
    plt.title(f'Process of becoming a master: {global_total_duration*100 / 10000:.2f}% \n Time Progress: {percentage_time:.2f}%')
    plt.show()

if __name__ == "__main__":
    log_directory = './log/'
    data = read_log_files(log_directory)
    daily_summary, global_total_duration = summarize_daily_durations(data)
    visualize_time_data(daily_summary, global_total_duration)