import logging
import time
from time import sleep

last_time = time.time()
start_time = time.time()

#logging.basicConfig(level=logging.DEBUG, filename='time.log', filemode='a', format='%(name)s - %(levelname)s - %(message)s')
logging.basicConfig(level=logging.CRITICAL, filename='data/time.log', filemode='a', format='%(message)s')

# starts the timer for the logging
def log_start():
    global last_time
    global start_time
    t = time.time()
    logging.critical('0.0'+ ' - ' +'start')
    start_time = t
    last_time = t

# logs a message with timeprint
def log_time(message):
    global last_time
    t = time.time()
    logging.critical(str(t-last_time)+ ' - ' +message)
    last_time = t

# logs the time spent til log_start
def log_end():
    logging.critical('time spent: ' + (str(time.time()-start_time)))
    logging.critical('---------------------------------------')

'''example to copy, insert message between the 's

l.log_time('')#logging

'''
'''
log_end()#logging
log_time('a')#logging
sleep(0.05)#logging
log_time('b')#logging
sleep(0.05)#logging
log_time('c')#logging
sleep(0.05)#logging
log_time('d')#logging
sleep(0.05)#logging
log_time('e')#logging
'''
