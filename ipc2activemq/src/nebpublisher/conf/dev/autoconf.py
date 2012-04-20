import topics
import re

def parse_regexps(properties, regexp):
  
  final_list = list()
  final_list.append(("host", "STRING", "IDENTIFIER"))
  final_list.append(("downtime", "INT", "VALUE"))

  #regexp to capture everything that's surrounded by parenthesis
  group = re.compile('(\(.+?\))')
  matched_groups = group.findall(regexp)
  for i, value in enumerate(matched_groups):
    if 'OK' in value or "WARNING" in value or "CRITICAL" in value:
      final_list.append((properties[i], "STRING", "VALUE"))
      continue
    if '.+' in value:
      final_list.append((properties[i], "STRING", "VALUE"))
      continue
    if '[\d.]+' in value:
      final_list.append((properties[i], "FLOAT", "VAlUE"))
      continue
    if '\d' in value:
      final_list.append((properties[i], "INT", "VALUE"))
      continue
  return final_list

def write_file(final_list, filename):
  
  file = open(filename + '.py', 'w')
  string = "PROPERTIES = %s" % final_list
  print >> file, string
  file.close()
  
