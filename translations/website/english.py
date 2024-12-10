UI_TRANSLATIONS = {
    "search_header": "Filter Mission",
    "difficulty_header": "Difficulties",
    "filter_header": "Modifiers",
    "event_filter_header": "Event Modifiers",
    "search_button": "Search",
    "copy_btn": "Copy",
    "copy_success": "Copied to clipboard!",
    "auric_translation": "Auric Only",
    "auric_maelstrom_translation": "Auric Maelstrom Only",
    "maps_header": "Maps",
}

DIFFICULTIES = {
    "Sedition": "Sedition (T1)",
    "Uprising": "Uprising (T2)",
    "Malice": "Malice (T3)",
    "Heresy": "Heresy (T4)",
    "Damnation": "Damnation (T5)",
}

BOOKS = {
    "No book": "No book",
    "Recover Scriptures": "Recover Scriptures",
    "Seize Grimoires": "Seize Grimoires",
}

FILTERS = {
    # Modifiers
    "Default": "Default",
    "Hi-Intensity": "Hi-Intensity",
    "Low-Intensity": "Low-Intensity",
    "Engagement Zone": "Engagement Zone",
    "Shock Troop": "Shock Troop",
    "Nurgle-Blessed": "Nurgle-Blessed",
    "Hunting Grounds": "Hunting Grounds",
    "Mutants": "Mutants",
    "Poxbursters": "Poxbursters",
    "Sniper": "Sniper",
    "Monstrous": "Monstrous",
    "Ventilation Purge": "Ventilation Purge",
    "Power Supply Interruption": "Power Supply Interruption",
    "Grenades": "Grenades",
    "Melee": "Melee",
    "Ranged": "Ranged",
    "Scab Enemies Only": "Scab Enemies Only",
    "Cooldowns Reduced": "Cooldowns Reduced",
    "Barrels": "Barrels",
    # Toxic Gas
    "Pox Gas": "Pox-Gas",
    "Pox Gas (High Concentration)": "Hi-Concentrated Pox-Gas",
    "Pox Gas (Low Concentration)": "Low-Concentrated Pox-Gas",
    # "High-Intensity Toxic Gas": "High-Intensity Toxic Gas",
    # "Low-Intensity Toxic Gas": "Low-Intensity Toxic Gas",
    "Twin Toxic Gas": "Twin Toxic Gas",
}

EVENT_FILTERS = {
    # "Infected Moebian 21st": "Infected Moebian 21st",
    # "Mutated Horrors": "Mutated Horrors",
}

MAPS = {
    "Archivum Sycorax": "Archivum Sycorax",
    "Ascension Riser 31": "Ascension Riser 31",
    "Chasm Logistratum": "Chasm Logistratum",
    "Chasm Station HL-16-11": "Chasm Station HL-16-11",
    "Clandestium Gloriana": "Clandestium Gloriana",
    "Comms-Plex 154/2f": "Comms-Plex 154/2f",
    "Consignment Yard HL-17-36": "Consignment Yard HL-17-36",
    "Enclavum Baross": "Enclavum Baross",
    "Excise Vault Spireside-13": "Excise Vault Spireside-13",
    "Hab Dreyko": "Hab Dreyko",
    "Magistrati Oubliette TM8-707": "Magistrati Oubliette TM8-707",
    "Mercantile HL-70-04": "Mercantile HL-70-04",
    "Power Matrix HL-17-36": "Power Matrix HL-17-36",
    "Refinery Delta-17": "Refinery Delta-17",
    "Relay Station TRS-150": "Relay Station TRS-150",
    "Rolling Steel": "Rolling Steel",
    "Silo Cluster 18-66/a": "Silo Cluster 18-66/a",
    "Smelter Complex HL-17-36": "Smelter Complex HL-17-36",
    "The Orthus Offensive": "The Orthus Offensive",
    "Vigil Station Oblivium": "Vigil Station Oblivium",
    "Warren 6-19": "Warren 6-19",
    "Dark Communion": "Dark Communion",
}

# Sort the maps alphabetically
MAPS = dict(sorted(MAPS.items()))

if __name__ == "__main__":
    print(dict(sorted(MAPS.items())))
