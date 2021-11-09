from .request import (
    get_all_animals, 
    get_single_animal, 
    create_animal, 
    delete_animal, 
    update_animal, 
    get_animal_by_status, 
    get_animals_by_location_id)

# ⭕️⭕️⭕️  this file is usually empty. (only has imports,)
# __init__ acts as a keyword, it tells python you can import from this directory. 即 this is a python package.
# it gathers all the imports so that you can import them in the main file.