from aws_cdk import (
    # Duration,
    Stack,
    aws_cloudwatch as cloudwatch,
    Duration,
    # aws_sqs as sqs,
)
from constructs import Construct


class MsTeamsNotificationStack(Stack):
    def __init__(self, scope: Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        self.create_cloudwatch_alarm(namespace="AWS/Lambda", metric_name="Invocations")

    def create_cloudwatch_alarm(
        self,
        namespace: str,
        metric_name: str,
        period: Duration = Duration.minutes(5),
        threshold: int = 100,
        evaluation_periods: int = 1,
        comparison_operator: cloudwatch.ComparisonOperator = cloudwatch.ComparisonOperator.GREATER_THAN_THRESHOLD,
        missing_data_treatment: cloudwatch.TreatMissingData = cloudwatch.TreatMissingData.MISSING,
    ):
        metric = cloudwatch.Metric(
            namespace=namespace,
            metric_name=metric_name,
            period=period,
        )

        alarm = cloudwatch.Alarm(
            self,
            f"DemoCloudwatchAlarmForMetic{metric_name}",
            metric=metric,
            threshold=threshold,
            evaluation_periods=evaluation_periods,
            alarm_description=f"High {metric_name}",
            alarm_name=f"High-{namespace}-{metric_name}-alarm",
            comparison_operator=comparison_operator,
            treat_missing_data=missing_data_treatment,
        )

    def create_sns_topic(self):
        ...

    def create_notification_lambda(self):
        ...
