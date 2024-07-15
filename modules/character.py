from typing import List, Optional

import requests
from bs4 import BeautifulSoup
from .characterdatainfo import *

TIBIA_URL="https://www.tibia.com"
class CharacterData:
    name: str
    former_names: Optional[List[str]]
    level: int
    title: str
    sex: str
    vocation: str
    level: int
    achievement_points: int
    world: str
    residence: str
    married_to: Optional[str]
    guild_membership: Optional[str]
    last_login: str
    comment: str
    premium: bool

    achievements: Optional[List[str]]
    loyalty_title: str
    created: str

    characters: Optional[List[str]]

    online: bool

    info_status: CharacterDataInfo

    def __init__(self, **kwargs):
        self.name = kwargs['name']

    @staticmethod
    def get_basic_info(character): # type: ignore
        try:
            character_url = "" + TIBIA_URL + f"/community/?subtopic=characters&name={character.name}"
            page = requests.get(character_url)
            soup = BeautifulSoup(page.content, "html.parser")

            classes = soup.find_all("td", attrs = {"class": "LabelV175"})

            for c in classes:
                content_name = c.contents[0]
                value = c.next_sibling.contents
                if content_name == "Name:":
                    character.name = value[0]
                elif content_name == "Former Names:":
                    character.former_names = [v for v in value]
                elif content_name == "Title:":
                    character.title = value[0]
                elif content_name == "Sex:":
                    character.sex = value[0]
                elif content_name == "Vocation:":
                    character.vocation = value[0]
                elif content_name == "Level:":
                    character.level = int(value[0])
                elif content_name == "Achievement Points:":
                    character.achievement_points = int(value[0])
                elif content_name == "World:":
                    character.world = value[0]
                elif content_name == "Residence:":
                    character.residence = value[0]
                elif content_name == "Married To:":
                    character.married_to = value[0]
                elif content_name == "Guild Membership:":
                    character.guild_membership = value[0]
                elif content_name == "Last Login:":
                    character.last_login = value[0]
                elif content_name == "Comment:":
                    character.comment = value[0]
                elif content_name == "Account Status:":
                    character.premium = value[0].lower() == "premium account"

                    
                #print(c, f"{c.contents}", "->", c.next_sibling, c.next_sibling.contents)

            character.info_status = CharacterDataInfo.VALID
            
        except:
            character.info_status = CharacterDataInfo.REQUEST_FAILED

    def get_achievements(character):
        pass

    @staticmethod
    def get(name: str):
        character = CharacterData(name = name)
        character.info_status = CharacterDataInfo.INVALID

        CharacterData.get_basic_info(character)
        

        return character
    
    def __repr__(self):
        output = "Character\n"
        for key, value in self.__dict__.items():
            output += f"\t{key}: {value}\n"
        return output
