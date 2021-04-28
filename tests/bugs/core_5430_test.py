#coding:utf-8
#
# id:           bugs.core_5430
# title:        Support for INCREMENT option in identity columns
# decription:   
#                  Checked on 4.0.0.474
#                  18.08.2020: replaced expected_stdout, checked on 4.0.0.2164.
#                
# tracker_id:   CORE-5430
# min_versions: ['4.0']
# versions:     4.0
# qmid:         None

import pytest
from firebird.qa import db_factory, isql_act, Action

# version: 4.0
# resources: None

substitutions_1 = []

init_script_1 = """"""

db_1 = db_factory(sql_dialect=3, init=init_script_1)

test_script_1 = """
    set list on;
    --set echo on;
    recreate table test1(
        id int generated by default as identity ( start with 12345 )
    );
    recreate table test2(
        id int generated by default as identity ( start with 12345 increment 22222 )
    );

    recreate table test3(
        id int generated by default as identity ( increment 33333 )
    );

    insert into test1 default values returning id as test1_id;
    insert into test2 default values returning id as test2_id;
    insert into test3 default values returning id as test3_id;
    commit;

    alter table test1 alter column id restart;
    alter table test2 alter column id restart with 23456;

    alter table test3 alter column id restart with 0;
    alter table test3 alter column id set increment 11111;
    commit;

    insert into test1 default values returning id as test1_restarted_id;
    insert into test2 default values returning id as test2_restarted_id;
    insert into test3 default values returning id as test3_chng_incr_id;
  """

act_1 = isql_act('db_1', test_script_1, substitutions=substitutions_1)

expected_stdout_1 = """
    TEST1_ID                        12345
    TEST2_ID                        12345
    TEST3_ID                        1
    TEST1_RESTARTED_ID              12345
    TEST2_RESTARTED_ID              23456
    TEST3_CHNG_INCR_ID              -22222
  """

@pytest.mark.version('>=4.0')
def test_1(act_1: Action):
    act_1.expected_stdout = expected_stdout_1
    act_1.execute()
    assert act_1.clean_expected_stdout == act_1.clean_stdout
