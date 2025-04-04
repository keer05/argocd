# pip install ruamel.yaml.string 
import os
import ruamel.yaml
from pathlib import Path

path=os.getenv('PCM_CONFIG_PATH')
#path='apps/perf-controller-manager/overlays'
image_name=os.getenv('IMAGE_NAME')
#image_value=os.getenv('IMAGE_VALUE')
dev_folder_path='dev'
prod_folder_path='prod'
allowed_image_tags='main-'


config_set=set()

# Check dev landscapes
for folder in os.listdir(f"{path}/{dev_folder_path}"):
    if (folder == 'dev_base'):
      continue
    file_in = Path(f"{path}/{dev_folder_path}/{folder}/controller-configmap.yaml")
    yaml = ruamel.yaml.YAML(typ=['rt', 'string'])
    yaml.preserve_quotes = True
    data = yaml.load(file_in)
    config_yaml = yaml.load(data['data']['config'])
    #Get image tag
    image_tag=config_yaml['images'][image_name].split(':')[-1]
    # Check if tag contains allowed_image_tags.
    if (image_tag.startswith(allowed_image_tags)):  
       config_set.add(config_yaml['images'][image_name])


# If set has only 1 element, it means the image is uniform
# across all dev landscape. So update prod with the same.
if (len(config_set) == 1):
   image_value=next(iter(config_set))
   print(f"Unique  value for {image_name} :  {image_value}")
   for folder in os.listdir(f"{path}/{prod_folder_path}"):
     
     prod_file_in=Path(f"{path}/{prod_folder_path}/{folder}/controller-configmap.yaml")
     prod_yaml = ruamel.yaml.YAML(typ=['rt', 'string'])
     prod_yaml.preserve_quotes = True
     prod_data = prod_yaml.load(prod_file_in)
     prod_config_yaml = prod_yaml.load(prod_data['data']['config'])
     prod_config_yaml['images'][image_name]=next(iter(config_set))
     prod_data['data']['config'] = ruamel.yaml.scalarstring.LiteralScalarString(prod_yaml.dump_to_string(prod_config_yaml, add_final_eol=True))
     prod_yaml.dump(prod_data, prod_file_in)
elif (len(config_set) > 1):
   print(f"Multiple image value for {image_name}")
else:
   print("No images found")
