import pandas as pd
# import math
uld_data = [
    ("U1", 224, 150, 162, 2500),
    ("U2", 224, 318, 162, 2500),
    ("U3", 244, 318, 244, 2800),
    ("U4", 244, 318, 244, 2800),
    ("U5", 244, 318, 285, 3500)
    # ("U6", 244, 31, 28, 3500)
]
K=40 # delay for spreading priority packages into multiple ULDS

# Package data (from your input)
package_data = [
   ("P-1", 99, 53, 55, 61, False, 176),
("P-2", 56, 99, 81, 53, True, None),
("P-3", 42, 101, 51, 17, True, None),
("P-4", 108, 75, 56, 73, False, 138),
("P-5", 88, 58, 64, 93, False, 139),
("P-6", 91, 56, 84, 47, True, None),
("P-7", 88, 78, 93, 117, False, 102),
("P-8", 108, 105, 76, 142, False, 108),
("P-9", 73, 71, 88, 50, True, None),
("P-10", 88, 70, 85, 81, True, None),
("P-11", 55, 80, 81, 23, False, 96),
("P-12", 48, 80, 88, 27, False, 117),
("P-13", 55, 94, 87, 41, False, 73),
("P-14", 45, 46, 81, 27, False, 68),
("P-15", 84, 49, 60, 57, True, None),
("P-16", 48, 93, 63, 82, True, None),
("P-17", 83, 63, 57, 29, True, None),
("P-18", 68, 101, 95, 96, False, 65),
("P-19", 51, 87, 69, 73, False, 107),
("P-20", 88, 106, 56, 71, True, None),
("P-21", 105, 71, 105, 223, False, 116),
("P-22", 100, 92, 99, 191, False, 86),
("P-23", 51, 50, 110, 59, True, None),
("P-24", 81, 109, 55, 123, False, 69),
("P-25", 44, 77, 53, 37, False, 108),
("P-26", 69, 56, 73, 56, False, 130),
("P-27", 93, 62, 49, 18, False, 122),
("P-28", 81, 64, 95, 70, False, 139),
("P-29", 62, 86, 53, 23, False, 122),
("P-30", 88, 85, 102, 164, False, 70),
("P-31", 71, 49, 76, 67, False, 76),
("P-32", 70, 44, 98, 53, False, 124),
("P-33", 90, 89, 73, 132, False, 136),
("P-34", 87, 45, 81, 45, False, 77),
("P-35", 83, 72, 63, 96, False, 103),
("P-36", 86, 80, 78, 146, True, None),
("P-37", 59, 76, 51, 33, False, 131),
("P-38", 84, 96, 48, 21, False, 60),
("P-39", 96, 64, 61, 61, False, 111),
("P-40", 70, 45, 90, 78, False, 106),
("P-41", 104, 90, 68, 72, True, None),
("P-42", 62, 109, 41, 46, True, None),
("P-43", 51, 86, 108, 87, False, 109)
# ("P-44", 84, 40, 49, 28, False, 87),
# ("P-45", 91, 72, 81, 92, True, None),
# ("P-46", 71, 62, 94, 39, True, None),
# ("P-47", 86, 58, 104, 149, False, 67),
# ("P-48", 53, 65, 48, 33, False, 67),
# ("P-49", 69, 40, 100, 55, True, None),
# ("P-50", 73, 104, 64, 75, True, None),
# ("P-51", 57, 86, 97, 65, False, 67),
# ("P-52", 104, 88, 102, 96, False, 121),
# ("P-53", 44, 53, 106, 14, False, 74),
# ("P-54", 106, 51, 59, 20, False, 98),
# ("P-55", 95, 93, 77, 71, False, 78),
# ("P-56", 65, 68, 109, 77, False, 85),
# ("P-57", 83, 64, 59, 32, False, 137),
# ("P-58", 95, 102, 55, 126, False, 134),
# ("P-59", 85, 79, 49, 26, False, 111),
# ("P-60", 60, 85, 87, 23, False, 84),
# ("P-61", 57, 109, 95, 130, False, 136),
# ("P-62", 43, 92, 88, 25, False, 84),
# ("P-63", 75, 69, 85, 111, False, 116),
# ("P-64", 100, 56, 104, 123, False, 62),
# ("P-65", 50, 78, 110, 56, False, 121),
# ("P-66", 50, 47, 86, 53, False, 72),
# ("P-67", 76, 57, 101, 34, False, 65),
# ("P-68", 92, 46, 81, 62, True, None),
# ("P-69", 84, 47, 54, 57, True, None),
# ("P-70", 108, 101, 77, 158, False, 102),
# ("P-71", 99, 43, 60, 41, True, None),
# ("P-72", 89, 83, 44, 79, False, 66),
# ("P-73", 104, 86, 63, 79, True, None),
# ("P-74", 73, 87, 69, 115, False, 61),
# ("P-75", 74, 43, 85, 42, False, 128),
# ("P-76", 40, 92, 96, 81, False, 123),
# ("P-77", 96, 50, 65, 57, False, 88),
# ("P-78", 74, 104, 42, 85, False, 116),
# ("P-79", 86, 62, 75, 61, False, 91),
# ("P-80", 43, 85, 44, 20, False, 127),
# ("P-81", 110, 101, 93, 94, False, 116),
# ("P-82", 66, 71, 97, 130, True, None),
# ("P-83", 106, 105, 99, 168, False, 97),
# ("P-84", 94, 66, 78, 41, False, 82),
# ("P-85", 47, 68, 44, 42, False, 74),
# ("P-86", 65, 63, 41, 50, True, None),
# ("P-87", 54, 53, 107, 84, False, 116),
# ("P-88", 70, 106, 62, 106, False, 74),
#("P-89", 68, 109, 108, 60, False, 117)

]
uld_df = pd.DataFrame(uld_data, columns=["ULD_ID", "Length", "Width", "Height", "Weight_Limit"])
package_df = pd.DataFrame(package_data, columns=["Package_ID", "Length", "Width", "Height", "Weight", "Type", "Cost_of_Delay"])

