from pydrive.auth import GoogleAuth
from pydrive.drive import GoogleDrive
import os
def sanitize_folder_name(name):
    """ Replace invalid characters in folder names with hyphens. """
    return name.replace('/', '-')

def download_folder(drive, folder_id, local_path):
    # Ensure local folder exists
    os.makedirs(local_path, exist_ok=True)

    # List all files/folders in the Google Drive folder
    query = f"'{folder_id}' in parents and trashed=false"
    file_list = drive.ListFile({'q': query}).GetList()

    for file in file_list:
        # Sanitize folder name to avoid issues with file paths
        safe_title = sanitize_folder_name(file['title'])

        # Download file if item is a file, recurse if item is a folder
        if file['mimeType'] == 'application/vnd.google-apps.folder':  # It's a folder
            print(f"Entering folder: {safe_title}")
            # Recursively download this folder
            download_folder(drive, file['id'], os.path.join(local_path, safe_title))
        else:  # It's a file
            print(f"Downloading file: {safe_title} to {local_path}")
            file.GetContentFile(os.path.join(local_path, safe_title))

# Authenticate and create the PyDrive client
gauth = GoogleAuth()
gauth.DEFAULT_SETTINGS['client_config_file'] = os.path.join('util', 'client_secrets.json')
gauth.LoadCredentialsFile(os.path.join('util', 'credentials.json'))
if gauth.credentials is None:
    # Authenticate if they're not there
    gauth.LocalWebserverAuth()
elif gauth.access_token_expired:
    # Refresh them if expired
    gauth.Refresh()
else:
    # Initialize the saved creds
    gauth.Authorize()

# Save the current credentials to a file
gauth.SaveCredentialsFile(os.path.join('util', 'credentials.json'))

drive = GoogleDrive(gauth)


# Your Google Drive folder ID
folder_id = '1gD65FUaLWg-m_CV6cjY-jikDWE2CCMxb'

# Local directory to download the files
local_download_path = './MedicalRecord'

# Start the recursive download
download_folder(drive, folder_id, local_download_path)

print("All files and folders have been downloaded successfully.")