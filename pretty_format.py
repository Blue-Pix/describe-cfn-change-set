import json
import sys

class ChangeSet:
  changes = None

  def __init__(self, changes):
    self.changes = changes

  def action(self):
    action = self.changes['ResourceChange']['Action']
    color = ""
    if self.changes['ResourceChange']['Action'] == "Modify":
      color = "<img src=\"https://placehold.it/12/0073bb/0073bb?text=+\" />"
    elif self.changes['ResourceChange']['Action'] == "Add":
      color = "<img src=\"https://placehold.it/12/1d8102/1d8102?text=+\" />"
    elif self.changes['ResourceChange']['Action'] == "Remove":
      color = "<img src=\"https://placehold.it/12/d13212/d13212?text=+\" />"
    return "%s %s" % (color, action)

  def logical_resource_id(self):
    return self.changes['ResourceChange']['LogicalResourceId']

  def physical_resource_id(self):
    if 'PhysicalResourceId' in self.changes['ResourceChange']:
      return self.changes['ResourceChange']['PhysicalResourceId']
    else:
      return "-"

  def resource_type(self):
    return self.changes['ResourceChange']['ResourceType']

  def replacement(self):
    if 'Replacement' in self.changes['ResourceChange']:
      return self.changes['ResourceChange']['Replacement']
    else:
      return "-"

  def details(self):
    arr = []
    for d in self.changes['ResourceChange']['Details']:
      if d['Target']['Attribute'] != 'Properties':
        continue
      arr.append("- %s" % d['Target']['Name'])
    return "<br>".join(arr)


if __name__ == '__main__':
  data = {}
  with open("%s.json" % sys.argv[1]) as f:
    data = json.load(f)

  body = "<h1>Change set</h1><h2>Stack Name: %s</h2><br>" % sys.argv[2]
  
  if len(data['Changes']) > 0:
    body += "<table><tr><th>Action&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;</th><th>ID</th><th>Type</th><th>Replacement</th><th>Changed Properties</th></tr>"
    for c in data['Changes']:
      body += "<tr>"
      change_set = ChangeSet(c)
      body += "<td>%s</td>" % change_set.action()
      body += "<td>%s</td>" % change_set.logical_resource_id()
      # cols.append(change_set.physical_resource_id())
      body += "<td>%s</td>" % change_set.resource_type()
      body += "<td>%s</td>" % change_set.replacement()
      body += "<td>%s</td>" % change_set.details()
      body += "</tr>"
    body += "</table>"
  else:
    body += "no change."
  
  with open("%s.html" % sys.argv[1], mode='w') as f:
    f.write(body)

