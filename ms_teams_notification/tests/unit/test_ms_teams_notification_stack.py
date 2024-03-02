import aws_cdk as core
import aws_cdk.assertions as assertions

from infrastructure.ms_teams_notification_stack import (
    MsTeamsNotificationStack,
)

# example tests. To run these tests, uncomment this file along with the example
# resource in ms_teams_notification/ms_teams_notification_stack.py
def test_sqs_queue_created():
    app = core.App()
    stack = MsTeamsNotificationStack(app, "ms-teams-notification")
    template = assertions.Template.from_stack(stack)


#     template.has_resource_properties("AWS::SQS::Queue", {
#         "VisibilityTimeout": 300
#     })
