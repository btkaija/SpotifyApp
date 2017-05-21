import shutil, os

os.chdir("A:")

path = r"Playlists\2013.m3u"

new_path = r"2013.m3u"

print ("copying a file with path", path, "to", new_path)

shutil.copy2(path, new_path)
