import json

# Load truck dataset
with open("truck_data_cleaned.json") as f:
    truck_data = json.load(f)

def recommend_vehicle(total_volume_cuft, max_length, max_width, max_height):
    for truck in truck_data:
        truck_volume = float(truck["Volume (cu ft)"])
        if (total_volume_cuft <= truck_volume and
            max_length <= float(truck["Length (ft)"]) and
            max_width <= float(truck["Width (ft)"]) and
            max_height <= float(truck["Height (ft)"])):
            return truck["Truck Type"]
    return "No suitable vehicle found"

# Example usage
vehicle = recommend_vehicle(120, 6.5, 4, 4.5)  # Example load
print(vehicle)



import json
import pandas as pd
with open('internship/data.json', 'r') as f: data = json.load(f)
filtered_items = []
for category in data.get("inventory", []):
    for subcategory in category.get("category", []):
        for item in subcategory.get("items", []):
            qty = item.get("qty", 0)
            if qty >= 1:
                name = item.get("displayName", item.get("name", "Unknown"))
                length = item.get("length_ft", 0)
                width = item.get("width_ft", 0)
                height = item.get("height_ft", 0)
                item_volume = item.get("item_volume_cuft", round(length * width * height, 2))
                total_volume = item.get("total_item_volume_cuft", round(item_volume * qty, 2))

                filtered_items.append({
                    "Item Name": name,
                    "Length (ft)": length,
                    "Width (ft)": width,
                    "Height (ft)": height,
                    "Quantity": qty,
                    "Item Volume (cuft)": item_volume,
                    "Total Volume (cuft)": total_volume
                })
df = pd.DataFrame(filtered_items)
#print(df.to_string(index=True))
df.to_csv("filtered_inventory.csv", index=True)

with open('internship/data copy.json', 'r') as f: data = json.load(f)
filtered_items = []
for category in data.get("inventory", []):
    for subcategory in category.get("category", []):
        for item in subcategory.get("items", []):
            qty = item.get("qty", 0)
            if qty >= 1:
                name = item.get("displayName", item.get("name", "Unknown"))
                length = item.get("length_ft", 0)
                width = item.get("width_ft", 0)
                height = item.get("height_ft", 0)
                item_volume = (round(length * width * height, 2))
                total_volume = (round(item_volume * qty, 2))
                
                filtered_items.append({
                    "Item Name": name,
                    "Length (ft)": length,
                    "Width (ft)": width,
                    "Height (ft)": height,
                    "Quantity": qty,
                    "Item Volume (cuft)": item_volume,
                    "Total Volume (cuft)": total_volume
                })
df = pd.DataFrame(filtered_items)
print(df.to_string(index=True))
df.to_csv("filtered_inventory.csv", index=True)
          
import json
import re

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

from py3dbp import Bin, Item, Packer
import json
import re

with open("internship/data.json") as f:
    inventory_data = json.load(f)

with open("internship/truck_data_cleaned.json") as f:
    truck_data = json.load(f)

def ft_to_inch(ft):
    return int(float(ft) * 12)

bins = []
for truck in truck_data:
    dims_str = truck.get("Dimensions (L × W × H)", "") or truck.get("Dimensions (LWH)", "")
    dims_str = dims_str.replace("×", "x").replace("*", "x")
    dims_match = re.findall(r"([\d.]+)", dims_str)

    if len(dims_match) == 3:
        length, width, height = map(ft_to_inch, dims_match)
        bins.append(
            Bin(
                truck.get("Truck Type", "Unknown"),
                length, width, height,
                10000  
            )
        )

items = []
item_counter = 1
for section in inventory_data["inventory"]:
    for category in section["category"]:
        for item in category["items"]:
            qty = item.get("qty", 0)
            length = ft_to_inch(item.get("length_ft", 0))
            width = ft_to_inch(item.get("width_ft", 0))
            height = ft_to_inch(item.get("height_ft", 0))
            weight = item.get("weight", 10)
            
            for i in range(qty):
                items.append(
                    Item(f"Item-{item_counter}", length, width, height, weight)
                )
                item_counter += 1
            


packer = Packer()
for b in bins:
    packer.add_bin(b)
for i in items:
    packer.add_item(i)

packer.pack()

packed_items = []
unfitted_items = []

for b in packer.bins:
    for item in b.items:
        packed_items.append({
            "item_id": item.name,
            "dimensions": [item.depth, item.width, item.height],  
            "position": [int(p) for p in item.position], 
            "rotation_type": item.rotation_type,
            "bin_assigned": b.name
        })
for item in b.unfitted_items:
        unfitted_items.append({
            "item_id": str(item.name),
            "dimensions": [float(item.depth), float(item.width), float(item.height)]
        })


print("\n Packed Items (3D bin packing):")
print(json.dumps(packed_items, indent=4, default=float))

print("\n Unfitted Items ")
print(json.dumps(unfitted_items, indent=4))