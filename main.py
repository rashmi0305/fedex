import pandas as pd
import csv

# Function to load data
def load_data():
    try:
        uld_df = pd.read_csv("C:\\Users\\rashm\\OneDrive\\Documents\\Fedex\\fedex\\uld.csv")
        package_df = pd.read_csv("C:\\Users\\rashm\\OneDrive\\Documents\\Fedex\\fedex\\packages.csv")
        config_df = pd.read_csv("C:\\Users\\rashm\\OneDrive\\Documents\\Fedex\\fedex\\config.csv")
        
        # Load K value from the config file
        K = config_df.loc[0, "K"]
        
        return uld_df, package_df, K
    except FileNotFoundError as e:
        print(f"Error: {e}")
        return None, None, None

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
# Greedy Algorithm to allocate packages to ULDs using rotation and overlap checking
def fit_packages_to_uld(uld_df, package_df):
    allocations = {uld: [] for uld in uld_df["ULD_ID"]}  # Initialize allocations dictionary
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

    # Sort packages by type (priority first), then by weight and volume for better packing
    package_df["Volume"] = package_df["Length"] * package_df["Width"] * package_df["Height"]
    package_df = package_df.sort_values(by=["Type", "Weight", "Volume"], ascending=[False, False, True])
    
    allocations_result = []

    # Allocate packages
    for _, package in package_df.iterrows():
        package_volume = package["Volume"]
        package_weight = package["Weight"]
        package_rotations = rotate_package(package)

        allocated = False  # Track if package is allocated
        for uld in allocations.keys():  # Iterate through ULDs in order
            uld_remaining = remaining_space[uld]

            # Check if package fits within ULD's remaining space and weight limit
            if uld_remaining["Volume"] >= package_volume and uld_remaining["Weight"] >= package_weight:
                for rotation in package_rotations:
                    p_length, p_width, p_height = rotation

                    # Check position in ULD
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
                                        # Allocate the package
                                        remaining_space[uld]["Volume"] -= package_volume
                                        remaining_space[uld]["Weight"] -= package_weight
                                        occupied_positions[uld].append(((x, y, z), rotation))
                                        allocations[uld].append(package["Package_ID"])
                                        allocations_result.append((package["Package_ID"], uld, (x, y, z), 
                                                                   (x + p_length, y + p_width, z + p_height)))
                                        allocated = True
                                        break  # Stop once allocated
                            if allocated:
                                break  # Stop Y-loop
                        if allocated:
                            break  # Stop X-loop
                    if allocated:
                        break  # Stop Rotation-loop
            if allocated:
                break  # Stop ULD-loop

        # If not allocated, record package with ULD as None
        if not allocated:
            allocations_result.append((package["Package_ID"], None, (-1, -1, -1), (-1, -1, -1)))

    return allocations_result


# Overlap checking
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

# Save results to CSV files
# Save results to CSV files
def save_results(allocations_result, K, priority_package_ids):
    # Convert Position_Start and Position_End into clean strings (without extra quotes)
    for i in range(len(allocations_result)):
        allocations_result[i] = (
            allocations_result[i][0],  # Package_ID
            allocations_result[i][1],  # ULD_ID
            f"({allocations_result[i][2][0]}, {allocations_result[i][2][1]}, {allocations_result[i][2][2]})",  # Position_Start
            f"({allocations_result[i][3][0]}, {allocations_result[i][3][1]}, {allocations_result[i][3][2]})"   # Position_End
        )

    # Create the allocations DataFrame
    allocations_df = pd.DataFrame(allocations_result, columns=["Package_ID", "ULD_ID", "Position_Start", "Position_End"])

    # Save the allocations DataFrame to CSV with proper quoting for tuple columns
    allocations_df.to_csv("allocations_result.csv", quoting=csv.QUOTE_MINIMAL)

    # Calculate priority package statistics
    priority_uld_count = len(set([uld for package_id, uld, _, _ in allocations_result if package_id in priority_package_ids and uld is not None]))
    cost_delay = K * priority_uld_count

    # Create a summary DataFrame for priority package statistics
    summary_data = [
        ["Number of ULDs with priority packages", priority_uld_count],
        ["Cost-Delay", cost_delay]
    ]
    summary_df = pd.DataFrame(summary_data, columns=["Metric", "Value"])

    # Save the summary DataFrame to CSV
    summary_df.to_csv("priority_package_summary.csv", index=False)

    print(f"Results saved to 'allocations_result.csv'.")
    print(f"Summary saved to 'priority_package_summary.csv'.")

# Main function to run the program
def main():
    uld_df, package_df, K = load_data()
    
    # If data is missing, return early
    if uld_df is None or package_df is None or K is None:
        print("Data loading failed. Exiting.")
        return
    
    # Perform the allocation
    allocations_result = fit_packages_to_uld(uld_df, package_df)
    
    # Get the list of priority package IDs
    priority_package_ids = package_df[package_df['Type'] == "priority"]['Package_ID'].tolist()
    
    # Check for overlaps in the allocations
    overlaps = check_for_overlaps(allocations_result)
    if overlaps:
        print(f"Overlaps found: {overlaps}")
    else:
        print("No overlaps detected.")
    
    # Save the results
    save_results(allocations_result, K, priority_package_ids)

if __name__ == "__main__":
    main()
