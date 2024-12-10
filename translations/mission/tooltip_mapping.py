TOOLTIP_MAPPING = {
    "Archivum Sycorax": "Archivum_Sycorax",
    "Ascension Riser 31": "Ascension_Riser_31",
    "Chasm Logistratum": "Chasm_Logistratum",
    "Chasm Station HL-16-11": "Chasm_Station_HL-16-11",
    "Comms-Plex 154/2f": "Comms-Plex_1542f",
    "Consignment Yard HL-17-36": "Consignment_Yard_HL-17-36",
    "Enclavum Baross": "Enclavum_Baross",
    "Excise Vault Spireside-13": "Excise_Vault_Spireside-13",
    "Hab Dreyko": "Hab_Dreyko",
    "Magistrati Oubliette TM8-707": "Magistrati_Oubliette_TM8-707",
    "Mercantile HL-70-04": "Mercantile_HL-70-04",
    "Power Matrix HL-17-36": "Power_Matrix_HL-17-36",
    "Refinery Delta-17": "Refinery_Delta-17",
    "Relay Station TRS-150": "Relay_Station_TRS-150",
    "Silo Cluster 18-66/a": "Silo_Cluster_18-66a",
    "Smelter Complex HL-17-36": "Smelter_Complex_HL-17-36",
    "Vigil Station Oblivium": "Vigil_Station_Oblivium",
    "Warren 6-19": "Warren_6-19",
    "Clandestium Gloriana": "Clandestium_Gloriana",
    "km_enforcer_twins": "The_Orthus_Offensive",
    "op_train": "Rolling_Steel",
    "Dark Communion": "Dark_Communion",
}


# Get image name based on raw english map name
def get_image_name_by_raw_map_name(map_name):
    image_name = TOOLTIP_MAPPING.get(map_name, "")
    if image_name == "":
        print(f"No image name found for map name: {map_name}")
    return image_name
