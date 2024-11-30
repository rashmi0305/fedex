import pandas as pd
import math

# ULD data (from your input)
uld_data = [
    ("U1", 224, 318, 162, 2500),
    ("U2", 224, 318, 162, 2500),
    ("U3", 244, 318, 244, 2800),
    ("U4", 244, 318, 244, 2800),
    ("U5", 244, 318, 285, 3500),
    ("U6", 244, 318, 285, 3500)
]

# Package data (from your input)
package_data = [
    ("P-1", 50, 50, 50, 20, False, 100),
    ("P-2", 70, 60, 60, 30, True, None),
    ("P-3", 100, 100, 15, 50, False, 200),
     ("P-4", 20, 20, 20, 10, True, None),
    ("P-4", 30, 30, 30, 10, True, None),
    ("P-5", 80, 80, 80, 90, True, None)
]

# Convert to DataFrames
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
    # Return all rotations
    return rotations

# Algorithm to allocate packages to ULDs using dynamic packing, greedy heuristic, and rotation
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

    # Sort packages using weight-to-volume ratio and then by size
    package_df["Weight_to_Volume_Ratio"] = package_df["Weight"] / (package_df["Length"] * package_df["Width"] * package_df["Height"])
    package_df = package_df.sort_values(by=["Type", "Weight_to_Volume_Ratio", "Weight", "Length", "Width", "Height"], ascending=[False, False, False, False, False, False])

    allocations_result = []
    
    # Allocate packages
    for _, package in package_df.iterrows():
        package_volume = package["Length"] * package["Width"] * package["Height"]
        package_weight = package["Weight"]
        package_rotations = rotate_package(package)

        allocated = False
        for uld in sorted(allocations, key=lambda uld: (remaining_space[uld]["Volume"], remaining_space[uld]["Weight"]), reverse=True):
            uld_remaining = remaining_space[uld]

            # Check if package fits within ULD's remaining space and weight limit
            if uld_remaining["Volume"] >= package_volume and uld_remaining["Weight"] >= package_weight:
                # Try to fit package into the ULD with rotation possibilities
                placed = False
                for rotation in package_rotations:
                    p_length, p_width, p_height = rotation
                    
                    # Try different positions in the ULD (more adaptive packing)
                    for x in range(0, uld_remaining["Length"] - p_length + 1):
                        for y in range(0, uld_remaining["Width"] - p_width + 1):
                            for z in range(0, uld_remaining["Height"] - p_height + 1):
                                # Check if the package fits at this (x, y, z) position
                                if (x + p_length <= uld_remaining["Length"] and 
                                    y + p_width <= uld_remaining["Width"] and
                                    z + p_height <= uld_remaining["Height"]):
                                    
                                    # Check for overlap with other packages already placed
                                    overlap = False
                                    for pos, dims in occupied_positions[uld]:
                                        if (x < pos[0] + dims[0] and x + p_length > pos[0] and
                                            y < pos[1] + dims[1] and y + p_width > pos[1] and
                                            z < pos[2] + dims[2] and z + p_height > pos[2]):
                                            overlap = True
                                            break
                                    
                                    if not overlap:
                                        # No overlap, so place the package here
                                        allocations[uld].append(package["Package_ID"])
                                        remaining_space[uld]["Volume"] -= package_volume
                                        remaining_space[uld]["Weight"] -= package_weight
                                        positions[uld].append((package["Package_ID"], (x, y, z)))
                                        
                                        # Update occupied positions
                                        occupied_positions[uld].append(((x, y, z), (p_length, p_width, p_height)))
                                        
                                        # Record the result with corners
                                        x1, y1, z1 = x + p_length, y + p_width, z + p_height
                                        allocations_result.append((package["Package_ID"], uld, (x, y, z), (x1, y1, z1)))
                                        placed = True
                                        allocated = True
                                        break
                            if placed:
                                break
                        if placed:
                            break
                    if placed:
                        break
                if allocated:
                    break  # Move to the next package once allocated
        
        # If not allocated, add it to the result with ULD ID as None
        if not allocated:
            allocations_result.append((package["Package_ID"], None, None, None))

    return allocations_result

# Fit the packages to the ULDs and get positions
allocations_result = fit_packages_to_uld(uld_df, package_df)


print("Package Allocations to ULDs, Positions, and Corners:")
for result in allocations_result:
    package_id, uld_id, (x0, y0, z0), (x1, y1, z1) = result
    if uld_id is None:
        print(f"Package {package_id} could not be allocated to any ULD.")
    else:
        print(f"Package {package_id} allocated to ULD {uld_id} at position (x0, y0, z0) = ({x0}, {y0}, {z0}), "
              f"diagonally opposite corner (x1, y1, z1) = ({x1}, {y1}, {z1})")
