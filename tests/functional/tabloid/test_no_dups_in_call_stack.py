#coding:utf-8
#
# id:           functional.tabloid.no_dups_in_call_stack
# title:        Avoid info duplication when statements in call stack attached to different transactions (for example: monitoring snapshot is created in autonomous transaction)
# decription:   Fixed in rev. 59971 for 3.0; rev. 59972 for 2.5 (backporting) -- 12-aug-2014
# tracker_id:   
# min_versions: ['2.5.4']
# versions:     2.5.4
# qmid:         None

import pytest
from firebird.qa import db_factory, isql_act, Action

# version: 2.5.4
# resources: None

substitutions_1 = []

init_script_1 = """
    -- sql.ru/forum/actualutils.aspx?action=gotomsg&tid=1109867&msg=16438071
    -- run: fbt_run -b <path to isql> functional.tabloid.no-dups-in-call-stack -o localhost/<port>
    set term ^;
    create or alter procedure dbg_get_stack as begin end^
    create or alter procedure p_01 as begin end^
    create or alter procedure p_02 as begin end^
    create or alter procedure p_03 as begin end^
    create or alter procedure p_04 as begin end^
    set term ;^
    recreate table dbg_stack(
         whoami varchar(31)
        ,call_level int
        ,statement_id int
        ,call_id int
        ,object_name char(31)
        ,object_type smallint
        ,source_line int
        ,source_column int
    );
    commit;

    set term ^;
    create or alter procedure dbg_get_stack(a_whoami varchar(31))
    as
        declare v_call_level smallint;
        declare v_mon$statement_id type of column mon$call_stack.mon$statement_id;
        declare v_mon$call_id type of column mon$call_stack.mon$call_id;
        declare v_mon$object_name type of column mon$call_stack.mon$object_name;
        declare v_mon$object_type type of column mon$call_stack.mon$object_type;
        declare v_mon$source_line type of column mon$call_stack.mon$source_line;
        declare v_mon$source_column type of column mon$call_stack.mon$source_column;
    begin
        in autonomous transaction do
        begin
            for
                with recursive
                r as (
                    select 1 call_level,
                         c.mon$statement_id,
                         c.mon$call_id,
                         c.mon$object_name,
                         c.mon$object_type,
                         c.mon$source_line,
                         c.mon$source_column
                    from mon$call_stack c
                    where c.mon$caller_id is null

                    UNION ALL

                    select r.call_level+1,
                           c.mon$statement_id,
                           c.mon$call_id,
                           c.mon$object_name,
                           c.mon$object_type,
                           c.mon$source_line,
                           c.mon$source_column
                    from mon$call_stack c
                      join r
                        on c.mon$caller_id = r.mon$call_id
                )
             select
                r.call_level
               ,r.mon$statement_id
               ,r.mon$call_id
               ,r.mon$object_name
               ,r.mon$object_type
               ,r.mon$source_line
               ,r.mon$source_column
            from r
            --as cursor cr do
            into
                v_call_level
               ,v_mon$statement_id
               ,v_mon$call_id
               ,v_mon$object_name
               ,v_mon$object_type
               ,v_mon$source_line
               ,v_mon$source_column
            do begin
                insert into dbg_stack
                values(
                    :a_whoami
                   ,:v_call_level
                   ,:v_mon$statement_id
                   ,:v_mon$call_id
                   ,:v_mon$object_name
                   ,:v_mon$object_type
                   ,:v_mon$source_line
                   ,:v_mon$source_column
                );
            end
       end

    end
    ^
    set term ;^
    commit;

    ---------------------------------
    set term ^;
    create or alter procedure p_04 as
        declare n int;
    begin
                    -- dummy row 1
                    -- dummy row 2
                    -- dummy row 3
                    -- dummy row 4
                    execute procedure dbg_get_stack( 'p_04' );
    end
    ^
    create or alter procedure p_03 as
        declare n int;
    begin
                -- dummy row 1
                -- dummy row 2
                -- dummy row 3
                execute procedure p_04;
    end
    ^
    create or alter procedure p_02 as
        declare n int;
    begin
            -- dummy row 1
            -- dummy row 2
            execute procedure p_03;
    end
    ^
    create or alter procedure p_01 as
        declare n int;
    begin
        -- dummy row 1
        delete from dbg_stack;
        execute procedure p_02;
    end
    ^
    set term ;^
    commit;
  """

db_1 = db_factory(page_size=4096, sql_dialect=3, init=init_script_1)

test_script_1 = """
    delete from dbg_stack;
    commit;
    execute procedure p_01;
    commit;
    set width whoami 6;
    set width object_name 15;
    select s.whoami, s.call_level, s.object_name, s.object_type, s.source_line
    from dbg_stack s;
  """

act_1 = isql_act('db_1', test_script_1, substitutions=substitutions_1)

expected_stdout_1 = """
WHOAMI   CALL_LEVEL OBJECT_NAME     OBJECT_TYPE  SOURCE_LINE
====== ============ =============== =========== ============
p_04              1 P_01                      5            6
p_04              2 P_02                      5            6
p_04              3 P_03                      5            7
p_04              4 P_04                      5            8
p_04              5 DBG_GET_STACK             5           13
  """

@pytest.mark.version('>=2.5.4')
def test_1(act_1: Action):
    act_1.expected_stdout = expected_stdout_1
    act_1.execute()
    assert act_1.clean_expected_stdout == act_1.clean_stdout
