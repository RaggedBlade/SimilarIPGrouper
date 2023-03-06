import ipaddress

# Define the paths to the input and output files
input_file_path = r'OriginalIPList.txt'
output_file_path = r'SimilarIPs.txt'

# Read in the IP addresses from the input file
print(f"Reading IP addresses from {input_file_path}...")
with open(input_file_path, 'r', encoding='utf-8') as input_file:
    ip_blocks = [line.split()[0] for line in input_file.readlines() if not line.startswith('#')]

# Convert the IP addresses to ipaddress objects for easier comparison
print("Converting IP addresses to ipaddress objects...")
ip_objects = []
for ip_block in ip_blocks:
    if '/' in ip_block:
        ip_objects.append(ipaddress.IPv4Network(ip_block, strict=False))
    else:
        ip_objects.append(ipaddress.IPv4Address(ip_block))

# Group similar IP addresses together
print("Grouping similar IP addresses together...")
similar_groups = []
for ip_object in ip_objects:
    group_found = False
    for group in similar_groups:
        if isinstance(ip_object, ipaddress.IPv4Address) and isinstance(group[0], ipaddress.IPv4Address) and \
                str(ip_object)[:-2] == str(group[0])[:-2]:
            group.append(ip_object)
            group_found = True
            break
        elif isinstance(ip_object, ipaddress.IPv4Network) and isinstance(group[0], ipaddress.IPv4Network) and \
                ip_object.supernet().subnet_of(group[0].supernet()):
            group.append(ip_object)
            group_found = True
            break
    if not group_found:
        similar_groups.append([ip_object])

# Write the similar IP addresses to the output file
print(f"Writing similar IP addresses to {output_file_path}...")
with open(output_file_path, 'w', encoding='utf-8') as output_file:
    for group in similar_groups:
        if len(group) > 1:
            output_file.write(f"IP Addresses Similar to [{str(group[0])}]:\n")
            output_file.write('\n'.join([f"- {str(ip_object)}" for ip_object in group]))
            output_file.write('\n\n')
print("Done!")
