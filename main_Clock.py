import random

class Page:
    def __init__(self, pid, page_num):
        self.pid = pid
        self.page_num = page_num

class Process:
    def __init__(self, pid, num_pages):
        self.pid = pid
        self.pages = [Page(pid, i) for i in range(num_pages)]
    
class Kernel:
    def __init__(self, num_frames):
        self.num_frames = num_frames
        self.physical_memory = [None] * num_frames
        self.free_frame_list = list(range(num_frames))
        self.page_table = {}
    
    def get_free_frame(self):
        if not self.free_frame_list:
            self.evict_page()
        frame = self.free_frame_list.pop(0)
        return frame
    
    def evict_page(self):
        frame = random.randint(0, self.num_frames - 1)
        evicted = self.physical_memory[frame]
        del self.page_table[evicted]
        self.physical_memory[frame] = None
        self.free_frame_list.append(frame)
    
    def handle_page_fault(self, pid, page_num):
        if (pid, page_num) in self.page_table.values():
            return
        frame = self.get_free_frame()
        self.physical_memory[frame] = (pid, page_num)
        self.page_table[pid, page_num] = frame
    
    def handle_memory_access(self, pid, page_num):
        if (pid, page_num) not in self.page_table:
            self.handle_page_fault(pid, page_num)
        frame = self.page_table[pid, page_num]
        print(f"Process {pid} accessed page {page_num}, which is mapped to frame {frame}")
    
    def simulate(self, processes):
        for process in processes:
            for page in process.pages:
                self.handle_memory_access(process.pid, page.page_num)

kernel = Kernel(10)
p1 = Process(1, 10)
p2 = Process(2, 10)
p3 = Process(3, 10)
kernel.simulate([p1, p2, p3])
print("Physical memory:", kernel.physical_memory)

