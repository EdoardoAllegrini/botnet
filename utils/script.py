import subprocess

def exec_cmd(cmd):
    proc = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    o, e = proc.communicate()
    result = o.decode('ascii')
    return result
    
def get_my_ip():
    cmd = ['hostname', '-I']
    my_ip = exec_cmd(cmd)
    return my_ip[:-2]