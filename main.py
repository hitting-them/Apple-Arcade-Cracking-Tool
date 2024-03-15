import os
import glob
import shutil
import zipfile
import plistlib
import tempfile

def remove_nsapp_keys(info_plist_path):
    with open(info_plist_path, "rb") as plist_file:
        plist_data = plist_file.read()
        info_plist = plistlib.loads(plist_data)
    
    keys_to_remove = [key for key in info_plist.keys() if key.startswith("NSApp")]
    for key in keys_to_remove:
        del info_plist[key]

    with open(info_plist_path, "wb") as plist_file:
        plistlib.dump(info_plist, plist_file)

def apply_crack(ipa_file):
    with tempfile.TemporaryDirectory() as temp_dir:
        extract_dir = os.path.join(temp_dir, "extracted_ipa")
        os.makedirs(extract_dir, exist_ok=True)
        with zipfile.ZipFile(ipa_file, "r") as ipa_zip:
            ipa_zip.extractall(extract_dir)

        payload_dir = os.path.join(extract_dir, "Payload")
        app_dirs = glob.glob(os.path.join(payload_dir, "*.app"))
        for app_dir in app_dirs:
            info_plist_path = os.path.join(app_dir, "Info.plist")
            remove_nsapp_keys(info_plist_path)

        with zipfile.ZipFile(ipa_file, "w", compression=zipfile.ZIP_DEFLATED, compresslevel=3) as ipa_zip:
            for root, dirs, files in os.walk(extract_dir):
                for file in files:
                    file_path = os.path.join(root, file)
                    relative_path = os.path.relpath(file_path, extract_dir)
                    ipa_zip.write(file_path, relative_path)
        
        cracked_ipa_path = os.path.join("cracked", os.path.basename(ipa_file))
        shutil.move(ipa_file, cracked_ipa_path)


def main():
    os.makedirs("games", exist_ok=True)
    os.makedirs("cracked", exist_ok=True)
    
    for ipa_path in glob.glob("games\\*.ipa"):
        apply_crack(ipa_path)

if __name__ == "__main__":
    main()
