import topics
import re

def check_known_properties(properties)
    
    #is this really necessary?
  for i in range(len(properties)):
    

def parse_unknown_properties(properties, regexp):
  
  final_list = list()

  #regexp to capture everything that's surrounded by parenthesis
  group = re.compile('(\(.+?\))')
  matched_groups = group.findall(regexp)
  
  for i in range(len(matched_groups)):
    if matched_groups[i].find('OK') or matched_groups[i].find('WARNING') or
    matched_groups[i].find('CRITICAL'):
      final_list.append((properties[i], "STRING", "VALUE"))
      continue
    if matched_groups[i].find('.+'):
      final_list.append((properties[i], "STRING", "VALUE"))
      continue
    if matched_groups[i].find('\d+'):
      final_list.append((properties[i], "INT", "VALUE"))
      continue
    if matched_groups[i].find('[\d.]+'):
      final_list.append((properties[i], "FLOAT", "VAlUE"))
      continue

def write_file(structure):

