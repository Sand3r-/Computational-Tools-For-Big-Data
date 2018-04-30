from threading import Thread, Semaphore
import time
import random
from multiprocessing import Queue
from queue import Empty
from multiprocessing import cpu_count
import sqlite3
import cProfile

num_workers = cpu_count() - 1
# num_workers = 4

# kill python taskkill /IM python.exe /F

queue = Queue()
stop = False
list_of_word_sets = [set()] * (num_workers)
# worker_done = [Semaphore()] * (num_workers) # TOnDO - never do this again ffs
worker_done = []
for i in range(num_workers):
    worker_done.append(Semaphore())
cmt_available = Semaphore(0)

class ProducerThread(Thread):
    def __init__(self):
      Thread.__init__(self)
      self.query_sub =  """SELECT id, name FROM subreddits LIMIT 10"""

    def runx(self):
        cProfile.runctx('self.runx()', globals(), locals(), 'profile-%s.prof' % "Producer")

    def run(self):
        self.conn = sqlite3.connect("reddit.db")
        global queue
        global worker_done
        for id, name in self.conn.execute(self.query_sub):
            self.query_com = "SELECT body FROM comments WHERE subreddit_id='" + str(id) + "'"
            comment_pack = []
            for body in self.conn.execute(self.query_com):
                comment_pack.append(body[0])
                if len(comment_pack) > 200:
                    queue.put_nowait(comment_pack)
                    comment_pack = []
                    cmt_available.release()
            if len(comment_pack) > 0:
                queue.put(comment_pack)
                cmt_available.release()

            while not queue.empty():
                pass

            for i in range(num_workers):
                worker_done[i].acquire()

            final_set = set()
            print(id, name, len(final_set.union(*list_of_word_sets)))

            for i in range(len(list_of_word_sets)):
                list_of_word_sets[i] = set()

            for i in range(num_workers):
                worker_done[i].release()

        global stop
        stop = True
        for i in range(num_workers):
            queue.put([])
            cmt_available.release()

        print("Producer finished")


class ConsumerThread(Thread):

    def __init__(self, threadID):
      Thread.__init__(self)
      self.threadID = threadID

    def runx(self):
        cProfile.runctx('self.runx()', globals(), locals(), 'profile-%s.prof' % self.threadID)

    def run(self):
        global queue
        symbols = ['\n','`','~','!','@','#','$','%','^','&','*','(',')','_','-','+','=','{','[',']','}','|','\\',':',';','"',"'",'<','>','.','?','/',',']
        global worker_done
        while not stop:
            cmt_available.acquire()
            worker_done[self.threadID].acquire()
            comments = queue.get() # This prolly takes long af.
            words = set()
            for comment in comments:
                comment = comment.lower()
                for sym in symbols:
                    comment = comment.replace(sym, " ")
                words = words.union(comment.split(" "))
            words.discard('')

            list_of_word_sets[self.threadID] = list_of_word_sets[self.threadID].union(words)
            worker_done[self.threadID].release()


producerThread = ProducerThread()

producerThread.start()

threads = []
for i in range(num_workers):
    threads.append(ConsumerThread(i))

for thread in threads:
    thread.start()


for thread in threads:
    thread.join()

print("I'm after thread joins")

producerThread.join()

print("I'm after producer join")