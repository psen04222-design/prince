import subprocess
import re

def get_saved_wifi_passwords():
    print(f"{'SSID Name':<30} | {'Password':<30}")
    print("-" * 65)

    try:
        # Run command to get all saved profiles
        meta_data = subprocess.check_output(['netsh', 'wlan', 'show', 'profiles']).decode('utf-8', errors="backslashreplace")
        data = meta_data.split('\n')
        
        # Extract profile names
        profiles = [i.split(":")[1][1:-1].strip() for i in data if "All User Profile" in i]

        for profile in profiles:
            try:
                # Run command to show profile details including the clear text key
                results = subprocess.check_output(['netsh', 'wlan', 'show', 'profile', profile, 'key=clear']).decode('utf-8', errors="backslashreplace")
                results_data = results.split('\n')
                
                # Extract the key content (password)
                password_lines = [b.split(":")[1][1:-1].strip() for b in results_data if "Key Content" in b]
                
                if password_lines:
                    wifi_password = password_lines[0]
                else:
                    wifi_password = "None / Open Network"
                
                print(f"{profile:<30} | {wifi_password:<30}")
                
            except subprocess.CalledProcessError:
                print(f"{profile:<30} | {'ENCODING ERROR / RESTRICTED':<30}")
                
    except Exception as e:
        print(f"An error occurred: {e}")

if __name__ == "__main__":
    get_saved_wifi_passwords()