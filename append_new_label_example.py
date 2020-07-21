"""
        Author : Fatih Kahraman
        Mail   : fatih.khrmn@hotmail.com
"""

from class_admin import Admin
from generate_label_data import Upgrader

admin = Admin()

data_generate = Upgrader()

new_label = "oyuncak"

data_generate.setDefaultWord(new_label)
new_data = data_generate.generate()

admin.mode.append_dict(new_label, new_data)
admin.mode.create_data()