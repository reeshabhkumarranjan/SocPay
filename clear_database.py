import os
from glob import glob

def clear():
    confirm = input("Are you sure to continue? (y/n)")
    if confirm.lower() == "y":
        for file in glob('*/migrations/000*.py'):
            print("removing", str(file))
            os.remove(file)

        db_path = "db.sqlite3"
        print("removing", db_path)
        os.remove(db_path)
    else:
        print("Canceling operation")

