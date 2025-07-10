# load_affiliates.py
import json
from pathlib import Path

CONFIG_PATH = Path(__file__).parent / "../config/affiliate.json"

def load_affiliate_config():
    try:
        with open(CONFIG_PATH, "r") as f:
            config = json.load(f)
            return config
    except FileNotFoundError:
        print("❌ affiliate.json not found.")
        return {}
    except json.JSONDecodeError:
        print("❌ Error decoding affiliate.json.")
        return {}

def get_affiliate_id(network):
    config = load_affiliate_config()
    return config.get(network)

if __name__ == "__main__":
    config = load_affiliate_config()
    print("🔑 Loaded affiliate config:")
    print(json.dumps(config, indent=2))
