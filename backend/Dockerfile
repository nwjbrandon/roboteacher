FROM public.ecr.aws/lambda/python:3.9

COPY requirements.txt ./

RUN pip3 install --no-cache-dir -r requirements.txt --target "${LAMBDA_TASK_ROOT}"

COPY __init__.py lambda_function.py roboteacher/ ./

ADD roboteacher roboteacher

CMD [ "lambda_function.lambda_handler" ] 