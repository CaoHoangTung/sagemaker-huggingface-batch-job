import boto3
from pprint import pprint

client = boto3.client('sagemaker')


def main():
    model_names = []

    for key in paginate(client.list_models):
        model_names.append(key['ModelName'])

    delete_multiple_models(model_names)


def delete_multiple_models(model_names):
    for model_name in model_names:
        print('Deleting model: {}'.format(model_name))
        client.delete_model(ModelName=model_name)


def paginate(method, **kwargs):
    client = method.__self__
    paginator = client.get_paginator(method.__name__)
    for page in paginator.paginate(**kwargs).result_key_iters():
        for result in page:
            yield result


if __name__=="__main__":
    main()