import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import os
import logging

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(levelname)s: %(message)s')

def calculate_score_percentage(df):
    """Calculates the percentage of each score in the DataFrame."""
    score_counts = df['score'].value_counts(normalize=True) * 100
    return score_counts

def plot_heatmap_from_csv(csv_file, fill_value=None, font_type='Arial', font_size=22, cmap='flare'):
    try:
        # Read the CSV file into a DataFrame
        df = pd.read_csv(csv_file)

        # Normalize column names to lowercase
        df.columns = df.columns.str.lower()

        # Validate the presence of required columns
        if 'well' not in df.columns or 'score' not in df.columns:
            logging.error(f"Missing 'well' or 'score' column in {csv_file}.")
            return

        # Handle missing score values
        if fill_value is not None:
            df['score'].fillna(fill_value, inplace=True)  # Fill missing scores
        else:
            df.dropna(subset=['score'], inplace=True)  # Drop rows where 'score' is NaN

        # Group by 'well' and get the maximum score
        df_max = df.groupby('well', as_index=False)['score'].max().round()

        # Extract row and column information from well labels
        df_max['row'] = df_max['well'].str.extract('([A-H])')[0]
        df_max['column'] = df_max['well'].str.extract('(\d+)')[0].astype(int)

        # Pivot the DataFrame for the 96-well format
        pivot_table = df_max.pivot(index='row', columns='column', values='score')

        # Drop rows and columns that are completely empty
        pivot_table = pivot_table.dropna(how='all').dropna(axis=1, how='all')

        # Set the correct order for rows and columns
        pivot_table = pivot_table.reindex(index=['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H'],
                                          columns=range(1, 13), fill_value=None)

        # Check if the pivot table has any data before plotting
        if pivot_table.empty:
            logging.warning(f'No data available to plot for {csv_file}.')
            return

        # Calculate the percentage of each score
        score_percentage = calculate_score_percentage(df_max)
        logging.info(f"Score percentage for {csv_file}:")
        logging.info(score_percentage)

        # Extract the title from the CSV file name
        title = os.path.splitext(os.path.basename(csv_file))[0]

        # Create the heatmap with wider aspect ratio
        plt.figure(figsize=(13.5, 8))  # Adjusted figsize for wider output
        ax = sns.heatmap(pivot_table, annot=True, fmt=".0f", cmap=cmap,
                         cbar_kws={'label': 'Score', 'ticks': [0.0, 1.0, 2.0, 3.0,]},
                         vmin=0.0, vmax=4.0,
                         annot_kws={'size': font_size})

        # Move the column labels to the top
        ax.xaxis.set_ticks_position('top')
        ax.xaxis.set_label_position('top')

        # Adjust colorbar label size
        cbar = ax.collections[0].colorbar
        cbar.ax.set_ylabel('Score', fontsize=font_size)

        plt.title(f'Heatmap for {title}', fontsize=font_size, pad=20)
        plt.xlabel('Column', fontsize=font_size, labelpad=15)
        plt.ylabel('Row', fontsize=font_size, labelpad=15)
        plt.xticks(rotation=0, fontsize=font_size)
        plt.yticks(rotation=0, fontsize=font_size)

        # Set font type
        plt.rc('font', family=font_type)

        plt.tight_layout()

        # Save the heatmap
        output_file_path = os.path.join(os.path.dirname(csv_file), f'{title}.png')
        plt.savefig(output_file_path, dpi=500)
        plt.close()
        logging.info(f'Saved heatmap to {output_file_path}')
    
    except Exception as e:
        logging.error(f"Error processing {csv_file}: {e}")

def plot_heatmaps_in_directory(fill_value=None, font_type='Arial', font_size=22, cmap='flare'):
    directory = "" # add directory path

    # Walk through the directory and process each CSV file
    for root, _, files in os.walk(directory):
        for file in files:
            if file.endswith('.csv'):
                csv_file_path = os.path.join(root, file)
                logging.info(f'Processing {csv_file_path}...')
                plot_heatmap_from_csv(csv_file_path, fill_value, font_type, font_size, cmap)

# Example usage
plot_heatmaps_in_directory(font_type='Arial', font_size=22, cmap='flare')


# Example usage
plot_heatmaps_in_directory()
