import streamlit as st
from src.data_loader import load_matches

# ============================================================
# APP TITLE
# ============================================================

st.title("Esferico ⚽️ — EPL Analytics Tutor")

# ============================================================
# LOAD DATA
# ============================================================

df = load_matches()

# ============================================================
# TEAM SELECTION
# ============================================================

st.write("Rows, Columns:", df.shape)
st.dataframe(df.head(10))
show_raw = st.checkbox("Show raw data")
if show_raw:
    st.dataframe(df)

# Get all unique teams from home and away columns
teams = sorted(set(df["HomeTeam"]).union(set(df["AwayTeam"])))

# Dropdown selector
selected_team = st.selectbox("Select a Team", teams)

st.write("You selected:", selected_team)

# ============================================================
# TEAM MATCH FILTERING
# ============================================================

# Filter matches where selected team played
team_matches = df[
    (df["HomeTeam"] == selected_team) |
    (df["AwayTeam"] == selected_team)
]

col1, col2, col3 = st.columns(3)

st.dataframe(team_matches)
#st.write("Total Matches:", len(team_matches))
col1.metric("Matches", len(team_matches))

# goals scored, home and away
home_goals = team_matches[team_matches["HomeTeam"] == selected_team]["FTHG"].sum()
away_goals = team_matches[team_matches["AwayTeam"] == selected_team]["FTAG"].sum()

goals_scored = home_goals + away_goals

#st.write("Goals Scored:", goals_scored)
col2.metric("Goals Scored", goals_scored)


# goals conceded, home and away
home_conceded = team_matches[team_matches["HomeTeam"] == selected_team]["FTAG"].sum()
away_conceded = team_matches[team_matches["AwayTeam"] == selected_team]["FTHG"].sum()

goals_conceded = home_conceded + away_conceded

#st.write("Goals Conceded:", goals_conceded)
col3.metric("Goals Conceded:", goals_conceded)

# ============================================================
# LAST 5 MATCHES
# ============================================================

# Sort by date (most recent last in dataset, so we sort descending)
team_matches_sorted = team_matches.sort_values("Date", ascending=False)

# Select last 5 matches

last_5 = team_matches_sorted.head(5)

st.subheader("Last 5 Matches")
st.dataframe(last_5[["Date", "HomeTeam", "AwayTeam", "FTHG", "FTAG", "FTR"]])

# ============================================================
# LAST 5 PERFORMANCE METRICS
# ============================================================

points = 0
goals_scored = 0
goals_conceded = 0

for _, row in last_5.iterrows():

    # Determine if team was home or away
    if row["HomeTeam"] == selected_team:
        goals_scored += row["FTHG"]
        goals_conceded += row["FTAG"]

        if row["FTR"] == "H":
            points += 3
        elif row["FTR"] == "D":
            points += 1

    else:
        goals_scored += row["FTAG"]
        goals_conceded += row["FTHG"]

        if row["FTR"] == "A":
            points += 3
        elif row["FTR"] == "D":
            points += 1

st.subheader("Last 5 Summary")
st.write("Points:", points)
st.write("Goals Scored:", goals_scored)
st.write("Goals Conceded:", goals_conceded)

# ============================================================
# FORM
# ============================================================

form = []
for _, row in last_5.iterrows():
    ftr = row["FTR"]

    if ftr == "D":
        form.append("D")

    elif ftr == "H":
        # Home team won
        form.append("W" if row["HomeTeam"] == selected_team else "L")

    elif ftr == "A":
        # Away team won
        form.append("W" if row["AwayTeam"] == selected_team else "L")

    else:
        form.append("?")

form_string = " ".join(form[:: -1])
# st.write("Form:", form_string)
form_string = " ".join(form)
st.markdown(f"**Form:** `{form_string}`")