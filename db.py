import dataset
import os

APP_ROOT = os.path.dirname(os.path.abspath(__file__))   # refers to application_top
ROOT_FOLDER = os.path.join(APP_ROOT, 'database')

db= dataset.connect('sqlite:///'+ROOT_FOLDER+'.db?check_same_thread=False')

table_meme = db['meme']
