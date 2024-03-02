import aws_cdk as cdk

from infrastructure.ms_teams_notification_stack import (
    MsTeamsNotificationStack,
)


app = cdk.App()
MsTeamsNotificationStack(
    app,
    "DemoMsTeamsNotificationStack",
)

app.synth()
