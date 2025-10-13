import subprocess as sp

def shell(args, ret_output=False):
    '''Call Bash shell with input string as argument'''
    _ = sp.Popen(args, shell=True, stdout=sp.PIPE, stderr=sp.PIPE)
    out, err = _.communicate()
    if ret_output:
        return out + err
