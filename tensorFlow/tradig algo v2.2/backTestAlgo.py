import tradingAlgo.main as tradingAlgo
import marketSim as ms
import os
import pandas as pd
import time
import matplotlib.pyplot as plt
import matplotlib.animation as animation

timings = True

# Function to initialize and run the backtesting
def runBackTesting():
    myPortfolio = ms.Portfolio()  # Initialize the portfolio
    fileList = os.listdir('nasdaq100')  # Folder to generate test data from
    dirDfArr = []

    for file in fileList:
        dirDfArr.append([file, pd.read_csv(f'nasdaq100/{file}')])

    # Only read the directory once to optimize speed
    count = 1
    x_data, y_data = [], []  # Data for the plot (x: iteration, y: earnings)

    # Create the figure and axis for plotting
    fig, ax = plt.subplots()

    # Function to animate the plot during each iteration
    def animate(i):
        nonlocal count  # Ensure the count variable is updated within the animation function

        # Update the backtesting data
        for attr in dirDfArr:
            fileName = attr[0]
            df = attr[1]
            newdf = df.iloc[-(20 + count):-count]  # Get the slice of data for backtesting
            newdf.to_csv(f'backtestingData/{fileName}')  # Save the sliced data

        # Run the trading algorithm
        if timings:
            start = time.time()
        tradingAlgo.main(myPortfolio)  # Call the trading algorithm
        if timings:
            print(f'main finished in: \t{round(time.time()-start,3)}s\t|')
            print('+-------------------------------+')
        
                # Track portfolio earnings
        earnings = myPortfolio.getTotalEarnings()  # Get current earnings
        x_data.append(count)  # Append the iteration number to x_data
        y_data.append((earnings/100000)*100)  # Append the earnings to y_data

        # Clear the previous plot and replot
        ax.clear()
        ax.plot(x_data, y_data, label="Portfolio Earnings", color="blue")
        ax.set_title("Portfolio Earnings Over Time")
        ax.set_xlabel("Iteration")
        ax.set_ylabel("Earnings as pct of initial wallet value")
        ax.legend()

        count += 1

    # Create the animation
    ani = animation.FuncAnimation(fig, animate, interval=1000)  # Update every second

    # Show the plot
    plt.show()

if __name__ == '__main__':
    runBackTesting()


