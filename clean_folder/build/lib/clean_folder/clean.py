import sys
from pathlib import Path
import re
import shutil

CATEGORIES = {'audios':['.mp3', '.wma', '.ogg'], 'images':['.png', '.jpg', '.jpeg'],
 'documents':['.doc', '.docx', '.txt', '.xlsx', '.pptx'], 
 'video':['.avi', '.mp4', '.mov', '.mkv'], 'archives':['.zip', '.gz', '.tar', '.rar'], 'unknown':[]}

def normalize(file_name):
    CYRILLIC_SYMBOLS = "абвгдеёжзийклмнопрстуфхцчшщъыьэюяєіїґ"
    TRANSLATION = ("a", "b", "v", "g", "d", "e", "e", "j", "z", "i", "j", "k", "l", "m", "n", "o", "p", "r", "s", "t", "u",
               "f", "h", "ts", "ch", "sh", "sch", "", "y", "", "e", "yu", "u", "ja", "je", "ji", "g")
    
    TRANS = {}
    for c, t in zip(CYRILLIC_SYMBOLS, TRANSLATION):
      TRANS[ord(c)] = t
      TRANS[ord(c.upper())] = t.upper()
    pre_norm_file_name = file_name.translate(TRANS)      
    pre_norm_file_name_split = re.split('\.', pre_norm_file_name)    
    norm_file_name_0 = ''
    for i in pre_norm_file_name_split[0]:      
        p = re.sub('\W', '_', i)
        norm_file_name_0 += p
    norm_file_name = f'{norm_file_name_0}.{pre_norm_file_name_split[1]}'
    return norm_file_name


def move_file(file:Path, root_dir:Path, category:str):
    if category == 'unknown':
        return file.replace(root_dir.joinpath(file.name))
    target_dir = root_dir / category
    
    if not target_dir.exists():
        target_dir.mkdir()
    return file.replace(target_dir / normalize(file.name))

def get_categories(file:Path):
    extension = file.suffix.lower()
    for cat, exts in CATEGORIES.items():
        if extension in exts:
            return cat
    return 'unknown'

def sort_dir(root_dir:Path, current_dir=Path):

    for item in [f for f in current_dir.glob('*') if f.name not in CATEGORIES.keys()]:
        if not item.is_dir():
            category = get_categories(item)
            new_path = move_file(item, root_dir, category)
            print(new_path)
        else:
            sort_dir(root_dir, item)
            item.rmdir()

def main():
    try:
        path = Path(sys.argv[1])
        #return "OK"
    except IndexError:
        return f"No path to folder"

    if not path.exists():
        return "Sorry, folder is not exist"

    sort_dir(path, path)

    return "All Ok"

if __name__ == "__main__":
    print(main())    