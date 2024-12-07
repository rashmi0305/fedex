import pandas as pd
import csv

# Function to load data
def load_data():
    try:
        uld_df = pd.read_csv("C:\\Users\\rashm\\OneDrive\\Documents\\Fedex\\fedex\\uld.csv")
        package_df = pd.read_csv("C:\\Users\\rashm\\OneDrive\\Documents\\Fedex\\fedex\\packages1.csv")
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
    total_cost_delay = 0  # Variable to track cost delay for unallocated packages
    placed = 0  # Count how many priority packages are successfully allocated

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

                                        
                                        placed+= 1

                                        break  # Stop once allocated
                            if allocated:
                                break  # Stop Y-loop
                        if allocated:
                            break  # Stop X-loop
                    if allocated:
                        break  # Stop Rotation-loop
            if allocated:
                break  # Stop ULD-loop

        # If not allocated, record package with ULD as None and add cost delay
        if not allocated:
            total_cost_delay += package["Cost_of_Delay"]
            allocations_result.append((package["Package_ID"], None, (-1, -1, -1), (-1, -1, -1)))

    return allocations_result, total_cost_delay, placed


# Save results to CSV files
def save_results(allocations_result, K, cost, placed,priority_allocated_count):
    # Open CSV for writing
    with open("allocations.csv", mode="w", newline='') as file:
        writer = csv.writer(file, quoting=csv.QUOTE_MINIMAL)
        
        # Write the first row with cost and priority_allocated_count
        writer.writerow([ K + cost, placed,priority_allocated_count])
        
        # Write the allocation rows with the new format
        for allocation in allocations_result:
            package_id = allocation[0]
            uld_id = allocation[1]
            # Unpack start and end coordinates directly into integers
            if allocation[1] is not None:
                x_start, y_start, z_start = allocation[2]
                x_end, y_end, z_end = allocation[3]
            else:
                x_start, y_start, z_start = 0, 0, 0
                x_end, y_end, z_end = 0, 0, 0

            # Write in the required format
            writer.writerow([package_id, uld_id, x_start, y_start, z_start, x_end, y_end, z_end])

    print(f"Results saved to 'allocations.csv'.")

# Main function
def main():
    uld_df, package_df, K = load_data()
    if uld_df is None or package_df is None or K is None:
        print("Data loading failed. Exiting.")
        return

    allocations_result, economy_delay, placed = fit_packages_to_uld(uld_df, package_df)
    priority_package_ids = package_df[package_df['Type'] == "Priority"]["Package_ID"].tolist()
    
    priority_uld_count = len(set([uld for package_id, uld, _, _ in allocations_result if package_id in priority_package_ids and uld is not None]))
    cost1 = K * priority_uld_count
    print(priority_uld_count)
    print(cost1)
    save_results(allocations_result, cost1, economy_delay, placed,priority_uld_count)

    # save_results(allocations_result, cost1, total_cost_delay)

if __name__ == "__main__":
    main()