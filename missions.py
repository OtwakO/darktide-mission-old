# -*- coding: utf-8 -*-
import json
import re

import requests
from bs4 import BeautifulSoup

from translations.mission.flash import FLASH_MISSIONS


class MissionGatherer:
    def __init__(self):
        self.language = "en"
        self.filter_keywords = []
        pass

    # Helper functions
    def get_missions(self, auric_maelstrom_only=False):
        req_url = "https://maelstroom.net/filtered.php"
        headers_list = {"Content-Type": "application/x-www-form-urlencoded"}
        if auric_maelstrom_only:
            payload = "bookCir=0&missionDif=Damnation&missionCir=&flashOnly=0&button1=Filter+Missions"
        else:
            payload = "bookCir=0&missionDif=&missionCir=&button1=Filter+Missions"

        response = requests.request("POST", req_url, data=payload, headers=headers_list)
        soup = BeautifulSoup(response.content, "html.parser")

        body = soup.select_one("body").getText("||")
        contents = body.split("||")

        self.missions = contents[::2]
        self.mmt_codes = contents[1::2]

        self.fix_new_mission()

    def fix_new_mission(self):
        # If new missions are missing mission type etc...

        # # Fix core_research missions --> Patched
        # self.missions = [
        #     mission.replace("core_research · ", "core_research · Repair · ")
        #     for mission in self.missions
        # ]

        # Fix Twin missions
        self.missions = [
            mission.replace("km_enforcer_twins · ", "km_enforcer_twins · Special · ")
            for mission in self.missions
        ]

        # Fix Train missions
        self.missions = [
            mission.replace("op_train · ", "op_train · Operations · ")
            for mission in self.missions
        ]

        # Change /mmtimport to /mmt
        self.mmt_codes = [code.replace("/mmtimport", "/mmt") for code in self.mmt_codes]

    def filter_missions(self, missions, keywords: list[str]):
        filtered_missions_index = [
            index
            for index, mission in enumerate(missions)
            if all([keyword.lower() in mission.lower() for keyword in keywords])
        ]

        filtered_missions = [missions[index] for index in filtered_missions_index]
        filtered_mmt_codes = [
            self.mmt_codes[index] for index in filtered_missions_index
        ]

        return filtered_missions, filtered_mmt_codes

    def convert_flash_missions(self, missions):
        converted_missions = []
        for mission in missions:
            translated_mission = mission
            for replacement in FLASH_MISSIONS:
                translated_mission = re.sub(
                    rf"{replacement[0]}", replacement[1], translated_mission
                )
            converted_missions.append(translated_mission)
        return converted_missions

    def translate_missions(self, missions, language="zh-tw"):
        if language == "zh-tw":
            from translations.mission.traditional_chinese import TRANSLATION

        # Return English missions if language is not supported
        else:
            from translations.mission.english import TRANSLATION

        translated_missions = []
        for mission in missions:
            translated_mission = mission
            for replacement in TRANSLATION:
                translated_mission = re.sub(
                    rf"{replacement[0]}", replacement[1], translated_mission
                )
            translated_missions.append(translated_mission)
        return translated_missions

    def get_mission_info(self, mission):
        try:
            map_name, mission_type, difficulty, modifiers, book, started_time = (
                mission.split(" · ")
            )
        except ValueError:
            print(f"Invalid mission format: {mission}")
        except Exception as e:
            print(f"Error parsing mission: {mission} with error {e}")
        return (
            map_name,
            mission_type,
            difficulty,
            [modifier.strip() for modifier in modifiers.split("#") if modifier != ""],
            book,
            started_time.strip(),
        )

    # Main functions
    def get_requested_missions(self, auric_maelstrom_only=False):
        mission_data = []
        self.get_missions(auric_maelstrom_only)
        converted_missions = self.convert_flash_missions(self.missions)
        translated_missions = self.translate_missions(converted_missions, self.language)
        chosen_missions, chosen_mmt_codes = self.filter_missions(
            translated_missions, self.filter_keywords
        )
        for index, mission in enumerate(chosen_missions):
            map_name, mission_type, difficulty, modifiers, book, started_time = (
                self.get_mission_info(mission)
            )
            mission_data.append(
                {
                    "map_name": map_name,
                    "mission_type": mission_type,
                    "difficulty": difficulty,
                    "modifiers": modifiers,
                    "book": book,
                    "started_time": started_time,
                    "mmt_code": chosen_mmt_codes[index],
                }
            )
        with open("result.json", "w", encoding="utf-8") as f:
            json.dump(mission_data, f, ensure_ascii=False, indent=4)
        return mission_data


if __name__ == "__main__":
    test = MissionGatherer()
    test.language = "en"
    test.filter_keywords = ["Toxic Gas"]
    missions = test.get_requested_missions(auric_maelstrom_only=False)
    print(missions)
