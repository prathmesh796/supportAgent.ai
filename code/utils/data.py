from huggingface_hub import login, upload_folder, snapshot_download
import os

token = os.getenv("HF_TOKEN")

def upload_data():
    login(token=token)
    # Push your dataset files
    upload_folder(folder_path="./data", repo_id="prathmesh796/supportAgent.ai", repo_type="dataset")

def download_data():
    # Download your dataset files

    local_path = snapshot_download(
        repo_id="prathmesh796/supportAgent.ai",
        repo_type="dataset",              
        local_dir="./data",  
        token=token
    )
    print(local_path)