import json
import xml.etree.ElementTree as ET
import uuid
import os

COMMAND_TEMPLATE_FILE = "VACommandTemplate.xml"
PROFILE_TEMPLATE_FILE = "VAProfileTemplate.xml"
ARTICLES_JSON = "Articles.json"


def createCommand(command, python_arg):    
    template_xml = ET.parse(COMMAND_TEMPLATE_FILE)
    command_root = template_xml.getroot()
    id = command_root.find("Id")
    id.text = str(uuid.uuid4())
    command_string = command_root.find("CommandString")
    command_string.text = command
    command_actions = command_root.findall("./ActionSequence/CommandAction")
    for ca in command_actions:
        command_action_id = ca.find("Id")
        command_action_id.text = str(uuid.uuid4())
    context = command_actions[1].find("Context2")
    context.text = f'main.py "{python_arg}"'
    
    cwd = command_actions[1].find("Context3")
    cwd.text = os.getcwd()
    
    
    
    return command_root

links = {}
with open(ARTICLES_JSON, 'r') as f:
    links = json.load(f)

profile = ET.parse(PROFILE_TEMPLATE_FILE)
profile_root = profile.getroot()
commands_node = profile_root.find("Commands")

COMMAND_BASE = "Tell me about [the] @@;Can you tell me about [the] @@; What do you know about [the] @@"

for k,v in links.items():
    for title,link in v.items():
        command = COMMAND_BASE.replace("@@", title)
        node = createCommand(command, title)
        commands_node.append(node)
    
profile.write("Galactapedia.vap",encoding="utf-8")