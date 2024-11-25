import pandas
import matplotlib.pyplot as plt
import matplotlib.dates as mdates

def plot_expenses_with_histogram(df, granularity='day'):
    users = df['name'].unique()
    fig, ax1 = plt.subplots(figsize=(12, 6))

    for user in users:
        user_data = df[df['name'] == user]
        ax1.plot(user_data['timestamp'], user_data['expense'], label=user, marker='o')

    ax1.xaxis.set_major_locator(mdates.DayLocator() if granularity == 'day' else mdates.MonthLocator())
    ax1.xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m-%d' if granularity == 'day' else '%Y-%m'))

    fig.autofmt_xdate()  

    ax1.set_xlabel(f"{granularity.capitalize()}s")
    ax1.set_ylabel("Expense Amount (Per User)")

    ax2 = ax1.twinx()  # Create a twin Axes sharing the x-axis
    total_expenses_per_day = df.groupby('timestamp')['expense'].sum().reset_index()
    

    bars = ax2.bar(total_expenses_per_day['timestamp'], total_expenses_per_day['expense'], 
                   alpha=0.2, color='gray', width=0.8)

    ax2.set_ylabel("Total Expenses (All Users)")

    for bar, total in zip(bars, total_expenses_per_day['expense']):
        ax2.text(bar.get_x() + bar.get_width() / 2, bar.get_height(), f'{total}', 
                 ha='center', va='bottom', fontsize=10, color='black')

    ax1.legend(loc='upper left')
    plt.title(f"Expenses ({granularity.capitalize()}wise) per User with Total Expenses")
    plt.show()

plot_expenses_with_histogram(df_daywise, granularity='day')
