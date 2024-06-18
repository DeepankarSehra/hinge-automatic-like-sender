import os
import shutil

print(len(os.listdir('profile_elements')))

folder_path = 'profile_elements'
for i in range(len(os.listdir(folder_path))):
    os.rename(os.path.join(folder_path) + '/' + os.listdir('profile_elements')[i], os.path.join(folder_path) + f'/element_{i}.png')