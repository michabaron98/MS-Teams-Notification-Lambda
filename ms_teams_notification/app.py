import aws_cdk as cdk

from ms_teams_notification_infrastructure.ms_teams_notification_stack import (
    MsTeamsNotificationStack,
)


app = cdk.App()
MsTeamsNotificationStack(
    app,
    "MsTeamsNotificationStack",
)

app.synth()
