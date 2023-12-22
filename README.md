# dromomania

> Non-clinical description of a desire for frequent traveling or walking 

## Archicture
3 main components:
* core - core for handling database updates (triggered by agents) and inform user (by client)
* agents - works for scraping data. Every site has its own scrapper
* tbot - interface for interacting with service by user - by telegram bot
