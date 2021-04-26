#coding:utf-8
#
# id:           bugs.core_6379
# title:        Bugcheck 179
# decription:   
#                   Could not reproduce with scenario described in the ticket.
#                   Test uses steps described by letter from me to Vlad, date: 15-JUL-2020 10:53 (subj: "read consistency tests").
#                   Scripts for initial test can be found here:
#                   https://drive.google.com/drive/folders/1CEOSVfOMHzlZ1F3Gi0Jv3TEbvWLs9DPR?usp=sharing
#               
#                   Reproduced problem on 4.0.0.2108 SS:
#                   1. Content of firebird.log:
#                   	deadlock
#                   	update conflicts with concurrent update
#                   	concurrent transaction number is 12
#                   	internal Firebird consistency check (wrong record version (185), file: Savepoint.cpp line: 267)
#                   2. Client gets:
#                       Statement failed, SQLSTATE 08006
#                       Error reading data from the connection.
#               
#                       Statement failed, SQLSTATE 08006
#                       Error writing data to the connection.
#                       -send_packet/send
#               
#                   Checked on 4.0.0.2170 SS/CS - all fine.
#                
# tracker_id:   
# min_versions: ['4.0']
# versions:     4.0
# qmid:         

import pytest
from firebird.qa import db_factory, isql_act, Action

# version: 4.0
# resources: None

substitutions_1 = [('=', ''), ('[ \t]+', ' ')]

init_script_1 = """"""

db_1 = db_factory(sql_dialect=3, init=init_script_1)

# test_script_1
#---
# 
#  import os
#  import sys
#  import subprocess
#  from subprocess import Popen
#  from fdb import services
#  import time
#  
#  os.environ["ISC_USER"] = user_name
#  os.environ["ISC_PASSWORD"] = user_password
#  
#  db_conn.close()
#  
#  #--------------------------------------------
#  
#  def flush_and_close( file_handle ):
#      # https://docs.python.org/2/library/os.html#os.fsync
#      # If you're starting with a Python file object f, 
#      # first do f.flush(), and 
#      # then do os.fsync(f.fileno()), to ensure that all internal buffers associated with f are written to disk.
#      global os
#      
#      file_handle.flush()
#      if file_handle.mode not in ('r', 'rb') and file_handle.name != os.devnull:
#          # otherwise: "OSError: [Errno 9] Bad file descriptor"!
#          os.fsync(file_handle.fileno())
#      file_handle.close()
#  
#  #--------------------------------------------
#  
#  def cleanup( f_names_list ):
#      global os
#      for f in f_names_list:
#         if type(f) == file:
#            del_name = f.name
#         elif type(f) == str:
#            del_name = f
#         else:
#            print('Unrecognized type of element:', f, ' - can not be treated as file.')
#            del_name = None
#  
#         if del_name and os.path.isfile( del_name ):
#             os.remove( del_name )
#      
#  #--------------------------------------------
#  
#  sql_init='''
#      create table test(id int generated by default as identity, x int, s varchar(32765) );
#      set term ^;
#      execute block as
#          declare n_limit int = 1000;
#          declare i int = 1;
#      begin
#         rdb$set_context('USER_SESSION', 'N_LIMIT', n_limit);
#         while (i <= n_limit) do
#         begin
#             insert into test(x, s) values(0, lpad('', 32765, gen_uuid()));
#             i = i + 1;
#         end
#      end
#      ^
#      set term ^;
#      commit;
#  
#      delete from test order by id rows ( cast( rdb$get_context('USER_SESSION', 'N_LIMIT') as int) - 13 );
#      commit;
#  '''
#  runProgram('isql', [ dsn, '-q' ], sql_init)
#  
#  con_lock_1 = fdb.connect( dsn = dsn )
#  con_lock_2 = fdb.connect( dsn = dsn )
#  
#  
#  #########################
#  ###  L O C K E R - 1  ###
#  #########################
#  con_lock_1.execute_immediate( 'update test set x = -1111 order by id rows 6 to 6' )
#  
#  
#  # Scenario for WORKER:
#  ######################
#  sql_text='''
#      connect '%(dsn)s';
#      set autoddl off;
#      commit;
#      set transaction read committed read consistency;
#      set count on;
#  
#      set bail on;
#      delete from test;
#  
#      set heading on;
#      select rdb$db_key, id, x from test order by rdb$db_key;
#  '''  % dict(globals(), **locals())
#  
#  f_worker_sql=open( os.path.join(context['temp_directory'],'tmp_6379.sql'), 'w')
#  f_worker_sql.write(sql_text)
#  flush_and_close(f_worker_sql)
#  
#  f_worker_log=open( ''.join( ( os.path.splitext(f_worker_sql.name)[0], '.log') ), 'w')
#  f_worker_err=open( ''.join( ( os.path.splitext(f_worker_log.name)[0], '.err') ), 'w')
#  
#  ############################################################################
#  ###  L A U N C H     W O R K E R    U S I N G     I S Q L,   A S Y N C.  ###
#  ############################################################################
#  
#  p_worker = Popen( [ context['isql_path'], '-pag', '9999', '-q', '-i', f_worker_sql.name ],stdout=f_worker_log, stderr=f_worker_err)
#  time.sleep(1)
#  
#  #########################
#  ###  L O C K E R - 2  ###
#  #########################
#  con_lock_2.execute_immediate( 'insert into test(x) values(3333)' )
#  con_lock_2.commit()
#  
#  
#  #########################
#  ###  L O C K E R - 1  ###
#  #########################
#  con_lock_1.commit()
#  con_lock_2.commit()
#  
#  # Here we wait for ISQL complete its mission:
#  p_worker.wait()
#  
#  flush_and_close(f_worker_log)
#  flush_and_close(f_worker_err)
#  
#  # Close lockers:
#  ################
#  for c in (con_lock_1, con_lock_2):
#      c.close()
#  
#  
#  # CHECK RESULTS
#  ###############
#  with open(f_worker_log.name,'r') as f:
#      for line in f:
#          print(line)
#  
#  with open(f_worker_err.name,'r') as g:
#      for line in g:
#          if line:
#              print( 'UNEXPECTED STDERR IN ' + g.name + ':' +  line)
#  
#  
#  # Cleanup.
#  ##########
#  time.sleep(1)
#  cleanup( (f_worker_sql, f_worker_log, f_worker_err)  )
#  
#    
#---
#act_1 = python_act('db_1', test_script_1, substitutions=substitutions_1)

expected_stdout_1 = """
    Records affected: 14
    Records affected: 0
  """

@pytest.mark.version('>=4.0')
@pytest.mark.xfail
def test_core_6379_1(db_1):
    pytest.fail("Test not IMPLEMENTED")

