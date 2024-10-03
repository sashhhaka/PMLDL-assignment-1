import pandas as pd
import sys
from sklearn.model_selection import train_test_split


def load_data(file_path):
    """Load the data from a CSV file."""
    return pd.read_csv(file_path)


def clean_data(file_path, output_file):
    """Clean the data by handling missing values and removing outliers for each column."""
    df = load_data(file_path)

    # Handle missing values
    df = df.dropna()

    # Define a function to remove outliers from a Series
    def remove_outliers(series):
        if series.dtype in ['int64', 'float64']:  # Only process numeric columns
            lower_bound = series.quantile(0.05)
            upper_bound = series.quantile(0.95)
            return series[(series >= lower_bound) & (series <= upper_bound)]
        return series  # Return unchanged for non-numeric columns

    # Apply the remove_outliers function to each column
    cleaned_df = df.apply(remove_outliers)

    # Drop any remaining NaNs
    cleaned_df = cleaned_df.dropna()

    # Save the cleaned DataFrame to a CSV file
    cleaned_df.to_csv(output_file, index=False)
    print(f"Cleaned data saved to {output_file}")


def split_and_save_data(file_path, train_file_path, test_file_path, test_size=0.2, random_state=42):
    """
    Split the data into training and testing datasets and save them to CSV files.

    Parameters:
    - file_path: File path to load the data from.
    - train_file_path: File path to save the training data.
    - test_file_path: File path to save the testing data.
    - test_size: Proportion of the dataset to include in the test split (default: 0.2).
    - random_state: Random seed for reproducibility (default: 42).
    """
    df = load_data(file_path)

    # Split the data
    train_df, test_df = train_test_split(df, test_size=test_size, random_state=random_state)

    # Save the training DataFrame to a CSV file
    train_df.to_csv(train_file_path, index=False)

    # Save the testing DataFrame to a CSV file
    test_df.to_csv(test_file_path, index=False)

    print(f"Training data saved to {train_file_path}")
    print(f"Testing data saved to {test_file_path}")


def main(operation, input_file, output_file=None, output_train=None, output_test=None):
    """Main function to handle command line operations."""
    if operation == "load":
        df = load_data(input_file)
        print(df.head())
    elif operation == "clean":
        clean_data(input_file, output_file)
    elif operation == "split_and_save":
        split_and_save_data(input_file, output_train, output_test)
    else:
        print("Invalid operation. Choose from: load, clean, split_and_save.")


if __name__ == "__main__":
    # Pass the command line arguments to the main function
    main(*sys.argv[1:])
