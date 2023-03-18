# BGNSSIW
A Discord bot for logging message edits and deletions.

You will need to:
    - Create an app in the Discord developer portal
    - Generate a bot user
    - Enable the correct intents
    - Generate the invite URL
    - Invite the bot to your server
    - Add it to the @admin role.
    - Define the required variables in config/config.py

v2.0 ChangeLog 2023.03.18:
    - Variables in config/config.py are MANDATORY and this bot will not run without them!
    - Implemented slash commands!
        - Logging can be paused using /logpause or resumed using /logrun
            Note: by default, logging will be enabled on start. To change
                  this, default logging variable can be changed from True
                  to False in log.py(26)
        - Bot now supports excluding users from logging
            - These are stored by numeric user ID. As such, changes to diplay
              names will not affect this configuration
