import random

class Page:
    def __init__(self, page_num, pid):
        self.page_num = page_num
        self.pid = pid
        self.referenced = False

class Process:
    def __init__(self, pid, pages):
        self.pid = pid
        self.pages = pages

class Kernel:
    def __init__(self, num_frames):
        self.num_frames = num_frames
        self.physical_memory = [None] * num_frames
        self.clock_hand = 0

    def simulate(self, processes):
        for process in processes:
            for page in process.pages:
                self.handle_memory_access(process.pid, page.page_num)

    def handle_memory_access(self, pid, page_num):
        frame = self.find_page_frame(pid, page_num)

        if frame is None:
            frame = self.get_free_frame()
            if frame is None:
                frame = self.evict_page()
            self.physical_memory[frame] = Page(page_num, pid)
        else:
            self.physical_memory[frame].referenced = True

        print(f"Process {pid} accessed page {page_num}, which is mapped to frame {frame}")

    def find_page_frame(self, pid, page_num):
        for i, page in enumerate(self.physical_memory):
            if page is not None and page.pid == pid and page.page_num == page_num:
                return i
        return None

    def get_free_frame(self):
        for i, page in enumerate(self.physical_memory):
            if page is None:
                return i
        return None

    def evict_page(self):
        while True:
            page = self.physical_memory[self.clock_hand]
            if page.referenced:
                page.referenced = False
            else:
                return self.clock_hand
            self.clock_hand = (self.clock_hand + 1) % self.num_frames

# Запуск симуляції
process1 = Process(1, [Page(0, 1), Page(1, 1), Page(2, 1), Page(3, 1), Page(4, 1)])
process2 = Process(2, [Page(0, 2), Page(1, 2), Page(2, 2), Page(3, 2), Page(4, 2)])

kernel = Kernel(3)
kernel.simulate([process1, process2])

