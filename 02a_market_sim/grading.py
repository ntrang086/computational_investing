"""MLT - Grading components (based on pytest fixtures).

Note: Writes results to "comments.txt" in current working directory.

Copyright 2017, Georgia Tech Research Corporation
Atlanta, Georgia 30332-0415
All Rights Reserved
"""

import pytest
import signal
from collections import namedtuple
from contextlib import contextmanager
import multiprocessing
import sys,traceback

timeout_manager = multiprocessing.Manager()

GradeResult = namedtuple('GradeResult', ['outcome', 'points', 'msg'])

class IncorrectOutput(Exception): pass

class TimeoutException(Exception): pass

class Grader(object):
    """Main grader class; an instance of this is passed in through a pytest fixture."""

    def __init__(self, max_points=None, html_pre_block=False):
        self.max_points = max_points
        self.html_pre_block = html_pre_block
        self.total_points = 0.0
        self.results = []
        self.performance = None

    def add_result(self, result):
        self.results.append(result)
        self.add_points(result.points)

    def add_points(self, points):
        self.total_points += points

    def add_performance(self,perf):
        if self.performance is None:
            self.performance = perf
        else:
            self.performance = self.performance + perf

    def summary(self):
        num_tests = len(self.results)
        max_points = self.max_points if self.max_points is not None else float(num_tests)
        tests_passed = len([result for result in self.results if result.outcome == 'passed'])
        # (BPH) return "Total points: {} out of {}\nTests passed: {} out of {}".format(self.total_points, max_points, tests_passed, num_tests)
        # (BPH) Removing points earned from comments.txt output as part
        # (BPH) of the autograder -> "test suite" move
        return "Tests passed: {} out of {}".format(tests_passed, num_tests)

    def details(self):
        # (BPH) return "\n".join("Test #{}: {}, points earned: {}{}".format(i, self.results[i].outcome, self.results[i].points, (("\n" + self.results[i].msg + "\n") if self.results[i].msg is not None else "")) for i in range(len(self.results)))
        # (BPH) Removing point's earned from comments.txt output as part
        # (BPH) of the autograder->"test suite" move
        return "\n".join("Test #{}: {} {}".format(i, self.results[i].outcome, (("\n" + self.results[i].msg + "\n") if self.results[i].msg is not None else "")) for i in range(len(self.results)))

    def write_points(self, filename="points.txt"):
        print ("[GRADER] Writing points to \"{}\"...".format(filename))  # [debug]
        with open(filename, "w") as f:
            f.write("{}\n".format(self.total_points))
    def write_performance(self,filename="performance.txt"):
        if self.performance is None:
            print ("No performance metric collected, skipping")
        else:
            print ("[GRADER] Writing performance to \"{}\"...".format(filename))
            with open(filename,"w") as f:
                f.write("{}\n".format(self.performance))
    def write_comments(self, filename="comments.txt"):
        # Build comments string
        print ("[GRADER] Writing comments to \"{}\"...".format(filename))  # [debug]
        comments = "--- Summary ---\n" + self.summary() + "\n"
        details = self.details()
        if details:
            comments += "\n--- Details ---\n" + details + "\n"
        print ("\n{}".format(comments))  # [debug]

        # Write to file
        with open(filename, "w") as f:
            if self.html_pre_block:
                f.write("<pre>")
            f.write(comments)
            if self.html_pre_block:
                f.write("</pre>\n")

    def __str__(self):
        return "<{} at {:x}: total_points: {}, #results: {}>".format(self.__class__.__name__, id(self), self.total_points, len(self.results))


@contextmanager
def time_limit(seconds, msg="Exceeded time limit!"):
    """A contextmanager that raises a TimeoutException if execution takes longer than specified time.

    Usage:
        with time_limit(1):
            # do stuff within 1 second

    Note: seconds must be an integer.
    Based on: http://stackoverflow.com/a/601168
    """
    def signal_handler(signum, frame):
        raise (TimeoutException, msg)
    signal.signal(signal.SIGALRM, signal_handler)
    signal.alarm(seconds)
    try:
        yield
    finally:
        signal.alarm(0)


def proc_wrapper(func,rv,pos_args,keyword_args):
    try:
        rv['output'] = func(*pos_args,**keyword_args)
    except Exception as e:
        rv['exception'] = e
        rv['traceback'] = traceback.extract_tb(sys.exc_info()[2])

def run_with_timeout(func,timeout_seconds,pos_args,keyword_args):
    rv_dict = timeout_manager.dict()
    p = multiprocessing.Process(target=proc_wrapper,args=(func,rv_dict,pos_args,keyword_args))
    p.start()
    p.join(timeout_seconds)
    if p.is_alive():
        p.terminate()
        raise TimeoutException("Exceeded time limit!")
    if not('output' in rv_dict):
        if 'exception' in rv_dict:
            e = rv_dict['exception']
            e.grading_traceback=None
            if 'traceback' in rv_dict:
                e.grading_traceback = rv_dict['traceback']
            raise e
        raise Exception('Unknown Exception')
    return rv_dict['output']

# Test fixtures
@pytest.fixture(scope="module")
def grader(request):
    """A module-level grading fixture."""
    max_points = getattr(request.module, "max_points", None)  # picked up from test module, if defined
    html_pre_block = getattr(request.module, "html_pre_block", False)  # surround with HTML <pre> tag?
    #print "[GRADER] max_points: {}".format(max_points)  # [debug]
    _grader = Grader(max_points=max_points, html_pre_block=html_pre_block)  # singleton
    def fin():
        _grader.write_points()
        _grader.write_comments()
        _grader.write_performance()
        print ("[GRADER] Done!")  # [debug]
    request.addfinalizer(fin)
    return _grader
