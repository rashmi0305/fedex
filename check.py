def is_overlapping(pkg1, pkg2):
   
    (x0_1, y0_1, z0_1), (x1_1, y1_1, z1_1) = pkg1
    (x0_2, y0_2, z0_2), (x1_2, y1_2, z1_2) = pkg2
    
    # Check if they overlap in the x, y, and z dimensions
    overlap_x = not (x1_1 <= x0_2 or x1_2 <= x0_1)
    overlap_y = not (y1_1 <= y0_2 or y1_2 <= y0_1)
    overlap_z = not (z1_1 <= z0_2 or z1_2 <= z0_1)
    
    # Return True if they overlap in all three dimensions
    return overlap_x and overlap_y and overlap_z

def check_for_overlaps(allocations_result):
    
    # Dictionary to store packages by ULD
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

# Example allocation result (package_id, uld_id, (x0, y0, z0), (x1, y1, z1))
allocations_result = [
    ('P-10', 'U5', (0, 0, 0), (88, 70, 85)),
    ('P-9', 'U6', (0, 0, 0), (73, 71, 88)),
    ('P-2', 'U6', (0, 0, 88), (56, 99, 169)),
    ('P-6', 'U5', (0, 0, 85), (91, 56, 169)),
    ('P-15', 'U6', (0, 0, 169), (84, 49, 229)),
    ('P-3', 'U5', (0, 0, 169), (42, 101, 220)),
    ('P-8', 'U6', (0, 49, 169), (108, 154, 245)),
    ('P-7', 'U5', (0, 70, 0), (88, 148, 93)),
    ('P-4', 'U5', (0, 0, 220), (108, 75, 276)),
    ('P-13', 'U6', (0, 71, 0), (55, 165, 87)),
    ('P-11', 'U5', (0, 101, 93), (55, 181, 174)),
    ('P-12', 'U6', (0, 154, 87), (48, 234, 175)),
    ('P-5', 'U5', (0, 75, 220), (88, 133, 284)),
    ('P-1', 'U6', (0, 99, 87), (99, 152, 142)),
    ('P-14', 'U5', (0, 133, 174), (45, 179, 255)),
]

# Check for overlaps
overlaps = check_for_overlaps(allocations_result)

# Print results
if overlaps:
    print("Overlapping packages found:")
    for uld_id, i, j in overlaps:
        print(f"ULD {uld_id}: Package {allocations_result[i][0]} overlaps with Package {allocations_result[j][0]}")
else:
    print("No overlaps found.")
