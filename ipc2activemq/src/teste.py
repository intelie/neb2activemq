
import os, sys, imp
import re


ENV="dev"

def main():
  
  #read settings module
  conf_dir = os.path.join( os.path.abspath(os.path.dirname(__file__)), "nebpublisher/conf/" + ENV )
  
  topics_path = os.path.join(conf_dir, "topics.py")
  
  print topics_path
  
  
  #read topic expressions
  fin = open(topics_path, 'rb')
  topics = imp.load_source("topics", topics_path, fin)
  
  # compile the regexps once
  for topic in topics.expressions:
    regexp = topic['regexp']
    topic['regexp'] = re.compile(regexp)
  
  event = {'host' : 'teste' }
  
  #for topic in topics.expressions:
  topic = topics.expressions[7]
  print '%s (%s):' % (topic['description'],topic['eventtype'])
  regexp = topic['regexp']
  
  print testeExpression
  m = regexp.match(testeExpression)
  
  i = 1 # first match is the whole expression
  for property in topic['properties']:
      print 'property %s: %s' % (property, m.group(i))
      event[property] = m.group(i)
      i = i + 1
  
  print event
  
if __name__ == "__main__":
    main()
    
    