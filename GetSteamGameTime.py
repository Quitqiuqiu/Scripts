import requests
import pandas as pd

# 你的 Steam API Key 和 Steam64 ID（需要手动替换）
STEAM_API_KEY = "4A103211AC1E894B0E50B76709043734"
STEAM_ID = "76561199085956364"

# 获取游戏游玩时长的 API URL
URL = f"http://api.steampowered.com/IPlayerService/GetOwnedGames/v0001/?key={STEAM_API_KEY}&steamid={STEAM_ID}&format=json&include_appinfo=true"

# 发送请求获取数据
response = requests.get(URL)
data = response.json()

# 解析游戏数据
games = data["response"].get("games", [])

# 过滤掉游玩时长为 0 的游戏，并整理数据
game_list = [
    {"Game Name": game["name"], "Playtime (hours)": round(game["playtime_forever"] / 60, 2)}
    for game in games if game["playtime_forever"] > 0
]

# 按游玩时长降序排序
df = pd.DataFrame(game_list).sort_values(by="Playtime (hours)", ascending=False)

# 保存为 CSV 文件
csv_filename = "C:/Users/Qiu/Desktop/steam_playtime.csv"
df.to_csv(csv_filename, index=False, encoding="utf-8-sig")

print(f"数据已保存为 {csv_filename}")