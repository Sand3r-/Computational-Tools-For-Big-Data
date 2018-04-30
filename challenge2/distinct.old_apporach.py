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
# peewee

queue = Queue()
cursor = None;
stop = False
list_of_word_sets = [set()] * (num_workers)
# worker_done = [Semaphore()] * (num_workers) # TOnDO - never do this again ffs
worker_done = []
for i in range(num_workers):
    worker_done.append(Semaphore())
cmt_available = Semaphore(0)
subreddit_finished = Semaphore(0)
cursor_lock = Semaphore(0)

class ProducerThread(Thread):
    def __init__(self):
      Thread.__init__(self)
      self.query_sub =  """SELECT id, name FROM subreddits LIMIT 10"""

    def runx(self):
        cProfile.runctx('self.runx()', globals(), locals(), 'profile-%s.prof' % "Producer")

    def run(self):
        self.conn = sqlite3.connect("reddit.db", check_same_thread=False)
        self.cursor = self.conn.cursor()
        global queue
        global worker_done
        global cursor
        for id, name in self.conn.execute(self.query_sub):
            self.query_com = "SELECT body FROM comments WHERE subreddit_id='" + str(id) + "'"
            self.cursor.execute(self.query_com)
            # cursor_lock.acquire()
            cursor = self.cursor
            cursor.execute(self.query_com)
            cursor_lock.release()
            subreddit_finished.acquire()
            # comments = cursor.fetchmany(250)
            # while comments:
            #     queue.put_nowait(comments)
            #     cmt_available.release()
            #     comments = cursor.fetchmany(250)

            # for body in self.conn.execute(self.query_com):
            #     comment_pack.append(body[0])
            #     if len(comment_pack) > 200:
            #         queue.put_nowait(comment_pack)
            #         comment_pack = []
            #         cmt_available.release()
            # if len(comment_pack) > 0:
            #     queue.put(comment_pack)
            #     cmt_available.release()

            while not queue.empty():
                pass

            for i in range(num_workers):
                worker_done[i].acquire()

            if name == "freedonuts":
                with open("old.txt", "w", encoding="utf-8") as f:
                    wrds = list(final_set.union(*list_of_word_sets))
                    for word in wrds:
                        f.write(word + '\n')

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
        global cursor
        global cursor_lock
        while not stop:
            cursor_lock.acquire()
            worker_done[self.threadID].acquire()
            comments = cursor.fetchmany(700)
            if not comments:
                subreddit_finished.release()
                worker_done[self.threadID].release()
                continue
            cursor_lock.release()
            # cmt_available.acquire()
            # worker_done[self.threadID].acquire()
            # comments = queue.get() # This prolly takes long af.
            words = set()
            for comment in comments:
                comment = comment[0].lower()
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