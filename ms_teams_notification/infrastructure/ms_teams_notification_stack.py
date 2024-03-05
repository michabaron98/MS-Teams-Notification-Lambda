from aws_cdk import (
    Stack,
    aws_cloudwatch as cloudwatch,
    aws_cloudwatch_actions as cw_actions,
    Duration,
    aws_sns as sns,
    aws_sns_subscriptions,
    aws_secretsmanager as secrets,
    aws_lambda,
)
from constructs import Construct


class MsTeamsNotificationStack(Stack):
    def __init__(self, scope: Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        sns_topic = self.create_sns_topic()
        self.create_cloudwatch_alarm(
            namespace="AWS/Lambda", metric_name="Invocations", sns_topic=sns_topic
        )
        self.create_notification_lambda(
            ms_teams_secret_arn="arn:aws:secretsmanager:REGION:ACCOUNT_ID:secret:YOUR_SECRET_ARN",
            sns_topic=sns_topic,
        )

    def create_cloudwatch_alarm(
        self,
        namespace: str,
        metric_name: str,
        sns_topic: sns.Topic,
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

        sns_action = cw_actions.SnsAction(sns_topic)
        alarm.add_alarm_action(sns_action)

    def create_sns_topic(self) -> sns.Topic:
        return sns.Topic(
            self,
            "DemoCloudWatchNotificationSnsTopic",
            topic_name=f"demo-cloud-watch-notifications",
            display_name="Demo cloud watch Notifications",
        )

    def create_notification_lambda(
        self,
        ms_teams_secret_arn: str,
        sns_topic: sns.Topic,
    ):
        notify_teams_lambda = aws_lambda.Function(
            self,
            "DemoNotifyMSTeamsHandler",
            function_name=f"notify-msteams-lambda",
            runtime=aws_lambda.Runtime.PYTHON_3_9,
            code=aws_lambda.Code.from_asset(
                "infrastructure/src",
            ),
            handler="ms_teams_notification_lambda.lambda_handler",
            environment={
                "SECRET_NAME": ms_teams_secret_arn,
                "SECRET_REGION": self.region,
                "LOG_LEVEL": "INFO",
            },
            timeout=Duration.seconds(10),
        )

        msteams_webhook_secret = secrets.Secret.from_secret_complete_arn(
            scope=self,
            id="secretHook",
            secret_complete_arn=ms_teams_secret_arn,
        )

        msteams_webhook_secret.grant_read(grantee=notify_teams_lambda)

        sns_topic.add_subscription(
            aws_sns_subscriptions.LambdaSubscription(notify_teams_lambda)
        )