# Function to rotate package dimensions
def rotate_package(package):
    # Generate all possible rotations of the package
    rotations = [
        (package["Length"], package["Width"], package["Height"]),
        (package["Length"], package["Height"], package["Width"]),
        (package["Width"], package["Length"], package["Height"]),
        (package["Width"], package["Height"], package["Length"]),
        (package["Height"], package["Length"], package["Width"]),
        (package["Height"], package["Width"], package["Length"])
    ]
    return rotations

# Greedy Algorithm to allocate packages to ULDs using rotation and overlap checking
def fit_packages_to_uld(uld_df, package_df):
    allocations = {uld: [] for uld in uld_df["ULD_ID"]}  # Initialize allocations dictionary
    positions = {uld: [] for uld in uld_df["ULD_ID"]}  # Store positions of packages in ULD
    occupied_positions = {uld: [] for uld in uld_df["ULD_ID"]}  # Track occupied positions for overlap detection
    remaining_space = {
        uld: {
            "Length": uld_df.loc[uld_df["ULD_ID"] == uld, "Length"].values[0],
            "Width": uld_df.loc[uld_df["ULD_ID"] == uld, "Width"].values[0],
            "Height": uld_df.loc[uld_df["ULD_ID"] == uld, "Height"].values[0],
            "Volume": uld_df.loc[uld_df["ULD_ID"] == uld, "Length"].values[0] *
                     uld_df.loc[uld_df["ULD_ID"] == uld, "Width"].values[0] *
                     uld_df.loc[uld_df["ULD_ID"] == uld, "Height"].values[0], 
            "Weight": uld_df.loc[uld_df["ULD_ID"] == uld, "Weight_Limit"].values[0]
        }
        for uld in uld_df["ULD_ID"]
    }

    # Sort packages by size (volume), weight, and type for better packing
    package_df["Volume"] = package_df["Length"] * package_df["Width"] * package_df["Height"]
    package_df = package_df.sort_values(by=["Type", "Volume", "Weight"], ascending=[False, False, False])

    allocations_result = []

    # Allocate packages
    for _, package in package_df.iterrows():
        package_volume = package["Volume"]
        package_weight = package["Weight"]
        package_rotations = rotate_package(package)

        allocated = False
        best_leftover_space = float('inf')
        best_rotation = None
        best_position = None
        best_uld = None

        # Try to allocate the package
        for uld in sorted(allocations, key=lambda uld: (remaining_space[uld]["Volume"], remaining_space[uld]["Weight"]), reverse=True):
            uld_remaining = remaining_space[uld]
            print("entering uld",uld)
            # Check if package fits within ULD's remaining space and weight limit
            if uld_remaining["Volume"] >= package_volume and uld_remaining["Weight"] >= package_weight:
                for rotation in package_rotations:
                    p_length, p_width, p_height = rotation
                    
                    # Track best fitting rotation and position
                    for x in range(0, uld_remaining["Length"] - p_length + 1):
                        for y in range(0, uld_remaining["Width"] - p_width + 1):
                            for z in range(0, uld_remaining["Height"] - p_height + 1):
                                if (x + p_length <= uld_remaining["Length"] and 
                                    y + p_width <= uld_remaining["Width"] and
                                    z + p_height <= uld_remaining["Height"]):
                                    
                                    # Check for overlap with other packages
                                    overlap = False
                                    for pos, dims in occupied_positions[uld]:
                                        if (x < pos[0] + dims[0] and x + p_length > pos[0] and
                                            y < pos[1] + dims[1] and y + p_width > pos[1] and
                                            z < pos[2] + dims[2] and z + p_height > pos[2]):
                                            overlap = True
                                            break
                                    
                                    if not overlap:
                                        # Calculate the leftover space in the ULD after placing the package
                                        leftover_space = (uld_remaining["Volume"] - package_volume)
                                        if leftover_space < best_leftover_space:
                                            best_leftover_space = leftover_space
                                            best_rotation = rotation
                                            best_position = (x, y, z)
                                            best_uld = uld
                                        break
            print(best_uld)
            if best_uld is not None:  # If a suitable position is found, break early
                break
        
        # Place the package if a valid position is found
        if best_uld is not None:
            allocations[best_uld].append(package["Package_ID"])
            remaining_space[best_uld]["Volume"] -= package_volume
            remaining_space[best_uld]["Weight"] -= package_weight
            positions[best_uld].append((package["Package_ID"], best_position))
            
            # Update occupied positions
            occupied_positions[best_uld].append((best_position, best_rotation))
            
            # Record the result with corners
            x1, y1, z1 = best_position[0] + best_rotation[0], best_position[1] + best_rotation[1], best_position[2] + best_rotation[2]
            allocations_result.append((package["Package_ID"], best_uld, best_position, (x1, y1, z1)))
            allocated = True
        
        # If not allocated, add it to the result with ULD ID as None
        if not allocated:
            x1=-1
            y1=z1=-1
            x0=y0=z0=-1
            allocations_result.append((package["Package_ID"], None, (-1,-1,-1), (-1,-1,-1)))

    return allocations_result







