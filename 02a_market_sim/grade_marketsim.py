"""MC2-P1: Market simulator - grading script.

Usage:
- Switch to a student feedback directory first (will write "points.txt" and "comments.txt" in pwd).
- Run this script with both ml4t/ and student solution in PYTHONPATH, e.g.:
    PYTHONPATH=ml4t:MC1-P2/jdoe7 python ml4t/mc2_p1_grading/grade_marketsim.py

Copyright 2017, Georgia Tech Research Corporation
Atlanta, Georgia 30332-0415
All Rights Reserved
"""

import pytest
from grading import grader, GradeResult, time_limit, run_with_timeout, IncorrectOutput

import os
import sys
import traceback as tb

import numpy as np
import pandas as pd
from collections import namedtuple

from grading_util import get_data
from grading_util import get_orders_data_file

# Student code
main_code = "marketsim"  # module name to import

# Test cases
MarketsimTestCase = namedtuple('MarketsimTestCase', ['description', 'group', 'inputs', 'outputs'])
marketsim_test_cases = [
    MarketsimTestCase(
        description="Orders 1",
        group='basic',
        inputs=dict(
            orders_file='orders-01.csv',
            start_val=1000000,
            commission=0.,
            impact=0.
        ),
        outputs=dict(
            num_days = 245 ,
            last_day_portval = 1115569.2,
            sharpe_ratio = 0.612340613407 ,
            avg_daily_ret = 0.00055037432146
        )
    ),
    MarketsimTestCase(
        description="Orders 2",
        group='basic',
        inputs=dict(
            orders_file='orders-02.csv',
            start_val=1000000,
            commission=0.,
            impact=0.
        ),
        outputs=dict(
            num_days = 245 ,
            last_day_portval = 1095003.35,
            sharpe_ratio = 1.01613520942,
            avg_daily_ret = 0.000390534819609
        )
    ),
    MarketsimTestCase(
        description="Orders 3",
        group='basic',
        inputs=dict(
            orders_file='orders-03.csv',
            start_val=1000000,
            commission=0.,
            impact=0.
        ),
        outputs=dict(
            num_days = 240,
            last_day_portval = 857616.0,
            sharpe_ratio = -0.759896272199,
            avg_daily_ret = -0.000571326189931
        )
    ),
    MarketsimTestCase(
        description="Orders 4",
        group='basic',
        inputs=dict(
            orders_file='orders-04.csv',
            start_val=1000000,
            commission=0.,
            impact=0.
        ),
        outputs=dict(
            num_days = 233,
            last_day_portval = 923545.4,
            sharpe_ratio = -0.266030146916,
            avg_daily_ret = -0.000240200768212
        )
    ),
    MarketsimTestCase(
        description="Orders 5",
        group='basic',
        inputs=dict(
            orders_file='orders-05.csv',
            start_val=1000000,
            commission=0.,
            impact=0.
        ),
        outputs=dict(
            num_days = 296,
            last_day_portval = 1415563.0,
            sharpe_ratio = 2.19591520826,
            avg_daily_ret = 0.00121733290744
        )
    ),
    MarketsimTestCase(
        description="Orders 6",
        group='basic',
        inputs=dict(
            orders_file='orders-06.csv',
            start_val=1000000,
            commission=0.,
            impact=0.
        ),
        outputs=dict(
            num_days = 210,
            last_day_portval = 894604.3,
            sharpe_ratio = -1.23463930987,
            avg_daily_ret = -0.000511281541086
        )
    ),
    MarketsimTestCase(
        description="Orders 7",
        group='basic',
        inputs=dict(
            orders_file='orders-07.csv',
            start_val=1000000,
            commission=0.,
            impact=0.
        ),
        outputs=dict(
            num_days = 237,
            last_day_portval = 1106563.3,
            sharpe_ratio = 2.10356512897,
            avg_daily_ret = 0.0004345040621
        )
    ),
    MarketsimTestCase(
        description="Orders 8",
        group='basic',
        inputs=dict(
            orders_file='orders-08.csv',
            start_val=1000000,
            commission=0.,
            impact=0.
        ),
        outputs=dict(
            num_days = 229,
            last_day_portval = 1074884.1,
            sharpe_ratio = 0.941858298061,
            avg_daily_ret = 0.000332404156893
        )
    ),
    MarketsimTestCase(
        description="Orders 9",
        group='basic',
        inputs=dict(
            orders_file='orders-09.csv',
            start_val=1000000,
            commission=0.,
            impact=0.
        ),
        outputs=dict(
            num_days = 37,
            last_day_portval = 1067710.0,
            sharpe_ratio = 2.90848480553,
            avg_daily_ret = 0.00187252252117
        )
    ),
    #########################
    # Commission and impact #
    #########################
    MarketsimTestCase(
        description="Orders 11, commission",
        group='commission',
        inputs=dict(
            orders_file='orders-11.csv',
            start_val=1000000,
            commission=9.95,
            impact=0.
        ),
        outputs=dict(
            num_days = 37,
            last_day_portval = 1045700.45,
            sharpe_ratio = 1.80327835983,
            avg_daily_ret = 0.00130745837411
        )
    ),
    MarketsimTestCase(
        description="Orders 12, impact",
        group='impact',
        inputs=dict(
            orders_file='orders-12.csv',
            start_val=1000000,
            commission=0.,
            impact=0.005
        ),
        outputs=dict(
            num_days = 240,
            last_day_portval = 1705686.6665,
            sharpe_ratio = 1.26427802107,
            avg_daily_ret = 0.00290246139389
        )
    ),
    MarketsimTestCase(
        description="Orders 10, impact and commission",
        group='both',
        inputs=dict(
            orders_file='orders-10.csv',
            start_val=1000000,
            commission=9.95,
            impact=0.005
        ),
        outputs=dict(
            num_days = 141,
            last_day_portval = 1026658.3265,
            sharpe_ratio = 0.627643575702,
            avg_daily_ret = 0.000222013722594
        )
    )
    #######################
    # Withheld test cases #
    #######################
]

