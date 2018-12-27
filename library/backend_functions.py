import paramiko
import time
import getpass
import sys
import socket
import subprocess
import os.path


###### SWITCHING ##########

username="username"
password="pwd"

def login(username, password,ip):
        try:
            # Create instance of SSHClient object
            remote_conn_pre = paramiko.SSHClient()
            # Automatically add untrusted hosts (make sure okay for security policy in your environment)
            remote_conn_pre.set_missing_host_key_policy(paramiko.AutoAddPolicy())
            # initiate SSH connection
            remote_conn_pre.connect(ip, username=username, password=password, timeout=5, look_for_keys=False, allow_agent=False)
            # Use invoke_shell to establish an 'interactive session'
            remote_conn = remote_conn_pre.invoke_shell()
            ## remote_conn.close()
            return True
        except paramiko.AuthenticationException:
            print "\nAuthentication Failed\n"
            return False
        except paramiko.SSHException:
            print "\nIssues with SSH service\n"
            return False
        except socket.error,e:
            print "\nConnection Error\n"
            return False

def new_config_switchport(ip,name_interface,description_vlan,vlan_id):

    try:
        # Create instance of SSHClient object
        remote_conn_pre = paramiko.SSHClient()
        # Automatically add untrusted hosts (make sure okay for security policy in your environment)
        remote_conn_pre.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        # initiate SSH connection
        remote_conn_pre.connect(ip, username=username, password=password, look_for_keys=False, allow_agent=False)
        print "SSH connection established to %s" % ip+"\n"
        # Use invoke_shell to establish an 'interactive session'
        remote_conn = remote_conn_pre.invoke_shell()
        print "Interactive SSH session established\n"
        #return True
    except paramiko.AuthenticationException:
        print "\nAuthentication Failed\n"
        return False
    except paramiko.SSHException:
        print "\nIssues with SSH service\n"
        return False
    except socket.error,e:
        print "\nConnection Error\n"
        return False

    # Strip the initial router prompt
    output = remote_conn.recv(10000000)

    # See what we have
    print output

    # Send the sw a command
    remote_conn.send("\n"
    +"conf t\n"
    +"default interface "+name_interface+"\n"
    +"\n"
    +"interface "+name_interface+"\n"
    +"\n"
    +"description " + description_vlan +"\n"
    +"\n"
    +"switchport mode access\n"
    +"\n"
    +"switchport access vlan "+vlan_id+"\n"
    +"\n"
    +"spanning-tree bpduguard enable\n"
    +"\n"
    +"no shut\n"
    +"\n"
    +"end\n"
    +"\n"
    +"\nshow run int "+name_interface+"\n"
    +"\n"
    +"\n"
    +"show int "+name_interface+" status\n"
    +"\n"
    +"\nwr\n")

    # Wait for the command to complete
    time.sleep(3)

    #Display output
    output = remote_conn.recv(10000000)

    # See what we have
    print output
    return output.replace("\n","<br>")
    #Close shell
    remote_conn_pre.close()

def disable_switchport(ip,name_interface):

    try:
        # Create instance of SSHClient object
        remote_conn_pre = paramiko.SSHClient()
        # Automatically add untrusted hosts (make sure okay for security policy in your environment)
        remote_conn_pre.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        # initiate SSH connection
        remote_conn_pre.connect(ip, username=username, password=password, look_for_keys=False, allow_agent=False)
        print "SSH connection established to %s" % ip+"\n"
        # Use invoke_shell to establish an 'interactive session'
        remote_conn = remote_conn_pre.invoke_shell()
        print "Interactive SSH session established\n"
        #return True
    except paramiko.AuthenticationException:
        print "\nAuthentication Failed\n"
        return False
    except paramiko.SSHException:
        print "\nIssues with SSH service\n"
        return False
    except socket.error,e:
        print "\nConnection Error\n"
        return False

    # Strip the initial router prompt
    output = remote_conn.recv(10000000)

    # See what we have
    print output

    # Send the sw a command
    remote_conn.send("\n"
    +"conf t\n"
    +"default interface "+name_interface+"\n"
    +"\n"
    +"interface "+name_interface+"\n"
    +"description Quarantine\n"
    +"\n"
    +"switchport mode access\n"
    +"\n"
    +"switchport access vlan 999\n"
    +"\n"
    +"spanning-tree bpduguard enable\n"
    +"\n"
    +"shut\n"
    +"\n"
    +"end\n"
    +"\n"
    +"\nshow run int "+name_interface+"\n"
    +"\n"
    +"\n"
    +"show int "+name_interface+" status\n"
    +"\n"
    +"\nwr\n")

    # Wait for the command to complete
    time.sleep(3)

    output = remote_conn.recv(10000000)

    # See what we have
    print output
    return output.replace("\n","<br>")
    #Close shell
    remote_conn_pre.close()

def checkconfig_switchport(ip,name_interface):

    try:
        # Create instance of SSHClient object
        remote_conn_pre = paramiko.SSHClient()
        # Automatically add untrusted hosts (make sure okay for security policy in your environment)
        remote_conn_pre.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        # initiate SSH connection
        remote_conn_pre.connect(ip, username=username, password=password, look_for_keys=False, allow_agent=False)
        print "SSH connection established to %s" % ip+"\n"
        # Use invoke_shell to establish an 'interactive session'
        remote_conn = remote_conn_pre.invoke_shell()
        print "Interactive SSH session established\n"
        #return True
    except paramiko.AuthenticationException:
        print "\nAuthentication Failed\n"
        return False
    except paramiko.SSHException:
        print "\nIssues with SSH service\n"
        return False
    except socket.error,e:
        print "\nConnection Error\n"
        return False

    # Strip the initial router prompt
    output = remote_conn.recv(10000000)

    # See what we have
    print output

    # Send the sw a command
    remote_conn.send("\n"
    +"show run int "+name_interface+"\n"
    +"\n"
    +"show int "+name_interface+" status\n")

    # Wait for the command to complete
    time.sleep(2)

    output = remote_conn.recv(10000000)

    # See what we have
    print output
    return output.replace("\n","<br>")
    #Close shell
    remote_conn_pre.close()

def list_switches(switch_info):

    j=len(switch_info)

    tmpRet = []
    for l in range (0,j):
        ###### split the lines via /n #####
        sw = str(switch_info[l]).split(' ')
        tmpRet.append({"name":sw[1],"ip":sw[0]})

    return tmpRet

def getNameSW(ip,switch_info):
    db = list_switches(switch_info)

    for i in db:
        if ip == i["ip"]:
            return i["name"]

def generate_interface_file(switch_ip):

    if os.path.isfile("/var/app/interface_"+switch_ip+".txt") == True:
        print "ja existe CRL"
    else:
        print "Nao existe CRL"
        print "start"
        subprocess.call("sshpass -p '"+password+"' ssh "+username+"@"+switch_ip+" sh int status >> sw_interfaces/interface_"+switch_ip+".txt", shell=True)
        print "end"

    return "interface_"+switch_ip+".txt"

def list_interfaces(interface_file):
    #####OPEN FILE####
    f=open(interface_file,"r")
    #####READ FROM FILE####
    lines=f.readlines()
    ##### Extract all the information ###
    result=[]
    for x in lines:
        result.append(x.split(" ")[0])
        ### CLOSE THE FILE ###
        f.close()

    ##### return RESULT #####
    j=len(result)
    tmpRet = []
    for l in range (3,j):
        sw = str(result[l]).split(" ")
        tmpRet.append({"interface":sw[0]})

    return tmpRet
