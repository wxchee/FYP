import sys
from time import sleep, time
from shared import aMag, getRotMag

# record acceleration data during casual movements
# def run():
    # DURATION = 10
    # print('{} seconds acceleration data'.format(DURATION))
    # accT = 0
    # prevT = time()
    # while (True):
    #     print(aMag.value)
    #     sys.stdout.flush()
        
    #     accT += time() - prevT
    #     prevT = time()
        
    #     if accT > DURATION:
    #         print('end record')
    #         break
        
    #     sleep(0.02) # using the same pause interval as control.py
    
    # return 0

# record acceleration data during mode switch action
# def run():     
#     while True:
#         if (aMag.value > 1.5):
#             dp = 0
#             while dp < 100:
#                 print(aMag.value)
#                 sys.stdout.flush()
#                 dp = dp+1

#                 sleep(0.02)
#         sleep(0.02)

    
#     return 0

# record rotation magnitude during casual movement
# def run():     
#     while True:
#         dp = 0
#         while dp < 200:
#             print(getRotMag())
#             sys.stdout.flush()
#             dp = dp+1

#             sleep(0.02)
#         sleep(0.02)

    
#     return 0

# record rotation magnitude during twist movement
def run():     
    while True:
        dp = 0
        if getRotMag() > 6:
            while dp < 200:
                print(getRotMag())
                sys.stdout.flush()
                dp = dp+1

                sleep(0.02)
        sleep(0.02)

    
    return 0