import urllib.request
import os

def download_dataset():
    # Official UCI Repository URL for the Excel version of the dataset
    url = "https://archive.ics.uci.edu/ml/machine-learning-databases/00350/default%20of%20credit%20card%20clients.xls"
    dest_dir = "data/raw"
    dest_path = os.path.join(dest_dir, "default of credit card clients.xls")
    
    # Ensure the directory exists
    os.makedirs(dest_dir, exist_ok=True)
    
    print(f"Downloading dataset from UCI Machine Learning Repository...")
    print(f"Source URL: {url}")
    print(f"Destination: {dest_path}")
    
    try:
        # Download the file
        urllib.request.urlretrieve(url, dest_path)
        print("Download completed successfully!")
        
        # Verify file size
        file_size = os.path.getsize(dest_path)
        print(f"File size: {file_size / (1024 * 1024):.2f} MB")
        
    except Exception as e:
        print(f"Error downloading dataset: {e}")
        print("Please check your internet connection or try downloading the file manually.")

if __name__ == "__main__":
    download_dataset()
