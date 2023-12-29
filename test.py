import os
import threading
import multiprocessing
import subprocess
import time
import ctypes
import psutil

TIMEOUT = 20 #s



class Problemo:
    def __init__(self, problem_path, input_path, output_path):
        self.problem_path = problem_path
        self.input_path = input_path
        self.output_path = output_path
        self.status = {}

    def execute(self):
        self.status["t0"] = time.time()
        input_file = open(self.input_path)
        output_file = open(self.output_path, 'x')
        sbp = subprocess.Popen(["./tmp/x"], stdin=input_file, stdout=output_file)
        output_file.close()
        input_file.close()

        pid = sbp.pid
        self.status["memory"] = 0
        while sbp.poll() is None and time.time() - self.status["t0"] <= TIMEOUT:
            cur_mem = psutil.Process(sbp.pid).memory_info().rss / (1024**2)
            self.status["memory"] = max(self.status["memory"],  cur_mem)
        if sbp.returncode is None:
            sbp.kill()
            sbp.poll()
        self.status["t1"] = time.time()
        self.status["exitcode"] = sbp.returncode


competitions = os.listdir("src")

def verify(judge_out):
    user_out = open("tmp/user_out").readlines()
    judge_out = open(judge_out).readlines()

    error = False
    where = None
    if len(user_out) != len(judge_out):
        error = True
    for (id, (u, j)) in enumerate(zip(user_out, judge_out)):
        if(u != j):
            error = True
            where = id
    if error:
        if where is None:
            where = min(len(user_out), len(judge_out)) + 1
        print("\t\tWA on line "+str(where))
    else:
        print("\t\tAC")

def test_file(comp, problem, inp, out):
    print("Verify "+problem)
    print("\tCompiling " + problem)
    if not os.path.exists("tmp"):
        os.system("mkdir tmp")
    if os.path.exists("tmp/user_out"):
        os.system("rm tmp/user_out")
    if os.path.exists("tmp/x"):
        os.system("rm tmp/x")
    os.system("g++ "+problem+" -o tmp/x")
    print("\tRunning " + inp)
    
    pb = Problemo(problem, inp, "tmp/user_out")
    pb.execute()

    process_status = pb.status

    if process_status["t1"] == 0:
        print("\t\tTime limit")
        return
    # even if you use more than 1 Gb, still gives you feedback of Ac or Wa
    if process_status["memory"] > 1024:
        print("\t\tMemory limit")

    if process_status["exitcode"] != 0:
        print("\t\tRuntime Error")
        return

    duration = process_status["t1"] - process_status["t0"]
    memory = process_status["memory"]
    print("\t\tTime of Execution = " + str(round(duration, 4)))
    print("\t\tMemory used = " + str(round(memory, 4)) + " Mb")
    verify(out)


for comp in competitions:
    path_to_problems = os.path.join("src", comp)
    problems = os.listdir(path_to_problems)

    for problem in problems:
        problem_base_name = os.path.splitext(problem)[0]
        test_path = os.path.join("tests", comp)
        problem_path = os.path.join("src", comp, problem)
        inp_path = os.path.join(test_path, problem_base_name + ".in")
        out_path = os.path.join(test_path, problem_base_name + ".out")

        if(os.path.exists(inp_path)):
            test_file(comp, problem_path, inp_path, out_path)

