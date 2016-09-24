import json
import sys
import subprocess
import re

json_output_indent=None

# Pretty output
json_output_indent=2

# Sample output from 'VBoxManage list vms'
#"Win7 (32bit)" {11111111-2222-3333-4444-123456789012}
#"Clone_win7" {22222222-2222-3333-4444-123456789012}
#"node1" {33333333-2222-3333-4444-123456789012}

# Forma is 
#"name"<space>{UUID}

vm_list_matcher = re.compile('^"([^"]+)" (.*$)') # group1 - VM name, group2 - VM UUID


def list_vms():
    '''
        Get VM list using 'VBoxManage list vms'
    '''
    p = subprocess.Popen(("VBoxManage list vms").split(' '), 
                            stdout=subprocess.PIPE)
    
    (vbox_stdout, vbox_stderr) = p.communicate()

    return [vm_list_matcher.match(vm).group(1) for vm in vbox_stdout.split('\n') if len(vm)>0]
    
    
def main():
    outcome = None

    try:
        # Zabbix Discovery data output

        #{"data": [{"{#VM_NAME}": "Win7 (32bit)"},
        #          {"{#VM_NAME}": "Clone_win7"},
        #          {"{#VM_NAME}": "node1"}
        #         ]
        #} 

        outcome = dict(data = [{ "{#VM_NAME}": vm_name} for vm_name in list_vms()])

    except Exception, e:
        print type(e)
        print 'Error: %s' % e
        sys.exit(1)
    finally:
        if outcome is not None:
            print json.dumps(outcome, indent=json_output_indent)
            
    
if __name__ == '__main__':
    main()
    