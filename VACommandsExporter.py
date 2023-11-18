import json
import xml.etree.ElementTree as ET
import uuid
import os

COMMAND_TEMPLATE_FILE = "VACommandTemplate.xml"
PROFILE_TEMPLATE_FILE = "VAProfileTemplate.xml"
LINKS_JSON = "links.json"


def createCommand(command, python_arg, cont=False):
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
    context = command_actions[2].find("Context2")
    context.text = f'main.py "{python_arg}"'
    if cont:
        context.text += " --continue"

    command_actions[4].find("Context2").text = f'{python_arg}'

    cwd = command_actions[2].find("Context3")
    cwd.text = os.getcwd()

    if python_arg != "*" and not cont:
        command_actions[0].find("_caption").text = f"Say, 'Searching {python_arg} in the Galactapedia'"
        command_actions[0].find("Caption").text = f"Say, 'Searching {python_arg} in the Galactapedia'"
        command_actions[0].find("Context").text = f"Searching {python_arg} in the Galactapedia"



    return command_root

links = {}
with open(LINKS_JSON, 'r') as f:
    links = json.load(f)

profile = ET.parse(PROFILE_TEMPLATE_FILE)
profile_root = profile.getroot()
commands_node = profile_root.find("Commands")

cont_command = commands_node.findall("./Command")[1]
cont_command_actions = cont_command.findall("./ActionSequence/CommandAction")
cont_command_actions[0].find("Context3").text = os.getcwd()

commands_node.append(createCommand("Tell me about something new", "*"))
COMMAND_BASE = "Tell me about [the;] @@;Can you tell me about [the;] @@; What do you know about [the;] @@"

for title,link in links.items():
    cmd = title.replace("(", "[").replace(")", ";]")
    command = COMMAND_BASE.replace("@@", cmd)
    node = createCommand(command, title)
    commands_node.append(node)


profile.write("Galactapedia.vap",encoding="utf-8")
