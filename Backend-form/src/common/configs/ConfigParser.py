import yaml
from pathlib import Path


# from django.conf import settings

CONFIG_DIR = Path(__file__).resolve()


class ConfigParser:
    def __init__(self, config_path=None):
        self.config_path = config_path
        self.settings_environ = "develop"  # settings.ENVIRON

    def load(self, envs=None, *, get_all=False):
        if not self.config_path:
            raise ValueError("config_path is required")

        path = "/".join(self.config_path.split(".")) + ".yml"
        filepath = CONFIG_DIR.parent / path
        try:
            with open(filepath, "r") as file:
                base_data = yaml.safe_load(file)

            settings = {}

            if envs:
                if isinstance(envs, str):
                    obj = {envs: base_data.get(envs)}
                    return obj

                for env in envs:
                    settings.update({env: base_data[env]})
            else:
                if get_all:
                    settings = base_data
                else:
                    settings.update(
                        {self.settings_environ: base_data[self.settings_environ]}
                    )

            return settings

        except Exception as e:
            return {"error": str(e), "setting": self.settings_environ}


if __name__ == "__main__":
    import json

    parser = ConfigParser(config_path="settings.ntfy")
    data = parser.load(envs="develop")
    # data = parser.load()

    print(json.dumps(data, indent=4))

    # parser = ConfigParser(config_path="settings.database_settings")
    # data = parser.load(envs="dummy")
    # # data = parser.load()

    # print(json.dumps(data, indent=4))
