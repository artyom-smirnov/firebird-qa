#coding:utf-8
#
# id:           bugs.core_5986
# title:        Incorrect evaluation of NULL IS [NOT] {FALSE | TRUE}
# decription:   
#                    Test was implemented on the basis of 7IWD2-02-Foundation-2011-12.pdf, page 322
#                    (as it was suggested by Mark Rotteveel in the ticket, see his note 17/Jan/19 03:13 PM).
#                    Checked on:
#                       4.0.0.1421: OK, 1.485s.
#                       3.0.5.33097: OK, 0.844s.
#                
# tracker_id:   CORE-5986
# min_versions: ['3.0']
# versions:     3.0
# qmid:         None

import pytest
from firebird.qa import db_factory, isql_act, Action

# version: 3.0
# resources: None

substitutions_1 = []

init_script_1 = """"""

db_1 = db_factory(sql_dialect=3, init=init_script_1)

test_script_1 = """
    set bail on;
    set list on;

    -- General rules: "NOT(True) is False, NOT(False) is True, and NOT(Unknown) is Unknown"
    select not true b1, not false b2, not unknown b3
    from rdb$database;

    -- Data for output in Truth-tables:
    recreate table test( x boolean, y boolean );
    insert into test(x,y) select 
    true,   true    from rdb$database union all select
    true,   false   from rdb$database union all select
    true,   unknown from rdb$database union all select
    false,  true    from rdb$database union all select
    false,  false   from rdb$database union all select
    false,  unknown from rdb$database union all select
    unknown,true    from rdb$database union all select
    unknown,false   from rdb$database union all select
    unknown,unknown from rdb$database
    ;
    commit;

    -- Table 11. Truth table for the AND boolean operator.
    select x, y, x and y as "x_AND_y" from test;

    -- Table 12. Truth table for the OR boolean operator.
    select x, y, x or y as "x_OR_y" from test;

    -- Table 12. Truth table for the IS boolean operator.
    --select x, y, x is y as "x_IS_y" from test; --> token unknown; doing this using ES

    set term ^;
    execute block returns( x boolean, y boolean, "x_IS_y" boolean) as
        declare run_expr varchar(128);
    begin
        for 
            select
                 x
                ,y 
                ,''||coalesce(x,'unknown') || ' is ' || coalesce(y,'unknown')
            from test
        into x, y, run_expr
        do begin
            execute statement 'select ' || run_expr || ' from rdb$database' into "x_IS_y";
            suspend;
        end
    end
    ^
    set term ;^
    /*
              X       Y x_AND_y
        ======= ======= =======
        <true>  <true>  <true>
        <true>  <false> <false>
        <true>  <null>  <null>
        <false> <true>  <false>
        <false> <false> <false>
        <false> <null>  <false>
        <null>  <true>  <null>
        <null>  <false> <false>
        <null>  <null>  <null>


              X       Y  x_OR_y
        ======= ======= =======
        <true>  <true>  <true>
        <true>  <false> <true>
        <true>  <null>  <true>
        <false> <true>  <true>
        <false> <false> <false>
        <false> <null>  <null>
        <null>  <true>  <true>
        <null>  <false> <null>
        <null>  <null>  <null>


              X       Y  x_IS_y
        ======= ======= =======
        <true>  <true>  <true>
        <true>  <false> <false>
        <true>  <null>  <false>
        <false> <true>  <false>
        <false> <false> <true>
        <false> <null>  <false>
        <null>  <true>  <false>
        <null>  <false> <false>
        <null>  <null>  <true>
    */


  """

act_1 = isql_act('db_1', test_script_1, substitutions=substitutions_1)

expected_stdout_1 = """
    B1                              <false>
    B2                              <true>
    B3                              <null>


    X                               <true>
    Y                               <true>
    x_AND_y                         <true>

    X                               <true>
    Y                               <false>
    x_AND_y                         <false>

    X                               <true>
    Y                               <null>
    x_AND_y                         <null>

    X                               <false>
    Y                               <true>
    x_AND_y                         <false>

    X                               <false>
    Y                               <false>
    x_AND_y                         <false>

    X                               <false>
    Y                               <null>
    x_AND_y                         <false>

    X                               <null>
    Y                               <true>
    x_AND_y                         <null>

    X                               <null>
    Y                               <false>
    x_AND_y                         <false>

    X                               <null>
    Y                               <null>
    x_AND_y                         <null>


    X                               <true>
    Y                               <true>
    x_OR_y                          <true>

    X                               <true>
    Y                               <false>
    x_OR_y                          <true>

    X                               <true>
    Y                               <null>
    x_OR_y                          <true>

    X                               <false>
    Y                               <true>
    x_OR_y                          <true>

    X                               <false>
    Y                               <false>
    x_OR_y                          <false>

    X                               <false>
    Y                               <null>
    x_OR_y                          <null>

    X                               <null>
    Y                               <true>
    x_OR_y                          <true>

    X                               <null>
    Y                               <false>
    x_OR_y                          <null>

    X                               <null>
    Y                               <null>
    x_OR_y                          <null>


    X                               <true>
    Y                               <true>
    x_IS_y                          <true>

    X                               <true>
    Y                               <false>
    x_IS_y                          <false>

    X                               <true>
    Y                               <null>
    x_IS_y                          <false>

    X                               <false>
    Y                               <true>
    x_IS_y                          <false>

    X                               <false>
    Y                               <false>
    x_IS_y                          <true>

    X                               <false>
    Y                               <null>
    x_IS_y                          <false>

    X                               <null>
    Y                               <true>
    x_IS_y                          <false>

    X                               <null>
    Y                               <false>
    x_IS_y                          <false>

    X                               <null>
    Y                               <null>
    x_IS_y                          <true>
  """

@pytest.mark.version('>=3.0')
def test_core_5986_1(act_1: Action):
    act_1.expected_stdout = expected_stdout_1
    act_1.execute()
    assert act_1.clean_expected_stdout == act_1.clean_stdout
