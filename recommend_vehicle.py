import json
import re

def get_recommended_vehicle():

    with open("internship/data.json") as f:
        inventory_data = json.load(f)

    with open("internship/truck_data_cleaned.json") as f:
        truck_data = json.load(f)

    
    total_used_volume = 0.0
    max_item_height = 0.0
    for section in inventory_data["inventory"]:
        for category in section["category"]:
            for item in category["items"]:
                qty = item.get("qty", 0)
                volume_per_item = item.get("item_volume_cuft", 0)
                total_used_volume += qty * volume_per_item

                height = item.get("height_ft", 0)
                if height > max_item_height:
                    max_item_height = height


    packed_containers = []
    for truck in truck_data:
        volume_str = truck.get("Volume (cu ft)", "")
        match = re.search(r"([\d.]+)", volume_str)
        if not match:
            continue
        container_volume = float(match.group(1))

        dims_str = truck.get("Dimensions (L × W × H)", "") 
        dims_match = re.findall(r"([\d.]+)", dims_str)
        if len(dims_match) != 3:
            continue
        truck_length, truck_width, truck_height = map(float, dims_match)
         
        if total_used_volume <= container_volume and max_item_height <= truck_height:
            utilization = (total_used_volume / container_volume) * 100
            packed_containers.append({
                "Vechile Type": truck.get("Truck Type"),
                "Dimensions (L×W×H)": dims_str,
                "Volume (cu ft)": round(container_volume, 2),
                "Total Used Volume (cu ft)": round(total_used_volume, 2),
                "Utilization %": round(utilization, 2),
                "Truck Height (ft)": truck_height,
                "Max Item Height (ft)": max_item_height
            })
            break

    return packed_containers
