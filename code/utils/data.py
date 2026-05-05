from huggingface_hub import login, upload_folder, snapshot_download
from config import HF_TOKEN

def upload_data():
    login()
    # Push your dataset files
    upload_folder(folder_path="./data", repo_id="prathmesh796/supportAgent.ai", repo_type="dataset")

def download_data():
    # Download your dataset files
    local_path = snapshot_download(
        repo_id="prathmesh796/supportAgent.ai",
        repo_type="dataset",              
        local_dir="./data",  
        token=HF_TOKEN
    )
    print(local_path)