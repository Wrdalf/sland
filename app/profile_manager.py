import json

class ProfileManager:
    def __init__(self, file_path="config/profiles.json"):
        self.file_path = file_path
        self.profiles = self.load_profiles()

    def load_profiles(self):
        try:
            with open(self.file_path, "r", encoding="utf-8") as f:
                return json.load(f)
        except FileNotFoundError:
            return {}

    def save_profiles(self):
        with open(self.file_path, "w", encoding="utf-8") as f:
            json.dump(self.profiles, f, indent=4, ensure_ascii=False)

    def add_profile(self, name, api_key):
        self.profiles[name] = {"api_key": api_key}
        self.save_profiles()

    def delete_profile(self, name):
        if name in self.profiles:
            del self.profiles[name]
            self.save_profiles()