seconds_per_test_case = 10  # execution time limit

# Grading parameters (picked up by module-level grading fixtures)
max_points = 100.0  # 9.5 * 10 + 2.5 * 2 + 1 secret point
html_pre_block = True  # surround comments with HTML <pre> tag (for T-Square comments field)

# Test functon(s)
@pytest.mark.parametrize("description,group,inputs,outputs", marketsim_test_cases)
def test_marketsim(description, group, inputs, outputs, grader):
    """Test compute_portvals() returns correct daily portfolio values.

    Requires test description, test case group, inputs, expected outputs, and a grader fixture.
    """

    points_earned = 0.0  # initialize points for this test case
    try:
        # Try to import student code (only once)
        if not main_code in globals():
            import importlib
            # * Import module
            mod = importlib.import_module(main_code)
            globals()[main_code] = mod
            # * Import methods to test
            for m in ['compute_portvals']:
                globals()[m] = getattr(mod, m)

        incorrect = False
        msgs = []

        if group == 'author':
            try:
                auth_string = run_with_timeout(marketsim.author,seconds_per_test_case,(),{})
                if auth_string == 'tb34':
                    incorrect = True
                    msgs.append("   Incorrect author name (tb34)")
                    points_earned = -10
                elif auth_string == '':
                    incorrect = True
                    msgs.append("   Empty author name")
                    points_earned = -10
            except Exception as e:
                incorrect = True
                msgs.append("   Exception occured when calling author() method: {}".format(e))
                points_earned = -10
        else:
            # Unpack test case
            orders_file = inputs['orders_file']
            start_val = inputs['start_val']
            impct = inputs['impact']
            commish = inputs['commission']

            portvals = None
            fullpath_orders_file = get_orders_data_file(orders_file)
            portvals = run_with_timeout(compute_portvals,seconds_per_test_case,(),{'orders_file':fullpath_orders_file,'start_val':start_val,'commission':commish,'impact':impct})

            # * Check return type is correct, coax into Series
            assert (type(portvals) == pd.Series) or (type(portvals) == pd.DataFrame and len(portvals.columns) == 1), "You must return a Series or single-column DataFrame!"
            if type(portvals) == pd.DataFrame:
                portvals = portvals[portvals.columns[0]]  # convert single-column DataFrame to Series
            if group == 'basic':
                if len(portvals) != outputs['num_days']:
                    incorrect=True
                    msgs.append("   Incorrect number of days: {}, expected {}".format(len(portvals), outputs['num_days']))
                else: 
                    points_earned += 2.0
                if abs(portvals[-1]-outputs['last_day_portval']) > (0.001*outputs['last_day_portval']):
                    incorrect=True
                    msgs.append("   Incorrect final value: {}, expected {}".format(portvals[-1],outputs['last_day_portval']))
                else:
                    points_earned += 5.0
                adr,sr = get_stats(portvals)
                if abs(sr-outputs['sharpe_ratio']) > abs(0.001*outputs['sharpe_ratio']):
                    incorrect=True
                    msgs.append("   Incorrect sharpe ratio: {}, expected {}".format(sr,outputs['sharpe_ratio']))
                else:
                    points_earned += 1.0
                if abs(adr-outputs['avg_daily_ret']) > abs(0.001*outputs['avg_daily_ret']):
                    incorrect=True
                    msgs.append("   Incorrect avg daily return: {}, expected {}".format(adr,outputs['avg_daily_ret']))
                else:
                    points_earned += 1.0
            elif group=='commission' or group=='impact' or group=='both':
                if abs(portvals[-1]-outputs['last_day_portval']) > 0.001:
                    incorrect = True
                    msgs.append("   Incorrect final value: {}, expected {}".format(portvals[-1],outputs['last_day_portval']))
                else:
                    points_earned += 2.0
        if incorrect:
            raise (IncorrectOutput)
    except Exception as e:
        # Test result: failed
        msg = "Test case description: {}\n".format(description)
        
        # Generate a filtered stacktrace, only showing erroneous lines in student file(s)
        
        tb_list = tb.extract_tb(sys.exc_info()[2])
        if 'grading_traceback' in dir(e):
            tb_list = e.grading_traceback
        for i in range(len(tb_list)):
            row = tb_list[i]
            tb_list[i] = (os.path.basename(row[0]), row[1], row[2], row[3])  # show only filename instead of long absolute path
        tb_list = [row for row in tb_list if row[0] == 'marketsim.py']
        if tb_list:
            msg += "Traceback:\n"
            msg += ''.join(tb.format_list(tb_list))  # contains newlines
        msg += "{}: {}".format(e.__class__.__name__, str(e))

        # Report failure result to grader, with stacktrace
        grader.add_result(GradeResult(outcome='failed', points=max(points_earned,0), msg=msg))
        raise
    else:
        # Test result: passed (no exceptions)
        grader.add_result(GradeResult(outcome='passed', points=points_earned, msg=None))

def get_stats(port_val):
    daily_rets = (port_val / port_val.shift(1)) - 1
    daily_rets = daily_rets[1:]
    avg_daily_ret = daily_rets.mean()
    std_daily_ret = daily_rets.std()
    sharpe_ratio = np.sqrt(252) * daily_rets.mean() / std_daily_ret
    return avg_daily_ret, sharpe_ratio

if __name__ == "__main__":
    pytest.main(["-s", __file__])
