import ipaddress

# Define the paths to the input and output files
input_file_path = r'OriginalIPList.txt'
similar_ips_file_path = r'SimilarIPs.txt'
similar_cidrs_file_path = r'SimilarCIDRs.txt'

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

# Group similar IP addresses and CIDRs together
print("Grouping similar IP addresses and CIDRs together...")
similar_groups = []
cidr_groups = []
for ip_object in ip_objects:
    if isinstance(ip_object, ipaddress.IPv4Address):
        group_found = False
        for group in similar_groups:
            if isinstance(group[0], ipaddress.IPv4Address) and \
                    str(ip_object)[:-2] == str(group[0])[:-2]:
                group.append(ip_object)
                group_found = True
                break
        if not group_found:
            similar_groups.append([ip_object])
    else:
        group_found = False
        for group in cidr_groups:
            if group[0].supernet() == ip_object.supernet():
                group.append(ip_object)
                group_found = True
                break
        if not group_found:
            cidr_groups.append([ip_object])

# Write the similar IP addresses to the SimilarIPs.txt file
print(f"Writing similar IP addresses to {similar_ips_file_path}...")
with open(similar_ips_file_path, 'w', encoding='utf-8') as similar_ips_file:
    for group in similar_groups:
        if len(group) > 1:
            similar_ips_file.write(f"IP Addresses Similar to [{str(group[0])}]:\n")
            similar_ips_file.write('\n'.join([f"- {str(ip_object)}" for ip_object in group]))
            similar_ips_file.write('\n\n')
print(f"Done writing similar IP addresses to {similar_ips_file_path}!")

# Write the similar CIDRs to the SimilarCIDRs.txt file
print(f"Writing similar CIDRs to {similar_cidrs_file_path}...")
with open(similar_cidrs_file_path, 'w', encoding='utf-8') as similar_cidrs_file:
    for group in cidr_groups:
        if len(group) > 1:
            similar_cidrs_file.write(f"IP CIDRs Similar to [{str(group[0])}]:\n")
            similar_cidrs_file.write('\n'.join([f"- {str(ip_object)}" for ip_object in group]))
            similar_cidrs_file.write('\n\n')
print(f"Done writing similar CIDRs to {similar_cidrs_file_path}!")
