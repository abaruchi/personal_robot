# Marvin Robot

This repo has the source code of a robot that helps me during the week. Some 
times I just want to know if it is better go to the office by car or subway, 
or just know the name of the current street (Im really bad to remember 
streets names) and if it is necessary to close my apartment windows (my cat 
doesnt like to be inside the house all day long..).
So, in order to help me with this small questions during my day, I 
implemented this robot that gets some information for me. 

For now, I have implemented following commands:

* `/metro` - Sends information about the Sao Paulo subway (metro)
* `/cptm` - Sends information about trains lines in Sao Paulo (cptm)
* `/weather` - Sends information about rain probability and weather summary
* `/gohome` - Check the distance and duration between home and work (master only)
* `/gowork` - Check the distance and duration between work and home (master (only)
* `/letsgo` - Start a small talk with Marvin to get distance and location from or
 to your location
* `/done` - Stops conversation with Marvin

If you want to have this robot working for you, first step is to get your 
robot from the BotFather (see below links). After getting all the tokens you 
need to create a file, called `config.ini` with the following content:

```
[Telegram]
Token: <Your Telegram API Token Here>

[GoogleMaps]
Token: <Your Google Developer API here>
Home: <House Address Here>
Work: <Your Work Address Here>


[Subway]
metro: https://direto-do-metro.appspot.com/dftm
cptm: https://direto-da-cptm.appspot.com/dftc

[Weather]
Token: <Your Weather API here - 
Home_coordinates: <lat and long of your house - comma separated>
Work_coordinates: <lat and long of your work - comma separated>
```

Anyway, if you want to use this robot, you can add it to your telegram 
contacts, his name is @Marvin. But let me aware you... hes is kind of rude.


# Tokens

## Telegram API
If you have never implemented a Telegram Bot, please, start reading this page
. It has the procedure to create the Token and all necessary steps to start 
coding your own bot.
* [How Do I Create a Bot](https://core.telegram.org/bots#3-how-do-i-create-a-bot)


## Google Developer API
Google has a very good API to be used by developers. This bot uses this API 
to get google traffic information. Please go to the following link to get 
your Token!
* [Google Developers API](https://console.developers.google.com/apis/)


## Weather API
Finally, to get data about weather I used the Dark Sky API. In order to use 
it, you should have a Token. Check the following link to receive the Token.

* [Dark Sky API](https://darksky.net/dev/)


# To DO
Well.. I know that the coding is not good yet. Probably in next months I'll 
be refactoring the code, and probably will change how some commands works. 
Also, I'll implement some kind of alerts.. (Working on it.. don't rush me.)

**Remember**.. this bot is open source, if you want to clone it or use it as code
 example to learn how to code a Telegram Bot.. Go Ahead!
 
 

