import boto3

# Create an AWS CloudFormation resource
cloudformation = boto3.resource('cloudformation')

# Specify the CloudFormation stack name and template file location
stack_name = 'my-stack'
template_file = 'path/to/template.yml'

# Create a stack using the specified template
with open(template_file) as f:
    template_body = f.read()

stack = cloudformation.create_stack(
    StackName=stack_name,
    TemplateBody=template_body,
    Capabilities=['CAPABILITY_NAMED_IAM']
)

# Wait for the stack creation to complete
stack.wait_until_exists()

# Check the stack status after completion
stack_status = stack.stack_status
if stack_status == 'CREATE_COMPLETE':
    print('Stack deployment complete')
else:
    print('Stack deployment failed with status:', stack_status)