import autoconf
import topics


def main():
  
  keys_list = topics.expressions.keys()
  for i in range(len(keys_list)):
    final_list = autoconf.parse_regexps(topics.expressions[keys_list[i]][0]['regexps'][0]['properties'], topics.expressions[keys_list[i]][0]['regexps'][0]['regexp'])
    autoconf.write_file(final_list, keys_list[i])
