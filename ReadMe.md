
# Galactapedia for voice attack

The crawler.py script goes through every article listed in the Index section on https://robertsspaceindustries.com/galactapedia/ and save the title and the link and dumps it in a json file.  

After that you should run the VACommandsExporter script which creates a Voice Attack profile containing a command for each article.  
The commands in Voice attack get trigger by saying :   
    * Tell me about (the) ...
    * Can you tell me about (the) ...
    * What do you know about (the) ...
    
If you don't want to use the default TTS from Windows you need to change the 3rd <Context2> field in the VACommandTemplate.xml file to the name of the TTS that you want to use  
    
Requirements:  
    * [Python](https://www.python.org) - and install the required modules by running the command `pip install -r Requirements.txt`  
    * Voice Attack  
    * Google Chrome and [ChromeDriver](https://chromedriver.chromium.org/downloads) for the crawler (you can change the code to use other browsers if you want to, but I haven't tested with anything else). Also make sure that chromedriver is in your PATH environment variable  
    

    