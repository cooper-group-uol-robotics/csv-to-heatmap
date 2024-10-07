import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import os


def plot_heatmap_from_csv(csv_file, fill_value=None):
    # Read the CSV file into a DataFrame
    df = pd.read_csv(csv_file)

    # Handle missing score values
    if fill_value is not None:
        df['Score'].fillna(fill_value, inplace=True)  # Fill missing scores with the specified value
    else:
        df.dropna(subset=['Score'], inplace=True)  # Drop rows where 'score' is NaN

    # Group by 'Well' and get the maximum score for each well, rounding to nearest whole number
    df_max = df.groupby('Well', as_index=False)['Score'].max().round()

    # Extract row and column information from well labels
    df_max['row'] = df_max['Well'].str.extract('([A-H])')[0]
    df_max['column'] = df_max['Well'].str.extract('(\d+)')[0].astype(int)

    # Pivot the DataFrame for the 96-well format
    pivot_table = df_max.pivot(index='row', columns='column', values='Score')

    # Set the correct order for rows (A to H) and columns (1 to 12)
    pivot_table = pivot_table.reindex(index=['A', 'B', 'C', 'D', 'E', 'F',],
                                      columns=range(1, 13))

    # Extract the title from the CSV file name (without extension)
    title = os.path.splitext(os.path.basename(csv_file))[0]

    # Create the heatmap with adjusted scale
    plt.figure(figsize=(10, 8))
    ax = sns.heatmap(pivot_table, annot=True, fmt=".0f", cmap='flare',
                     cbar_kws={'label': 'Score', 'ticks': [1.0, 2.0, 3.0, 4.0]},
                     vmin=1.0, vmax=4.0,
                     annot_kws={'size': 12})  # Change this value to adjust annotation size

    # Move the column labels to the top
    ax.xaxis.set_ticks_position('top')
    ax.xaxis.set_label_position('top')

    # Adjust colorbar label size using set_ylabel method
    cbar = ax.collections[0].colorbar
    cbar.ax.set_ylabel('Score', fontsize=14)  # Set colorbar label size

    plt.title(f'Heatmap for {title}', fontsize=14, pad=20)  # Increase pad to move title up
    plt.xlabel('Column', fontsize=14, labelpad=15)  # Increase labelpad for x-axis
    plt.ylabel('Row', fontsize=14, labelpad=15)  # Increase labelpad for y-axis
    plt.xticks(rotation=0, fontsize=12)  # Change x-tick font size
    plt.yticks(rotation=0, fontsize=12)  # Change y-tick font size

    # Adjust layout to prevent title cut-off
    plt.tight_layout()

    # Save the heatmap to a file in the same directory as the CSV file
    output_file_path = os.path.join(os.path.dirname(csv_file), f'{title}.png')
    plt.savefig(output_file_path)  # Save the figure
    plt.close()  # Close the plot to free memory


def plot_heatmaps_in_directory(fill_value=None):
    # Use the directory where the .csv files are saved
    directory = "C:/Users/sgcshiel/Documents/Project_work/Crystal plates/csvs_to_convert"

    # Walk through the directory and process each CSV file
    for root, _, files in os.walk(directory):
        for file in files:
            if file.endswith('.csv'):
                csv_file_path = os.path.join(root, file)
                print(f'Processing {csv_file_path}...')
                plot_heatmap_from_csv(csv_file_path, fill_value)


# Example usage
plot_heatmaps_in_directory()