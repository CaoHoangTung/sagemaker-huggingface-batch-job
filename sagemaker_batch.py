"""
This script creates a SageMaker Batch Transform job, which utilize HuggingFace endpoint to process files from a S3 bucket.

Simple usage:
python sagemaker_batch.py
--s3-path [YOUR S3 PATH]

Full usage:
python sagemaker_batch.py
--role-name sagemaker-summarization \
--hf_task summarization \
--hf-model-id sshleifer/distilbart-cnn-12-6 \
--transformer-version 4.26 \
--pytorch-version 1.13 \
--py-version py39 \
--num-instances 5 \
--instance-type ml.g4dn.xlarge \
--assemble-with Line \
--strategy SingleRecord \
--content-type application/jsonn \
--split-type Line \
--s3-path [YOUR S3 PATH]
"""

import argparse
import boto3
from sagemaker.huggingface.model import HuggingFaceModel

def get_iam_role(role_name):
    iam_client = boto3.client('iam')
    role = iam_client.get_role(RoleName=role_name)['Role']['Arn']
    return role

def main(args):
    # Hub model configuration <https://huggingface.co/models>

    # create Hugging Face Model Class
    huggingface_model = HuggingFaceModel(
        env= {
            'HF_MODEL_ID': args.hf_model_id,
            'HF_TASK': args.hf_task
        },                                      # configuration for loading model from Hub
        role=get_iam_role(args.role_name),      # IAM role with permissions to create an endpoint
        transformers_version=args.transformers_version,     # Transformers version used
        pytorch_version=args.pytorch_version,               # PyTorch version used
        py_version=args.py_version,                         # Python version used
    )

    # create transformer to run a batch job
    batch_job = huggingface_model.transformer(
        accept=args.content_type,
        instance_count=args.num_instances,
        instance_type=args.instance_type,
        max_concurrent_transforms=args.num_instances,
        assemble_with=args.assemble_with,
        strategy=args.strategy
    )

    # starts batch transform job and uses S3 data as input
    batch_job.transform(
        data=args.s3_path,
        # data='s3://sagemaker-summarization-input/test01_5k_1xml.g4dn.xlarge',
        content_type=args.content_type,
        output_filter=args.output_filter,
        join_source=args.join_source,
        split_type=args.split_type,
    )


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--role-name", type=str, default='sagemaker-summarization', help="Role name that would be used by the batch processing job")
    parser.add_argument("--hf-task", type=str, default='summarization', help="The huggingface model task type")
    parser.add_argument("--hf-model-id", type=str, default='sshleifer/distilbart-cnn-12-6', help="The huggingface model id")
    parser.add_argument("--transformers-version", type=str, default='4.26', help="The version of the transformer library")
    parser.add_argument("--pytorch-version", type=str, default='1.13', help="The version of the pytorch library")
    parser.add_argument("--py-version", type=str, default='py39', help="The version of the python library")
    
    parser.add_argument("--num-instances", type=int, default=5, help="Number of instances that would be used for the job. It should be from 1-20.")
    parser.add_argument("--instance-type", type=str, default='ml.g4dn.xlarge', help="Type of instance that would be used for the job.")
    parser.add_argument("--assemble-with", type=str, default='Line', help="Indication of how to assemble the output")
    parser.add_argument("--strategy", type=str, default='SingleRecord', help="Batch job strategy. Could be SingleRecord/MultiRecord")


    parser.add_argument("--s3-path", type=str, help="Path to S3 data folder that would be processed")
    parser.add_argument("--content-type", type=str, default="application/json", help="Content type of S3 data")
    parser.add_argument("--join-source", type=str, default="Input", help="Decide whenever we join input with output or not. Could be Input|None")
    parser.add_argument("--output-filter", type=str, default="$['domain','SageMakerOutput']", help="Fields to include in outptu file. Default to all")
    parser.add_argument("--split-type", type=str, default="Line", help="Split type of S3 files")

    args = parser.parse_args()
    main(args)