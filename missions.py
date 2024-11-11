# -*- coding: utf-8 -*-
import json
import re

import requests
from bs4 import BeautifulSoup

from translations.mission.flash import FLASH_MISSIONS
from translations.mission.tooltip_mapping import get_image_name_by_raw_map_name


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

    # Get mission credits and xp data
    def get_all_mission_credits_xp(self):
        req_url = "https://maelstroom.net/DT.json"
        response = requests.get(req_url)
        mission_data = response.json()
        return mission_data

    def find_mission_credits_xp_by_code(self, specific_mission_data):
        credits = specific_mission_data["credits"]
        xp = specific_mission_data["xp"]
        if specific_mission_data["extraRewards"]:
            for extra_reward_type, extra_reward_info in specific_mission_data[
                "extraRewards"
            ].items():
                credits += extra_reward_info["credits"]
                xp += extra_reward_info["xp"]
        return credits, xp

    # Check if mission is auric
    def is_auric_mission(self, specific_mission_data):
        is_auric = specific_mission_data.get("category", False)
        if is_auric:
            return True
        return False

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

        elif language == "zh-cn":
            from translations.mission.simplified_chinese import TRANSLATION

        # Return English missions if language is not supported
        else:
            from translations.mission.english import TRANSLATION

        translated_missions = []
        for mission in missions:
            translated_mission = mission
            for replacement in TRANSLATION:
                translated_mission = re.sub(
                    rf"{replacement[0]}",
                    replacement[1],
                    translated_mission,
                    flags=re.IGNORECASE,
                )
            translated_missions.append(translated_mission)
        return translated_missions

    def get_raw_map_name_for_image_tooltip(self, map_name, language):
        if language == "zh-tw":
            from translations.mission.traditional_chinese import TRANSLATION

        elif language == "zh-cn":
            from translations.mission.simplified_chinese import TRANSLATION

        else:
            from translations.mission.english import TRANSLATION
        for replacement in TRANSLATION:
            if map_name == replacement[1]:
                return replacement[0]

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
        all_credits_xp_data = self.get_all_mission_credits_xp()
        converted_missions = self.convert_flash_missions(self.missions)
        translated_missions = self.translate_missions(converted_missions, self.language)
        chosen_missions, chosen_mmt_codes = self.filter_missions(
            translated_missions, self.filter_keywords
        )
        for index, mission in enumerate(chosen_missions):
            map_name, mission_type, difficulty, modifiers, book, started_time = (
                self.get_mission_info(mission)
            )
            credits, xp = self.find_mission_credits_xp_by_code(
                all_credits_xp_data[chosen_mmt_codes[index].replace("/mmt ", "")]
            )
            is_auric = self.is_auric_mission(
                all_credits_xp_data[chosen_mmt_codes[index].replace("/mmt ", "")]
            )
            raw_map_name = self.get_raw_map_name_for_image_tooltip(
                map_name, self.language
            )
            mission_data.append(
                {
                    "map_name": map_name,
                    "mission_type": mission_type,
                    "difficulty": difficulty,
                    "modifiers": modifiers,
                    "book": book,
                    "credits": credits,
                    "xp": xp,
                    "is_auric": is_auric,
                    "started_time": started_time,
                    "raw_mission_name": raw_map_name,
                    "image_name": get_image_name_by_raw_map_name(raw_map_name),
                    "mmt_code": chosen_mmt_codes[index],
                }
            )
        with open("result.json", "w", encoding="utf-8") as f:
            json.dump(mission_data, f, ensure_ascii=False, indent=4)
        return mission_data


if __name__ == "__main__":
    test = MissionGatherer()
    test.language = "en"
    # test.filter_keywords = ["Monstrous", "Shock Troop", "Damnation", "Enclavum Baross"]
    test.filter_keywords = ["Monstrous"]
    missions = test.get_requested_missions(auric_maelstrom_only=False)
    print(missions[0])

    # debug_missions = [
    #     "Enclavum Baross · Strike · Damnation · Monstrous Shock Troop Gauntlet With Snipers & Pox Gas · No books · Started 16hrs ago",
    #     "Vigil Station Oblivium · Espionage · Damnation · Hi-intensity Pox Gas · No books · Started 6.5hrs ago",
    # ]
    # debug_result = test.translate_missions(debug_missions, "zh-cn")
    # print(debug_result)
