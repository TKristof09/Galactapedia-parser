
# Galactapedia for voice attack

These scripts help you create commands for voice attack that read out the articles found on https://robertsspaceindustries.com/galactapedia/ using text to speech.

## Setup
Requirements:

* [Python](https://www.python.org) - make sure to add python to your PATH during the installation
* Install the required python modules by running the command `pip install -r Requirements.txt`
* [Voice Attack](https://voiceattack.com/)
* Google Chrome and [ChromeDriver](https://chromedriver.chromium.org/downloads/version-selection) for the crawler (you can change the code to use other browsers if you want to, but I haven't tested with anything else). Also make sure that chromedriver is in your PATH environment variable or in the same folder as the python scripts.

## Usage


The `crawler.py` script goes through every article listed in the Index section on https://robertsspaceindustries.com/galactapedia/ and saves the title and the link and dumps it in a json file. You can execute this but it isn't needed as a preloaded article list is already included in the repository.

After that you **need** to run the `VACommandsExporter.py` script which creates a Voice Attack profile containing a command for each article. Make sure you run this from the same folder as where the `main.py` file is so that the working directory of the voice attack commands get set up properly.


The commands in Voice attack get triggered by saying:
* Tell me about something new. - This reads a random article
* Tell me about (the) ...
* Can you tell me about (the) ...
* What do you know about (the) ...

If an article is too long it will be split up into several parts, to continue to the next part just say "continue" or "yes continue" when the TTS asks if you want to continue or not.

If you want to stop the TTS at any point, just say "stop"/"stop talking"/"thanks"/"thank you"

If you don't want to use the default TTS from Windows you need to uncomment and change a few lines in the `VACommandTemplate.xml` and `VAProfileTemplate.xml` files to the name of the TTS that you want to use. The lines to change look like the following, just remove the "<--" and "-->" and enter your desired text to speech engine in place of "Microsoft Hazel Desktop".
```
<!--<Context2 xml:space="preserve">Microsoft Hazel Desktop</Context2>-->
```



## Updating the list with new articles

If in the future you want to load new articles you need to execute `crawler.py` and `VACommandsExporter.py` once again (and optionally preload\_articles.py). And if CIG decides to update the already existing articles in the future you'll have to either delete the whole articles.json file to force a full reload or delete from the json file only the articles you want to reload.

## Notes
You may want to add the profile as a global profile in Voice Attack to use it alongside other profiles such as HCS voicepacks

The first time you ask for an article it might take a long time for the TTS to start reading it, this is because the script has to fetch the text from the galactapedia website and this can take some time. However, as you ask for articles they will get stored in the `articles.json` so when asking for them in the future the main script won't have to fetch it from the website and so the TTS will read it much quicker. The included `articles.json` contains the galactapedia articles as of 11/2023.

You can also launch `preload_articles.py` to download the articles into `articles.json` to avoid having to download them when using voice attack, thus making voice attack more responsive. This process however takes a very long time (on purpose) in order to avoid sending too many requests to the galactapedia website which would cause request timeouts. Ideally you should launch this and let it run in the background while doing other things. The script can be stopped at any time using Ctrl-C and it will save its progress, it also saves progress every 10 articles into checkpoint files in case your computer crashes or something, these can be safely deleted afterwards as only the `articles.json` will be used.

## Know issues
* Voice attack shows an error message relating to the speech engine when loading the profile. Not sure why this happens but it doesn't seem to have any effect and voice attack still functions correctly.
* The preloading script writes a lot of log messages sometimes, these can safely be ignored.

