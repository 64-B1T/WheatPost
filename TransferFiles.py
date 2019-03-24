import os

def MoveTemp(user1, user2):
    if not ((isinstance(user1, str)) and (isinstance(user2, str))):
        print("Invalid Input")
        return -1

    dir_path = os.path.dirname(os.path.realpath(__file__))
    dirA = os.path.join(dir_path, user1)
    dirB = os.path.join(dir_path, user2)
    if not os.path.exists(dirA):
        os.makedirs(dirA)
    if not os.path.exists(dirB):
        os.makedirs(dirB)

    files = os.listdir(dirA)
    for file in files:
        f_A = os.path.join(dirA, file)
        f_B = os.path.join(dirB, file)
        os.rename(f_A, f_B)


    return 1
