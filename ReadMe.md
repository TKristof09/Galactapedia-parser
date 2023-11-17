
# Galactapedia for voice attack

These scripts help you create commands for voice attack that read out the articles found on https://robertsspaceindustries.com/galactapedia/ using text to speech.

The crawler.py script goes through every article listed in the Index section on https://robertsspaceindustries.com/galactapedia/ and saves the title and the link and dumps it in a json file.

You may optionally execute the preload\_articles.py script which will load the articles and save them to a file. This makes voice attack more responsive, as otherwise it has to load the article you ask for when you ask for it for the first time. However, this process takes a very long time (on purpose) in order to not send too many requests too quickly to the galactapedia website so if you do decide to preload the articles you should let it run in the background while doing something else (you can also stop it at any point using Ctrl-C and it will save its progress).

After that you should run the VACommandsExporter.py script which creates a Voice Attack profile containing a command for each article.
The commands in Voice attack get trigger by saying:
* Tell me about something new.
* Tell me about (the) ...
* Can you tell me about (the) ...
* What do you know about (the) ...

If you want to stop the TTS at any point, just say stop/stop talking/thanks/thank you

If you don't want to use the default TTS from Windows you need to uncomment and change the two lines in the VACommandTemplate.xml file to the name of the TTS that you want to use. The lines to change look like the following, just remove the "<--" and "-->" and enter your desired text to speech engine in place of "Microsoft Hazel Desktop".
```
<!--<Context2 xml:space="preserve">Microsoft Hazel Desktop</Context2>-->
```

Requirements:

* [Python](https://www.python.org) - make sure to add python to your PATH during the installation
* Install the required python modules by running the command `pip install -r Requirements.txt`
* Voice Attack
* Google Chrome and [ChromeDriver](https://chromedriver.chromium.org/downloads/version-selection) for the crawler (you can change the code to use other browsers if you want to, but I haven't tested with anything else). Also make sure that chromedriver is in your PATH environment variable


## Notes
You may want to add the profile as a global profile in Voice Attack to use it alongside other profiles such as HCS voicepacks

## Know issues
Asking for the article called "Xi'an Cuisine" causes a hang
