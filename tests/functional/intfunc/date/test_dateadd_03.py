#coding:utf-8
#
# id:           functional.intfunc.date.dateadd_03
# title:        test de la fonction dateadd  pour l'ajout d'une année
# decription:   Returns a date/time/timestamp value increased (or decreased, when negative) by the specified amount of time.
# tracker_id:   
# min_versions: []
# versions:     2.1
# qmid:         functional.intfunc.date.dateadd_03

import pytest
from firebird.qa import db_factory, isql_act, Action

# version: 2.1
# resources: None

substitutions_1 = []

init_script_1 = """"""

db_1 = db_factory(sql_dialect=3, init=init_script_1)

test_script_1 = """select dateadd(-1 year TO date '2008-02-06' ) as yesterday from rdb$database;
select dateadd(year,-1, date '2008-02-06' ) as yesterday from rdb$database;
"""

act_1 = isql_act('db_1', test_script_1, substitutions=substitutions_1)

expected_stdout_1 = """
  YESTERDAY
===========
2007-02-06


  YESTERDAY
===========
2007-02-06

"""

@pytest.mark.version('>=2.1')
def test_dateadd_03_1(act_1: Action):
    act_1.expected_stdout = expected_stdout_1
    act_1.execute()
    assert act_1.clean_expected_stdout == act_1.clean_stdout
