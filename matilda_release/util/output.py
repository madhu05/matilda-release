#!/usr/bin/env python


def get_output(console_output, search):
    ips, amis, policies = [], [], []
    lines = (iter(console_output.splitlines()))
    if search.lower() == 'ip':
        for line in lines:
            pos = line.find('"IP"')
            if pos >= 0:
                ip = line[(pos + 7):]
                ip = ip[:ip.find('"')]
                if not ip in ips:
                    ips.append(ip)
        return ips
    elif search.lower() == 'ami':
        for line in lines:
            pos = line.find('"ami-')
            if pos >= 0:
                ami = line[pos + 1:(pos + 22)]
                if not ami in amis:
                    amis.append(ami)
        return amis
    elif search.lower() == 'policy':
        for line in lines:
            pos = line.find('arn:aws:kms:')
            if pos >= 0:
                policy = line[pos:-1]
                if not policy in policies:
                    region = line[(pos + 12):]
                    policies.append({
                        region[:region.find(':')]: policy
                    })
        return policies
    else:
        return "Wrong Key passed"


def main():
    from pprint import pprint
    payload_ip = """Ansible Plus Playbook Engine Starts Invoking - From : saclpcelva028
============= Generating Dynamic Inventory =============
============= Generating Dynamic Inventory =============
PLAY [localhost] ***************************************************************
TASK [fail if stash repo is not private] *************************************** skipping: [localhost]
TASK [synching git repo with AuditID and with out Branch] ********************** skipping: [localhost]
TASK [synching playbook with AuditID and with out Branch] ********************** changed: [localhost]
TASK [synching git repo with out AuditID and with out Branch] ****************** skipping: [localhost]
TASK [synching git repo with AuditID and with Branch name] ********************* skipping: [localhost]
TASK [synching git repo with out AuditID and with Branch name] ***************** skipping: [localhost]
PLAY RECAP *********************************************************************
localhost                  : ok=1    changed=1    unreachable=0    failed=0
localhost                  : ok=1    changed=1    unreachable=0    failed=0
PLAY [localhost] ***************************************************************
TASK [Prepare : fail if stash repo is not private] ***************************** skipping: [localhost]
TASK [Prepare : validating User AWS VPC based on the Portfolio] **************** changed: [localhost]
TASK [Prepare : fail] ********************************************************** skipping: [localhost]
TASK [Prepare : Validating User access for application based AWS ADOM group for Non prod AWS] *** changed: [localhost]
TASK [Prepare : fail] ********************************************************** skipping: [localhost]
TASK [Prepare : Creating Temporary GIT Directory] ****************************** changed: [localhost]
TASK [Prepare : Fetching Users CloudFormation Template] ************************ skipping: [localhost]
TASK [Prepare : Fetching Users CloudFormation Template when Branch mentioned] *** changed: [localhost]
TASK [sts-assume-role : Collecting Encrypted Credentials From Database] ******** ok: [localhost]
TASK [sts-assume-role : Setting Up Variables] ********************************** ok: [localhost]
TASK [sts-assume-role : Obtaining Temporary Token] ***************************** changed: [localhost]
TASK [sts-assume-role : Setting Up Variables for others] *********************** ok: [localhost]
TASK [sts-assume-role : Setting Up Variables for Shared service] *************** skipping: [localhost]
TASK [Prepare : Setting Up Variables - Output Path] **************************** ok: [localhost]
TASK [Prepare : Validate nested cloudformation template] *********************** ok: [localhost]
TASK [Prepare : fail] ********************************************************** skipping: [localhost]
TASK [Prepare : set template parameters] ***************************************
TASK [Prepare : Run CFN-NAG validation on the Child Templates when nested for s3 resource type] *** skipping: [localhost]
TASK [Prepare : debug] ********************************************************* skipping: [localhost]
TASK [Prepare : Run CFN-NAG validation on the main Template for s3 resource type] *** changed: [localhost]
TASK [Prepare : debug] ********************************************************* skipping: [localhost]
TASK [Prepare : Setting Up Variables - Nested S3] ****************************** ok: [localhost]
TASK [NestedS3 : Setting Up Variables - Nested S3] ***************************** skipping: [localhost]
TASK [NestedS3 : assigning temp params] **************************************** skipping: [localhost]
TASK [NestedS3 : debug] ******************************************************** skipping: [localhost]
TASK [NestedS3 : Uploading Nested templates to S3 other bucket] **
TASK [NestedS3 : Uploading Nested Stacks to S3 to Shared service bucket] *******
TASK [LaunchCF : Launch Cloudformation Stack] ********************************** changed: [localhost]
TASK [LaunchCF : Setting Up Ansible Plus Inventory when AutoScaling is defined] *** skipping: [localhost]
TASK [LaunchCF : Setting up the inventory to a variable] *********************** ok: [localhost]
TASK [LaunchCF : Displaying all the outputs] *********************************** ok: [localhost] => {    "cf.stack_outputs": {        "AZ": "us-east-1a",        "InstanceId": "i-08d1f9271a7d523ad",        "PrivateIP": "10.118.131.249"    },    "changed": false } TASK [LaunchCF : Setting up the instance id to a variable] ********************* ok: [localhost] TASK [LaunchCF : Setting up the ip to a variable] ****************************** ok: [localhost]
TASK [LaunchCF : Performing Post Validations] ********************************** changed: [localhost]
TASK [LaunchCF : Performing Post Validations] ********************************** skipping: [localhost]
TASK [LaunchCF : setting up variables] ***************************************** ok: [localhost]
TASK [LaunchCF : setting up variables] ***************************************** skipping: [localhost]
TASK [LaunchCF : debug] ******************************************************** ok: [localhost] => {    "changed": false,    "msg": [        {            "ID": "i-08d1f9271a7d523ad",            "IP": "10.118.131.249",            "Name": "PrivateIP",            "OS": "windows"        }    ] }
TASK [LaunchCF : Setting Up Variables - Instance Details] ********************** ok: [localhost]
TASK [LaunchCF : Fail IF No PrivateIP Returned] ******************************** skipping: [localhost]
TASK [LaunchCF : Set flag for backend operations] ****************************** ok: [localhost] => (item={"IP": "10.118.131.249", "OS": "windo ws", "Name": "PrivateIP", "ID": "i-08d1f9271a7d523ad"}) TASK [LaunchCF : Waiting For Unix Instance] ************************************ skipping: [localhost] => (item={"IP": "10.118.131.249", "OS": "windows", "Name": "PrivateIP", "ID": "i-08d1f9271a7d523ad"})
TASK [LaunchCF : Please wait while your Linux Ec2 HPSA register/remediate are in progress...] *** skipping: [localhost] => (item={"IP": "10.118.131.249", "OS": "windows", "Name": "PrivateIP", "ID": "i-08d1f9271a7d523ad"}) TASK [LaunchCF : fail] ********************************************************* skipping: [localhost] => (item={"skipped": True, "_ansible_no_log": False, "skip_reason": "Conditional result was False", "_ansible_item_result": True, "item": {"IP": "10.118.131.249", "OS": "windows", "Name": "PrivateIP", "ID": "i-08d1f9271a7d523ad"}, "changed": False})
TASK [LaunchCF : Waiting For Windows Instance on port 5986] ******************** ok: [localhost] => (item={"IP": "10.118.131.249", "OS": "windows", "Name": "PrivateIP", "ID": "i-08d1f9271a7d523ad"}) TASK [LaunchCF : calling security API to add netgroups - NP] ******************* skipping: [localhost] => (item={"IP": "10.118.131.249", "OS": "windows", "Name": "PrivateIP", "ID": "i-08d1f9271a7d523ad"})
TASK [LaunchCF : debug] ******************************************************** skipping: [localhost] => (item={"skipped": True, "_ansible_no_log": False, "skip_reason": "Conditional result was False", "_ansible_item_result": True, "item": {"IP": "10.118.131.249", "OS": "windows", "Name": "PrivateIP", "ID": "i-08d1f9271a7d523ad"}, "changed": False})
TASK [LaunchCF : Waiting on server to add service account -NP] ***************** skipping: [localhost] => (item={"IP": "10.118.131.249", "OS": "windows", "Name": "PrivateIP", "ID": "i-08d1f9271a7d523ad"})
Playbook executed successfully
******************Finished Executing AnsiblePlus CloudFormation******************

Hygieia: Failed Publishing Build Complete Data. Response Code: 200.
Notifying upstream projects of job completion
Finished: SUCCESS"""

    payload_ami = """
    TASK [ami-tagger : Pre-process user-defined tags] ****************************** skipping: [localhost] => (item=) TASK [ami-tagger : Add user-defined tags to published AMIs] ******************** skipping: [localhost] => (item=NONPROD) TASK [epilogue : Display image IDs of encrypted AMIs] ************************** ok: [localhost] => {    "changed": false,    "image_ids": {        "NONPROD": {            "us-east-1": "ami-01a2bb98061bb576e",            "us-west-2": "ami-0f4466f1f9e5cd699"        }    } } PLAY RECAP ********************************************************************* localhost                  : ok=79   changed=27   unreachable=0    failed=0   localhost                  : ok=79   changed=27   unreachable=0    failed=0   **********VZ AWS Encrypt Base AMI Plugin execution End********** Hygieia: Published Build Complete Data. Response Code: 201. Response Value= 5c095050b1ff5475b59b01c6 Notifying upstream projects of job completion Finished: SUCCESS
TASK [ami-tagger : Pre-process user-defined tags] ****************************** skipping: [localhost] => (item=) TASK [ami-tagger : Add user-defined tags to published AMIs] ******************** skipping: [localhost] => (item=NONPROD) TASK [epilogue : Display image IDs of encrypted AMIs] ************************** ok: [localhost] => {    "changed": false,    "image_ids": {        "NONPROD": {            "us-east-1": "ami-01a2bb98061bb576e",            "us-west-2": "ami-0f4466f1f9e5cd699"        }    } } PLAY RECAP ********************************************************************* localhost                  : ok=79   changed=27   unreachable=0    failed=0   localhost                  : ok=79   changed=27   unreachable=0    failed=0   **********VZ AWS Encrypt Base AMI Plugin execution End********** Hygieia: Published Build Complete Data. Response Code: 201. Response Value= 5c095050b1ff5475b59b01c6 Notifying upstream projects of job completion Finished: SUCCESS
    """

    payload_policy = """
    VzPol-CEDV-KMS-Key exists in us-east-1. Updating stack... 
Waiting for VzPol-CEDV-KMS-Key in us-east-1 to update... 
VzPol-CEDV-KMS-Key in us-east-1 updated. 
CEDV KMS Key Alias: alias/VzPol-CEDV-NonProd-key-alias 

CEDV KMS Key ARN: arn:aws:kms:us-east-1:759031157600:key/d64d83ad-84b3-423d-bfa5-ed7080d22610 

VzPol-CEDV-KMS-Key exists in us-west-2. Updating stack... 
Waiting for VzPol-CEDV-KMS-Key in us-west-2 to update... 
VzPol-CEDV-KMS-Key in us-west-2 updated. 
CEDV KMS Key Alias: alias/VzPol-CEDV-NonProd-key-alias 

CEDV KMS Key ARN: arn:aws:kms:us-west-2:759031157600:key/6645b92e-03af-44e9-ac0e-9b8db56ff022 

Hygieia: Failed Publishing Build Complete Data. Response Code: 200. 
Notifying upstream projects of job completion 
Finished: SUCCESS
    """

    # print(get_output(payload_ip, 'IP'))
    # print(get_output(payload_ami, 'AMI'))
    # pprint(get_output(payload_policy, 'policy'))
    # print(get_output(payload_policy, 'hello'))


if __name__ == '__main__':
    main()
