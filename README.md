# Bernkastel
Personal Discord Bot

`main2.py` is the set-version of AMQ
`main.py` is the normal-version of AMQ

You would need a local postgres instance to run this bot. I forgot the specifics, but have 4 tables under a database (name configured in bot config):

main_scoresheet: Tracks the scores for the particular question. Resets for each question
question_scoresheet: Tracks the scores for the entire session. Resets for each session
logs: Logs everything
set_scoresheet: Tracks the scores for a particular set (main2.py)



# Example AMQ json:

This has to be on the same path as main2.py

```
{
"AMQ": [
    {
        "name": "Q1",
        "options": [
            "Nisemonogatari",
            "Nisekoi",
            "Horimiya",
            "Shoujo Kageki Revue Starlight",
            "K-On"
        ],
        "answer": 1
    }
]}

```

# bot_config.ini

Path: src/bot_config.ini

[secret]
token = <INSERT_BOT_TOKEN>
log_ch = <CHANNEL_ID_TO_DEBUG> (this is optional)

[postgres]
host=localhost
database=<LOCAL_DATABASE_PASSWORD>
user=postgres
password=<DATABASE_PASSWORD>