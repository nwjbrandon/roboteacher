resource "aws_cloudwatch_log_group" "api_lambda_cloudwatch_log_group" {
  name              = "/aws/lambda/${aws_lambda_function.api_lambda_function.function_name}"
  retention_in_days = 7
}

resource "aws_lambda_permission" "cloudwatch_event_permission" {
  statement_id  = "AllowExecutionFromCloudWatch"
  action        = "lambda:InvokeFunction"
  function_name = aws_lambda_function.api_lambda_function.function_name
  principal     = "events.amazonaws.com"
  source_arn    = aws_cloudwatch_event_rule.api_lambda_cloudwatch_event_rule.arn
}

resource "aws_cloudwatch_event_rule" "api_lambda_cloudwatch_event_rule" {
  name                = "${var.PROJECT_NAMESPACE}-api-lambda"
  schedule_expression = "cron(0 0 * * ? *)"
}

resource "aws_cloudwatch_event_target" "cv_lambda_cloudwatch_event_target" {
  rule = aws_cloudwatch_event_rule.api_lambda_cloudwatch_event_rule.name
  arn  = aws_lambda_function.api_lambda_function.arn
}