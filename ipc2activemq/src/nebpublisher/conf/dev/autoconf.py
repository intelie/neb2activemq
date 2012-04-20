import topics
import re
import sys

def parse_regexps(properties, regexp):
  final_list = list()
  final_list.append(("host", "STRING", "IDENTIFIER"))
  final_list.append(("downtime", "INT", "VALUE"))

  #regexp to capture everything that's surrounded by parenthesis
  group_regex = re.compile(r'((?<!\\)\(.+?\))')
  matched_groups = group_regex.findall(regexp)

  if len(matched_groups) != len(properties):
      print "Different number of properties"
      print "Aborting..."
      sys.exit(-1)

  for i, value in enumerate(matched_groups):
    if 'OK' in value or "WARNING" in value or "CRITICAL" in value:
      final_list.append((properties[i], "STRING", "VALUE"))
      continue
    if '.+' in value:
      final_list.append((properties[i], "STRING", "VALUE"))
      continue
    if '[\d.]+' in value:
      final_list.append((properties[i], "FLOAT", "VALUE"))
      continue
    if '\d' in value:
      final_list.append((properties[i], "INT", "VALUE"))
      continue
  return final_list

def write_file(final_list, filename):
  
  file = open('files/' + filename + '.py', 'w')
  string = "PROPERTIES = %s" % final_list
  print >> file, string
  file.close()
  
