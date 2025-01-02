import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.backends.backend_pdf import PdfPages

# Read the CSV file
df = pd.read_csv('results/metrics.csv')

# Create a PDF file
with PdfPages('metrics_report.pdf') as pdf:
    # Group the data by the 'model' column
    grouped = df.groupby('model')

    for model, group in grouped:
        # Create a figure and axis
        fig, ax = plt.subplots(figsize=(8.27, 11.69))  # A4 size in inches

        # Hide the axes
        ax.axis('tight')
        ax.axis('off')

        # Create the table
        table = ax.table(cellText=group.values, colLabels=group.columns, cellLoc='center', loc='center')

        # Adjust the table properties
        table.auto_set_font_size(False)
        table.set_fontsize(8)
        table.scale(1.2, 1.2)

        # Add a title for the table
        ax.set_title(f'Model: {model}', fontsize=12, pad=20)

        # Save the figure to the PDF
        pdf.savefig(fig, bbox_inches='tight')

        # Close the figure
        plt.close(fig)