# fb-message-bot
FB chatbot for personal use + logs everything into a database.

# Usage

First, you should comment out the bottommost part and type:
> DatabaseHandler('logs/logs.db',0).__first_launch__()    

Launch the file, this will get the database initiated. You can now remove the comments and delete the line.

Lastly, you need to make a config.ini file. This is how an example one looks:

[Credentials]    
email=facebook@email.com    
password=dupa123    

[Delays]    
queue_delay=0.5    
db_save_delay=5  

[Other]    
debug=1    
db_name=logs/logs.db    
bot_id=the bot's id, a long numerical int. Get it by going into conversation with his account and copying from url.
owner_ids=The owners' ids, seperated by commas. 

The commands are listed [atm] in MessageParser - around 320 lines mark.
