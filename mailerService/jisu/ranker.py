import pandas as pd
import glob
import os
from datetime import datetime

folder = "progress"
all_files = sorted(glob.glob(os.path.join(folder, "*.csv")))

# Extract date like: "JIS University - Kolkata, India [21 Nov].csv"
def extract_date(filename):
    base = os.path.basename(filename)
    start = base.find("[") + 1
    end = base.find("]")
    date_str = base[start:end]   # e.g., "21 Nov"

    # Parse without year → assume year 2025
    parsed = datetime.strptime(date_str, "%d %b")
    parsed = parsed.replace(year=2025)

    return parsed

data = {}

for file in all_files:
    day = extract_date(file)
    df = pd.read_csv(file)

    for _, row in df.iterrows():
        email = row["User Email"].strip().lower()

        if email not in data:
            data[email] = {
                "name": row["User Name"],
                "badges": {},
                "games": {},
            }

        # Skill badges - split by pipe (|) not comma
        sb_raw = row["Names of Completed Skill Badges"]
        if isinstance(sb_raw, str) and sb_raw.strip():
            for b in sb_raw.split("|"):
                badge = b.strip()
                if badge and badge not in data[email]["badges"]:
                    data[email]["badges"][badge] = day

        # Arcade games - split by pipe (|) not comma
        ag_raw = row["Names of Completed Arcade Games"]
        if isinstance(ag_raw, str) and ag_raw.strip():
            for g in ag_raw.split("|"):
                game = g.strip()
                if game and game not in data[email]["games"]:
                    data[email]["games"][game] = day


# Build final ranking table
rows = []
for email, info in data.items():
    all_dates = list(info["badges"].values()) + list(info["games"].values())
    finish_date = max(all_dates) if all_dates else None

    rows.append({
        "User Name": info["name"],
        "User Email": email,
        "Google Cloud Skills Boost Profile URL": "",
        "Profile URL Status": "All Good",
        "Access Code Redemption Status": "Yes" if len(info["badges"]) > 0 or len(info["games"]) > 0 else "No",
        "All Skill Badges & Games Completed": "Yes" if (len(info["badges"]) > 0 and len(info["games"]) > 0) else "No",
        "# of Skill Badges Completed": len(info["badges"]),
        "Names of Completed Skill Badges": " | ".join(info["badges"].keys()),
        "# of Arcade Games Completed": len(info["games"]),
        "Names of Completed Arcade Games": " | ".join(info["games"].keys()),
    })

df_final = pd.DataFrame(rows)

# Sort by: Total Skill Badges (desc) → Total Arcade Games (desc) → Name (asc)
df_final = df_final.sort_values(
    by=["# of Skill Badges Completed", "# of Arcade Games Completed", "User Name"],
    ascending=[False, False, True]
)

df_final.to_csv("final_ranking.csv", index=False)
print("final_ranking.csv generated successfully!")