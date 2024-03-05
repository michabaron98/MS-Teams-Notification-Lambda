import aws_cdk as core
import aws_cdk.assertions as assertions

from infrastructure.ms_teams_notification_stack import (
    MsTeamsNotificationStack,
)


def test_sqs_queue_created():
    app = core.App()
    stack = MsTeamsNotificationStack(app, "ms-teams-notification")
    template = assertions.Template.from_stack(stack)

    template.has_resource_properties(
        "AWS::CloudWatch::Alarm",
        {
            "AlarmDescription": "High Invocations",
            "AlarmName": "High-AWS/Lambda-Invocations-alarm",
            "ComparisonOperator": "GreaterThanThreshold",
            "EvaluationPeriods": 1,
            "MetricName": "Invocations",
            "Namespace": "AWS/Lambda",
            "Period": 300,
            "Statistic": "Average",
            "Threshold": 100,
            "TreatMissingData": "missing",
        },
    )

    template.has_resource_properties(
        "AWS::Lambda::Function",
        {
            "Environment": {
                "Variables": {
                    "SECRET_NAME": assertions.Match.any_value(),
                    "SECRET_REGION": {"Ref": "AWS::Region"},
                    "LOG_LEVEL": "INFO",
                }
            },
            "FunctionName": "notify-msteams-lambda",
            "Handler": "ms_teams_notification_lambda.lambda_handler",
            "Role": {
                "Fn::GetAtt": ["DemoNotifyMSTeamsHandlerServiceRole1F0FF3DF", "Arn"]
            },
            "Runtime": "python3.9",
            "Timeout": 10,
        },
    )