allocations_result = fit_packages_to_uld(uld_df, package_df)

priority_package_ids = package_df[package_df['Type'] == True]['Package_ID'].tolist()


priority_uld_count = len(set([uld for package_id, uld, _, _ in allocations_result if package_id in priority_package_ids and uld is not None]))


print(f"Number of ULDs with priority packages: {priority_uld_count}")
print(f"Cost Delay: {K*priority_uld_count}")

print("Package Allocations to ULDs, Positions, and Corners:")
for result in allocations_result:
    package_id, uld_id, (x0, y0, z0), (x1, y1, z1) = result
    if uld_id is None:
        print(f"Package {package_id} could not be allocated to any ULD.",(x0, y0, z0),(x1, y1, z1))
    else:
        print(f"Package {package_id} allocated to ULD {uld_id} at position (x0, y0, z0) = ({x0}, {y0}, {z0}), "
              f"diagonally opposite corner (x1, y1, z1) = ({x1}, {y1}, {z1})")
def is_overlapping(pkg1, pkg2):
   
    (x0_1, y0_1, z0_1), (x1_1, y1_1, z1_1) = pkg1
    (x0_2, y0_2, z0_2), (x1_2, y1_2, z1_2) = pkg2
    
   
    overlap_x = not (x1_1 <= x0_2 or x1_2 <= x0_1)
    overlap_y = not (y1_1 <= y0_2 or y1_2 <= y0_1)
    overlap_z = not (z1_1 <= z0_2 or z1_2 <= z0_1)
    
    
    return overlap_x and overlap_y and overlap_z

def check_for_overlaps(allocations_result):
    
    
    uld_allocations = {}

    # Group packages by ULD
    for package_id, uld_id, (x0, y0, z0), (x1, y1, z1) in allocations_result:
        if uld_id not in uld_allocations:
            uld_allocations[uld_id] = []
        uld_allocations[uld_id].append(((x0, y0, z0), (x1, y1, z1)))

    # Check for overlaps within each ULD
    overlaps = []
    for uld_id, packages in uld_allocations.items():
        for i in range(len(packages)):
            for j in range(i + 1, len(packages)):
                if is_overlapping(packages[i], packages[j]):
                    overlaps.append((uld_id, i, j))

    return overlaps
overlaps = check_for_overlaps(allocations_result)

# Print results
if overlaps:
    print("Overlapping packages found:")
    for uld_id, i, j in overlaps:
        print(f"ULD {uld_id}: Package {allocations_result[i][0]} overlaps with Package {allocations_result[j][0]}")
else:
    print("No overlaps found.")
