import json,requests
import boto3

username="" #mention bitbucket username
app_password="" #mention App password. Check Readme to see steps to create App password

def lambda_handler(event, context):
    print(json.dumps(event))
    branch=event['push']['changes'][0]['new']['name']
    print("Branch is: "+branch)
    new_commit_id=event['push']['changes'][0]['commits'][0]['hash']
    old_commit_id=event['push']['changes'][0]['commits'][0]['parents'][0]['hash']
    diff_url=event['push']['changes'][0]['commits'][0]['links']['diff']['href']
    diff_url=diff_url.replace("diff","diffstat")
    print(diff_url)

    payload={}
    
    response = requests.request("GET", diff_url,data=payload,auth=(username, app_password))
    print(response.text)
    res=json.loads(response.text)
    folder=[]
    for change in res['values']:
        print(change['new']['path'])
        fol=change['new']['path'].split('/')[1]
        print(fol)
        folder.append(fol)
    print("Folders changed:")
    print(folder)

    try:

        codepipeline=boto3.client('codepipeline')
        
        #check conditions and start pipeline based on your requirement
        if branch=="master": #change branch name
            if 'folder_name' in folder: #change folder-name
                print("Starting Pipeline..")
                codepipeline.start_pipeline_execution(name="name-of-pipeline") #mention relevent pipeline name

    except Exception as e:
        print("Error"+str(e))