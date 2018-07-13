import sys
import os
import subprocess
from subprocess import call
from subprocess import check_output
import time


'''VARS'''

converge_timeout = 10
check_timeout = 5
peered_with_rs = False

state_log = '/home/rp2/log_fnm.txt'
state_log_bancount_cmd = 'cat ' + state_log + ' | grep -c ban'
state_log_lastline_cmd = 'tail -n 1 ' + state_log

ban_cmd_21 = "ssh root@10.0.0.5 'bash -s' < traffic_reject.sh bgp_ce 3.3.3.0/24"
ban_cmd_22 = "ssh root@10.0.0.5 'bash -s' < traffic_reject.sh bgp_arp 3.3.3.0/24"
ban_cmd_23 = "ssh root@10.0.0.2 'bash -s' < openvswitch_acl.sh set"

unban_cmd_21 = "ssh root@10.0.0.5 'bash -s' < traffic_reject.sh unban 3.3.3.0/24"
unban_cmd_22 = "ssh root@10.0.0.5 'bash -s' < traffic_reject.sh unban 3.3.3.0/24"
unban_cmd_23 = "ssh root@10.0.0.2 'bash -s' < openvswitch_acl.sh unset"

seconds_cmd = 'date +%s'
dev_null = open(os.devnull, 'w')


'''FUNCTIONS'''

def check_if_mitigation_successful():
  first_nr_of_bans = int(check_output(state_log_bancount_cmd, shell=True))
  time.sleep(check_timeout)
  second_nr_of_bans = int(check_output(state_log_bancount_cmd, shell=True))
  if first_nr_of_bans == second_nr_of_bans:
    return True
  else:
    return False


def run_until_interrupt(unban_cmd):
  try:
    while True:
      time.sleep(0.1)
  except KeyboardInterrupt:
    call(unban_cmd, stdout=dev_null, stderr=subprocess.STDOUT, shell=True)
    sys.exit()


def exec_acl_mitigation():
  global start_time
  current_time = int(check_output(seconds_cmd, shell=True))
  print('Performing 2.3 mitigation, running continously at ' + str(current_time - start_time))
  call(ban_cmd_23, stdout=dev_null, stderr=subprocess.STDOUT, shell=True)
  run_until_interrupt(unban_cmd_23)


'''PROGRAM'''

start_time = int(check_output(seconds_cmd, shell=True))

while True:
  state_log_last_line = str(check_output(state_log_lastline_cmd, shell=True))
  if state_log_last_line == 'ban\n':
    current_time = int(check_output(seconds_cmd, shell=True))
    print('Exceeded threshold detected at ' + str(current_time - start_time))
    break
  time.sleep(0.1)


if peered_with_rs == True:
  print('Culprit AS is peered with the RS')
  #call(ban_cmd_21, stdout=dev_null, stderr=subprocess.STDOUT, shell=True)
  #current_time = int(check_output(seconds_cmd, shell=True))
  #print('Performed 2.1 mitigation at ' + str(current_time - start_time))
  #time.sleep(converge_timeout)
  #print('2.1 converge timeout finished at ' + str(current_time - start_time + converge_timeout))

  #if check_if_mitigation_successful() == True:
    #current_time = int(check_output(seconds_cmd, shell=True))
    #print('2.1 mitigation is successful, running continously at ' + str(current_time - start_time))
    #run_until_interrupt(unban_cmd_21)
  #else:
  current_time = int(check_output(seconds_cmd, shell=True))
    #print('2.1 mitigation is NOT successful at ' + str(current_time - start_time))
  print('Performing 2.2 mitigation at ' + str(current_time - start_time))
    #call(unban_cmd_21, stdout=dev_null, stderr=subprocess.STDOUT, shell=True)
  call(ban_cmd_22, stdout=dev_null, stderr=subprocess.STDOUT,  shell=True)
  time.sleep(converge_timeout)

  if check_if_mitigation_successful() == True:
    current_time = int(check_output(seconds_cmd, shell=True))
    print('2.2 mitigation is successful, running continously at ' + str(current_time - start_time))
    run_until_interrupt(unban_cmd_22)
  else:
    current_time = int(check_output(seconds_cmd, shell=True))
    print('2.2 mitigation is NOT successful at ' + str(current_time - start_time))
    call(unban_cmd_22, stdout=dev_null, stderr=subprocess.STDOUT, shell=True)
    exec_acl_mitigation()
else:
  print('Culprit AS is NOT peered with the RS')
  exec_acl_mitigation()

