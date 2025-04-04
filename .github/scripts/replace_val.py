# Prerequisite: pip install ruamel.yaml.string 

# This script is used to promote generic Yaml Paths.

import os
from sde import collection,sde


#Dev Base Path
dev_path=os.getenv('FROM_PATH',default="")
#dev_path='apps/perf-controller-manager/overlays/dev/dev_base/kustomization.yaml'

#Prod Base Path
prod_path=os.getenv('TO_PATH')
#prod_path='apps/perf-controller-manager/base/kustomization.yaml'


property_path=os.getenv('PROP_PATH')
#property_path='images.0.newTag'

starts_with=os.getenv('PROMOTE_VERSION_PREFIX',default='')
#starts_with='j'



data_out = collection.DottedDict(sde.read_file(prod_path,'YAML'))
data_in = collection.DottedDict(sde.read_file(dev_path,'YAML'))

try:
    data_in_val=str(data_in[property_path])
    print(data_in_val)
except KeyError:
    raise ValueError('{} is not present in {}'.format(property_path, data_in))
if data_in_val.startswith(starts_with):
  print(f"value contains pattern {starts_with}")
  try:
    data_out[property_path]=data_in_val
  except KeyError:
    raise ValueError('{} is not present in {}'.format(property_path, data_out))
  sde.write_file(prod_path,"YAML",data_out)
else:
   print(f"value does not contain pattern {starts_with}") 
