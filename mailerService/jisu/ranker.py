import pandas as pd
import glob
import os
from datetime import datetime

final_df = pd.read_csv("final_gnit.csv")

eligible_emails = {
    row["User Email"].strip().lower(): row
    for _, row in final_df.iterrows()
    if str(row["All Skill Badges & Games Completed"]).strip().lower() == "yes"
}

print(f"Eligible participants: {len(eligible_emails)}")

folder = "progress/jisu_progress"
all_files = sorted(glob.glob(os.path.join(folder, "*.csv")))

def extract_date(filename):
    base = os.path.basename(filename)
    start = base.find("[") + 1
    end = base.find("]")
    date_str = base[start:end]   

    parsed = datetime.strptime(date_str, "%d %b")
    parsed = parsed.replace(year=2025)

    return parsed

progress_data = {}

for file in all_files:
    day = extract_date(file)
    df = pd.read_csv(file)

    for _, row in df.iterrows():
        email = row["User Email"].strip().lower()
        if email not in eligible_emails:
            continue

        if email not in progress_data:
            progress_data[email] = {
                "badges": {},
                "games": {}
            }

        # Split with "|" not comma
        sb_raw = row["Names of Completed Skill Badges"]
        if isinstance(sb_raw, str) and sb_raw.strip():
            for b in sb_raw.split("|"):
                badge = b.strip()
                if badge and badge not in progress_data[email]["badges"]:
                    progress_data[email]["badges"][badge] = day

        ag_raw = row["Names of Completed Arcade Games"]
        if isinstance(ag_raw, str) and ag_raw.strip():
            for g in ag_raw.split("|"):
                game = g.strip()
                if game and game not in progress_data[email]["games"]:
                    progress_data[email]["games"][game] = day


ranking_rows = []

for email, final_row in eligible_emails.items():

    badges = progress_data.get(email, {}).get("badges", {})
    games = progress_data.get(email, {}).get("games", {})

    all_dates = list(badges.values()) + list(games.values())
    finish_date = max(all_dates) if all_dates else datetime(2025, 12, 31)

    ranking_rows.append({
        "finish_date": finish_date,
        "row": final_row  
    })

ranking_rows.sort(key=lambda x: x["finish_date"])

top50 = ranking_rows[:54]


output_rows = []
for entry in top50:
    r = entry["row"]

    output_rows.append({
        "User Name": r["User Name"],
        "User Email": r["User Email"],
        "Google Cloud Skills Boost Profile URL": r["Google Cloud Skills Boost Profile URL"],
        "Profile URL Status": r["Profile URL Status"],
        "Access Code Redemption Status": r["Access Code Redemption Status"],
        "All Skill Badges & Games Completed": r["All Skill Badges & Games Completed"],
        "# of Skill Badges Completed": r["# of Skill Badges Completed"],
        "Names of Completed Skill Badges": r["Names of Completed Skill Badges"],
        "# of Arcade Games Completed": r["# of Arcade Games Completed"],
        "Names of Completed Arcade Games": r["Names of Completed Arcade Games"],
    })

out_df = pd.DataFrame(output_rows)
out_df.to_csv("top_54_jisu.csv", index=False)

print("top_54_jisu.csv generated successfully!")