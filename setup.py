from setuptools import find_packages, setup
from typing import List

HED = '-e .'
def get_requirements(file_path: str)->List[str]:
    
    ''' This function is designed to return the list of requirements '''
    
    with open('requirements.txt') as file_obj:
        reqs = file_obj.readlines()
        reqs = [r.replace("\n", "") for r in reqs]
        
        if HED: 
            reqs.remove(HED)
    return reqs                
        
setup(
    name = 'dsproject',
    version = '0.0.1',
    description = "An attempt to build an impactful DS Project",
    author = "Zaid Roshan Mayers",
    author_email = "zaidmayers@gmail.com",
    packages = find_packages(),
    install_requires=get_requirements('requirements.txt'),
)