# Game Development Dashboard

This was a weekend project to turn a Python Jupyter Notebook report into a proper data dashboard for design and balancing purposes for the development of [Bat Bots](https://store.steampowered.com/app/3099010/Bat_Bots/).

This dashboard seeks to surface insights on how players are playing Bat Bots and how best to balance some of our quantitative achievements (score thresholds, bat stun numbers and so on). All data collected was anonymized play data that helped us better identify how to improve the game during development. No further or new data is being collected.

## Architecture

The architecture for data capture is described in the diagram below. This is how we collected data during playtesting and early release.

<img width="1423" height="702" alt="image" src="https://github.com/user-attachments/assets/1223d235-9f15-4ff6-a723-fee57b886422" />


This dashboard is built using an MVC architecture approach; model classes match the records stored in the database, controller classes process instances of model classes to respond to requests that the Dashboard view generates.

## Features to come

Data is currently being displayed statically after processing JSON files from the Bat Bots database backups. There is further insight to be gained from being able to filter some of this data down. Adding these filters is the current next objective.
